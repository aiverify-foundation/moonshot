from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.runners.runner_arguments import RunnerArguments
from moonshot.src.runs.run import Run
from moonshot.src.runs.run_arguments import RunArguments
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.storage import Storage


class Runner:
    sql_create_run_table = """
        CREATE TABLE IF NOT EXISTS run_table (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_type text NOT NULL,
        recipes text,
        cookbooks text,
        endpoints text NOT NULL,
        num_of_prompts INTEGER NOT NULL,
        results_file text NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        duration INTEGER NOT NULL,
        error_messages text NOT NULL,
        results text NOT NULL,
        status text NOT NULL
        );
    """

    def __init__(self, runner_args: RunnerArguments) -> None:
        self.id = runner_args.id
        self.name = runner_args.name
        self.run_type = runner_args.run_type
        self.recipes = runner_args.recipes
        self.cookbooks = runner_args.cookbooks
        self.endpoints = runner_args.endpoints
        self.num_of_prompts = runner_args.num_of_prompts
        self.database_instance = runner_args.database_instance
        self.database_file = runner_args.database_file
        self.progress_callback_func = runner_args.progress_callback_func

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
                    "Unable to create runner because the runner file does not exists."
                )
            runner_args = Runner.read(runner_id)
            runner_args.database_instance = Storage.create_database_connection(
                EnvVariables.DATABASES.name, runner_id, "db"
            )
            runner_args.progress_callback_func = progress_callback_func
            return cls(runner_args)

        except Exception as e:
            print(f"Failed to load runner: {str(e)}")
            raise e

    @classmethod
    def create(cls, runner_args: RunnerArguments) -> Runner:
        """
        This method is responsible for creating a new runner.

        It accepts a RunnerArguments object as an argument, from which it generates a runner_id based on the
        runner's name.
        The method then checks if a runner file with the same id already exists.
        If such a file is found, it raises a RuntimeError.
        If no such file is found, it creates a new runner file and establishes a new database connection.
        Finally, it returns a new instance of the Runner class.

        Args:
            runner_args (RunnerArguments): The parameters for the runner.

        Returns:
            Runner: A newly created instance of the Runner class.

        Raises:
            RuntimeError: If a runner file with the same id already exists.
        """
        try:
            runner_id = slugify(runner_args.name, lowercase=True)

            # Check if runner file exists. If it exists, raise an error.
            if Storage.is_object_exists(EnvVariables.RUNNERS.name, runner_id, "json"):
                raise RuntimeError(
                    "Unable to create runner because the runner file exists."
                )

            runner_info = {
                "id": runner_id,
                "name": runner_args.name,
                "run_type": runner_args.run_type,
                "recipes": runner_args.recipes,
                "cookbooks": runner_args.cookbooks,
                "endpoints": runner_args.endpoints,
                "num_of_prompts": runner_args.num_of_prompts,
                "database_file": Storage.get_filepath(
                    EnvVariables.DATABASES.name, runner_id, "db"
                ),
                "progress_callback_func": runner_args.progress_callback_func,
            }
            runner_args = RunnerArguments(**runner_info)
            runner_args.database_instance = Storage.create_database_connection(
                EnvVariables.DATABASES.name, runner_id, "db"
            )

            # Create run table
            Storage.create_database_table(
                runner_args.database_instance, Runner.sql_create_run_table
            )

            # Create runner file
            Storage.create_object(
                EnvVariables.RUNNERS.name, runner_id, runner_args.to_dict(), "json"
            )
            return cls(runner_args)

        except Exception as e:
            print(f"Failed to create runner: {str(e)}")
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
            print(f"Failed to read runner: {str(e)}")
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
            print(f"Failed to delete runner: {str(e)}")
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
            print(f"Failed to get available runners: {str(e)}")
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

    def cancel(self) -> None:
        """
        Cancels the runner instance.

        This method is responsible for cancelling the runner instance. If a run is currently in progress,
        it stops the run and releases any resources associated with it.

        Raises:
            Exception: If any error occurs while cancelling the runner or releasing the resources.
        """
        pass

    async def run(self) -> None:
        """
        Executes the runner instance.

        This method is tasked with executing the runner instance. It first prepares the necessary run arguments,
        then initiates a new run. The execution of the run is performed asynchronously.

        Raises:
            Exception: If an error is encountered during the preparation of the run arguments or during the
            execution of the run.
        """
        new_run_args = RunArguments(
            run_type=self.run_type,
            recipes=self.recipes,
            cookbooks=self.cookbooks,
            endpoints=self.endpoints,
            num_of_prompts=self.num_of_prompts,
            database_instance=self.database_instance,
            results_file=Storage.get_filepath(
                EnvVariables.RESULTS.name, self.id, "json"
            ),
            progress=RunProgress(
                exec_id=str(self.id),
                exec_name=self.name,
                exec_type=self.run_type.name,
                bm_progress_callback_func=self.progress_callback_func,
            ),
            start_time=time.time(),
            end_time=time.time(),
            duration=0,
            error_messages=[],
            results={},
            status=RunStatus.PENDING,
        )
        current_run = Run(new_run_args)
        await current_run.run()
