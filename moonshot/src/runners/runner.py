from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Callable

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.session import Session
from moonshot.src.runners.runner_arguments import RunnerArguments
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run import Run
from moonshot.src.storage.storage import Storage


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
                    "[Runner] Unable to create runner because the runner file does not exists."
                )
            runner_args = Runner.read(runner_id)
            runner_args.database_instance = Storage.create_database_connection(
                EnvVariables.DATABASES.name, runner_id, "db"
            )
            runner_args.progress_callback_func = progress_callback_func
            return cls(runner_args)

        except Exception as e:
            print(f"[Runner] Failed to load runner: {str(e)}")
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

            # Check if runner file exists. If it exists, raise an error.
            if Storage.is_object_exists(EnvVariables.RUNNERS.name, runner_id, "json"):
                raise RuntimeError(
                    "[Runner] Unable to create runner because the runner file exists."
                )

            runner_info = {
                "id": runner_id,
                "name": runner_args.name,
                "endpoints": runner_args.endpoints,
                "database_file": Storage.get_filepath(
                    EnvVariables.DATABASES.name, runner_id, "db", True
                ),
                "progress_callback_func": runner_args.progress_callback_func,
            }
            runner_args = RunnerArguments(**runner_info)
            runner_args.database_instance = Storage.create_database_connection(
                EnvVariables.DATABASES.name, runner_id, "db"
            )

            # Create runner file
            Storage.create_object(
                EnvVariables.RUNNERS.name, runner_id, runner_args.to_dict(), "json"
            )

            # Create runner cache table
            Storage.create_database_table(
                runner_args.database_instance, Runner.sql_create_runner_cache_table
            )

            return cls(runner_args)

        except Exception as e:
            print(f"[Runner] Failed to create runner: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
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
            return RunnerArguments(
                **Storage.read_object(EnvVariables.RUNNERS.name, runner_id, "json")
            )

        except Exception as e:
            print(f"[Runner] Failed to read runner: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete(runner_id: str) -> None:
        """
        Removes the runner file and its corresponding database.

        This method requires a runner_id as a parameter and employs the StorageManager to eliminate the runner file
        along with its linked database.

        Args:
            runner_id (str): The unique identifier of the runner.

        Raises:
            Exception: If an issue arises during the file removal process or any other operation within the method.
        """
        try:
            Storage.delete_object(EnvVariables.RUNNERS.name, runner_id, "json")
            Storage.delete_object(EnvVariables.DATABASES.name, runner_id, "db")

        except Exception as e:
            print(f"[Runner] Failed to delete runner: {str(e)}")
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

                runner_info = RunnerArguments(
                    **Storage.read_object(
                        EnvVariables.RUNNERS.name, Path(runner).stem, "json"
                    )
                )
                retn_runners.append(runner_info)
                retn_runners_ids.append(runner_info.id)

            return retn_runners_ids, retn_runners

        except Exception as e:
            print(f"[Runner] Failed to get available runners: {str(e)}")
            raise e

    def close(self) -> None:
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
                print(f"[Runner] {self.id} - Cancelling current run...")
                self.current_operation.cancel_run()
                self.current_operation = None  # Reset the current operation

    async def run_recipes(
        self,
        recipes: list[str],
        num_of_prompts: int = 0,
        random_seed: int = 0,
        system_prompt: str = "",
        runner_processing_module: str = "benchmarking",
    ) -> None:
        """
        Initiates a benchmark run with a given set of recipes asynchronously.

        This method is designed to start a benchmarking process by creating a new benchmark run instance.
        It takes a list of recipes and optional parameters such as the number of prompts, a system prompt,
        and a runner processing module to configure the benchmark run.

        Once configured, the benchmark run is executed asynchronously.

        Args:
            recipes (list[str]): The recipes to be executed during the benchmark run.

            num_of_prompts (int, optional): Specifies the number of prompts to be used.
            Defaults to 0 if not provided.

            random_seed (int, optional): The seed for random number generation to ensure reproducibility.
            Defaults to 0 if not provided.

            system_prompt (str, optional): The system-wide prompt to be used for all recipes in the run.
            Defaults to an empty string if not provided.

            runner_processing_module (str, optional): Identifies the processing module that will handle the run.
            Defaults to "benchmarking" if not provided.

        Raises:
            Exception: An error is raised if there is a failure during the setup or
            the execution phase of the benchmark run.
        """
        async with self.current_operation_lock:  # Acquire the lock
            # Create new benchmark recipe test run
            print(f"[Runner] {self.id} - Running benchmark recipe run...")
            self.current_operation = Run(
                self.id,
                RunnerType.BENCHMARK,
                {
                    "recipes": recipes,
                    "num_of_prompts": num_of_prompts,
                    "random_seed": random_seed,
                    "system_prompt": system_prompt,
                    "runner_processing_module": runner_processing_module,
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
            print(f"[Runner] {self.id} - Benchmark recipe run completed and reset.")

    async def run_cookbooks(
        self,
        cookbooks: list[str],
        num_of_prompts: int = 0,
        random_seed: int = 0,
        system_prompt: str = "",
        runner_processing_module: str = "benchmarking",
    ) -> None:
        """
        Initiates an asynchronous benchmark run using a set of cookbooks.

        This method sets up and starts a benchmark run tailored for cookbooks. It instantiates a benchmark run object,
        applies the configuration based on the provided cookbooks, number of prompts, random seed, system prompt, and
        the specified runner processing module, and then commences the run asynchronously.

        Args:
            cookbooks (list[str]): The cookbooks to be included in the benchmark run.

            num_of_prompts (int, optional): The count of prompts to utilize during the benchmark. Defaults to 0.

            random_seed (int, optional): The seed for random number generation to ensure reproducibility. Defaults to 0.

            system_prompt (str, optional): The system-level prompt for the benchmark run. Defaults to an empty string.

            runner_processing_module (str, optional): The module responsible for processing the run.
            Defaults to "benchmarking".

        Raises:
            Exception: An error is raised if there is a failure during the setup or
            the execution phase of the benchmark run.
        """
        async with self.current_operation_lock:  # Acquire the lock
            # Create new benchmark cookbook test run
            print(f"[Runner] {self.id} - Running benchmark cookbook run...")
            self.current_operation = Run(
                self.id,
                RunnerType.BENCHMARK,
                {
                    "cookbooks": cookbooks,
                    "num_of_prompts": num_of_prompts,
                    "random_seed": random_seed,
                    "system_prompt": system_prompt,
                    "runner_processing_module": runner_processing_module,
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
            print(f"[Runner] {self.id} - Benchmark cookbook run completed and reset.")

    async def run_red_teaming(
        self,
        red_team_args: dict,
        system_prompt: str = "",
        runner_processing_module: str = "redteaming",
    ) -> None:
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
            # automated red teaming
            if (
                "attack_strategies" in red_team_args
                and red_team_args.get("attack_strategies") is not None
            ):
                print(f"[Runner] {self.id} - Running red teaming session...")
                self.current_operation = Session(
                    self.id,
                    RunnerType.REDTEAM,
                    {
                        **red_team_args,
                        "system_prompt": system_prompt,
                        "runner_processing_module": runner_processing_module,
                    },
                    self.database_instance,
                    self.endpoints,
                    Storage.get_filepath(
                        EnvVariables.RESULTS.name, self.id, "json", True
                    ),
                    self.progress_callback_func,
                )
            else:
                # manual red teaming
                return

        # Note: The lock is held during setup but should be released before long-running operations
        # Execute the long-running operation outside of the lock
        await self.current_operation.run()

        # After completion, reset current_operation to None within the lock
        async with self.current_operation_lock:
            self.current_operation = None
            print(
                f"[Runner] {self.id} - Automated red teaming run completed and reset."
            )

    async def run(self, runner_type: RunnerType, runner_args: dict) -> None:
        """
        Asynchronously runs a test based on the runner type and arguments provided.

        This method determines the type of test to run based on the `runner_type` parameter. It supports running
        benchmark tests (either recipe or cookbook based) and redteaming sessions (either manual or automated).
        The method initializes the appropriate test instance with the provided arguments and database instance,
        then executes the test asynchronously. Upon completion, it logs the completion status.

        Args:
            runner_type (RunnerType): The type of runner to execute, which determines the test type.
            runner_args (dict): A dictionary of arguments required for the test run.

        Raises:
            Exception: If an unknown runner type is provided.
        """
        if runner_type is RunnerType.BENCHMARK:
            async with self.current_operation_lock:  # Acquire the lock
                # Create new benchmark test run
                print(f"[Runner] {self.id} - Running benchmark run...")
                self.current_operation = Run(
                    self.id,
                    runner_type,
                    runner_args,
                    self.database_instance,
                    self.endpoints,
                    Storage.get_filepath(
                        EnvVariables.RESULTS.name, self.id, "json", True
                    ),
                    self.progress_callback_func,
                )
                # Note: The lock is held during setup but should be released before long-running operations

            # Execute the long-running operation outside of the lock
            # Run new benchmark test run
            await self.current_operation.run()

            # After completion, reset current_operation to None within the lock
            async with self.current_operation_lock:
                self.current_operation = None
                print(f"[Runner] {self.id} - Benchmark run completed and reset.")

        elif runner_type is RunnerType.REDTEAM:
            async with self.current_operation_lock:  # Acquire the lock
                # Create new redteaming test session
                print(f"[Runner] {self.id} - Running redteaming session...")
                # self.current_operation = Session(runner_type, runner_args)
                # Note: The lock is held during setup but should be released before long-running operations

            # Execute the long-running operation outside of the lock
            # Run new redteaming test run
            # await self.current_operation.run()

            # After completion, reset current_operation to None within the lock
            async with self.current_operation_lock:
                self.current_operation = None
                print(f"[Runner] {self.id} - Redteaming session completed.")

        else:
            # Unknown runner type.
            print(f"[Runner] Failed to determine runner type: {runner_type}")
