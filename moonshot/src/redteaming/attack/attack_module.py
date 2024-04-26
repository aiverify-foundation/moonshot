from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, AsyncGenerator

from jinja2 import Template
from pydantic import BaseModel

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.metrics.metric import Metric
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.redteaming.attack.context_strategy import ContextStrategy
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class AttackModule:
    sql_create_chat_record = """
        INSERT INTO {} (connection_id,context_strategy,prompt_template,attack_module,
        metric,prompt,prepared_prompt,system_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """

    def __init__(self, am_args: AttackModuleArguments):
        self.id = am_args.name
        self.description = "Overwrite this with your attack module description!"
        self.name = am_args.name
        self.connector_ids = am_args.connector_eps
        self.prompt_templates = am_args.prompt_templates
        self.prompt = am_args.prompt
        self.system_prompt = am_args.system_prompt
        self.metric_ids = am_args.metric_ids
        self.context_strategy_ids = am_args.context_strategy_ids
        self.db_instance = am_args.db_instance
        self.params = am_args.params

    @classmethod
    def load(cls, am_arguments: AttackModuleArguments) -> AttackModule:
        """
        Retrieves an attack module instance by its ID.

        This method attempts to load an attack module instance using the provided ID. If the attack module instance
        is found, it is returned. If the attack module instance does not exist, a RuntimeError is raised.

        Args:
            am_id (str): The unique identifier of the attack module to be retrieved.

        Returns:
            AttackModule: The retrieved attack module instance.

        Raises:
            RuntimeError: If the attack module instance does not exist.
        """
        attack_module_inst = get_instance(
            am_arguments.name,
            Storage.get_filepath(
                EnvVariables.ATTACK_MODULES.name, am_arguments.name, "py"
            ),
        )
        if attack_module_inst:
            return attack_module_inst(am_arguments)
        else:
            raise RuntimeError(
                f"Unable to get defined attack module instance - {am_arguments.name}"
            )

    @abstractmethod
    def check_stop_condition(self):
        """
        Checks if the stop condition has been fulfilled. If it is fulfilled, stop red teaming.
        Stop condition can be number of prompts sent to the target LLM(s), the response from the LLM matching
        a certain word, or the response from the LLM having a certain metric score.
        """
        pass

    async def _generate_prompts(
        self, prompt: str, target_llm_connector_id: str
    ) -> AsyncGenerator[RedTeamingPromptArguments, None]:
        """
        Generates prompts for red teaming.

        This method asynchronously generates prompts for red teaming based on the provided prompt and target LLM
        connector ID. It processes the prompt using context strategy and prompt template if specified, and
        yields RedTeamingPromptArguments for each generated prompt.

        Args:
            prompt (str): The prompt to be processed and sent to the target LLM.
            target_llm_connector_id (str): The unique identifier of the target LLM connector.

        Yields:
            RedTeamingPromptArguments: An instance of RedTeamingPromptArguments containing the
            generated prompt details.

        """
        num_of_previous_chats = 3
        if self.context_strategy_ids:
            context_strategy_instance = self.context_strategy_instances[0]
            prompt = ContextStrategy.process_prompt_cs(
                prompt,
                context_strategy_instance.id,
                self.db_instance,
                target_llm_connector_id,
                num_of_previous_chats,
            )
        if self.prompt_templates:
            # prepare prompt template generator
            pt_id = self.prompt_templates[0]
            pt_info = Storage.read_object_generator(
                EnvVariables.PROMPT_TEMPLATES.name, pt_id, "json", "template"
            )
            pt = next(pt_info)
            jinja2_template = Template(pt)
            prompt = jinja2_template.render({"prompt": prompt})

        yield RedTeamingPromptArguments(
            conn_id=target_llm_connector_id,
            am_id=self.name,
            cs_id=self.context_strategy_ids[0] if self.context_strategy_ids else "",
            pt_id=self.prompt_templates[0] if self.prompt_templates else "",
            me_id=self.metric_ids[0] if self.metric_ids else "",
            original_prompt=self.prompt,
            system_prompt=self.system_prompt,
            start_time="",
            connector_prompt=ConnectorPromptArguments(
                prompt_index=0,
                prompt=prompt,
                target="",
            ),
        )

    async def _send_prompt_to_all_llm_default(self) -> list:
        """
        Asynchronously sends prompts to all Language Learning Models (LLMs) using default settings.

        This method prepares prompts by processing them with prompt templates and/or context strategies if specified,
        generates predictions for the prompts, and yields the results as a generator list.

        Returns:
            list: A list of generators containing the results of the generated prompts.
        """
        generator_list = []
        if self.connector_ids:
            for target_llm_connector in self.connector_instances:
                gen_prompts_generator = self._generate_prompts(
                    self.prompt, target_llm_connector.id
                )
                gen_results_generator = self._generate_predictions(
                    gen_prompts_generator, target_llm_connector
                )
                generator_list.append(gen_results_generator)
        return generator_list

    async def _send_prompt_to_all_llm(self, list_of_prompts: list) -> list:
        """
        Asynchronously sends prompts to all Language Learning Models (LLMs).

        This method takes a list of prompts, sends each prompt to all LLM connectors, records the responses,
        and returns a list of consolidated responses.

        Args:
            list_of_prompts (list): A list of prompts to be sent to the LLM connectors.

        Returns:
            list: A list of consolidated responses from all LLM connectors.
        """
        consolidated_responses = []
        for prepared_prompt in list_of_prompts:
            for target_llm_connector in self.connector_instances:
                new_prompt_info = ConnectorPromptArguments(
                    prompt_index=1, prompt=prepared_prompt, target=""
                )
                start_time = datetime.now()
                response = await Connector.get_prediction(
                    new_prompt_info, target_llm_connector
                )
                consolidated_responses.append(response)
                chat_tuple = (
                    target_llm_connector.id,
                    self.context_strategy_ids[0] if self.context_strategy_ids else "",
                    self.prompt_templates[0] if self.prompt_templates else "",
                    self.name,
                    self.metric_ids[0] if self.metric_ids else "",
                    self.prompt,  # original prompt
                    prepared_prompt,  # prepared prompt
                    self.system_prompt,  # system prompt
                    response.predicted_results,
                    response.duration,
                    str(start_time),
                )
                self._write_record_to_db(chat_tuple, target_llm_connector.id)
        return consolidated_responses

    async def _send_prompt_to_single_llm(
        self, list_of_prompts: list, target_llm_connector: Connector
    ) -> list:
        """
        Asynchronously sends prompts to a single Language Learning Model (LLM) connector.

        This method takes a list of prompts, sends each prompt to the specified LLM connector, records the response,
        and returns a list of consolidated responses.

        Args:
            list_of_prompts (list): A list of prompts to be sent to the LLM connector.
            target_llm_connector: The target LLM connector to send the prompts to.

        Returns:
            list: A list of consolidated responses from the specified LLM connector.
        """
        consolidated_responses = []
        for prepared_prompt in list_of_prompts:
            new_prompt_info = ConnectorPromptArguments(
                prompt_index=1, prompt=prepared_prompt, target=""
            )
            start_time = datetime.now()
            response = await Connector.get_prediction(
                new_prompt_info, target_llm_connector
            )
            consolidated_responses.append(response)
            chat_tuple = (
                target_llm_connector.id,
                self.context_strategy_ids[0] if self.context_strategy_ids else "",
                self.prompt_templates[0] if self.prompt_templates else "",
                self.name,
                self.metric_ids[0] if self.metric_ids else "",
                self.prompt,  # original prompt
                prepared_prompt,  # prepared prompt
                self.system_prompt,  # system prompt
                response.predicted_results,
                response.duration,
                str(start_time),
            )
            self._write_record_to_db(chat_tuple, target_llm_connector.id)
        return consolidated_responses

    def _write_record_to_db(
        self,
        chat_record_tuple: tuple,
        chat_record_id: str,
    ) -> None:
        """
        Writes the chat record to the database.

        Args:
            chat_record_tuple (tuple): A tuple containing the chat record information.
            chat_record_id (str): The ID of the chat record.
        """
        endpoint_id = chat_record_id.replace("-", "_")
        Storage.create_database_record(
            self.db_instance,
            chat_record_tuple,
            AttackModule.sql_create_chat_record.format(endpoint_id),
        )

    @abstractmethod
    async def execute(self) -> Any:
        """
        Houses the logic of the attack and is an entry point.
        * Do not change the name of this function in the attack module

        Returns:
            Any: the return type from the execution
        """
        pass

    async def _generate_predictions(
        self,
        gen_prompts_generator: AsyncGenerator[RedTeamingPromptArguments, None],
        llm_connector: Connector,
    ) -> AsyncGenerator[RedTeamingPromptArguments, None]:
        """
        Asynchronously generates predictions for the given prompts.

        Args:
            gen_prompts_generator (AsyncGenerator[RedTeamingPromptArguments, None]): An asynchronous generator
            yielding RedTeamingPromptArguments.

            llm_connector (Connector): The connector to the Language Learning Model (LLM).

        Yields:
            RedTeamingPromptArguments: An asynchronous generator yielding the new prompt information.
        """
        async for prompt_info in gen_prompts_generator:
            new_prompt_info = RedTeamingPromptArguments(
                conn_id=prompt_info.conn_id,
                am_id=prompt_info.am_id,
                cs_id=prompt_info.cs_id,
                me_id=prompt_info.me_id,
                pt_id=prompt_info.pt_id,
                original_prompt=self.prompt,
                system_prompt=prompt_info.system_prompt,
                connector_prompt=prompt_info.connector_prompt,
                start_time=str(datetime.now()),
            )

            # send processed prompt to llm and write record to db
            new_prompt_info.connector_prompt = await Connector.get_prediction(
                new_prompt_info.connector_prompt, llm_connector
            )
            self._write_record_to_db(new_prompt_info.to_tuple(), llm_connector.id)
            yield new_prompt_info

    def load_modules(self):
        """
        Loads connector, metric, and context strategy instances if available.
        """
        if self.connector_ids:
            self.connector_instances = [
                Connector.create(ConnectorEndpoint.read(endpoint))
                for endpoint in self.connector_ids
            ]

        if self.metric_ids:
            self.metric_instances = [
                Metric.load(metric_id) for metric_id in self.metric_ids
            ]

        if self.context_strategy_ids:
            self.context_strategy_instances = [
                ContextStrategy.load(context_strategy_id)
                for context_strategy_id in self.context_strategy_ids
            ]


