import datetime
import glob
import json
import os
from pathlib import Path
from typing import Iterator, Union

from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)
from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.storage.db.db_accessor import DBAccessor
from moonshot.src.storage.db.db_manager import DatabaseManager
from moonshot.src.storage.generators.ds_info_generator import DatasetInfoGenerator
from moonshot.src.storage.generators.pt_info_generator import (
    PromptTemplateInfoGenerator,
)


class StorageManager:
    # ------------------------------------------------------------------------------
    # Connector Storage APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def create_connector_endpoint(ep_id: str, ep_info: dict) -> None:
        """
        Writes the endpoint information to a JSON file.

        This method takes the endpoint ID and information as arguments, constructs the file path using the endpoint ID
        and the designated directory for connector endpoints, and writes the endpoint information to a JSON file in a
        formatted manner. This ensures that the endpoint information is persistently stored and can be retrieved or
        modified later.

        Args:
            ep_id (str): The ID of the endpoint.
            ep_info (dict): A dictionary containing the endpoint information to be written.
        """
        ep_filepath = f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{ep_id}.json"
        with open(ep_filepath, "w") as json_file:
            json.dump(ep_info, json_file, indent=2)

    @staticmethod
    def read_connector_endpoint(ep_id: str) -> dict:
        """
        Reads the endpoint information from a JSON file.

        This method reads the endpoint information from a JSON file specified by the endpoint ID. It constructs
        the file path using the endpoint ID and the designated directory for connector endpoints. The method
        then reads the JSON file, extracts the creation timestamp, converts it to a human-readable datetime format,
        and adds this information to the endpoint details. The modified endpoint information, including the creation
        date, is returned as a dictionary.

        Args:
            ep_id (str): The ID of the endpoint.

        Returns:
            dict: A dictionary containing the endpoint information, including the creation date.
        """
        ep_filepath = f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{ep_id}.json"
        with open(ep_filepath, "r", encoding="utf-8") as json_file:
            creation_timestamp = os.path.getctime(ep_filepath)
            creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
            ep_info = json.load(json_file)
            ep_info["created_date"] = creation_datetime.replace(
                microsecond=0
            ).isoformat(" ")
        return ep_info

    @staticmethod
    def delete_connector_endpoint(ep_id: str) -> None:
        """
        Deletes the endpoint information from a JSON file.

        This method deletes the endpoint information from a JSON file specified by the endpoint ID. It constructs
        the file path using the endpoint ID and the designated directory for connector endpoints. The method
        then deletes the JSON file. If the file does not exist, it does nothing.

        Args:
            ep_id (str): The ID of the endpoint.
        """
        # Delete connector endpoint
        ep_path = Path(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{ep_id}.json")

        try:
            ep_path.unlink(missing_ok=True)

        except FileNotFoundError:
            pass

    @staticmethod
    def get_connector_endpoints() -> Iterator[str]:
        """
        Retrieves all the endpoint JSON files.

        This method uses the glob module to find all JSON files in the directory specified by the
        `EnvironmentVars.CONNECTORS_ENDPOINTS` environment variable. It returns an iterator that yields the
        filepaths of these JSON files.

        Returns:
            Iterator[str]: An iterator that yields the filepaths of the endpoint JSON files.
        """
        return glob.iglob(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/*.json")

    @staticmethod
    def get_connector_filepath(conn_id: str) -> str:
        """
        Constructs the file path for a connector.

        This method takes a connector ID as input and constructs the file path for the connector's Python file.
        The file path is constructed using the connector ID and the designated directory for connectors. The method
        then returns the constructed file path.

        Args:
            conn_id (str): The ID of the connector.

        Returns:
            str: The file path of the connector's Python file.
        """
        return f"{EnvironmentVars.CONNECTORS}/{conn_id}.py"

    @staticmethod
    def get_connectors() -> Iterator[str]:
        """
        Retrieves all the connector Python files.

        This method uses the glob module to find all Python files in the directory specified by the
        `EnvironmentVars.CONNECTORS` environment variable. It returns an iterator that yields the
        filepaths of these Python files.

        Returns:
            Iterator[str]: An iterator that yields the filepaths of the connector Python files.
        """
        return glob.iglob(f"{EnvironmentVars.CONNECTORS}/*.py")

    # ------------------------------------------------------------------------------
    # Prompt Templates Storage APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def get_prompt_templates() -> Iterator[str]:
        """
        Retrieves all the prompt template JSON files.

        This method uses the glob module to find all JSON files in the directory specified by the
        `EnvironmentVars.PROMPT_TEMPLATES` environment variable. It returns an iterator that yields the
        filepaths of these JSON files.

        Returns:
            Iterator[str]: An iterator that yields the filepaths of the prompt template JSON files.
        """
        return glob.iglob(f"{EnvironmentVars.PROMPT_TEMPLATES}/*.json")

    # ------------------------------------------------------------------------------
    # Cookbook Storage APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def create_cookbook(cb_id: str, cb_info: dict) -> None:
        """
        Creates a new cookbook.

        This method takes a cookbook ID and a dictionary containing the cookbook information as input. It constructs
        the file path using the cookbook ID and the designated directory for cookbooks. The method
        then writes the cookbook information to a JSON file.

        Args:
            cb_id (str): The ID of the cookbook.
            cb_info (dict): A dictionary containing the cookbook information.
        """
        cb_filepath = f"{EnvironmentVars.COOKBOOKS}/{cb_id}.json"
        with open(cb_filepath, "w") as json_file:
            json.dump(cb_info, json_file, indent=2)

    @staticmethod
    def read_cookbook(cb_id: str) -> dict:
        """
        Reads a cookbook from a JSON file.

        This method takes a cookbook ID as input, reads the corresponding JSON file from the directory specified by
        `EnvironmentVars.COOKBOOKS`, and returns a dictionary containing the cookbook's information.

        Args:
            cb_id (str): The ID of the cookbook.

        Returns:
            dict: A dictionary containing the cookbook's information.
        """
        cb_filepath = f"{EnvironmentVars.COOKBOOKS}/{cb_id}.json"
        with open(cb_filepath, "r", encoding="utf-8") as json_file:
            cb_info = json.load(json_file)
        return cb_info

    @staticmethod
    def delete_cookbook(cb_id: str) -> None:
        """
        Deletes a cookbook.

        This method takes a cookbook ID as input, constructs the file path using the cookbook ID and the designated
        directory for cookbooks, and deletes the corresponding JSON file. If the file does not exist, it does nothing.

        Args:
            cb_id (str): The ID of the cookbook.
        """
        # Delete cookbook
        cb_path = Path(f"{EnvironmentVars.COOKBOOKS}/{cb_id}.json")

        try:
            cb_path.unlink(missing_ok=True)

        except FileNotFoundError:
            pass

    @staticmethod
    def get_cookbooks() -> Iterator[str]:
        """
        Returns an iterator over the cookbook files in the directory specified by `EnvironmentVars.COOKBOOKS`.

        This method uses the `glob.iglob` function to create an iterator over the cookbook files in the directory
        specified by `EnvironmentVars.COOKBOOKS`. The `iglob` function returns an iterator which yields the
        paths matching a pathname pattern. The pattern used in this case is `*.json`, which matches all JSON files
        in the directory.

        Returns:
            Iterator[str]: An iterator over the cookbook files in the directory.
        """
        return glob.iglob(f"{EnvironmentVars.COOKBOOKS}/*.json")

    # ------------------------------------------------------------------------------
    # Recipe Storage APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def create_recipe(rec_id: str, rec_info: dict) -> None:
        """
        Writes the recipe information to a JSON file.

        This method takes a recipe ID and a dictionary containing the recipe information. It constructs
        the file path using the recipe ID and the designated directory for recipes. The method
        then writes the recipe information to the JSON file.

        Args:
            rec_id (str): The ID of the recipe.
            rec_info (dict): A dictionary containing the recipe information.
        """
        rec_filepath = f"{EnvironmentVars.RECIPES}/{rec_id}.json"
        with open(rec_filepath, "w") as json_file:
            json.dump(rec_info, json_file, indent=2)

    @staticmethod
    def read_recipe(rec_id: str) -> dict:
        """
        Reads the recipe information from a JSON file.

        This method reads the recipe information from a JSON file specified by the recipe ID. It constructs
        the file path using the recipe ID and the designated directory for recipes. The method
        then reads the JSON file and returns the recipe information as a dictionary.

        Args:
            rec_id (str): The ID of the recipe.

        Returns:
            dict: A dictionary containing the recipe information.
        """
        rec_filepath = f"{EnvironmentVars.RECIPES}/{rec_id}.json"
        with open(rec_filepath, "r", encoding="utf-8") as json_file:
            rec_info = json.load(json_file)
        return rec_info

    @staticmethod
    def delete_recipe(rec_id: str) -> None:
        """
        Deletes the recipe information from a JSON file.

        This method deletes the recipe information from a JSON file specified by the recipe ID. It constructs
        the file path using the recipe ID and the designated directory for recipes. The method
        then deletes the JSON file.

        Args:
            rec_id (str): The ID of the recipe.
        """
        # Delete recipe
        rec_path = Path(f"{EnvironmentVars.RECIPES}/{rec_id}.json")

        try:
            rec_path.unlink(missing_ok=True)

        except FileNotFoundError:
            pass

    @staticmethod
    def get_recipes() -> Iterator[str]:
        """
        Retrieves all the recipe JSON files.

        This method uses the glob module to find all JSON files in the directory specified by the
        `EnvironmentVars.RECIPES` environment variable. It returns an iterator that yields the
        filepaths of these JSON files.

        Returns:
            Iterator[str]: An iterator that yields the filepaths of the recipe JSON files.
        """
        return glob.iglob(f"{EnvironmentVars.RECIPES}/*.json")

    # ------------------------------------------------------------------------------
    # Executor Storage APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def get_executor_database_filepath(be_id: str) -> str:
        """
        Constructs the file path for the executor's database.

        This method constructs the file path for the executor's database using the executor ID and the designated
        directory for databases. The method then returns the constructed file path.

        Args:
            be_id (str): The ID of the executor.

        Returns:
            str: The file path of the executor's database.
        """
        return f"{EnvironmentVars.DATABASES}/{be_id}.db"

    @staticmethod
    def get_executor_results_filepath(be_id: str) -> str:
        """
        Constructs the file path for the executor's results.

        This method constructs the file path for the executor's results using the executor ID and the designated
        directory for results. The method then returns the constructed file path.

        Args:
            be_id (str): The ID of the executor.

        Returns:
            str: The file path of the executor's results.
        """
        return f"{EnvironmentVars.RESULTS}/{be_id}.json"

    @staticmethod
    def create_executor_database_connection(be_id: str) -> DBAccessor:
        """
        Creates a connection to the executor's database.

        This method constructs the file path for the executor's database using the executor ID and the designated
        directory for databases. It then creates a connection to the database using the DatabaseManager's
        create_benchmark_connection method and returns the DBAccessor instance.

        Args:
            be_id (str): The ID of the executor.

        Returns:
            DBAccessor: The DBAccessor instance if the connection is successfully established.

        Raises:
            RuntimeError: If the DBAccessor instance is not initialised.
        """
        db_file = Path(StorageManager.get_executor_database_filepath(be_id))
        db_instance = DatabaseManager.create_benchmark_connection(str(db_file))
        if not db_instance:
            raise RuntimeError("db instance is not initialised.")
        return db_instance

    @staticmethod
    def close_executor_database_connection(db_instance: DBAccessor) -> None:
        """
        Closes the connection to the executor's database.

        This method attempts to close the connection to the executor's database using the db_instance parameter.
        If the db_instance is not None, it calls the close_benchmark_connection method of the DatabaseManager.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to close the connection.

        Returns:
            None
        """
        DatabaseManager.close_benchmark_connection(db_instance)

    @staticmethod
    def create_executor_storage(
        metadata_record: tuple, db_instance: DBAccessor
    ) -> None:
        """
        Creates the executor's storage.

        This method creates the executor's storage by creating the metadata and cache tables in the executor's database
        using the db_instance parameter and metadata_record.
        If the db_instance is not None, it calls the create_benchmark_metadata_table, create_benchmark_cache_table,
        and create_benchmark_metadata_record methods of the DatabaseManager.
        If the db_instance is None, it raises a RuntimeError.

        Args:
            metadata_record (tuple): The metadata record to be created.
            db_instance (DBAccessor): The DBAccessor instance to create the tables and record.

        Returns:
            None

        Raises:
            RuntimeError: If the db_instance is None.
        """
        # Create metadata and cache table and update metadata information
        if db_instance:
            DatabaseManager.create_benchmark_metadata_table(db_instance)
            DatabaseManager.create_benchmark_cache_table(db_instance)
            DatabaseManager.create_benchmark_metadata_record(
                db_instance, metadata_record
            )
        else:
            raise RuntimeError("db instance is not initialised.")

    @staticmethod
    def read_executor_storage(be_id: str, db_instance: DBAccessor) -> tuple:
        """
        Reads the executor's storage.

        This method reads the executor's storage by reading the metadata and cache tables in the executor's database
        using the db_instance parameter and be_id.
        If the db_instance is not None, it calls the read_benchmark_metadata_record method of the DatabaseManager.
        If the db_instance is None, it raises a RuntimeError.

        Args:
            be_id (str): The benchmark executor ID to be read.
            db_instance (DBAccessor): The DBAccessor instance to read the tables and record.

        Returns:
            tuple: The metadata record if found, None otherwise.

        Raises:
            RuntimeError: If the db_instance is None.
        """
        # Get database filepath
        db_file = Path(StorageManager.get_executor_database_filepath(be_id))
        if not Path.exists(db_file):
            raise RuntimeError("benchmark executor file does not exist.")

        # Load database file
        if db_instance:
            metadata_record = DatabaseManager.read_benchmark_metadata_record(
                db_instance, (be_id,)
            )
            if not metadata_record:
                raise RuntimeError(
                    "benchmark executor file metadata record does not exist."
                )
            return metadata_record
        else:
            raise RuntimeError("db instance is not initialised.")

    @staticmethod
    def remove_executor_database(be_id: str) -> None:
        """
        Removes the executor's database.

        This method removes the executor's database by deleting the database file in the executor's directory
        using the be_id.
        If the database file does not exist, it does nothing.

        Args:
            be_id (str): The benchmark executor ID of the database to be removed.

        Returns:
            None
        """
        db_path = Path(StorageManager.get_executor_database_filepath(be_id))
        try:
            db_path.unlink(missing_ok=True)

        except FileNotFoundError:
            pass

    @staticmethod
    def remove_executor_results(be_id: str) -> None:
        """
        Removes the executor's results.

        This method removes the executor's results by deleting the results file in the executor's directory
        using the be_id.
        If the results file does not exist, it does nothing.

        Args:
            be_id (str): The benchmark executor ID of the results to be removed.

        Returns:
            None
        """
        res_path = Path(StorageManager.get_executor_results_filepath(be_id))
        try:
            res_path.unlink(missing_ok=True)

        except FileNotFoundError:
            pass

    @staticmethod
    def get_executors() -> Iterator[str]:
        """
        Returns a list of executor IDs.

        This method retrieves all the executor database files in the directory specified by `EnvironmentVars.DATABASES`.
        It then extracts the executor IDs from the file names and returns them as a list. Executors with "__" in their
        names are excluded. Only executors whose type matches one of the `BenchmarkExecutorTypes` are included.

        Returns:
            Iterator[str]: An iterator over the executor IDs.
        """
        return (
            Path(fp).stem
            for fp in glob.iglob(f"{EnvironmentVars.DATABASES}/*.db")
            if "__" not in fp
            and any(
                Path(fp).stem.startswith(executor_type.name.lower())
                for executor_type in BenchmarkExecutorTypes
            )
        )

    @staticmethod
    def update_executor_progress(progress_info: tuple, db_instance: DBAccessor) -> None:
        """
        Updates the executor's progress in the benchmark database.

        This method attempts to update the executor's progress in the benchmark database using the db_instance parameter
        and progress_info.
        If the db_instance is not None, it calls the update_benchmark_metadata_record method of the DatabaseManager.
        If the db_instance is None, it prints an error message.

        Args:
            progress_info (tuple): The data to be updated in the executor's progress record.
            db_instance (DBAccessor): The DBAccessor instance to update the record.

        Returns:
            None
        """
        if db_instance:
            DatabaseManager.update_benchmark_metadata_record(db_instance, progress_info)
        else:
            print("Unable to update executor progress: db_instance is not initialised.")

    @staticmethod
    def create_benchmark_cache_record(
        prompt_info: tuple, db_instance: DBAccessor
    ) -> None:
        """
        Creates a benchmark cache record.

        This method attempts to create a benchmark cache record in the database using the db_instance parameter
        and prompt_info.
        If the db_instance is not None, it calls the create_benchmark_cache_record method of the DatabaseManager.
        If the db_instance is None, it prints an error message.

        Args:
            prompt_info (tuple): The data to be stored in the cache record.
            db_instance (DBAccessor): The DBAccessor instance to create the record.

        Returns:
            None
        """
        if db_instance:
            DatabaseManager.create_benchmark_cache_record(db_instance, prompt_info)
        else:
            print(
                "Unable to create benchmark cache record: db_instance is not initialised."
            )

    @staticmethod
    def read_benchmark_cache_record(
        prompt_info: tuple, db_instance: DBAccessor
    ) -> Union[tuple, None]:
        """
        Reads a benchmark cache record.

        This method attempts to read a benchmark cache record from the database using the db_instance parameter
        and prompt_info.
        If the db_instance is not None, it calls the read_benchmark_cache_record method of the DatabaseManager.
        If the db_instance is None, it prints an error message.

        Args:
            prompt_info (tuple): The data to be read from the cache record.
            db_instance (DBAccessor): The DBAccessor instance to read the record.

        Returns:
            Union[tuple, None]: The cache record if found, None otherwise.
        """
        if db_instance:
            cache_record = DatabaseManager.read_benchmark_cache_record(
                db_instance, prompt_info
            )
            return cache_record if cache_record else None
        else:
            print(
                "Unable to create benchmark cache record: db_instance is not initialised."
            )
            return None

    @staticmethod
    def get_dataset_info(ds_id: str) -> Iterator:
        """
        Retrieves the dataset information from a JSON file.

        This method constructs the file path for the dataset using the dataset ID and the designated directory
        for datasets. It then creates an instance of the DatasetInfoGenerator class with the dataset file path as
        an argument and returns it.

        Args:
            ds_id (str): The ID of the dataset.

        Returns:
            Iterator: An instance of the DatasetInfoGenerator class.
        """
        ds_filepath = f"{EnvironmentVars.DATASETS}/{ds_id}.json"
        return DatasetInfoGenerator(ds_filepath)

    @staticmethod
    def get_prompt_template_info(pt_id: str) -> Iterator:
        """
        Retrieves the prompt template information from a JSON file.

        This method constructs the file path for the prompt template using the prompt template ID and the designated
        directory for prompt templates. It then creates an instance of the PromptTemplateInfoGenerator class with
        the prompt template file path as an argument and returns it.

        Args:
            pt_id (str): The ID of the prompt template.

        Returns:
            Iterator: An instance of the PromptTemplateInfoGenerator class.
        """
        pt_filepath = f"{EnvironmentVars.PROMPT_TEMPLATES}/{pt_id}.json"
        return PromptTemplateInfoGenerator(pt_filepath)
