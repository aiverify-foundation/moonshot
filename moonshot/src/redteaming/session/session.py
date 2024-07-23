from __future__ import annotations

import asyncio
import time
from ast import literal_eval
from datetime import datetime
from typing import Any, Callable

from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.chat import Chat
from moonshot.src.redteaming.session.red_teaming_progress import RedTeamingProgress
from moonshot.src.redteaming.session.red_teaming_type import RedTeamingType
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class SessionMetadata:
    # TODO: convert this into a pydantic model
    def __init__(
        self,
        session_id: str,
        endpoints: list[str],
        created_epoch: float,
        created_datetime: str,
        prompt_template: str,
        context_strategy: str,
        cs_num_of_prev_prompts: int,
        attack_module: str,
        metric: str,
        system_prompt: str,
    ):
        self.session_id = self.check_type(session_id, str)
        self.endpoints = self.check_type(endpoints, list)
        self.created_epoch = self.check_type(created_epoch, float)
        self.created_datetime = self.check_type(created_datetime, str)
        self.prompt_template = self.check_type(prompt_template, str)
        self.context_strategy = self.check_type(context_strategy, str)
        self.cs_num_of_prev_prompts = self.check_type(cs_num_of_prev_prompts, int)
        self.attack_module = self.check_type(attack_module, str)
        self.metric = self.check_type(metric, str)
        self.system_prompt = self.check_type(system_prompt, str)

    def to_dict(self) -> dict:
        """
        Converts the SessionMetadata instance into a dictionary.

        Returns:
            dict: A dictionary representation of the SessionMetadata instance.
        """
        return {
            "session_id": self.session_id,
            "endpoints": self.endpoints,
            "created_epoch": str(self.created_epoch),
            "created_datetime": self.created_datetime,
            "prompt_template": self.prompt_template,
            "context_strategy": self.context_strategy,
            "cs_num_of_prev_prompts": self.cs_num_of_prev_prompts,
            "attack_module": self.attack_module,
            "metric": self.metric,
            "system_prompt": self.system_prompt,
        }

    def to_tuple(self) -> tuple:
        """
        Converts the SessionMetadata instance into a tuple.

        Returns:
            tuple: A tuple representation of the SessionMetadata instance.
        """
        return (
            self.session_id,
            str(self.endpoints),
            self.created_epoch,
            self.created_datetime,
            self.prompt_template,
            self.context_strategy,
            self.cs_num_of_prev_prompts,
            self.attack_module,
            self.metric,
            self.system_prompt,
        )

    @classmethod
    def from_tuple(cls, data_tuple: tuple) -> SessionMetadata:
        """
        Creates a SessionMetadata instance from a tuple using the class method.

        Args:
            data_tuple (tuple): A tuple containing session_id, endpoints, created_epoch, and created_datetime.

        Returns:
            SessionMetadata: An instance of SessionMetadata.
        """
        (
            runner_id,
            endpoints,
            created_epoch,
            created_datetime,
            prompt_template,
            context_strategy,
            cs_num_of_prev_prompts,
            attack_module,
            metric,
            system_prompt,
        ) = data_tuple

        return cls(
            runner_id,
            literal_eval(endpoints),
            created_epoch,
            created_datetime,
            prompt_template,
            context_strategy,
            cs_num_of_prev_prompts,
            attack_module,
            metric,
            system_prompt,
        )

    def check_type(self, checked_attribute: Any, expected_type: type) -> Any:
        """
        Checks if the type of the given attribute matches the expected type.

        Args:
            checked_attribute (Any): The attribute to be checked.
            expected_type (type): The expected type of the attribute.

        Returns:
            Any: The checked attribute if its type matches the expected type.

        Raises:
            TypeError: If the type of the checked attribute does not match the expected type.
        """
        if not isinstance(checked_attribute, expected_type):
            raise TypeError(
                f"Expected type for {checked_attribute} is {expected_type}, but got {type(checked_attribute)}"
            )
        return checked_attribute


