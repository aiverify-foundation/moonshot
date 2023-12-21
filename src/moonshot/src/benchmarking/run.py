import glob
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Union

from slugify import slugify

from moonshot.src.benchmarking.cookbook import run_cookbooks_with_endpoints
from moonshot.src.benchmarking.recipe import run_recipes_with_endpoints
from moonshot.src.common.db import Database
from moonshot.src.common.db_sql_queries import (
    sql_create_cache_table,
    sql_create_run_metadata_records,
    sql_create_run_metadata_table,
    sql_read_run_metadata_records,
    sql_update_run_metadata_records,
)
from moonshot.src.common.env_variables import EnvironmentVars
from moonshot.src.utils.write_file import write_json_file


class RunTypes(Enum):
    RECIPE = "recipe"
    COOKBOOK = "cookbook"


class RunMetadata:
    def __init__(
        self,
        run_id: str,
        run_type: RunTypes,
        arguments: dict,
        start_time: float,
        end_time: float,
        duration: float,
        db_file: str,
        filepath: str,
        recipes: Union[str, list],
        cookbooks: Union[str, list],
        endpoints: list,
        num_of_prompts: int,
        results: str,
    ):
        self.run_id = run_id
        self.run_type = run_type
        self.arguments = arguments
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.db_file = db_file
        self.db_instance = None
        self.filepath = filepath
        self.recipes = recipes
        self.cookbooks = cookbooks
        self.endpoints = endpoints
        self.num_of_prompts = num_of_prompts
        self.results = results

    @classmethod
    def load_metadata(cls, metadata: tuple) -> Any:
        """
        Loads metadata from a tuple and creates a new instance of the class.

        Args:
            metadata (tuple): A tuple containing the metadata values in the following order:
                - run_id (int): The ID of the run.
                - run_type (str): The type of the run.
                - arguments (str): The arguments of the run.
                - start_time (datetime): The start time of the run.
                - end_time (datetime): The end time of the run.
                - duration (float): The duration of the run.
                - db_file (str): The path to the database file.
                - filepath (str): The path to the metadata file.
                - recipes (list): A list of recipes.
                - cookbooks (list): A list of cookbooks.
                - endpoints (list): A list of endpoints.
                - num_of_prompts (int): The number of prompts.
                - results (list): A list of results.

        Returns:
            cls: A new instance of the class with the loaded metadata.
        """
        (
            run_id,
            run_type,
            arguments,
            start_time,
            end_time,
            duration,
            db_file,
            filepath,
            recipes,
            cookbooks,
            endpoints,
            num_of_prompts,
            results,
        ) = metadata

        # Recover their types
        arguments, recipes, cookbooks, endpoints = map(
            eval, [arguments, recipes, cookbooks, endpoints]
        )
        return cls(
            run_id,
            RunTypes[run_type],
            arguments,
            start_time,
            end_time,
            duration,
            db_file,
            filepath,
            recipes if recipes else None,
            cookbooks if cookbooks else None,
            endpoints,
            num_of_prompts,
            results,
        )

    def create_metadata_in_database(self) -> None:
        # Create metadata records in the database.
        self.db_instance.create_metadata_records(
            sql_create_run_metadata_records, self.get_tuple()
        )

    def update_metadata_in_database(self) -> None:
        # Update metadata records in the database.
        self.db_instance.update_metadata_records(
            sql_update_run_metadata_records,
            (
                self.end_time,
                self.duration,
                str(self.results),
                self.run_id,
            ),
        )

    def get_dict(self) -> dict:
        """
        Returns a dictionary containing the attributes of the current instance of the class.

        Returns:
            dict: A dictionary with the following key-value pairs:
                 - "run_id": The unique ID of the run.
                 - "run_type": The type of the run.
                 - "arguments": The arguments of the run.
                 - "start_time": The start time of the run.
                 - "end_time": The end time of the run.
                 - "duration": The duration of the run.
                 - "db_file": The database file associated with the run.
                 - "filepath": The file path of the run.
                 - "recipes": The recipes used in the run.
                 - "cookbooks": The cookbooks used in the run.
                 - "endpoints": The endpoints accessed in the run.
                 - "num_of_prompts": The number of prompts used in the run.
                 - "results": The results of the run.
        """
        return {
            attr: getattr(self, attr)
            for attr in [
                "run_id",
                "run_type",
                "arguments",
                "start_time",
                "end_time",
                "duration",
                "db_file",
                "filepath",
                "recipes",
                "cookbooks",
                "endpoints",
                "num_of_prompts",
                "results",
            ]
        }

    def get_tuple(self) -> tuple:
        """
        Returns a tuple containing various attributes of the current instance of the class.

        Returns:
            tuple: A tuple containing the following attributes:
                - run_id (int): The ID of the run.
                - run_type (str): The name of the run type.
                - arguments (str): A string representation of the arguments.
                - start_time (datetime): The start time of the run.
                - end_time (datetime): The end time of the run.
                - duration (float): The duration of the run in seconds.
                - db_file (str): The path to the database file.
                - filepath (str): The path to the file.
                - recipes (str): A string representation of the recipes.
                - cookbooks (str): A string representation of the cookbooks.
                - endpoints (str): A string representation of the endpoints.
                - num_of_prompts (int): The number of prompts.
                - results: The results.
        """
        return (
            self.run_id,
            self.run_type.name,
            str(self.arguments),
            self.start_time,
            self.end_time,
            self.duration,
            self.db_file,
            self.filepath,
            str(self.recipes),
            str(self.cookbooks),
            str(self.endpoints),
            self.num_of_prompts,
            self.results,
        )


