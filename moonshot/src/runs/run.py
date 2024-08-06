from __future__ import annotations

import asyncio
import time
from typing import Any, Callable

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_arguments import RunArguments
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Run:
    sql_table_name = "run_table"
    sql_create_run_table = """
        CREATE TABLE IF NOT EXISTS run_table (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        runner_id text NOT NULL,
        runner_type text NOT NULL,
        runner_args text NOT NULL,
        endpoints text NOT NULL,
        results_file text NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        duration INTEGER NOT NULL,
        error_messages text NOT NULL,
        raw_results text NOT NULL,
        results text NOT NULL,
        status text NOT NULL
        );
    """
    sql_create_run_record = """
        INSERT INTO run_table (
        runner_id,runner_type,runner_args,endpoints,results_file,start_time,end_time,duration,error_messages,raw_results,results,status)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """
    sql_read_run_record = """
        SELECT * from run_table WHERE run_id=?
    """
    sql_read_latest_run_record = """
        SELECT * FROM run_table WHERE run_id=(SELECT MAX(run_id) FROM run_table)
    """
    sql_read_all_run_records = """
        SELECT * FROM run_table
    """

    def __init__(
        self,
        runner_id: str,
        runner_type: RunnerType,
        runner_args: dict,
        database_instance: Any | None,
        endpoints: list[str],
        results_file: str,
        progress_callback_func: Callable | None = None,
    ) -> None:
        # Create run arguments
        self.run_arguments = RunArguments(
            runner_id=runner_id,
            runner_type=runner_type,
            runner_args=runner_args,
            database_instance=database_instance,
            endpoints=endpoints,
            results_file=results_file,
            start_time=0.0,
            end_time=0.0,
            duration=0,
            error_messages=[],
            raw_results={},
            results={},
            status=RunStatus.PENDING,
        )
        # Pass the reference of run_arguments to RunProgress
        self.run_progress = RunProgress(
            self.run_arguments,
            progress_callback_func,
        )
        # Create a cancellation asyncio event
        self.cancel_event = asyncio.Event()
        # Create run table
        if database_instance:
            Storage.create_database_table(database_instance, Run.sql_create_run_table)

    @staticmethod
    def load(database_instance: DBInterface | None, run_id: int | None) -> RunArguments:
        """
        Loads run data for a given run_id from the database, or the latest run if run_id is None.

        This method retrieves run data for the specified run_id from the database, or if run_id is None,
        it retrieves the latest run. If the database instance is not provided, it raises a RuntimeError.
        If the database instance is provided, it invokes the read_record method of the database instance
        with the given run_id or the latest run and returns a RunArguments object created from the retrieved record.

        Parameters:
            database_instance (DBAccessor | None): The database accessor instance.
            run_id (int | None): The ID of the run to retrieve, or None to retrieve the latest run.

        Returns:
            RunArguments: An object containing the details of the run with the given run_id or the latest run.
        """
        if not database_instance:
            raise RuntimeError("[Run] Database instance not provided.")

        if run_id is not None:
            run_arguments_info = Storage.read_database_record(
                database_instance,
                (run_id,),
                Run.sql_read_run_record,
            )
        else:
            run_arguments_info = Storage.read_database_record(
                database_instance,
                (),
                Run.sql_read_latest_run_record,
            )

        if run_arguments_info:
            return RunArguments.from_tuple(run_arguments_info)
        else:
            raise RuntimeError(
                f"[Run] Failed to get database record for run_id {run_id}: {database_instance}"
            )

    @staticmethod
    def get_all_runs(database_instance: DBInterface) -> list[RunArguments]:
        """
        Retrieves all run records from the database.

        This method fetches all the run records from the database and converts them into a list of RunArguments objects.
        If the database instance is not provided, it raises a RuntimeError. If no records are found, it also raises
        a RuntimeError.

        Parameters:
            database_instance (DBInterface): The database interface to fetch records from.

        Returns:
            list[RunArguments]: A list of RunArguments objects representing each run record.
        """
        if not database_instance:
            raise RuntimeError("[Run] Database instance not provided.")

        # Check that the table exists
        if not Storage.check_database_table_exists(
            database_instance, Run.sql_table_name
        ):
            return []

        all_run_arguments_info = Storage.read_database_records(
            database_instance,
            Run.sql_read_all_run_records,
        )

        if all_run_arguments_info:
            output = [RunArguments.from_tuple(info) for info in all_run_arguments_info]
            return output
        else:
            return []

    def cancel(self) -> None:
        """
        Sets the cancel event to stop the run process.

        This method is used to signal that the run process should be cancelled. It sets the cancel_event
        which can be checked in various points of the asynchronous run process to gracefully stop the execution.

        Returns:
            None
        """
        logger.warning("[Run] Cancelling run...")
        self.cancel_event.set()

    async def run(self) -> ResultArguments | None:
        """
        Executes the run process asynchronously.

        This method is the main entry point for running the process. It performs the run operation
        asynchronously and returns a ResultArguments object if the run completes successfully, or None
        if the run is cancelled or fails to complete.

        Returns:
            ResultArguments | None: The result of the run operation if successful, otherwise None.

        Raises:
            RuntimeError: If any error occurs during the run process.
        """
        # ------------------------------------------------------------------------------
        # Part 0: Initialise
        # ------------------------------------------------------------------------------
        logger.debug("[Run] Part 0: Initialising run...")
        start_time = time.perf_counter()
        try:
            # Initialise the run
            self.run_arguments.start_time = time.time()
            self.run_arguments.end_time = time.time()

            # Create a new run record in database
            if self.run_arguments.database_instance:
                inserted_record = Storage.create_database_record(
                    self.run_arguments.database_instance,
                    self.run_arguments.to_create_tuple(),
                    Run.sql_create_run_record,
                )
                if inserted_record:
                    self.run_arguments.run_id = inserted_record[0]
                else:
                    raise RuntimeError(
                        "[Run] Failed to create record: record not inserted."
                    )
            else:
                raise RuntimeError(
                    "[Run] Failed to create record: db_instance is not initialised."
                )

            # Set status to running
            self.run_progress.notify_progress(status=RunStatus.RUNNING)

        except Exception as e:
            error_message = (
                f"[Run] Failed to initialise run in Part 0 due to error: {str(e)}"
            )
            self.run_progress.notify_error(error_message)

        finally:
            logger.debug(
                f"[Run] Initialise run took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 1: Get asyncio running loop
        # ------------------------------------------------------------------------------
        logger.debug("[Run] Part 1: Loading asyncio running loop...")
        loop = asyncio.get_running_loop()

        # ------------------------------------------------------------------------------
        # Part 2: Load runner and result processing module
        # ------------------------------------------------------------------------------
        logger.debug("[Run] Part 2: Loading modules...")
        start_time = time.perf_counter()
        runner_module_instance = None
        result_module_instance = None
        try:
            runner_module_instance = self._load_module(
                "runner_processing_module", EnvVariables.RUNNERS_MODULES.name
            )
            result_module_instance = self._load_module(
                "result_processing_module", EnvVariables.RESULTS_MODULES.name
            )
        except Exception as e:
            self.run_progress.notify_error(f"[Run] Module loading error: {e}")
        finally:
            logger.debug(
                f"[Run] Module loading took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Run runner processing module
        # ------------------------------------------------------------------------------
        logger.debug("[Run] Part 3: Running runner processing module...")
        start_time = time.perf_counter()
        runner_results = None
        try:
            if runner_module_instance:
                runner_results = await runner_module_instance.generate(  # type: ignore ; ducktyping
                    loop,
                    self.run_arguments.runner_args,
                    self.run_arguments.database_instance,
                    self.run_arguments.endpoints,
                    self.run_progress,
                    self.cancel_event,
                )
            else:
                raise RuntimeError("Failed to initialise runner module instance.")

        except Exception as e:
            error_message = f"[Run] Failed to run runner processing module in Part 3 due to error: {str(e)}"
            self.run_progress.notify_error(error_message)

        finally:
            logger.debug(
                f"[Run] Running runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 4: Run result processing module
        # ------------------------------------------------------------------------------
        logger.debug("[Run] Part 4: Running result processing module...")
        start_time = time.perf_counter()
        updated_runner_results = None
        try:
            if result_module_instance:
                updated_runner_results = result_module_instance.generate(  # type: ignore ; ducktyping
                    runner_results
                )
                if updated_runner_results:
                    self.run_progress.notify_progress(
                        results=updated_runner_results.results
                    )
            else:
                raise RuntimeError("Failed to initialise result module instance.")

        except Exception as e:
            error_message = f"[Run] Failed to run result processing module in Part 4 due to error: {str(e)}"
            self.run_progress.notify_error(error_message)

        finally:
            logger.debug(
                f"[Run] Running result processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 5: Wrap up run
        # ------------------------------------------------------------------------------
        logger.debug("[Run] Part 5: Wrap up run...")
        return updated_runner_results

    def _load_module(self, arg_key: str, env_var: str):
        """
        Load a module based on the argument key and environment variable.

        This method retrieves the module name from the runner arguments using the provided
        argument key. It then attempts to load the module using the name and the file path
        obtained from the environment variable. If the module name is not provided or the
        module instance cannot be created, a RuntimeError is raised.

        Args:
            arg_key (str): The key to look up the module name in the runner arguments.
            env_var (str): The environment variable used to obtain the file path of the module.

        Returns:
            An instance of the loaded module.

        Raises:
            RuntimeError: If the module name is not provided or the module instance cannot be created.
        """
        module_name = self.run_arguments.runner_args.get(arg_key)
        if not module_name:
            raise RuntimeError(f"[Run] Module name for '{arg_key}' not provided.")
        module_instance = get_instance(
            module_name,
            Storage.get_filepath(env_var, module_name, "py"),
        )
        if not module_instance:
            raise RuntimeError(
                f"[Run] Unable to get instance for module '{module_name}'."
            )
        return module_instance()
