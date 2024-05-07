from __future__ import annotations

import time
from datetime import datetime
from typing import Any, AsyncGenerator

from jinja2 import Template
from pydantic import BaseModel

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.redteaming.attack.context_strategy import ContextStrategy
from moonshot.src.redteaming.session.red_teaming_type import RedTeamingType
from moonshot.src.redteaming.session.session import SessionMetadata
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage


class RedTeaming:
    sql_create_session_metadata_table = """
            CREATE TABLE IF NOT EXISTS session_metadata_table (
            session_id text PRIMARY KEY NOT NULL,
            name text NOT NULL,
            description text NOT NULL,
            endpoints text NOT NULL,
            created_epoch INTEGER NOT NULL,
            created_datetime text NOT NULL,
            context_strategy text,
            prompt_template text,
            chat_ids text
            );
    """
    sql_create_chat_metadata_table = """
        CREATE TABLE IF NOT EXISTS chat_metadata_table (
        chat_id text PRIMARY KEY,
        endpoint text NOT NULL,
        created_epoch INTEGER NOT NULL,
        created_datetime text NOT NULL
        );
    """

    sql_create_chat_record = """
        INSERT INTO {} (connection_id,context_strategy,prompt_template,attack_module,
        metric,prompt,prepared_prompt,system_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """

    async def generate(
        self,
        event_loop: Any,
        runner_args: dict,
        database_instance: DBInterface,
        session_metadata: SessionMetadata,
        red_teaming_type: RedTeamingType,
    ) -> dict:
        """
        Asynchronously generates the red teaming session.

        This method is responsible for the orchestration of the red teaming session. It sets up the necessary
        environment, initializes the attack strategies, and executes the red teaming logic. It handles any errors
        encountered during the session and returns the results in a dictionary format.

        Args:
            event_loop (Any): The event loop in which asynchronous tasks will be scheduled.
            runner_args (dict): A dictionary containing arguments for the red teaming session.
            database_instance (DBAccessor | None): The database instance to connect to, or None if not available.
            session_metadata (SessionMetadata): Metadata associated with the red teaming session.

        Returns:
            dict: A dictionary containing the results of the red teaming session, including any errors encountered.
        """
        self.event_loop = event_loop
        self.runner_args = runner_args
        self.database_instance = database_instance
        self.session_metadata = session_metadata
        self.red_teaming_type = red_teaming_type

        if self.red_teaming_type == RedTeamingType.AUTOMATED:
            print("[Red Teaming] Starting automated red teaming...")
            await self.run_automated_red_teaming()
        elif self.red_teaming_type == RedTeamingType.MANUAL:
            print("[Red Teaming] Starting manual red teaming...")
            await self.run_manual_red_teaming()
        else:
            raise RuntimeError("[Session] Unable to determine red teaming type.")

    async def run_automated_red_teaming(self):
        """
        Asynchronously runs the automated red teaming process.

        This method orchestrates the automated red teaming session by loading attack modules, executing the
        attack strategies, and handling any encountered errors.

        Returns:
            dict: A dictionary containing the results of the automated red teaming session.
        """

        # ------------------------------------------------------------------------------
        # Part 1: Load attack module
        # ------------------------------------------------------------------------------
        print("[Red teaming] Part 1: Loading All Attack Module(s)...")
        loaded_attack_modules = []
        try:
            # load red teaming modules
            for attack_strategy_args in self.runner_args.get("attack_strategies", None):
                # load attack module with arguments
                attack_module_attack_arguments = AttackModuleArguments(
                    connector_ids=self.session_metadata.endpoints
                    if self.session_metadata.endpoints
                    else [],
                    prompt_templates=attack_strategy_args.get(
                        "prompt_template_ids", []
                    ),
                    prompt=attack_strategy_args.get("prompt", ""),
                    system_prompt=attack_strategy_args.get("system_prompt", ""),
                    metric_ids=attack_strategy_args["metric_ids"]
                    if "metric_ids" in attack_strategy_args
                    else [],
                    context_strategy_info=attack_strategy_args["context_strategy_info"]
                    if "context_strategy_info" in attack_strategy_args
                    else [],
                    db_instance=self.database_instance,
                )
                loaded_attack_module = AttackModule.load(
                    am_id=attack_strategy_args.get("attack_module_id"),
                    am_arguments=attack_module_attack_arguments,
                )
                loaded_attack_modules.append(loaded_attack_module)

        except Exception as e:
            print(f"Unable to load attack modules in attack strategy: {str(e)}")

        # ------------------------------------------------------------------------------
        # Part 2: Run attack module(s)
        # ------------------------------------------------------------------------------
        print("[Red teaming] Part 2: Running Attack Module(s)...")

        responses_from_attack_module = []
        for attack_module in loaded_attack_modules:
            print(f"[Red teaming] Starting to run attack module [{attack_module.name}]")
            start_time = time.perf_counter()

            attack_module_response = await attack_module.execute()
            print(
                f"[Red teaming] Running attack module [{attack_module.name}] took "
                f"{(time.perf_counter() - start_time):.4f}s"
            )
            responses_from_attack_module.append(attack_module_response)
        return {}

    async def run_manual_red_teaming(self) -> list:
        """
        Runs the manual red teaming process based on the provided arguments.

        Retrieves the manual red teaming arguments from the runner arguments and initializes the prompt templates and
        context strategy information. It then loads the required modules and validates the prompt for manual
        red teaming. After that, it iterates through the target connectors to generate prompts and predictions,
        consolidating the results into a list.

        Returns:
        list: A list of consolidated results from the manual red teaming process.
        """
        # assign manual red teaming arguments to self.rt_args
        self.rt_args = self.runner_args.get("manual_rt_args", "")
        if not self.rt_args:
            raise RuntimeError("[Session] Unable to get red teaming arguments.")

        # assign prompt template and context strategy to self. if not specified, they will be defaulted to empty list
        self.prompt_templates = self.rt_args.get("prompt_template_ids", [])
        self.context_strategy_info = self.rt_args.get("context_strategy_info", [])

        self.load_modules()

        self.prompt = self.rt_args.get("prompt", "")
        if not self.prompt:
            raise RuntimeError("[Session] Unable to get prompt for manual red teaming.")

        self.system_prompt = self.rt_args.get("system_prompt", "")

        consolidated_result_list = []
        generator_list = []
        for target_llm_connector in self.connector_instances:
            gen_prompts_generator = self._generate_prompts(target_llm_connector.id)
            gen_results_generator = self._generate_predictions(
                gen_prompts_generator, target_llm_connector
            )
            generator_list.append(gen_results_generator)
        for generator in generator_list:
            async for result in generator:
                consolidated_result_list.append(result)
        return consolidated_result_list

    async def _generate_prompts(
        self, target_llm_connector_id: str
    ) -> AsyncGenerator[RedTeamingPromptArguments, None]:
        """
        Generates prompts for the red teaming process based on the provided arguments.

        Retrieves the prompt from the context strategy instance and processes it using the specified prompt template.
        Yields a RedTeamingPromptArguments object containing the generated prompt information.

        Args:
            target_llm_connector_id (str): The ID of the target LLM connector.

        Yields:
            RedTeamingPromptArguments: An object containing the generated prompt information.
        """
        prompt = self.prompt

        if self.context_strategy_info:
            context_strategy_instance = self.context_strategy_instances[0]
            num_of_prev_prompts = self.context_strategy_info[0].get(
                "num_of_prev_prompts"
            )
            prompt = ContextStrategy.process_prompt_cs(
                self.prompt,
                context_strategy_instance.id,
                self.database_instance,
                target_llm_connector_id,
                num_of_prev_prompts,
            )
        if self.prompt_templates:
            # prepare prompt template generator
            pt_id = self.prompt_templates[0]
            pt_info = Storage.read_object_with_iterator(
                EnvVariables.PROMPT_TEMPLATES.name,
                pt_id,
                "json",
                iterator_keys=["template"],
            )
            pt = next(pt_info["template"])
            jinja2_template = Template(pt)
            prompt = jinja2_template.render({"prompt": prompt})

        yield RedTeamingPromptArguments(
            conn_id=target_llm_connector_id,
            cs_id=self.context_strategy_instances[0].id
            if self.context_strategy_info
            else "",
            pt_id=self.prompt_templates[0] if self.prompt_templates else "",
            original_prompt=self.prompt,
            system_prompt=self.system_prompt,
            start_time="",
            connector_prompt=ConnectorPromptArguments(
                prompt_index=0,
                prompt=prompt,
                target="",
            ),
        )

    async def _generate_predictions(
        self,
        gen_prompts_generator: AsyncGenerator[RedTeamingPromptArguments, None],
        llm_connector: Connector,
    ) -> AsyncGenerator[RedTeamingPromptArguments, None]:
        """
        Asynchronously generates predictions based on the provided prompts.

        Args:
            gen_prompts_generator (AsyncGenerator[RedTeamingPromptArguments, None]): An asynchronous generator yielding
            RedTeamingPromptArguments.
            llm_connector (Connector): The LLM connector used for generating predictions.

        Yields:
            AsyncGenerator[RedTeamingPromptArguments, None]: An asynchronous generator yielding
            RedTeamingPromptArguments with updated predictions.
        """
        async for prompt_info in gen_prompts_generator:
            new_prompt_info = RedTeamingPromptArguments(
                conn_id=prompt_info.conn_id,
                cs_id=prompt_info.cs_id,
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
            self.database_instance,
            chat_record_tuple,
            RedTeaming.sql_create_chat_record.format(endpoint_id),
        )

    def load_modules(self) -> None:
        """
        Loads connector, metric, and context strategy instances if available.
        """
        if self.session_metadata.endpoints:
            self.connector_instances = [
                Connector.create(ConnectorEndpoint.read(endpoint))
                for endpoint in self.session_metadata.endpoints
            ]
        else:
            raise RuntimeError(
                "[Red Teaming] No endpoint connectors specified for red teaming."
            )

        if self.context_strategy_info:
            self.context_strategy_instances = [
                ContextStrategy.load(context_strategy_info.get("context_strategy_id"))
                for context_strategy_info in self.context_strategy_info
            ]
        return None


class RedTeamingPromptArguments(BaseModel):
    conn_id: str  # The ID of the connection, default is an empty string

    cs_id: str = ""  # The ID of the context strategy, default is an empty string

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
            "",  # attack module name which is not applicable for manual red teaming
            "",  # metric module name which is not applicable for manual red teaming
            self.original_prompt,
            self.connector_prompt.prompt,
            self.system_prompt,
            str(self.connector_prompt.predicted_results),
            str(self.connector_prompt.duration),
            self.start_time,
        )
