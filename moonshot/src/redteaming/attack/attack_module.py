from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from pathlib import Path
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
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class AttackModule:
    cache_name = "cache"
    cache_extension = "json"
    sql_create_chat_record = """
        INSERT INTO {} (connection_id,context_strategy,prompt_template,attack_module,
        metric,prompt,prepared_prompt,system_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """
    sql_create_chat_history_table = """
        CREATE TABLE IF NOT EXISTS {} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        connection_id text NOT NULL,
        context_strategy text,
        prompt_template text,
        attack_module text,
        metric text,
        prompt text NOT NULL,
        prepared_prompt text NOT NULL,
        system_prompt text,
        predicted_result text NOT NULL,
        duration text NOT NULL,
        prompt_time text NOT NULL
        );
    """

    def __init__(self, am_id: str, am_arguments: AttackModuleArguments | None = None):
        self.id = am_id
        self.req_and_config = self.get_attack_module_req_and_config()
        if am_arguments is not None:
            self.connector_ids = am_arguments.connector_ids
            self.prompt_templates = am_arguments.prompt_templates
            self.prompt = am_arguments.prompt
            self.system_prompt = am_arguments.system_prompt
            self.metric_ids = am_arguments.metric_ids
            self.context_strategy_info = am_arguments.context_strategy_info
            self.db_instance = am_arguments.db_instance
            self.red_teaming_progress = am_arguments.red_teaming_progress
            self.cancel_event = am_arguments.cancel_event
            self.optional_params = am_arguments.optional_params

    @classmethod
    def load(
        cls, am_id: str, am_arguments: AttackModuleArguments | None = None
    ) -> AttackModule:
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
            am_id,
            Storage.get_filepath(EnvVariables.ATTACK_MODULES.name, am_id, "py"),
        )

        if attack_module_inst:
            return attack_module_inst(am_id, am_arguments)
        else:
            raise RuntimeError(
                f"Unable to get defined attack module instance - {am_id}"
            )

    @abstractmethod
    def get_metadata(self) -> dict:
        """
        Get metadata for the attack module.

        Returns a dictionary of the attack module metadata.
        Returns:
            dict: A dictionary containing the metadata of the attack module.
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
        if self.context_strategy_info:
            context_strategy_instance = self.context_strategy_instances[0]
            num_of_prev_prompts = self.context_strategy_info[0].get(
                "num_of_prev_prompts"
            )
            prompt = ContextStrategy.process_prompt_cs(
                prompt,
                context_strategy_instance.id,
                self.db_instance,
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
            am_id=self.id,
            cs_id=self.context_strategy_instances[0].id
            if self.context_strategy_info
            else "",
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
        NOTE: this method does not currently handle callbacks
        Asynchronously sends the default prompt to all Language Learning Models (LLMs).

        This method generates prompts by appending the contents of the prompt template and modifies the prompt with the
        context strategy for each LLM, sends each prompt to the respective LLM, and consolidates the responses into a
        list.

        Returns:
            list: A list of consolidated responses from all LLMs.
        """
        generator_list = []
        consolidated_result_list = []
        if self.connector_ids:
            for target_llm_connector in self.connector_instances:
                gen_prompts_generator = self._generate_prompts(
                    self.prompt, target_llm_connector.id
                )
                gen_results_generator = self._generate_predictions(
                    gen_prompts_generator, target_llm_connector
                )
                generator_list.append(gen_results_generator)

            for generator in generator_list:
                async for result in generator:
                    if self.cancel_event.is_set():
                        logger.warning(
                            "[Red Teaming] Cancellation flag is set. Cancelling task..."
                        )
                        break
                    consolidated_result_list.append(result)
        return consolidated_result_list

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
                if self.cancel_event.is_set():
                    logger.warning(
                        "[Red Teaming] Cancellation flag is set. Cancelling task..."
                    )
                    break

                if self.red_teaming_progress:
                    self.red_teaming_progress.update_red_teaming_progress()

                new_prompt_info = ConnectorPromptArguments(
                    prompt_index=1, prompt=prepared_prompt, target=""
                )
                start_time = datetime.now()
                response = await Connector.get_prediction(
                    new_prompt_info, target_llm_connector
                )
                consolidated_responses.append(response)

                red_teaming_prompt_arguments = RedTeamingPromptArguments(
                    conn_id=target_llm_connector.id,
                    am_id=self.id,
                    cs_id=self.context_strategy_instances[0].id
                    if self.context_strategy_info
                    else "",
                    me_id=self.metric_ids[0] if self.metric_ids else "",
                    pt_id=self.prompt_templates[0] if self.prompt_templates else "",
                    original_prompt=self.prompt,  # original prompt
                    system_prompt=self.system_prompt,  # system prompt
                    start_time=str(start_time),
                    connector_prompt=response,
                )

                if self.red_teaming_progress:
                    self.red_teaming_progress.update_red_teaming_chats(
                        red_teaming_prompt_arguments.to_dict(), RunStatus.RUNNING
                    )

                self._write_record_to_db(
                    red_teaming_prompt_arguments.to_tuple(), target_llm_connector.id
                )

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

        # perform a check to see if the target endpoint has its table in the db. if not, create one
        endpoint_id = target_llm_connector.id.replace("-", "_")
        if not Storage.check_database_table_exists(self.db_instance, endpoint_id):
            Storage.create_database_table(
                self.db_instance,
                AttackModule.sql_create_chat_history_table.format(endpoint_id),
            )

        for prepared_prompt in list_of_prompts:
            if self.cancel_event.is_set():
                logger.warning(
                    "[Red Teaming] Cancellation flag is set. Cancelling task..."
                )
                break

            if self.red_teaming_progress:
                self.red_teaming_progress.update_red_teaming_progress()

            new_prompt_info = ConnectorPromptArguments(
                prompt_index=1, prompt=prepared_prompt, target=""
            )
            start_time = datetime.now()
            response = await Connector.get_prediction(
                new_prompt_info, target_llm_connector
            )
            consolidated_responses.append(response)
            red_teaming_prompt_arguments = RedTeamingPromptArguments(
                conn_id=target_llm_connector.id,
                am_id=self.id,
                cs_id=self.context_strategy_instances[0].id
                if self.context_strategy_info
                else "",
                me_id=self.metric_ids[0] if self.metric_ids else "",
                pt_id=self.prompt_templates[0] if self.prompt_templates else "",
                original_prompt=self.prompt,  # original prompt
                system_prompt=self.system_prompt,  # system prompt
                start_time=str(start_time),
                connector_prompt=response,
            )

            # update callback arguments
            if self.red_teaming_progress:
                self.red_teaming_progress.update_red_teaming_chats(
                    red_teaming_prompt_arguments.to_dict(), RunStatus.RUNNING
                )
            self._write_record_to_db(
                red_teaming_prompt_arguments.to_tuple(), target_llm_connector.id
            )

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
            if self.cancel_event.is_set():
                logger.warning(
                    "[Red Teaming] Cancellation flag is set. Cancelling task..."
                )
                break
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

    def load_modules(self) -> None:
        """
        Loads connector, metric, and context strategy instances if available.
        """
        if self.connector_ids:
            self.connector_instances = [
                Connector.create(ConnectorEndpoint.read(endpoint))
                for endpoint in self.connector_ids
            ]
        else:
            raise RuntimeError(
                "[Red Teaming] No connector endpoints specified for red teaming."
            )

        if self.metric_ids:
            self.metric_instances = [
                Metric.load(metric_id) for metric_id in self.metric_ids
            ]

        if self.context_strategy_info:
            self.context_strategy_instances = [
                ContextStrategy.load(context_strategy_info.get("context_strategy_id"))
                for context_strategy_info in self.context_strategy_info
            ]
        return None

    @staticmethod
    def get_cache_information() -> dict:
        """
        Retrieves cache information from the storage.

        This method attempts to read the cache information from the storage and return it as a dictionary.
        If the cache information does not exist or an error occurs, it returns an empty dictionary.

        Returns:
            dict: A dictionary containing the cache information or an empty dictionary if an error occurs
            or if the cache information does not exist.

        Raises:
            Exception: If there's an error during the retrieval process, it is logged and an
            empty dictionary is returned.
        """
        try:
            # Retrieve cache information from the storage and return it as a dictionary
            cache_info = Storage.read_object(
                EnvVariables.ATTACK_MODULES.name, AttackModule.cache_name, "json"
            )
            return cache_info if cache_info else {}
        except Exception as e:
            logger.error(f"No previous cache information: {str(e)}")
            return {}

    @staticmethod
    def write_cache_information(cache_info: dict) -> None:
        """
        Writes the updated cache information to the storage.

        Args:
            cache_info (dict): The cache information to be written.
        """
        try:
            Storage.create_object(
                obj_type=EnvVariables.ATTACK_MODULES.name,
                obj_id=AttackModule.cache_name,
                obj_info=cache_info,
                obj_extension=AttackModule.cache_extension,
            )
        except Exception as e:
            logger.error(f"Failed to write cache information: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[dict]]:
        """
        Retrieves the list of available attack modules and their information.

        This method scans the storage for attack modules, filters out any non-relevant files,
        and updates the cache information if necessary. It returns a tuple containing a list of
        attack module IDs and a list of dictionaries with detailed information about each module.

        Returns:
            tuple[list[str], list[dict]]: A tuple with two elements. The first element is a list
                                           of attack module IDs. The second element is a list of
                                           dictionaries, each containing information about an
                                           attack module.
        """
        try:
            retn_ams = []
            retn_am_ids = []
            am_cache_info = AttackModule.get_cache_information()
            cache_needs_update = False  # Initialize a flag to track cache updates
            ams = Storage.get_objects(EnvVariables.ATTACK_MODULES.name, "py")

            for am in ams:
                if "__" in am:
                    continue

                am_name = Path(am).stem
                am_info, cache_updated = AttackModule._get_or_update_attack_module_info(
                    am_name, am_cache_info
                )
                if cache_updated:
                    cache_needs_update = True  # Set the flag if any cache was updated

                retn_ams.append(am_info)
                retn_am_ids.append(am_name)

            if cache_needs_update:  # Check the flag after the loop
                AttackModule.write_cache_information(am_cache_info)

            return retn_am_ids, retn_ams

        except Exception as e:
            logger.error(f"Failed to get available attack modules: {str(e)}")
            raise e

    @staticmethod
    def _get_or_update_attack_module_info(
        am_name: str, am_cache_info: dict
    ) -> tuple[dict, bool]:
        """
        Retrieves or updates the attack module information from the cache.

        This method checks if the attack module information is already available in the cache and if the file hash
        matches the one stored in the cache. If it does, the information is retrieved from the cache.

        If not, the attack module information is read from the storage, the cache is updated with the new information
        and the new file hash, and a flag is set to indicate that the cache has been updated.

        Args:
            am_name (str): The name of the attack module.
            am_cache_info (dict): A dictionary containing the cached attack module information.

        Returns:
            tuple[dict, bool]: A tuple containing the dictionary with the attack module information
                               and a boolean indicating whether the cache was updated or not.
        """
        file_hash = Storage.get_file_hash(
            EnvVariables.ATTACK_MODULES.name, am_name, "py"
        )
        cache_updated = False

        if am_name in am_cache_info and file_hash == am_cache_info[am_name]["hash"]:
            am_metadata = am_cache_info[am_name].copy()
            am_metadata.pop("hash", None)
        else:
            am_metadata = AttackModule.load(am_name).get_metadata()  # type: ignore ; ducktyping
            am_cache_info[am_name] = am_metadata.copy()
            am_cache_info[am_name]["hash"] = file_hash
            cache_updated = True

        return am_metadata, cache_updated

    def get_attack_module_req_and_config(self) -> dict:
        """
        Retrieves the configuration for a specific attack module by its identifier.

        Returns:
            dict: The attack module configuration as a dictionary. Returns an empty dict if the configuration
            is not found.

        Raises:
            Exception: If reading the attack module configuration fails or if the configuration cannot be created.
        """
        attack_module_config = "attack_modules_config"
        try:
            obj_results = Storage.read_object(
                EnvVariables.ATTACK_MODULES.name, attack_module_config, "json"
            )
            return obj_results.get(self.id, {})
        except Exception as e:
            logger.warning(
                f"[AttackModule] Failed to read attack module configuration: {str(e)}"
            )
            logger.info("Attempting to create empty attack module configuration...")
            try:
                Storage.create_object(
                    obj_type=EnvVariables.ATTACK_MODULES.name,
                    obj_id=attack_module_config,
                    obj_info={},
                    obj_extension="json",
                )
                # After creation, attempt to read it again to ensure it was created successfully
                obj_results = Storage.read_object(
                    EnvVariables.ATTACK_MODULES.name, attack_module_config, "json"
                )
                return obj_results.get(self.id, {})
            except Exception as e:
                raise Exception(
                    f"[AttackModule] Failed to retrieve attack modules configuration: {str(e)}"
                )

    @staticmethod
    def delete(am_id: str) -> bool:
        """
        Deletes the specified attack module from storage.

        This method attempts to delete the attack module identified by the given ID from the storage.
        If the deletion is successful, it returns True. If an exception occurs during the deletion process,
        it prints an error message and re-raises the exception.

        Args:
            am_id (str): The ID of the attack module to be deleted.

        Returns:
            bool: True if the attack module was successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.ATTACK_MODULES.name, am_id, "py")
            return True

        except Exception as e:
            logger.error(f"Failed to delete attack module: {str(e)}")
            raise e


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
        Converts the RedTeamingPromptArguments instance into a tuple.

        This method collects all the attributes of the RedTeamingPromptArguments instance and forms a tuple
        with the attribute values in this specific order: conn_id, cs_id, pt_id, am_id, me_id, original_prompt,
        connector_prompt.prompt, system_prompt, connector_prompt.predicted_results.response,
        connector_prompt.duration, start_time.

        Returns:
            tuple: A tuple representation of the RedTeamingPromptArguments instance.
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
            self.connector_prompt.predicted_results.response
            if self.connector_prompt.predicted_results
            else "",
            str(self.connector_prompt.duration),
            self.start_time,
        )

    def to_dict(self) -> dict:
        """
        Converts the RedTeamingPromptArguments instance into a dictionary.

        This method collects all the attributes of the RedTeamingPromptArguments instance and forms a dictionary
        with the keys: conn_id, cs_id, pt_id, am_id, me_id, original_prompt, system_prompt, prepared_prompt,
        response, duration, start_time.

        Returns:
            dict: A dictionary representation of the RedTeamingPromptArguments instance.
        """
        return {
            "conn_id": self.conn_id,
            "cs_id": self.cs_id,
            "pt_id": self.pt_id,
            "am_id": self.am_id,
            "me_id": self.me_id,
            "original_prompt": self.original_prompt,
            "prepared_prompt": self.connector_prompt.prompt,
            "system_prompt": self.system_prompt,
            "response": (
                self.connector_prompt.predicted_results.response
                if self.connector_prompt.predicted_results
                else ""
            ),
            "duration": str(self.connector_prompt.duration),
            "start_time": self.start_time,
        }
