from __future__ import annotations

import asyncio
import time
from typing import Any

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_arguments import RunArguments
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class Run:
    sql_create_run_record = """
        INSERT INTO run_table (
        runner_type,runner_args,endpoints,results_file,start_time,end_time,duration,error_messages,results,status)
        VALUES(?,?,?,?,?,?,?,?,?,?)
    """
    sql_update_run_record = """
        UPDATE run_table SET runner_type=?,runner_args=?,endpoints=?,results_file=?,start_time=?,end_time=?,
        duration=?,error_messages=?,results=?,status=?
        WHERE run_id=(SELECT MAX(run_id) FROM run_table)
    """
    # sql_read_run_record = """
    #     SELECT * from run_table WHERE run_id=(SELECT MAX(run_id) FROM run_table)
    # """

    def __init__(
        self,
        runner_type: RunnerType,
        runner_args: dict,
        database_instance: Any | None,
        endpoints: list[str],
        results_file: str,
        progress: RunProgress | None,
    ) -> None:
        # These attributes will be provided by the runner
        self.runner_type = runner_type
        self.runner_args = runner_args
        self.database_instance = database_instance
        self.endpoints = endpoints
        self.results_file = results_file
        self.progress = progress

        # These attributes will be in default values
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.duration: int = 0
        self.error_messages: list[str] = []
        self.results: dict = {}
        self.status: RunStatus = RunStatus.PENDING

    # @staticmethod
    # def load(database_instance: DBAccessor | None) -> RunArguments:
    #     """
    #     Loads the latest run data from the database.

    #     This method retrieves the most recent run data from the database. If the database instance is not provided,
    #     it raises a RuntimeError. If the database instance is provided, it invokes the read_record method of the
    #     database instance and returns a RunArguments object created from the retrieved record.

    #     Returns:
    #         RunArguments: An object containing the details of the latest run.
    #     """
    #     if database_instance:
    #         run_arguments_info = Storage.read_database_record(
    #             database_instance,
    #             (),
    #             Run.sql_read_run_record,
    #         )
    #         if run_arguments_info:
    #             return RunArguments.from_tuple(run_arguments_info)
    #         else:
    #             raise RuntimeError(
    #                 f"[Run] Failed to get database record: {database_instance}"
    #             )
    #     else:
    #         raise RuntimeError(f"[Run] Failed to get database instance: {database_instance}")

    def handle_error_message(self, error_message: str) -> None:
        """
        This method is used to handle error messages during the execution of a run. It takes an error message as input,
        prints it, and adds it to the error_messages list. It then updates the progress status to RUNNING_WITH_ERRORS
        and calls the update_progress method to update the progress status and error messages.

        Args:
            error_message (str): The error message to be handled.

        Returns:
            None
        """
        # Print the error message and add to the error messages list
        print(error_message)
        self.error_messages.append(error_message)

        # Update the progress status
        self.update_progress(RunStatus.RUNNING_WITH_ERRORS)
        if self.progress:
            self.progress.update_progress(
                status=self.status.name, error_messages=self.error_messages
            )

    def update_progress(self, status: RunStatus | None = None) -> None:
        """
        This method is used to update the progress of a run. It takes an optional status as input,
        updates the end time and duration of the run, and if a status is provided, updates the run status as well.
        If a database instance is available, it updates the database record with the current run arguments.
        If no database instance is available, it prints an error message.

        Args:
            status (RunStatus | None): The status to be updated. Default is None.

        Returns:
            None
        """
        self.end_time = time.time()
        self.duration = int(self.end_time - self.start_time)
        if status:
            self.status = status

        if self.database_instance:
            Storage.update_database_record(
                self.database_instance,
                self.get_arguments().to_tuple(),
                Run.sql_update_run_record,
            )
        else:
            print(
                "[Run] Unable to update run progress: db_instance is not initialised."
            )

    def get_arguments(self) -> RunArguments:
        """
        Retrieves the current run's configuration and status information.

        It constructs and returns a RunArguments object encapsulating various details such as the type of runner,
        runner-specific arguments, database connection instance, endpoints involved, location of the results file,
        current progress tracker, and timestamps marking the start and end of the run.

        Additionally, it includes the run's duration, any error messages that have been logged,
        the results collected so far, and the current status of the run.

        Returns:
            RunArguments: An encapsulation of the run's configuration and status information.
        """
        return RunArguments(
            runner_type=self.runner_type,
            runner_args=self.runner_args,
            database_instance=self.database_instance,
            endpoints=self.endpoints,
            results_file=self.results_file,
            progress=self.progress,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            error_messages=self.error_messages,
            results=self.results,
            status=self.status,
        )

    async def run(self) -> dict:
        """
        Asynchronously executes the run process.

        This method orchestrates the entire run process asynchronously. It initializes the run, sets up the necessary
        environment, executes the runner's main logic, handles any errors, and finally, compiles and returns the results
        in a dictionary format. Throughout the process, it updates the run's status and logs progress.

        Returns:
            dict: A dictionary containing the results of the run, including any errors encountered.
        """
        # ------------------------------------------------------------------------------
        # Part 0: Initialise
        # ------------------------------------------------------------------------------
        print("[Run] Part 0: Initialising run...")
        start_time = time.perf_counter()
        try:
            # Initialise the run
            self.start_time = time.time()
            self.end_time = time.time()

            # Create a new run record in database
            if self.database_instance:
                Storage.create_database_record(
                    self.database_instance,
                    RunArguments(
                        runner_type=self.runner_type,
                        runner_args=self.runner_args,
                        database_instance=self.database_instance,
                        endpoints=self.endpoints,
                        results_file=self.results_file,
                        progress=self.progress,
                        start_time=self.start_time,
                        end_time=self.end_time,
                        duration=self.duration,
                        error_messages=self.error_messages,
                        results=self.results,
                        status=self.status,
                    ).to_tuple(),
                    Run.sql_create_run_record,
                )
            else:
                raise RuntimeError(
                    f"Failed to get database instance: {self.database_instance}"
                )

        except Exception as e:
            error_message = (
                f"[Run] Failed to initialise run in Part 0 due to error: {str(e)}"
            )
            self.handle_error_message(error_message)

        finally:
            print(
                f"[Run] Initialise run took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 1: Get asyncio running loop
        # ------------------------------------------------------------------------------
        print("[Run] Part 1: Loading asyncio running loop...")
        loop = asyncio.get_running_loop()

        # ------------------------------------------------------------------------------
        # Part 2: Load runner processing module
        # ------------------------------------------------------------------------------
        print("[Run] Part 2: Loading runner processing module...")
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
            error_message = f"[Run] Failed to load runner processing module in Part 2 due to error: {str(e)}"
            self.handle_error_message(error_message)

        finally:
            print(
                f"[Run] Loading runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Run runner processing module
        # ------------------------------------------------------------------------------
        print("[Run] Part 3: Running runner processing module...")
        start_time = time.perf_counter()
        runner_results = {}
        try:
            if runner_module_instance:
                runner_results = await runner_module_instance.generate(  # type: ignore ; ducktyping
                    loop,
                    self.runner_args,
                    self.database_instance,
                    self.endpoints,
                    self.handle_error_message,
                )
            else:
                raise RuntimeError("Failed to initialise runner module instance.")

        except Exception as e:
            error_message = f"[Run] Failed to run runner processing module in Part 3 due to error: {str(e)}"
            self.handle_error_message(error_message)

        finally:
            print(
                f"[Run] Running runner processing module took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 4: Write results
        # ------------------------------------------------------------------------------
        print("[Run] Part 4: Writing results...")
        start_time = time.perf_counter()
        try:
            pass

        except Exception as e:
            error_message = (
                f"[Run] Failed to write results in Part 4 due to error: {str(e)}"
            )
            self.handle_error_message(error_message)

        finally:
            print(
                f"[Run] Writing results took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 5: Return results
        # ------------------------------------------------------------------------------
        return runner_results
