from __future__ import annotations

import asyncio
import time
from ast import literal_eval
from datetime import datetime
from typing import Any, Callable

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.chat import Chat
from moonshot.src.redteaming.session.red_teaming_type import RedTeamingType
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class SessionMetadata:
    def __init__(
        self,
        session_id: str,
        endpoints: list[str],
        created_epoch: float,
        created_datetime: str,
        prompt_template: str,
        context_strategy: str,
    ):
        self.session_id = session_id
        self.endpoints = endpoints
        self.created_epoch = created_epoch
        self.created_datetime = created_datetime
        self.prompt_template = prompt_template
        self.context_strategy = context_strategy

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
        ) = data_tuple
        return cls(
            runner_id,
            literal_eval(endpoints),
            created_epoch,
            created_datetime,
            prompt_template,
            context_strategy,
        )


class Session:
    sql_create_session_metadata_table = """
            CREATE TABLE IF NOT EXISTS session_metadata_table (
            session_id text PRIMARY KEY NOT NULL,
            endpoints text NOT NULL,
            created_epoch INTEGER NOT NULL,
            created_datetime text NOT NULL,
            prompt_template text,
            context_strategy text
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
        session_id,endpoints,created_epoch,created_datetime,prompt_template,context_strategy)
        VALUES(?,?,?,?,?,?)
    """

    sql_read_session_metadata = """
        SELECT * from session_metadata_table
    """

    sql_update_context_strategy = """
        UPDATE session_metadata_table SET context_strategy=? WHERE session_id=?
    """

    sql_update_prompt_template = """
        UPDATE session_metadata_table SET prompt_template=? WHERE session_id=?
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

        self.runner_args = runner_args
        self.runner_type = runner_type
        self.results_file_path = results_file_path
        self.progress_callback_func = progress_callback_func
        self.database_instance = database_instance

        prompt_template = self.runner_args.get("prompt_template", "")
        context_strategy = self.runner_args.get("context_strategy", "")

        if self.database_instance:
            # Create session metadata table and update metadata
            Storage.create_database_table(
                self.database_instance, Session.sql_create_session_metadata_table
            )
            # Check if the session metadata record already exists
            session_metadata_records = Storage.read_database_records(
                self.database_instance, Session.sql_read_session_metadata
            )
            if session_metadata_records:
                self.session_metadata = SessionMetadata.from_tuple(
                    session_metadata_records[0]
                )

            # If the session metadata does not exist, create a new record
            else:
                self.session_metadata = SessionMetadata(
                    runner_id,
                    endpoints,
                    created_epoch,
                    created_datetime,
                    prompt_template,
                    context_strategy,
                )
                Storage.create_database_record(
                    self.database_instance,
                    self.session_metadata.to_tuple(),
                    Session.sql_create_session_metadata_record,
                )

            # Create chat history table for each endpoint
            for endpoint in endpoints:
                endpoint_id = endpoint.replace("-", "_")
                Storage.create_database_table(
                    self.database_instance,
                    Session.sql_create_chat_history_table.format(endpoint_id),
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
            raise RuntimeError("[Session] Database instance not provided.")

        if not Storage.check_database_table_exists(
            database_instance, "session_metadata_table"
        ):
            # runner file does not have session created
            return None

        session_metadata_info = Storage.read_database_records(
            database_instance,
            Session.sql_read_session_metadata,
        )

        if not session_metadata_info:
            raise RuntimeError("[Session] Failed to get Session metadata.")

        session_metadata = SessionMetadata.from_tuple(session_metadata_info[0])
        session_metadata_obj = SessionMetadata.from_tuple(session_metadata_info[0])
        session_metadata_dict = session_metadata_obj.to_dict()

        chats = {}
        for endpoint_id in session_metadata.endpoints:
            list_of_chats_from_one_ep = Chat.load_chat_history(
                database_instance, endpoint_id.replace("-", "_")
            )
            chats.update({endpoint_id: list_of_chats_from_one_ep})

        session_metadata_dict["chats"] = chats
        return session_metadata_dict

    async def run(self) -> dict:
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
        print("[Session] Part 1: Loading asyncio running loop...")
        loop = asyncio.get_running_loop()

        # ------------------------------------------------------------------------------
        # Part 2: Load runner processing module
        # ------------------------------------------------------------------------------
        print("[Session] Part 2: Loading runner processing module...")
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
            print(
                f"[Session] Failed to load runner processing module in Part 2 due to error: {str(e)}"
            )
            raise e

        finally:
            print(
                f"[Session] Loading runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Run runner processing module
        # ------------------------------------------------------------------------------
        print("[Session] Part 3: Running runner processing module...")
        start_time = time.perf_counter()
        runner_results = {}

        # check if manual/auto red teaming argument is present
        self.check_redteaming_type()

        try:
            if runner_module_instance:
                runner_results = await runner_module_instance.generate(  # type: ignore ; ducktyping
                    loop,
                    self.runner_args,
                    self.database_instance,
                    self.session_metadata,
                )
            else:
                raise RuntimeError("Failed to initialise runner module instance.")

        except Exception as e:
            print(
                f"[Session] Failed to run runner processing module in Part 3 due to error: {str(e)}"
            )
            raise e

        finally:
            print(
                f"[Session] Running runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 4: Wrap up run
        # ------------------------------------------------------------------------------
        print("[Session] Part 4: Wrap up run...")
        return runner_results

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
    ) -> None:
        """
        Updates the context strategy for a specific runner in the database.

        Args:
            db_instance (DBInterface | None): The database instance to update the context strategy in.
            runner_id (str): The ID of the runner.
            context_strategy (str): The name of the context strategy to be used.

        Raises:
            RuntimeError: If the database instance is not provided or if the context strategy does not exist.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        if not Storage.is_object_exists(
            EnvVariables.CONTEXT_STRATEGY.name, context_strategy, "py"
        ):
            raise RuntimeError(
                f"[Session] Context Strategy {context_strategy} does not exist."
            )
        else:
            Storage.update_database_record(
                db_instance,
                (context_strategy, runner_id),
                Session.sql_update_context_strategy,
            )

    @staticmethod
    def update_prompt_template(
        db_instance: DBInterface | None, runner_id: str, prompt_template: str
    ) -> None:
        """
        Updates the prompt template in the database for the specified runner.

        Args:
            db_instance (DBInterface | None): The database instance to update the prompt template in.
            runner_id (str): The ID of the runner.
            prompt_template (str): The new prompt template to be used.

        Raises:
            RuntimeError: If the database instance is not provided or if the prompt template does not exist.
        """
        if not db_instance:
            raise RuntimeError("[Session] Database instance not provided.")
        if not Storage.is_object_exists(
            EnvVariables.PROMPT_TEMPLATES.name, prompt_template, "json"
        ):
            raise RuntimeError(
                f"[Session] Prompt Template {prompt_template} does not exist."
            )
        else:
            Storage.update_database_record(
                db_instance,
                (prompt_template, runner_id),
                Session.sql_update_prompt_template,
            )

    @staticmethod
    def delete_session(database_instance: DBInterface | None) -> None:
        """
        Deletes the session metadata and associated endpoint tables from the database.

        Args:
            database_instance (DBInterface | None): The database instance to delete the session from.

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