class Session:
    DEFAULT_CONTEXT_STRATEGY_PROMPT = 5
    sql_create_session_metadata_table = """
            CREATE TABLE IF NOT EXISTS session_metadata_table (
            session_id text PRIMARY KEY NOT NULL,
            endpoints text NOT NULL,
            created_epoch INTEGER NOT NULL,
            created_datetime text NOT NULL,
            prompt_template text,
            context_strategy text,
            cs_num_of_prev_prompts int,
            attack_module text,
            metric text,
            system_prompt text
            );
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

    sql_create_session_metadata_record = """
        INSERT INTO session_metadata_table (
        session_id,endpoints,created_epoch,created_datetime,prompt_template,context_strategy,cs_num_of_prev_prompts,
        attack_module, metric, system_prompt) VALUES(?,?,?,?,?,?,?,?,?,?)
    """

    sql_read_session_metadata = """
        SELECT * from session_metadata_table
    """

    sql_update_session_metadata_field = """
        UPDATE session_metadata_table SET {}=? WHERE session_id=?
    """

    sql_drop_table = """
        DROP TABLE IF EXISTS {}
    """

    def __init__(
        self,
        runner_id: str,
        runner_type: RunnerType,
        runner_args: dict,
        database_instance: Any | None,
        endpoints: list[str],
        results_file_path: str,
        progress_callback_func: Callable | None = None,
    ):
        """
        Initializes a new session with the given parameters, creates session metadata,
        and sets up the database tables for session metadata and chat history.

        Args:
            runner_id (str): The unique identifier for the runner.
            runner_type (RunnerType): The type of runner being used.
            runner_args (dict): A dictionary of arguments specific to the runner.
            database_instance (Any | None): The database instance to connect to, or None if not available.
            endpoints (list[str]): A list of endpoint identifiers.
            results_file_path (str): The file path where results should be stored.
            progress_callback_func (Callable | None): An optional callback function for progress updates.
        """
        created_epoch = time.time()
        created_datetime = datetime.fromtimestamp(created_epoch).strftime(
            "%Y%m%d-%H%M%S"
        )

        self.runner_id = slugify(runner_id, lowercase=True)
        if self.runner_id != runner_id:
            raise RuntimeError(
                "[Session] Failed to initialise Session. Invalid Runner ID."
            )

        self.runner_args = runner_args
        self.runner_type = runner_type
        self.results_file_path = results_file_path
        self.progress_callback_func = progress_callback_func
        self.database_instance = database_instance

        self.red_teaming_progress = RedTeamingProgress(
            self.runner_id, self.runner_args, self.progress_callback_func
        )

        self.cancel_event = asyncio.Event()

        prompt_template = self.runner_args.get("prompt_template", "")
        context_strategy = self.runner_args.get("context_strategy", "")
        cs_num_of_prev_prompts = self.runner_args.get(
            "cs_num_of_prev_prompts", Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
        )
        attack_module = self.runner_args.get("attack_module", "")
        system_prompt = self.runner_args.get("system_prompt", "")
        metric_id = self.runner_args.get("metric_id", "")

        self.check_file_exists(
            EnvVariables.PROMPT_TEMPLATES.name,
            prompt_template,
            "Prompt Template",
            "json",
        )
        self.check_file_exists(
            EnvVariables.CONTEXT_STRATEGY.name,
            context_strategy,
            "Context Strategy",
            "py",
        )
        self.check_file_exists(
            EnvVariables.ATTACK_MODULES.name, attack_module, "Attack Module", "py"
        )
        self.check_file_exists(EnvVariables.METRICS.name, metric_id, "Metric", "py")

        if self.database_instance:
            # create session metadata table if it does not exist
            if not Storage.check_database_table_exists(
                self.database_instance, "session_metadata_table"
            ):
                Storage.create_database_table(
                    self.database_instance, Session.sql_create_session_metadata_table
                )

            # get session metadata record
            session_metadata_records = Storage.read_database_records(
                self.database_instance, Session.sql_read_session_metadata
            )

            # check if the session metadata record already exists
            if session_metadata_records:
                logger.info("[Session] Session already exists.")
                self.session_metadata = SessionMetadata.from_tuple(
                    session_metadata_records[0]
                )
            # create a new record if session metadata does not exist
            else:
                logger.info("[Session] Creating new session.")

                # create chat history table for each endpoint

                self.session_metadata = SessionMetadata(
                    runner_id,
                    endpoints,
                    created_epoch,
                    created_datetime,
                    prompt_template,
                    context_strategy,
                    cs_num_of_prev_prompts,
                    attack_module,
                    metric_id,
                    system_prompt,
                )

                for endpoint in endpoints:
                    endpoint_id = endpoint.replace("-", "_")
                    Storage.create_database_table(
                        self.database_instance,
                        Session.sql_create_chat_history_table.format(endpoint_id),
                    )

                Storage.create_database_record(
                    self.database_instance,
                    self.session_metadata.to_tuple(),
                    Session.sql_create_session_metadata_record,
                )
        else:
            raise RuntimeError(
                "[Session] Failed to initialise Session. No database instance provided."
            )

    @staticmethod
    def load(database_instance: DBInterface | None) -> dict | None:
        """
        Loads run data for a given session_id from the database, or the latest run if run_id is None.

        This method retrieves run data for the specified run_id from the database, or if run_id is None,
        it retrieves the latest run. If the database instance is not provided, it raises a RuntimeError.
        If the database instance is provided, it invokes the read_record method of the database instance
        with the given run_id or the latest run and returns a RunArguments object created from the retrieved record.

        Parameters:
            database_instance (DBInterface | None): The database accessor instance.
            run_id (int | None): The ID of the run to retrieve, or None to retrieve the latest run.

        Returns:
            RunArguments: An object containing the details of the run with the given run_id or the latest run.
        """
        if not database_instance:
            raise RuntimeError("[Session] Runner instance database not provided.")

        # runner does not have session, return None
        if not Storage.check_database_table_exists(
            database_instance, "session_metadata_table"
        ):
            return None

        # retrieve session metadata
        session_metadata_info = Storage.read_database_records(
            database_instance,
            Session.sql_read_session_metadata,
        )

        if not session_metadata_info:
            raise RuntimeError("[Session] Failed to get Session metadata.")

        # convert session metadata from tuple to dict
        session_metadata_obj = SessionMetadata.from_tuple(session_metadata_info[0])
        session_metadata_dict = session_metadata_obj.to_dict()

        return session_metadata_dict

    async def run(self) -> list | None:
        """
        Asynchronously executes the session run process.

        This method orchestrates the entire session run process asynchronously. It initializes the session,
        sets up the necessary environment, executes the session's main logic, handles any errors, and finally,
        compiles and returns the results in a dictionary format. Throughout the process, it updates
        the session's status and logs progress.

        Returns:
            dict: A dictionary containing the results of the session run, including any errors encountered.
        """
        # ------------------------------------------------------------------------------
        # Part 1: Get asyncio running loop
        # ------------------------------------------------------------------------------
        logger.debug("[Session] Part 1: Loading asyncio running loop...")
        loop = asyncio.get_running_loop()

        # ------------------------------------------------------------------------------
        # Part 2: Load runner processing module
        # ------------------------------------------------------------------------------
        logger.debug("[Session] Part 2: Loading runner processing module...")
        start_time = time.perf_counter()
        runner_module_instance = None
        try:
            runner_processing_module_name = self.runner_args.get(
                "runner_processing_module", None
            )
            if runner_processing_module_name:
                # Intialize the runner instance
                runner_module_instance = get_instance(
                    runner_processing_module_name,
                    Storage.get_filepath(
                        EnvVariables.RUNNERS_MODULES.name,
                        runner_processing_module_name,
                        "py",
                    ),
                )
                if runner_module_instance:
                    runner_module_instance = runner_module_instance()
                else:
                    raise RuntimeError(
                        f"Unable to get defined runner module instance - {runner_module_instance}"
                    )
            else:
                raise RuntimeError(
                    f"Failed to get runner processing module name: {runner_processing_module_name}"
                )

        except Exception as e:
            logger.error(
                f"[Session] Failed to load runner processing module in Part 2 due to error: {str(e)}"
            )
            raise e

        finally:
            logger.debug(
                f"[Session] Loading runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Run runner processing module
        # ------------------------------------------------------------------------------
        logger.debug("[Session] Part 3: Running runner processing module...")
        start_time = time.perf_counter()
        runner_results = {}

        try:
            if runner_module_instance:
                runner_results = await runner_module_instance.generate(  # type: ignore ; ducktyping
                    loop,
                    self.runner_args,
                    self.database_instance,
                    self.session_metadata,
                    self.check_redteaming_type(),
                    self.red_teaming_progress,
                    self.cancel_event,
                )
            else:
                raise RuntimeError("Failed to initialise runner module instance.")

        except Exception as e:
            logger.error(
                f"[Session] Failed to run runner processing module in Part 3 due to error: {str(e)}"
            )
            raise e

        finally:
            self.red_teaming_progress.status = RunStatus.COMPLETED
            if self.check_redteaming_type() == RedTeamingType.AUTOMATED:
                self.red_teaming_progress.notify_progress()
            logger.debug(
                f"[Session] Running runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 4: Wrap up run
        # ------------------------------------------------------------------------------
        logger.debug("[Session] Part 4: Wrap up run...")
        return runner_results

    def cancel(self) -> None:
        """
        Sets the cancel event to stop the automated red teaming process.

        This method is used to signal that the automated red teaming process should be cancelled. It sets the
        cancel_event which can be checked in various points of the asynchronous red teaming process to gracefully stop
        the execution.

        Returns:
            None
        """
        logger.warning("[Session] Cancelling automated red teaming...")
        self.cancel_event.set()

    def check_redteaming_type(self) -> RedTeamingType:
        """
        Checks the type of red teaming strategy based on the runner arguments.

        Returns:
            RedTeamingType: The type of red teaming strategy.

        Raises:
            RuntimeError: If the red teaming arguments are missing.
        """
        if (
            "attack_strategies" in self.runner_args
            and self.runner_args.get("attack_strategies") is not None
        ):
            return RedTeamingType.AUTOMATED
        elif (
            "manual_rt_args" in self.runner_args
            and self.runner_args.get("manual_rt_args") is not None
        ):
            return RedTeamingType.MANUAL
        else:
            raise RuntimeError("Missing red teaming arguments.")

    @staticmethod
    def update_context_strategy(
        db_instance: DBInterface | None, runner_id: str, context_strategy: str
    ) -> bool:
        """
        Updates the context strategy for a specific runner in the database.

        Args:
            db_instance (DBInterface | None): The database instance to update the context strategy in.
            runner_id (str): The ID of the runner.
            context_strategy (str): The name of the context strategy to be used.

        Returns:
            bool: The status on whether the context strategy is updated successfully.

        Raises:
            RuntimeError: If the database instance is not provided or if the context strategy does not exist.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        if context_strategy and not Storage.is_object_exists(
            EnvVariables.CONTEXT_STRATEGY.name, context_strategy, "py"
        ):
            raise RuntimeError(
                f"[Session] Context Strategy {context_strategy} does not exist."
            )
        else:
            Storage.update_database_record(
                db_instance,
                (context_strategy, runner_id),
                Session.sql_update_session_metadata_field.format("context_strategy"),
            )
            return True

    @staticmethod
    def update_cs_num_of_prev_prompts(
        db_instance: DBInterface | None, runner_id: str, cs_num_of_prev_prompts: int
    ) -> bool:
        """
        Updates the number of previous prompts for a specific runner in the database.

        Args:
            db_instance (DBInterface | None): The database instance to update the number of previous prompts in.
            runner_id (str): The ID of the runner.
            cs_num_of_prev_prompts (int): The new number of previous prompts to be used.

        Returns:
            bool: The status on whether the number of prompts for context strategy is updated successfully.

        Raises:
            RuntimeError: If the database instance is not provided.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        Storage.update_database_record(
            db_instance,
            (cs_num_of_prev_prompts, runner_id),
            Session.sql_update_session_metadata_field.format("cs_num_of_prev_prompts"),
        )
        return True

    @staticmethod
    def update_prompt_template(
        db_instance: DBInterface | None, runner_id: str, prompt_template: str
    ) -> bool:
        """
        Updates the prompt template in the database for the specified runner.

        Args:
            db_instance (DBInterface | None): The database instance to update the prompt template in.
            runner_id (str): The ID of the runner.
            prompt_template (str): The new prompt template to be used.

        Returns:
            bool: The status on whether the prompt template is updated successfully.

            Raises:
                RuntimeError: If the database instance is not provided or if the prompt template does not exist.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        if prompt_template and not Storage.is_object_exists(
            EnvVariables.PROMPT_TEMPLATES.name, prompt_template, "json"
        ):
            raise RuntimeError(
                f"[Session] Prompt Template {prompt_template} does not exist."
            )

        Storage.update_database_record(
            db_instance,
            (prompt_template, runner_id),
            Session.sql_update_session_metadata_field.format("prompt_template"),
        )
        return True

    @staticmethod
    def update_metric(
        db_instance: DBInterface | None, runner_id: str, metric_id: str
    ) -> bool:
        """
        Updates the metric in the database for the specified runner.

        Args:
            db_instance (DBInterface | None): The database instance to update the metric in.
            runner_id (str): The ID of the runner.
            metric_id (str): The new metric to be used.

        Returns:
            bool: The status on whether the metric is updated successfully.

        Raises:
            RuntimeError: If the database instance is not provided or if the metric does not exist.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        if metric_id and not Storage.is_object_exists(
            EnvVariables.METRICS.name, metric_id, "py"
        ):
            raise RuntimeError(f"[Session] Metric {metric_id} does not exist.")
        else:
            Storage.update_database_record(
                db_instance,
                (metric_id, runner_id),
                Session.sql_update_session_metadata_field.format("metric"),
            )
            return True

    @staticmethod
    def update_system_prompt(
        db_instance: DBInterface | None, runner_id: str, system_prompt: str
    ) -> bool:
        """
        Updates the system prompt in the database for the specified runner.

        Args:
            db_instance (DBInterface | None): The database instance to update the system prompt in.
            runner_id (str): The ID of the runner.
            system_prompt (str): The new system prompt to be used.

        Returns:
            bool: The status on whether the system prompt is updated successfully.

        Raises:
            RuntimeError: If the database instance is not provided.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        Storage.update_database_record(
            db_instance,
            (system_prompt, runner_id),
            Session.sql_update_session_metadata_field.format("system_prompt"),
        )
        return True

    @staticmethod
    def update_attack_module(
        db_instance: DBInterface | None, runner_id: str, attack_module_id: str
    ) -> bool:
        """
        Updates the attack module in the database for the specified runner.

        Args:
            db_instance (DBInterface | None): The database instance to update the attack module in.
            runner_id (str): The ID of the runner.
            attack_module_id (str): The new attack module to be used.

        Returns:
            bool: The status on whether the attack module is updated successfully.

        Raises:
            RuntimeError: If the database instance is not provided or if the attack module does not exist.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        if attack_module_id and not Storage.is_object_exists(
            EnvVariables.ATTACK_MODULES.name, attack_module_id, "py"
        ):
            raise RuntimeError(
                f"[Session] Attack Module {attack_module_id} does not exist."
            )
        else:
            Storage.update_database_record(
                db_instance,
                (attack_module_id, runner_id),
                Session.sql_update_session_metadata_field.format("attack_module"),
            )
            return True

    @staticmethod
    def delete(database_instance: DBInterface | None) -> bool:
        """
        Deletes the session metadata and associated endpoint tables from the database.

        Args:
            database_instance (DBInterface | None): The database instance to delete the session from.

        Returns:
            bool: The status on whether the session is deleted successfully.

        Raises:
            RuntimeError: If the database instance is not provided or if failed to get session metadata.
        """
        if not database_instance:
            raise RuntimeError("[Session] Database instance not provided.")

        session_metadata_info = Storage.read_database_records(
            database_instance,
            Session.sql_read_session_metadata,
        )
        if not session_metadata_info:
            raise RuntimeError("[Session] Failed to get Session metadata.")

        session_metadata_obj = SessionMetadata.from_tuple(session_metadata_info[0])
        Storage.delete_database_table(
            database_instance, Session.sql_drop_table.format("session_metadata_table")
        )
        for endpoint in session_metadata_obj.endpoints:
            endpoint = endpoint.replace("-", "_")
            Storage.delete_database_table(
                database_instance, Session.sql_drop_table.format(endpoint)
            )
        return True

    @staticmethod
    def get_session_chats(database_instance: DBInterface | None) -> dict:
        """
        Retrieves the chat history for all endpoints in a session.

        Args:
            database_instance (DBInterface | None): The database instance to retrieve the chat history from.

        Raises:
            RuntimeError: If the database instance is not provided.

        Returns:
            dict: A dictionary where the keys are endpoint IDs and the values are lists of chat history
            for each endpoint.
        """
        if not database_instance:
            raise RuntimeError("[Session] Database instance not provided.")

        session_metadata = Session.load(database_instance)
        chats = {}
        if session_metadata is not None and "endpoints" in session_metadata:
            endpoint_list = session_metadata.get("endpoints", [])
            for endpoint_id in endpoint_list:
                list_of_chats_from_one_ep = Chat.load_chat_history(
                    database_instance, endpoint_id.replace("-", "_")
                )
                chats.update({endpoint_id: list_of_chats_from_one_ep})
        return chats

    def check_file_exists(
        self, env_var_name: str, file_name: str, file_type: str, extension: str
    ) -> None:
        """
        Checks if a specified file exists in the storage.

        Args:
            env_var_name (str): The environment variable name where the file is stored.
            file_name (str): The name of the file to check.
            file_type (str): The type of the file.
            extension (str): The extension of the file.

        Raises:
            RuntimeError: If the file does not exist in the storage.
        """
        if file_name and not Storage.is_object_exists(
            env_var_name, file_name, extension
        ):
            raise RuntimeError(f"[Session] {file_type} {file_name} does not exist.")