class Run:
    def __init__(
        self,
        run_type: RunTypes,
        arguments: dict,
        run_id: str = "",
        create_based_on_run_id: bool = False,
    ):
        if run_id:
            db_file = f"{EnvironmentVars.DATABASES}/{run_id}.db"
            if Path(db_file).exists():
                db_instance = Database(db_file)
                db_instance.create_connection()
                self.run_metadata = RunMetadata.load_metadata(
                    db_instance.read_metadata_records(
                        sql_read_run_metadata_records, run_id
                    )
                )
                self.run_metadata.db_instance = db_instance
                return
            elif not create_based_on_run_id:
                raise RuntimeError("Invalid run id")

        start_time = time.time()
        datetime_now = datetime.fromtimestamp(start_time)
        formatted_date = datetime_now.strftime("%Y%m%d-%H%M%S")

        if run_type is RunTypes.RECIPE:
            run_id = run_id or f"recipe-{formatted_date}"
            self.run_metadata = RunMetadata(
                run_id,
                run_type,
                arguments,
                start_time,
                start_time,
                0.0,
                f"{EnvironmentVars.DATABASES}/{run_id}.db",
                f"{EnvironmentVars.RESULTS}/{run_id}.json",
                arguments["recipes"],
                "",
                arguments["endpoints"],
                arguments["num_of_prompts"],
                "",
            )
        elif run_type is RunTypes.COOKBOOK:
            run_id = run_id or f"cookbook-{formatted_date}"
            self.run_metadata = RunMetadata(
                run_id,
                run_type,
                arguments,
                start_time,
                start_time,
                0.0,
                f"{EnvironmentVars.DATABASES}/{run_id}.db",
                f"{EnvironmentVars.RESULTS}/{run_id}.json",
                "",
                arguments["cookbooks"],
                arguments["endpoints"],
                arguments["num_of_prompts"],
                "",
            )
        else:
            raise RuntimeError("Invalid run types")

    @classmethod
    def load_run(cls, run_id: str) -> Any:
        """
        Loads a run using the provided run ID.

        Args:
            run_id (str): The ID of the run to be loaded.

        Returns:
            None: If the run ID is invalid or the file cannot be loaded.
            cls: An instance of the class representing the loaded run.
        """
        # Trigger loading existing file using run_id
        return cls(None, None, run_id)

    def get_run_stats(self) -> str:
        """
        Returns a string with the time taken to complete the run.

        Returns:
            str: A string containing the time taken to run the function.

        Example:
            ========================================
            Time taken to run: 0.123s
            ========================================
        """
        return (
            "=" * 39
            + "\nTime taken to run: {}s\n".format(self.run_metadata.duration)
            + "=" * 39
        )

    def create_run(self) -> dict:
        """
        Creates a run.

        Returns:
            dict: A dictionary representing the newly created run.
        """
        if self.run_metadata.run_type in RunTypes:
            if Path(self.run_metadata.db_file).exists():
                return self.resume_run()
            else:
                return self.create_new_run()
        else:
            raise RuntimeError("Invalid run types")

    def create_new_run(self) -> dict:
        """
        Creates a new run.

        Returns:
            dict: A dictionary representing the new run.
        """
        # Create run database and tables
        self.run_metadata.db_instance = Database(self.run_metadata.db_file)
        self.run_metadata.db_instance.create_connection()
        self.run_metadata.db_instance.create_table(sql_create_run_metadata_table)
        self.run_metadata.db_instance.create_table(sql_create_cache_table)

        # Create database metadata entry
        self.run_metadata.create_metadata_in_database()

        # Run recipes or cookbooks
        if self.run_metadata.run_type is RunTypes.RECIPE:
            self.run_metadata.results = run_recipes_with_endpoints(
                self.run_metadata.recipes,
                self.run_metadata.endpoints,
                self.run_metadata.num_of_prompts,
                self.run_metadata.db_file,
            )
        else:
            self.run_metadata.results = run_cookbooks_with_endpoints(
                self.run_metadata.cookbooks,
                self.run_metadata.endpoints,
                self.run_metadata.num_of_prompts,
                self.run_metadata.db_file,
            )

        # Write json output file
        write_json_file(self.run_metadata.results, self.run_metadata.filepath)

        # Update run stats
        self.run_metadata.end_time = time.time()
        self.run_metadata.duration = (
            self.run_metadata.end_time - self.run_metadata.start_time
        )

        # Update the run metadata
        self.run_metadata.update_metadata_in_database()

        return self.run_metadata.results

    def resume_run(self) -> dict:
        """
        Resumes the execution of a run.

        Returns:
            dict: The results of the resumed run.
        """
        # Update new start time
        self.run_metadata.start_time = time.time()

        # Run recipes or cookbooks
        if self.run_metadata.run_type is RunTypes.RECIPE:
            self.run_metadata.results = run_recipes_with_endpoints(
                self.run_metadata.recipes,
                self.run_metadata.endpoints,
                self.run_metadata.num_of_prompts,
                self.run_metadata.db_file,
            )
        else:
            self.run_metadata.results = run_cookbooks_with_endpoints(
                self.run_metadata.cookbooks,
                self.run_metadata.endpoints,
                self.run_metadata.num_of_prompts,
                self.run_metadata.db_file,
            )

        # Write json output file
        write_json_file(self.run_metadata.results, self.run_metadata.filepath)

        # Update run stats
        self.run_metadata.end_time = time.time()
        self.run_metadata.duration = (
            self.run_metadata.end_time - self.run_metadata.start_time
        )

        # Update the run metadata
        self.run_metadata.update_metadata_in_database()

        return self.run_metadata.results


