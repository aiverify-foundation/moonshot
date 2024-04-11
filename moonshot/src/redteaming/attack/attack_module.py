from __future__ import annotations

import ast
from abc import abstractmethod
from datetime import datetime
from typing import AsyncGenerator

from jinja2 import Template
from pydantic import BaseModel

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance

# variable to cap the number of prompts sent to the LLMs in case the stop condition
# of the attack does not get fulfilled
MAX_NO_ITERATIONS = 5


class AttackModule:
    def __init__(self, am_args: AttackModuleArguments):
        self.name = am_args.name
        self.recipe_id = am_args.recipe_id
        self.num_of_prompts = am_args.num_of_prompts
        self.connector_instances = am_args.connector_instances
        self.stop_strategy_instances = am_args.stop_strategy_instances
        self.datasets = am_args.datasets
        self.prompt_templates = am_args.prompt_templates
        self.metric_instances = am_args.metric_instances
        self.context_strategies = am_args.context_strategies
        self.db_instance = am_args.db_instance

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

    # TODO to permutate the no. of datasets x prompt templates
    # currently, we're just taking the first dataset and prompt template defined
    def prepare_prompt(self) -> str:
        # if there is at least one dataset defined
        if self.datasets:
            ds_name = self.datasets[0]
            ds_details = Storage.read_object(
                EnvVariables.DATASETS.name, ds_name, "json"
            )
            prompt = ds_details["examples"]

        # TODO: if there is no dataset defined, decide where to get user prompt or a seed
        # user provide prompt
        else:
            prompt = ""

        if self.prompt_templates:
            pt_name = self.prompt_templates[0]
            pt_details = Storage.read_object(
                EnvVariables.PROMPT_TEMPLATES.name, pt_name, "json"
            )
            template = pt_details["template"]
            jinja_template = Template(template)
            return jinja_template.render({"prompt": prompt})

        return prompt

    def get_max_no_iterations(self) -> int:
        """
        Returns the default maximum number of iterations allowed.

        Returns:
            int: The default maximum number of iterations allowed.
        """
        return MAX_NO_ITERATIONS

    def check_stop_condition(
        self,
        prompt: str,
        iteration_count: int,
        llm_response: str,
    ) -> bool:
        """
        Checks if any stop strategy triggers the end of the red teaming attack based on the prompt iteration count
        and LLM response.

        Args:
            iteration_count (int): The current prompt iteration count.
            llm_response (str): The response from the LLM model.

        Returns:
            bool: True if any stop strategy triggers the end of the attack, False otherwise.
        """
        for stop_strategy in self.stop_strategy_instances:
            if stop_strategy.stop_red_teaming_attack(
                prompt, iteration_count, llm_response, self.metric_instances
            ):
                print("Stopping red teaming as criteria is fulfilled...")
                return True
        return False

    async def send_prompt(
        self,
        connector_instance: Connector,
        prepared_prompt: str,
    ) -> str:
        """
        Sends a prompt to a LLM endpoint, stores LLM prediction in the LLM chat table,
        and returns the predicted results.

        Args:
            connector_instance (Connector): The LLM connector instance to send the prompt to.
            prepared_prompt (str): The prepared prompt to send.

        Returns:
            str: The predicted results from the LLM endpoint.
        """
        prompt_template_name = ""
        if self.prompt_templates:
            prompt_template_name = self.prompt_templates[0]

        dataset_name = ""
        if self.datasets:
            dataset_name = self.datasets[0]

        new_prompt_info = ConnectorPromptArguments(
            prompt_index=1, prompt=prepared_prompt, target=""
        )

        prompt_start_time = datetime.now()

        # sends prompt to endpoint
        prediction_response = await Connector.get_prediction(
            new_prompt_info, connector_instance
        )

        # stores chat prompts, predictions and its config into DB
        chat_record_tuple = (
            "",
            "",
            prompt_template_name,
            dataset_name,
            prepared_prompt,
            prediction_response.predicted_results,
            prediction_response.duration,
            prompt_start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        )

        self.write_record_to_db(chat_record_tuple, connector_instance.id)
        return prediction_response.predicted_results

    def write_record_to_db(
        self,
        chat_record_tuple: tuple,
        chat_record_id,
    ) -> None:

        endpoint_id = chat_record_id.replace("-", "_")
        sql_create_chat_record = f"""
            INSERT INTO {endpoint_id} (connection_id,context_strategy,prompt_template,prompt,
            prepared_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?)
            """

        Storage.create_database_record(
            self.db_instance, chat_record_tuple, sql_create_chat_record
        )

    @abstractmethod
    async def execute(self):
        pass

    async def _generate_prompts(self) -> AsyncGenerator[PromptArguments, None]:
        """
        Asynchronously generates prompts based on the provided recipe ID, dataset IDs and prompt template IDs.

        This method uses the dataset IDs and prompt template IDs to retrieve the corresponding datasets and
        prompt templates. It then uses the Jinja2 template engine to render the prompts using the datasets and
        templates. If no prompt template IDs are provided, the method generates prompts using only the datasets.

        Args:
            rec_id (str): The recipe ID.
            ds_ids (list[str]): A list of dataset IDs.
            pt_ids (list[str], optional): A list of prompt template IDs. Defaults to an empty list.

        Yields:
            AsyncGenerator[PromptArguments, None]: An asynchronous generator that yields PromptArguments objects.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        if self.prompt_templates:

            # prepare prompt template generator
            for pt_id in self.prompt_templates:
                pt_info = Storage.read_object_generator(
                    EnvVariables.PROMPT_TEMPLATES.name, pt_id, "json", "template"
                )
                pt = next(pt_info)
                jinja2_template = Template(pt)

                for ds_id in self.datasets:
                    ds_info = Storage.read_object_generator(
                        EnvVariables.DATASETS.name, ds_id, "json", "examples.item"
                    )
                    for prompt_index, prompt in enumerate(ds_info, 1):
                        try:
                            if (
                                self.num_of_prompts != 0
                                and prompt_index > self.num_of_prompts
                            ):
                                break

                            rendered_prompt = jinja2_template.render(
                                {"prompt": prompt["input"]}
                            )
                            print(
                                f"Generating prompt with dataset [{ds_id}] and prompt template [{pt_id}]."
                            )
                            yield PromptArguments(
                                rec_id=self.recipe_id,
                                pt_id=pt_id,
                                ds_id=ds_id,
                                connector_prompt=ConnectorPromptArguments(
                                    prompt_index=prompt_index,
                                    prompt=rendered_prompt,
                                    target=prompt["target"],
                                ),
                            )
                        except Exception as e:
                            error_message = (
                                f"[RedTeamingError] Error while generating prompt for prompt_info "
                                f"[rec_id: {self.recipe_id}, ds_id: {ds_id}, pt_id: {pt_id}, \
                                    prompt_index: {prompt_index}] "
                                f"due to error: {str(e)}"
                            )
                            # self.handle_error_message(error_message)
                            print(error_message)
                            continue
        else:
            pt_id = "no-template"
            for ds_id in self.datasets:
                ds_info = Storage.read_object_generator(
                    EnvVariables.DATASETS.name, ds_id, "json", "examples.item"
                )
                for prompt_index, prompt in enumerate(ds_info, 1):
                    try:
                        if (
                            self.num_of_prompts != 0
                            and prompt_index > self.num_of_prompts
                        ):
                            break

                        yield PromptArguments(
                            rec_id=self.recipe_id,
                            pt_id=pt_id,
                            ds_id=ds_id,
                            connector_prompt=ConnectorPromptArguments(
                                prompt_index=prompt_index,
                                prompt=prompt["input"],
                                target=prompt["target"],
                            ),
                        )
                    except Exception as e:
                        error_message = (
                            f"[RedTeamingError] Error while generating prompt for prompt_info "
                            f"[rec_id: {self.recipe_id}, ds_id: {ds_id}, pt_id: {pt_id}, prompt_index: {prompt_index}] "
                            f"due to error: {str(e)}"
                        )
                        # self.handle_error_message(error_message)
                        print(error_message)
                        continue

    async def _generate_predictions(
        self,
        gen_prompt: AsyncGenerator[PromptArguments, None],
        llm_connector: Connector,
    ):
        """
        This method generates predictions for the given prompts using the provided recipe connectors and
        database instance.

        This method is a coroutine that takes an asynchronous generator of prompts, a list of recipe connectors,
        and a database instance.

        It iterates over the prompts from the generator and for each prompt, it iterates over the recipe connectors.
        For each connector, it updates the prompt with the connector id and checks if the prompt has saved records
        in the cache.
        If there are no saved records, it gets predictions from the connector and creates cache records.
        If there are saved records, it updates the prompt info from the cache records.
        Finally, it yields the updated prompt info.

        Args:
            gen_prompt (AsyncGenerator[PromptArguments, None]): An asynchronous generator of prompts.
            recipe_connectors (list[Connector]): A list of recipe connectors.
            database_instance (Any): A database instance.

        Yields:
            PromptArguments: The updated prompt info.

        Raises:
            Exception: If there is an error during cache reading or any other operation within the method.
        """
        iteration_count = 1
        async for prompt_info in gen_prompt:
            # Create a new prompt info with connection id
            new_prompt_info = PromptArguments(
                conn_id=llm_connector.id,
                rec_id=prompt_info.rec_id,
                pt_id=prompt_info.pt_id,
                ds_id=prompt_info.ds_id,
                connector_prompt=prompt_info.connector_prompt,
            )
            prompt_start_time = datetime.now()
            new_prompt_info.connector_prompt = await Connector.get_prediction(
                new_prompt_info.connector_prompt, llm_connector
            )

            # stores chat prompts, predictions and its config into DB
            chat_record_tuple = (
                "",
                "",
                new_prompt_info.pt_id,
                new_prompt_info.pt_id,
                new_prompt_info.connector_prompt.prompt,
                new_prompt_info.connector_prompt.predicted_results,
                new_prompt_info.connector_prompt.duration,
                prompt_start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            )
            self.write_record_to_db(chat_record_tuple, llm_connector.id)

            print(
                "Generated prompt:",
                new_prompt_info.connector_prompt.predicted_results,
                "\n",
            )

            # hit max no. of default iterations
            if iteration_count >= self.get_max_no_iterations():
                print("Stopping red teaming as maximum number of iteration is hit.")
                break
            iteration_count += 1

            yield new_prompt_info


class PromptArguments(BaseModel):
    conn_id: str = ""  # The ID of the connection, default is an empty string

    rec_id: str  # The ID of the recipe

    ds_id: str  # The ID of the dataset

    pt_id: str  # The ID of the prompt template

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
            self.rec_id,
            self.ds_id,
            self.pt_id,
            self.connector_prompt.prompt_index,
            self.connector_prompt.prompt,
            str(self.connector_prompt.target),
            str(self.connector_prompt.predicted_results),
            str(self.connector_prompt.duration),
        )

    @classmethod
    def from_tuple(cls, cache_record: tuple) -> PromptArguments:
        """
        Converts a tuple into a PromptArguments instance.

        This method accepts a tuple that contains attribute values in the following order:
        conn_id, rec_id, ds_id, pt_id, prompt_index, prompt, target, predicted_results, duration.
        It then constructs a PromptArguments instance using these values.
        This method is primarily used for deserialization tasks, such as retrieving prompt arguments data from a
        database or receiving it over a network.

        Args:
            cache_record (tuple): A tuple containing the attribute values for a PromptArguments instance.

        Returns:
            PromptArguments: A PromptArguments instance constructed from the tuple.
        """
        # The target and predicted_results fields may be stored as strings in the cache_record.
        # ast.literal_eval is used to attempt to convert these strings back into their original data types.
        # If the conversion fails (i.e., the fields are not string representations of Python literals),
        # the original string values are used.
        try:
            target = ast.literal_eval(cache_record[7])
        except Exception:
            target = cache_record[7]

        try:
            predicted_results = ast.literal_eval(cache_record[8])
        except Exception:
            predicted_results = cache_record[8]

        return cls(
            conn_id=cache_record[1],
            rec_id=cache_record[2],
            ds_id=cache_record[3],
            pt_id=cache_record[4],
            connector_prompt=ConnectorPromptArguments(
                prompt_index=cache_record[5],
                prompt=cache_record[6],
                target=target,
                predicted_results=predicted_results,
                duration=float(cache_record[9]),
            ),
        )
