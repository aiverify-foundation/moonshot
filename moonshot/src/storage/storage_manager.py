import datetime
import glob
import json
import os
from pathlib import Path
from typing import Any, Iterator, Union

from moonshot.src.benchmarking.executors.benchmark_executor_arguments import (
    BenchmarkExecutorArguments,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)
from moonshot.src.benchmarking.prompt_arguments import PromptArguments
from moonshot.src.configs.env_variables import EnvironmentVars
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
    def create_executor(
        be_args: BenchmarkExecutorArguments,
    ) -> BenchmarkExecutorArguments:
        """
        Creates a new executor.

        This method creates a new executor by constructing the file paths for the executor's database and results
        using the executor ID from the provided BenchmarkExecutorArguments. It then updates the
        BenchmarkExecutorArguments instance with these a new database connection.
        The method also creates the metadata and cache tables in the database and inserts a metadata record.
        Finally, it returns the updated BenchmarkExecutorArguments instance.

        Args:
            be_args (BenchmarkExecutorArguments): The arguments for the BenchmarkExecutor.

        Returns:
            BenchmarkExecutorArguments: The updated arguments for the BenchmarkExecutor.
        """
        # Validate if database exists
        if Path.exists(Path(be_args.database_file)):
            raise RuntimeError("benchmark executor file exists.")

        # Create a database file and update BenchmarkArguments
        db_conn = DatabaseManager.create_benchmark_connection(be_args.database_file)
        be_args.database_instance = db_conn

        # Create the metadata and the cache table and update the metadata information
        DatabaseManager.create_benchmark_metadata_table(db_conn)
        DatabaseManager.create_benchmark_cache_table(db_conn)
        DatabaseManager.create_benchmark_metadata_record(db_conn, be_args.to_tuple())

        return be_args

    @staticmethod
    def read_executor(be_id: str) -> Union[BenchmarkExecutorArguments, None]:
        """
        Reads an executor.

        This method reads an executor by loading the executor's database file and reading the metadata record.
        It constructs the file path for the database file using the executor ID and the designated directory for
        databases.
        If the file does not exist, it raises a RuntimeError.
        It then returns the BenchmarkExecutorArguments instance constructed from the metadata record, or None
        if the record could not be found.

        Args:
            be_id (str): The ID of the executor.

        Returns:
            Union[BenchmarkExecutorArguments, None]: The BenchmarkExecutorArguments instance, or None if the
            record could not be found.
        """
        db_file = Path(StorageManager.get_executor_database_filepath(be_id))
        if not Path.exists(db_file):
            raise RuntimeError("benchmark executor file does not exist.")

        # Load the database file
        db_conn = DatabaseManager.create_benchmark_connection(str(db_file))
        metadata_record = DatabaseManager.read_benchmark_metadata_record(db_conn, be_id)
        if metadata_record:
            be_args = BenchmarkExecutorArguments.from_tuple(metadata_record)
            be_args.database_instance = db_conn
            return be_args
        else:
            return None

    @staticmethod
    def update_executor(be_args: BenchmarkExecutorArguments) -> None:
        be_id = be_args.id
        db_file = Path(StorageManager.get_executor_database_filepath(be_id))
        if not Path.exists(db_file):
            raise RuntimeError("benchmark executor file does not exist.")

        # Load the database file
        db_conn = DatabaseManager.create_benchmark_connection(str(db_file))
        DatabaseManager.update_benchmark_metadata_record(db_conn, be_args.to_tuple())

    @staticmethod
    def delete_executor(be_id: str) -> None:
        """
        Deletes an executor.

        This method deletes an executor by removing both the executor's database file and results file.
        It constructs the file paths for these files using the executor ID and the designated directories for databases
        and results. If the files do not exist, it does nothing.

        Args:
            be_id (str): The ID of the executor.
        """
        # Delete both executor database file and result file
        db_path = Path(StorageManager.get_executor_database_filepath(be_id))
        res_path = Path(StorageManager.get_executor_results_filepath(be_id))

        try:
            db_path.unlink(missing_ok=True)
            res_path.unlink(missing_ok=True)

        except FileNotFoundError:
            pass

    @staticmethod
    def get_executors() -> list[str]:
        """
        Returns a list of executor IDs.

        This method retrieves all the executor database files in the directory specified by `EnvironmentVars.DATABASES`.
        It then extracts the executor IDs from the file names and returns them as a list. Executors with "__" in their
        names are excluded. Only executors whose type matches one of the `BenchmarkExecutorTypes` are included.

        Returns:
            list[str]: A list of executor IDs.
        """
        return [
            Path(fp).stem
            for fp in glob.iglob(f"{EnvironmentVars.DATABASES}/*.db")
            if "__" not in fp
            and any(
                Path(fp).stem.startswith(executor_type.name.lower())
                for executor_type in BenchmarkExecutorTypes
            )
        ]

    @staticmethod
    def create_benchmark_cache_record(
        db_instance: Any, prompt_info: PromptArguments
    ) -> None:
        """
        Creates a new cache record in the benchmark database.

        This method takes a database instance and a PromptArguments instance. It converts the PromptArguments
        instance into a tuple and inserts it as a new record in the cache table of the benchmark database.

        Args:
            db_instance (Any): The database instance where the cache record will be created.
            prompt_info (PromptArguments): The prompt information to be inserted as a cache record.
        """
        DatabaseManager.create_benchmark_cache_record(
            db_instance, prompt_info.to_tuple()
        )

    @staticmethod
    def read_benchmark_cache_record(
        db_instance: Any, prompt_info: PromptArguments
    ) -> Union[PromptArguments, None]:
        """
        Reads a cache record from the benchmark database.

        This method takes a database instance and a PromptArguments instance. It converts the PromptArguments
        instance into a tuple and uses it to read a record from the cache table of the benchmark database. If a
        cache record is found, it is converted back into a PromptArguments instance and returned. If no cache
        record is found, None is returned.

        Args:
            db_instance (Any): The database instance where the cache record will be read.
            prompt_info (PromptArguments): The prompt information to be used to read a cache record.

        Returns:
            Union[PromptArguments, None]: The cache record read from the database as a PromptArguments instance,
                                          or None if the record could not be found.
        """
        read_tuple = (
            prompt_info.rec_id,
            prompt_info.conn_id,
            prompt_info.pt_id,
            prompt_info.prompt,
        )
        cache_record = DatabaseManager.read_benchmark_cache_record(
            db_instance, read_tuple
        )
        return PromptArguments.from_tuple(cache_record) if cache_record else None

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
