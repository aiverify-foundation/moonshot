from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Optional

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.messages_constants import (
    RUN_CANCEL_WARNING,
    RUN_FORMAT_RESULTS_FORMATTING_ERROR,
    RUN_FORMAT_RESULTS_MODULE_INSTANCE_ERROR,
    RUN_GET_ALL_RUNS_LOAD_DB_INSTANCE_NOT_PROVIDED,
    RUN_INITIALIZE_RUN_DB_INSTANCE_NOT_INITIALISED,
    RUN_INITIALIZE_RUN_ERROR,
    RUN_INITIALIZE_RUN_FAILED_TO_CREATE_RECORD,
    RUN_LOAD_DB_INSTANCE_NOT_PROVIDED,
    RUN_LOAD_FAILED_TO_GET_DB_RECORD,
    RUN_LOAD_MODULE_NAME_NOT_PROVIDED,
    RUN_LOAD_MODULES_LOADING_ERROR,
    RUN_LOAD_UNABLE_TO_GET_INSTANCE,
    RUN_RUN_BENCHMARK_MODULE_INSTANCE_ERROR,
    RUN_RUN_BENCHMARK_PROCESSING_ERROR,
    RUN_RUN_FAILED,
)
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
    sql_table_name: str = "run_table"
    sql_create_run_table: str = """
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
    sql_create_run_record: str = """
        INSERT INTO run_table (
        runner_id,runner_type,runner_args,endpoints,results_file,start_time,end_time,duration,error_messages,raw_results,results,status)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """
    sql_read_run_record: str = """
        SELECT * from run_table WHERE run_id=?
    """
    sql_read_latest_run_record: str = """
        SELECT * FROM run_table WHERE run_id=(SELECT MAX(run_id) FROM run_table)
    """
    sql_read_all_run_records: str = """
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
        """
        Initialize a Run instance.

        Args:
            runner_id (str): The ID of the runner.
            runner_type (RunnerType): The type of the runner.
            runner_args (dict): Arguments for the runner.
            database_instance (Any | None): The database instance.
            endpoints (list[str]): List of endpoints.
            results_file (str): The results file path.
            progress_callback_func (Callable | None, optional): Callback function for progress updates.
        """
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
        Load run arguments from the database.

        Args:
            database_instance (DBInterface | None): The database instance.
            run_id (int | None): The ID of the run to load.

        Returns:
            RunArguments: The loaded run arguments.

        Raises:
            RuntimeError: If the database instance is not provided or if the record cannot be retrieved.
        """
        if not database_instance:
            raise RuntimeError(RUN_LOAD_DB_INSTANCE_NOT_PROVIDED)

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
                RUN_LOAD_FAILED_TO_GET_DB_RECORD.format(
                    run_id=run_id, database_instance=database_instance
                )
            )

    @staticmethod
    def get_all_runs(database_instance: DBInterface) -> list[RunArguments]:
        """
        Get all run arguments from the database.

        Args:
            database_instance (DBInterface): The database instance.

        Returns:
            list[RunArguments]: A list of all run arguments.

        Raises:
            RuntimeError: If the database instance is not provided.
        """
        if not database_instance:
            raise RuntimeError(RUN_GET_ALL_RUNS_LOAD_DB_INSTANCE_NOT_PROVIDED)

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
        Cancel the run by setting the cancel event.
        """
        logger.warning(RUN_CANCEL_WARNING)
        self.cancel_event.set()

    async def run(self) -> ResultArguments | None:
        """
        Execute the run process.

        Returns:
            ResultArguments | None: The result arguments if the run is successful, None otherwise.
        """
        try:
            # Initialize the run, setting up necessary parameters and database records
            self._initialize_run()

            # Get the current running event loop
            loop = asyncio.get_running_loop()

            # Load the runner and result processing modules
            runner_module_instance, result_module_instance = self._load_modules()

            # Execute the benchmarking tasks and get the results
            runner_results = await self._run_benchmark(loop, runner_module_instance)

            # Format the results obtained from the benchmarking tasks
            updated_runner_results = self._format_results(
                result_module_instance, runner_results
            )

            # Finalize the run, updating the status and cleaning up
            self._finalize_run()

            return updated_runner_results

        except Exception as e:
            # Log the error and notify the run progress of the failure
            self.run_progress.notify_error(RUN_RUN_FAILED.format(str(e)))
            return None

    def _initialize_run(self) -> None:
        """
        Initialize the run by setting start and end times, creating a database record,
        and notifying the run progress.

        Raises:
            RuntimeError: If the database instance is not initialized or if the record creation fails.
        """
        try:
            # Set the start and end times for the run
            self.run_arguments.start_time = time.time()
            self.run_arguments.end_time = time.time()

            # Check if the database instance is provided
            if self.run_arguments.database_instance:
                # Create a database record for the run
                inserted_record = Storage.create_database_record(
                    self.run_arguments.database_instance,
                    self.run_arguments.to_create_tuple(),
                    Run.sql_create_run_record,
                )
                if inserted_record:
                    self.run_arguments.run_id = inserted_record[0]
                else:
                    raise RuntimeError(RUN_INITIALIZE_RUN_FAILED_TO_CREATE_RECORD)
            else:
                raise RuntimeError(RUN_INITIALIZE_RUN_DB_INSTANCE_NOT_INITIALISED)

            # Notify that the run is in progress
            self.run_progress.notify_progress(status=RunStatus.RUNNING)

        except Exception as e:
            # Handle any exceptions that occur during initialization
            error_message = RUN_INITIALIZE_RUN_ERROR.format(error=str(e))
            self.run_progress.notify_error(error_message)

    async def _run_benchmark(
        self, loop: asyncio.AbstractEventLoop, runner_module_instance: Any
    ) -> Any:
        """
        Run the benchmark using the runner module instance.

        Args:
            loop (asyncio.AbstractEventLoop): The event loop to run the benchmark.
            runner_module_instance (Any): The instance of the runner module.

        Returns:
            Any: The results of the benchmark.

        Raises:
            RuntimeError: If the runner module instance is not provided or if there is an error during processing.
        """
        try:
            if runner_module_instance:
                # Run the benchmark using the runner module instance
                return await runner_module_instance.generate(  # type: ignore ; ducktyping
                    loop,
                    self.run_arguments.run_id,
                    self.run_arguments.runner_id,
                    self.run_arguments.runner_args,
                    self.run_arguments.database_instance,
                    self.run_arguments.endpoints,
                    self.run_progress,
                    self.cancel_event,
                )
            else:
                raise RuntimeError(RUN_RUN_BENCHMARK_MODULE_INSTANCE_ERROR)

        except Exception as e:
            # Handle any exceptions that occur during benchmark processing
            self.run_progress.notify_error(
                RUN_RUN_BENCHMARK_PROCESSING_ERROR.format(error=str(e))
            )

    def _format_results(
        self, result_module_instance: Any, runner_results: Any
    ) -> ResultArguments | None:
        """
        Format the results using the result module instance.

        Args:
            result_module_instance (Any): The instance of the result module.
            runner_results (Any): The results from the runner module.

        Returns:
            ResultArguments | None: The formatted runner results or None if formatting fails.

        Raises:
            RuntimeError: If the result module instance is not provided or if there is an error during formatting.
        """
        try:
            if result_module_instance:
                # Format the results using the result module instance
                formatted_runner_results = result_module_instance.generate(runner_results)  # type: ignore ; ducktyping
                if formatted_runner_results:
                    self.run_progress.notify_progress(
                        results=formatted_runner_results.results
                    )
                return formatted_runner_results
            else:
                raise RuntimeError(RUN_FORMAT_RESULTS_MODULE_INSTANCE_ERROR)

        except Exception as e:
            # Handle any exceptions that occur during result formatting
            self.run_progress.notify_error(
                RUN_FORMAT_RESULTS_FORMATTING_ERROR.format(error=str(e))
            )
            return None

    def _finalize_run(self) -> None:
        """
        Finalize the run by updating the run progress status based on the run state.
        """
        if self.cancel_event.is_set():
            # Notify that the run was cancelled
            self.run_progress.notify_progress(status=RunStatus.CANCELLED)

        elif self.run_progress.run_arguments.error_messages:
            # Notify that the run completed with errors
            self.run_progress.notify_progress(status=RunStatus.COMPLETED_WITH_ERRORS)

        else:
            # Notify that the run completed successfully
            self.run_progress.notify_progress(status=RunStatus.COMPLETED)

    def _load_modules(self) -> tuple[Optional[Any], Optional[Any]]:
        """
        Load the runner and result processing modules.

        Returns:
            tuple[Optional[Any], Optional[Any]]: A tuple containing the runner module instance
            and the result module instance.

        Raises:
            RuntimeError: If there is an error loading the modules.
        """
        runner_module_instance: Optional[Any] = None
        result_module_instance: Optional[Any] = None

        try:
            # Load the runner processing module
            runner_module_instance = self._load_module(
                "runner_processing_module", EnvVariables.RUNNERS_MODULES.name
            )
            # Load the result processing module
            result_module_instance = self._load_module(
                "result_processing_module", EnvVariables.RESULTS_MODULES.name
            )

        except Exception as e:
            # Handle any exceptions that occur during module loading
            self.run_progress.notify_error(
                RUN_LOAD_MODULES_LOADING_ERROR.format(error=str(e))
            )

        finally:
            return runner_module_instance, result_module_instance

    def _load_module(self, arg_key: str, env_var: str) -> Any:
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
            Any: An instance of the loaded module.

        Raises:
            RuntimeError: If the module name is not provided or the module instance cannot be created.
        """
        module_name = self.run_arguments.runner_args.get(arg_key)
        if not module_name:
            raise RuntimeError(
                RUN_LOAD_MODULE_NAME_NOT_PROVIDED.format(arg_key=arg_key)
            )
        module_instance = get_instance(
            module_name,
            Storage.get_filepath(env_var, module_name, "py"),
        )
        if not module_instance:
            raise RuntimeError(
                RUN_LOAD_UNABLE_TO_GET_INSTANCE.format(module_name=module_name)
            )
        return module_instance()
