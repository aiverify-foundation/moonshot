from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Callable

from pydantic import validate_call
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.session import Session
from moonshot.src.runners.runner_arguments import RunnerArguments
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run import Run
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Runner:
    sql_create_runner_cache_table = """
        CREATE TABLE IF NOT EXISTS runner_cache_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        connection_id text NOT NULL,
        recipe_id text,
        dataset_id text,
        prompt_template_id text,
        context_strategy_id text,
        attack_module_id text,
        prompt_index INTEGER,
        prompt text NOT NULL,
        target text NOT NULL,
        predicted_results text NOT NULL,
        duration text NOT NULL,
        random_seed INTEGER,
        system_prompt text
        );
    """

    def __init__(self, runner_args: RunnerArguments) -> None:
        self.id = runner_args.id
        self.name = runner_args.name
        self.description = runner_args.description
        self.endpoints = runner_args.endpoints
        self.database_instance = runner_args.database_instance
        self.database_file = runner_args.database_file
        self.progress_callback_func = runner_args.progress_callback_func

        # Set current run
        self.current_operation = None
        self.current_operation_lock = asyncio.Lock()  # Mutex lock for current operation

    @classmethod
    def load(
        cls, runner_id: str, progress_callback_func: Callable | None = None
    ) -> Runner:
        """
        This method is responsible for loading an existing runner.

        It accepts a runner_id and an optional progress_callback_func as arguments. The method first verifies the
        existence of the runner file corresponding to the provided runner_id. If the runner file does not exist,
        it raises a RuntimeError.
        If the runner file is found, the method reads the file and establishes a database connection. It then assigns
        the progress_callback_func (if provided) to the runner and returns a new Runner instance.

        Args:
            runner_id (str): The unique identifier of the runner to be loaded.
            progress_callback_func (Callable | None): An optional callback function for tracking the progress of
            the runner.

        Returns:
            Runner: An instance of the Runner class, initialized with the data loaded from the runner file.

        Raises:
            RuntimeError: If the runner file corresponding to the provided runner_id does not exist.
        """
        try:
            # Check if runner file exists. If it does not exists, raise an error.
            if not Storage.is_object_exists(
                EnvVariables.RUNNERS.name, runner_id, "json"
            ):
                raise RuntimeError(
                    "[Runner] Unable to load runner because the runner file does not exist."
                )
            runner_args = Runner.read(runner_id)
            runner_args.database_instance = Storage.create_database_connection(
                EnvVariables.DATABASES.name, Path(runner_args.database_file).stem, "db"
            )
            runner_args.progress_callback_func = progress_callback_func
            return cls(runner_args)

        except Exception as e:
            logger.error(f"[Runner] Failed to load runner: {str(e)}")
            raise e

    @classmethod
    def create(cls, runner_args: RunnerArguments) -> Runner:
        """
        Creates a new runner instance.

        This method takes a RunnerArguments object to generate a unique runner_id from the runner's name.
        It checks for the existence of a runner file with the same id.
        If found, a RuntimeError is raised to indicate the conflict.
        Otherwise, it proceeds to create a new runner file and sets up a database connection for the runner.
        A new Runner class instance, initialized with the provided arguments, is then returned.

        Args:
            runner_args (RunnerArguments): The configuration parameters for creating the runner.

        Returns:
            Runner: An instance of the Runner class, newly created with the specified arguments.

        Raises:
            RuntimeError: Raised if a runner file with the generated runner_id already exists,
            indicating a duplicate runner.
        """
        try:
            runner_id = slugify(runner_args.name, lowercase=True)
            runner_info = {
                "name": runner_args.name,
                "database_file": Storage.get_filepath(
                    EnvVariables.DATABASES.name, runner_id, "db", True
                ),
                "endpoints": runner_args.endpoints,
                "description": runner_args.description,
            }

            # Check if runner file exists. If it exists, raise an error.
            if Storage.is_object_exists(EnvVariables.RUNNERS.name, runner_id, "json"):
                raise RuntimeError(
                    "[Runner] Unable to create runner because the runner file exists."
                )
            # Check if all endpoint configuration files exist. If not, raise an error.
            for endpoint in runner_args.endpoints:
                if not Storage.is_object_exists(
                    EnvVariables.CONNECTORS_ENDPOINTS.name, endpoint, "json"
                ):
                    raise RuntimeError(
                        f"[Runner] Connector endpoint {endpoint} does not exist."
                    )

            # Create runner file
            Storage.create_object(
                EnvVariables.RUNNERS.name, runner_id, runner_info, "json"
            )

            # Add additional attributes (id, database instance and update progress_callback_func)
            runner_info["id"] = runner_id
            runner_info["database_instance"] = Storage.create_database_connection(
                EnvVariables.DATABASES.name, runner_id, "db"
            )
            runner_info["progress_callback_func"] = runner_args.progress_callback_func

            # Create runner cache table
            Storage.create_database_table(
                runner_info["database_instance"], Runner.sql_create_runner_cache_table
            )

            return cls(RunnerArguments(**runner_info))

        except Exception as e:
            logger.error(f"[Runner] Failed to create runner: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def read(runner_id: str) -> RunnerArguments:
        """
        Retrieves the runner data and constructs a RunnerArguments object.

        This method accepts a runner_id as an input and utilizes the StorageManager to fetch the runner data.
        It subsequently builds a RunnerArguments object using the fetched data and returns this object.

        Args:
            runner_id (str): The unique identifier of the runner.

        Returns:
            RunnerArguments: An object of RunnerArguments constructed with the runner's data.

        Raises:
            Exception: If an error occurs during the data retrieval or any other operation within the method.
        """
        try:
            if not runner_id:
                raise RuntimeError("Runner ID is empty.")

            runner_details = Runner._read_runner(runner_id)
            if not runner_details:
                raise RuntimeError(f"Runner with ID '{runner_id}' does not exist.")

            return RunnerArguments(**runner_details)

        except Exception as e:
            logger.error(f"[Runner] Failed to read runner: {str(e)}")
            raise e

    @staticmethod
    def _read_runner(runner_id: str) -> dict:
        """
        Retrieves the runner's information from a JSON file.

        This internal method is designed to fetch the details of a specific runner by its ID. It searches for the
        corresponding JSON file within the directory specified by `EnvVariables.RUNNERS`. The method returns a
        dictionary containing the runner's information.

        Args:
            runner_id (str): The unique identifier of the runner whose information is being retrieved.

        Returns:
            dict: A dictionary with the runner's information.
        """
        runner_info = {"id": runner_id}
        runner_info.update(
            Storage.read_object(EnvVariables.RUNNERS.name, runner_id, "json")
        )
        return runner_info

    @staticmethod
    @validate_call
    def delete(runner_id: str) -> bool:
        """
        Deletes the runner and its associated database instance.

        This method attempts to delete the runner identified by the provided runner_id from storage.
        It also attempts to delete the associated database instance. If both deletions are successful,
        it returns True. If an exception occurs during the deletion process, an error message is printed
        and the exception is re-raised.

        Args:
            runner_id (str): The unique identifier of the runner to be deleted.

        Returns:
            bool: True if the runner and its associated database instance were successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.RUNNERS.name, runner_id, "json")
            Storage.delete_object(EnvVariables.DATABASES.name, runner_id, "db")
            return True

        except Exception as e:
            logger.error(f"[Runner] Failed to delete runner: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[RunnerArguments]]:
        """
        Retrieves and returns a list of available runners.

        This method scans the directory specified by `EnvironmentVars.RUNNERS` and collects all stored runner files.
        It excludes any files that contain "__" in their names. For each valid runner file, the method reads the file
        content and constructs a RunnerArguments object encapsulating the runner's details. Both the RunnerArguments
        object and the runner ID are then appended to their respective lists.

        Returns:
            tuple[list[str], list[RunnerArguments]]: A tuple where the first element is a list of runner IDs and
            the second element is a list of RunnerArguments objects representing the details of each runner.

        Raises:
            Exception: If an error is encountered during the file reading process or any other operation within
            the method.
        """
        try:
            retn_runners = []
            retn_runners_ids = []
            runners = Storage.get_objects(EnvVariables.RUNNERS.name, "json")
            for runner in runners:
                if "__" in runner:
                    continue

                runner_info = RunnerArguments(**Runner._read_runner(Path(runner).stem))
                retn_runners.append(runner_info)
                retn_runners_ids.append(runner_info.id)

            return retn_runners_ids, retn_runners

        except Exception as e:
            logger.error(f"[Runner] Failed to get available runners: {str(e)}")
            raise e

    async def close(self) -> None:
        """
        Closes the runner instance.

        This method is responsible for closing the runner instance. If a database instance is associated with the
        runner, it also closes the database connection using the StorageManager's close_database_connection
        method.

        Raises:
            Exception: If any error occurs while closing the runner or the database connection.
        """
        if self.database_instance:
            Storage.close_database_connection(self.database_instance)

    async def cancel(self) -> None:
        """
        Cancels the runner instance.

        This method is responsible for cancelling the runner instance. If a run is currently in progress,
        it stops the run and releases any resources associated with it.

        Raises:
            Exception: If any error occurs while cancelling the runner or releasing the resources.
        """
        async with self.current_operation_lock:
            if self.current_operation:
                logger.warning(f"[Runner] {self.id} - Cancelling current operation...")
                self.current_operation.cancel()
                self.current_operation = None  # Reset the current operation

    async def run_recipes(
        self,
        recipes: list[str],
        prompt_selection_percentage: int = 100,
        random_seed: int = 0,
        system_prompt: str = "",
        runner_processing_module: str = "benchmarking",
        result_processing_module: str = "benchmarking-result",
    ) -> None:
        """
        Initiates an asynchronous benchmark run using a set of recipes.

        This method sets up and starts a benchmark run tailored for recipes. It instantiates a benchmark run object,
        applies the configuration based on the provided recipes, percentage of prompts, random seed, system prompt, and
        the specified runner and result processing modules, and then commences the run asynchronously.

        Args:
            recipes (list[str]): The recipes to be included in the benchmark run.
            prompt_selection_percentage (int, optional): The percentage of prompts to utilize during the benchmark.
                Defaults to 100.
            random_seed (int, optional): The seed for random number generation to ensure reproducibility.
                Defaults to 0.
            system_prompt (str, optional): The system prompt to be used during the benchmark.
                Defaults to an empty string.
            runner_processing_module (str, optional): The module responsible for processing the runner.
                Defaults to "benchmarking".
            result_processing_module (str, optional): The module responsible for processing the results.
                Defaults to "benchmarking-result".

        Raises:
            Exception: If any error occurs during the setup or execution of the benchmark run.
        """
        async with self.current_operation_lock:  # Acquire the lock
            # Create new benchmark recipe test run
            logger.info(f"[Runner] {self.id} - Running benchmark recipe run...")
            self.current_operation = Run(
                self.id,
                RunnerType.BENCHMARK,
                {
                    "recipes": recipes,
                    "prompt_selection_percentage": prompt_selection_percentage,
                    "random_seed": random_seed,
                    "system_prompt": system_prompt,
                    "runner_processing_module": runner_processing_module,
                    "result_processing_module": result_processing_module,
                },
                self.database_instance,
                self.endpoints,
                Storage.get_filepath(EnvVariables.RESULTS.name, self.id, "json", True),
                self.progress_callback_func,
            )
            # Note: The lock is held during setup but should be released before long-running operations

        # Execute the long-running operation outside of the lock
        # Run new benchmark recipe test run
        await self.current_operation.run()

        # After completion, reset current_operation to None within the lock
        async with self.current_operation_lock:
            self.current_operation = None
            logger.info(f"[Runner] {self.id} - Benchmark recipe run completed.")

    async def run_cookbooks(
        self,
        cookbooks: list[str],
        prompt_selection_percentage: int = 100,
        random_seed: int = 0,
        system_prompt: str = "",
        runner_processing_module: str = "benchmarking",
        result_processing_module: str = "benchmarking-result",
    ) -> None:
        """
        Asynchronously runs a set of cookbooks with the provided parameters.

        This method is responsible for initiating a benchmark cookbook run with the specified cookbooks and parameters.
        It creates a new benchmark cookbook run instance, configures it with the provided cookbook names,
        percentage of prompts, random seed, system prompt, runner processing module, and result processing module,
        and then starts the run asynchronously.

        Args:
            cookbooks (list[str]): A list of cookbook names to be run in the benchmark.
            prompt_selection_percentage (int, optional): The percentage of prompts to be used in the benchmark run.
                Defaults to 100.
            random_seed (int, optional): The seed for random number generation to ensure reproducibility.
                Defaults to 0.
            system_prompt (str, optional): A system prompt to be used in the benchmark run.
                Defaults to an empty string.
            runner_processing_module (str, optional): The module responsible for processing the runner.
                Defaults to "benchmarking".
            result_processing_module (str, optional): The module responsible for processing the results.
                Defaults to "benchmarking-result".

        Raises:
            Exception: If any error occurs during the setup or execution of the benchmark run.
        """
        async with self.current_operation_lock:  # Acquire the lock
            # Create new benchmark cookbook test run
            logger.info(f"[Runner] {self.id} - Running benchmark cookbook run...")
            self.current_operation = Run(
                self.id,
                RunnerType.BENCHMARK,
                {
                    "cookbooks": cookbooks,
                    "prompt_selection_percentage": prompt_selection_percentage,
                    "random_seed": random_seed,
                    "system_prompt": system_prompt,
                    "runner_processing_module": runner_processing_module,
                    "result_processing_module": result_processing_module,
                },
                self.database_instance,
                self.endpoints,
                Storage.get_filepath(EnvVariables.RESULTS.name, self.id, "json", True),
                self.progress_callback_func,
            )
            # Note: The lock is held during setup but should be released before long-running operations

        # Execute the long-running operation outside of the lock
        # Run new benchmark cookbook test run
        await self.current_operation.run()

        # After completion, reset current_operation to None within the lock
        async with self.current_operation_lock:
            self.current_operation = None
            logger.info(f"[Runner] {self.id} - Benchmark cookbook run completed.")

    async def run_red_teaming(
        self,
        red_team_args: dict,
        system_prompt: str = "",
        runner_processing_module: str = "redteaming",
    ) -> list | None:
        """
        Asynchronously runs a red teaming session with the provided arguments.

        This method is responsible for initiating a red teaming session with the specified arguments. It creates a new
        red teaming session instance, configures it with the provided red teaming arguments, system prompt, and
        runner processing module, and then starts the session asynchronously.

        Args:
            red_team_args (dict): A dictionary of arguments for the red teaming session.

            system_prompt (str, optional): A system prompt to be used in the red teaming session.
            Defaults to an empty string.

            runner_processing_module (str, optional): The processing module to be used for the session.
            Defaults to "redteaming".

        Raises:
            Exception: If any error occurs during the setup or execution of the red teaming session.
        """
        async with self.current_operation_lock:  # Acquire the lock
            logger.info(f"[Runner] {self.id} - Running red teaming session...")
            self.current_operation = Session(
                self.id,
                RunnerType.REDTEAM,
                {
                    **red_team_args,
                    "runner_processing_module": runner_processing_module,
                },
                self.database_instance,
                self.endpoints,
                Storage.get_filepath(EnvVariables.RESULTS.name, self.id, "json", True),
                self.progress_callback_func,
            )

        # Note: The lock is held during setup but should be released before long-running operations
        # Execute the long-running operation outside of the lock
        red_teaming_results = await self.current_operation.run()

        # After completion, reset current_operation to None within the lock
        async with self.current_operation_lock:
            self.current_operation = None
            logger.info(f"[Runner] {self.id} - Red teaming run completed.")

        return red_teaming_results