def get_all_runs() -> list:
    """
    This static method retrieves a list of available runs.

    Returns:
        list: A list of available runs. Each item in the list represents a run.
    """
    filepaths = [
        Path(fp).stem
        for fp in glob.iglob(f"{EnvironmentVars.DATABASES}/*.db")
        if "__" not in fp
        and (Path(fp).stem.startswith("cookbook") or Path(fp).stem.startswith("recipe"))
    ]
    return get_runs(filepaths)


def get_runs(desired_runs: list) -> list:
    """
    This static method retrieves a list of desired runs based on the input.

    Args:
        desired_runs: A list desired run names.

    Returns:
        list: A list of desired runs, where each run is represented as a dictionary or an object.
    """
    return_list = []
    for run_name in desired_runs:
        run_filename = slugify(run_name)
        run_db_file = f"{EnvironmentVars.DATABASES}/{run_filename}.db"

        # read metadata from file
        if Path(run_db_file).exists():
            # Load the db instance
            db_instance = Database(run_db_file)
            db_instance.create_connection()

            # Read metadata information
            run_metadata = RunMetadata.load_metadata(
                db_instance.read_metadata_records(
                    sql_read_run_metadata_records, run_filename
                )
            )
            # Update metadata with the db instance
            run_metadata.db_instance = db_instance

            # Get metadata info
            return_list.append(run_metadata.get_dict())
    return return_list