class RedTeamingPromptArguments(BaseModel):
    conn_id: str  # The ID of the connection, default is an empty string

    am_id: str  # The ID of the attack module, default is an empty string

    cs_id: str = ""  # The ID of the context strategy, default is an empty string

    me_id: str = (
        ""  # The ID of the metric used to score the result, default is an empty string
    )

    pt_id: str = ""  # The ID of the prompt template, default is en empty string

    original_prompt: str  # The original prompt used

    system_prompt: str = ""  # The system-generated prompt used

    start_time: str  # The start time of the prediction

    connector_prompt: ConnectorPromptArguments  # The prompt information to send

    def to_tuple(self) -> tuple:
        """
        Converts the PromptArguments instance into a tuple.

        This method collects all the attributes of the PromptArguments instance and forms a tuple
        with the attribute values in this specific order: conn_id, rec_id, ds_id, pt_id, prompt,
        target, predicted_results, duration.
        This tuple is suitable for serialization tasks, like storing the prompt arguments data
        in a database or transmitting it over a network.

        Returns:
            tuple: A tuple representation of the PromptArguments instance.
        """
        return (
            self.conn_id,
            self.cs_id,
            self.pt_id,
            self.am_id,
            self.me_id,
            self.original_prompt,
            self.connector_prompt.prompt,
            self.system_prompt,
            str(self.connector_prompt.predicted_results),
            str(self.connector_prompt.duration),
            self.start_time,
        )
