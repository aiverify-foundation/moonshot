import datetime
import glob
import json
import os
from pathlib import Path
from typing import Iterator, Optional, Union

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
        then deletes the JSON file. This ensures that the endpoint information is permanently removed.

        Args:
            ep_id (str): The ID of the endpoint.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        # Delete connector endpoint
        ep_path = Path(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{ep_id}.json")
        ep_path.unlink()

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

        This method takes a cookbook ID as input, deletes the corresponding JSON file from the directory specified by
        `EnvironmentVars.COOKBOOKS`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            cb_id (str): The ID of the cookbook to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        # Delete cookbook
        cb_path = Path(f"{EnvironmentVars.COOKBOOKS}/{cb_id}.json")
        cb_path.unlink()

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
        Deletes a recipe.

        This method takes a recipe ID as input, deletes the corresponding JSON file from the directory specified by
        `EnvironmentVars.RECIPES`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            rec_id (str): The ID of the recipe to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        # Delete recipe
        rec_path = Path(f"{EnvironmentVars.RECIPES}/{rec_id}.json")
        rec_path.unlink()

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
    # Metrics Storage APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def get_metric_filepath(met_id: str) -> str:
        """
        Constructs the file path for the metric.

        This method constructs the file path for the metric using the metric ID and the designated
        directory for metrics. The method then returns the constructed file path.

        Args:
            met_id (str): The ID of the metric.

        Returns:
            str: The file path of the metric.
        """
        return f"{EnvironmentVars.METRICS}/{met_id}.py"

    @staticmethod
    def delete_metric(met_id: str) -> None:
        """
        Deletes a metric.

        This method takes a metric ID as input, deletes the corresponding Python file from the directory specified by
        `EnvironmentVars.METRICS`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            met_id (str): The ID of the metric to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        # Delete metric
        met_path = Path(f"{EnvironmentVars.METRICS}/{met_id}.py")
        met_path.unlink()

    @staticmethod
    def get_metrics() -> Iterator[str]:
        """
        Retrieves a list of available metrics.

        This method scans the directory specified by the `EnvironmentVars.METRICS` environment variable for
        Python files, excluding any that are special or private files (denoted by "__" in their names). It
        extracts and returns the stem (the filename without the extension) of each Python file found, which
        represents the available metric names.

        Returns:
            list[str]: A list of the names of available metrics.
        """
        return glob.iglob(f"{EnvironmentVars.METRICS}/*.py")

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
        If the database file does not exist, it raises a FileNotFoundError.

        Args:
            be_id (str): The benchmark executor ID of the database to be removed.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        db_path = Path(StorageManager.get_executor_database_filepath(be_id))
        db_path.unlink()

    @staticmethod
    def remove_executor_results(be_id: str) -> None:
        """
        Removes the executor's results.

        This method removes the executor's results by deleting the results file in the executor's directory
        using the be_id.
        If the results file does not exist, it raises a FileNotFoundError.

        Args:
            be_id (str): The benchmark executor ID of the results to be removed.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        res_path = Path(StorageManager.get_executor_results_filepath(be_id))
        res_path.unlink()

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

    # ------------------------------------------------------------------------------
    # Results APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def create_result(res_id: str, res_info: dict) -> None:
        """
        Creates new result.

        This method takes a result ID and a dictionary containing result information as input. It writes the result
        information to a JSON file in the results directory. The file is named using the result ID.

        Args:
            res_id (str): The ID of the result.
            res_info (dict): A dictionary containing the result information.

        Returns:
            None
        """
        res_filepath = StorageManager.get_executor_results_filepath(res_id)
        with open(res_filepath, "w") as json_file:
            json.dump(res_info, json_file, indent=2)

    @staticmethod
    def read_result(res_id: str) -> dict:
        """
        Reads result from a JSON file.

        This method constructs the file path for the result using the result ID and the designated
        directory for results. It then opens the result file in read mode and loads the JSON content
        into a dictionary.

        Args:
            res_id (str): The ID of the result.

        Returns:
            dict: A dictionary containing the result information.
        """
        res_filepath = StorageManager.get_executor_results_filepath(res_id)
        with open(res_filepath, "r", encoding="utf-8") as json_file:
            res_info = json.load(json_file)
        return res_info

    @staticmethod
    def delete_result(res_id: str) -> None:
        """
        Deletes a result.

        This method takes a result ID as input, deletes the corresponding JSON file from the directory specified by
        `EnvironmentVars.RESULTS`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            res_id (str): The ID of the result to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        # Delete result
        res_path = Path(StorageManager.get_executor_results_filepath(res_id))
        res_path.unlink()

    @staticmethod
    def get_results() -> Iterator[str]:
        """
        Retrieves all result IDs.

        This method retrieves all the result IDs from the designated directory for results. It uses the glob module
        to find all JSON files in the directory, and then extracts the result IDs from the file names.

        Returns:
            Iterator[str]: An iterator that yields the IDs of all results.
        """
        return glob.iglob(f"{EnvironmentVars.RESULTS}/*.json")

    # ------------------------------------------------------------------------------
    # Redteaming APIs
    # ------------------------------------------------------------------------------
    @staticmethod
    def get_session_database_filepath(se_id: str) -> str:
        """
        Constructs and returns the file path for a session's database based on the session ID.

        This method generates the file path for the database of a specific session by appending the session ID
        to the base directory for session databases, as defined in `EnvironmentVars.SESSIONS`. The resulting
        file path is used to locate or create the database file associated with the given session ID.

        Args:
            se_id (str): The unique identifier for the session.

        Returns:
            str: The file path for the session's database.
        """
        return f"{EnvironmentVars.SESSIONS}/{se_id}.db"

    @staticmethod
    def create_session_database_connection(se_id: str) -> DBAccessor:
        """
        Creates and returns a database connection for a specific session based on its session ID.

        This method first constructs the file path for the session's database using the session ID. It then
        attempts to create a database connection using this file path. If the connection is successfully established,
        the database instance is returned. If the connection cannot be established, a RuntimeError is raised indicating
        that the database instance is not initialized.

        Args:
            se_id (str): The unique identifier for the session.

        Returns:
            DBAccessor: An instance of the database accessor if the connection is successfully established.

        Raises:
            RuntimeError: If the database instance cannot be initialized.
        """
        db_file = Path(StorageManager.get_session_database_filepath(se_id))
        db_instance = DatabaseManager.create_session_connection(str(db_file))
        if not db_instance:
            raise RuntimeError("db instance is not initialised.")
        return db_instance

    # create session and chat metadata tables
    @staticmethod
    def create_session_storage(
        session_metadata: tuple,
        db_instance: DBAccessor,
    ) -> None:
        """
        Initializes the storage for a new session by creating necessary tables and inserting session metadata.

        This method is responsible for setting up the database structure for a new session. It creates the session
        metadata table and the chat metadata table if they do not already exist. Additionally, it inserts the provided
        session metadata into the session metadata table. This setup is crucial for tracking session and chat
        information within the application.

        Args:
            session_metadata (tuple): The metadata for the session to be inserted into the session metadata table.
                                    This should include all necessary information such as session ID, start time, etc.
            db_instance (DBAccessor): The database accessor instance used for executing database operations.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating that the database connection could not
            be established.
        """
        if db_instance:
            DatabaseManager.create_session_metadata_table(db_instance)
            DatabaseManager.create_chat_metadata_table(db_instance)
            DatabaseManager.create_session_metadata_record(
                db_instance, session_metadata
            )
        else:
            raise RuntimeError("db instance is not initialised.")

    # create chat history table
    @staticmethod
    def create_chat_history_storage(
        chat_id: str, session_db_instance: DBAccessor
    ) -> None:
        """
        Initializes the storage for chat history by creating a dedicated table for a specific chat session.

        This method is tasked with setting up a unique table for storing the chat history of a specific chat session,
        identified by the chat_id. It delegates the creation of this table to the DatabaseManager, which executes the
        necessary SQL command to create the table if it does not already exist. This setup is essential for organizing
        and storing chat interactions in a structured and retrievable manner.

        Args:
            chat_id (str): The unique identifier for the chat session, which will be used as the table name.
            db_instance (DBAccessor): The database accessor instance used for executing the table creation operation.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating that the database connection
            could not be established.
        """
        if session_db_instance:
            DatabaseManager.create_chat_history_table(session_db_instance, chat_id)
        else:
            raise RuntimeError("db instance is not initialised.")

    @staticmethod
    def create_chat_metadata_record(
        chat_metadata: tuple, session_db_instance: DBAccessor
    ) -> None:
        """
        Inserts a new chat metadata record into the database.

        This method is responsible for adding a new record to the chat metadata table within the database. It utilizes
        the provided database instance to execute the insertion. The chat metadata, structured as a tuple, contains all
        necessary information that needs to be stored, such as chat IDs, timestamps, and other relevant data.

        Args:
            chat_metadata (tuple): The chat metadata to be inserted into the database. The structure of this tuple
                                must align with the schema of the chat metadata table.
            db_instance (DBAccessor): The database accessor instance used for executing the insertion operation.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating a failure to
            establish a database connection.
        """
        if session_db_instance:
            DatabaseManager.create_chat_metadata_record(
                session_db_instance, chat_metadata
            )

        else:
            raise RuntimeError("db instance is not initialised.")

    # update session metadata with chat ids
    @staticmethod
    def update_session_metadata_with_chat_info(
        chat_info: tuple, db_instance: DBAccessor
    ) -> None:
        """
        Updates session metadata with chat information in the database.

        This method is designed to update an existing session's metadata with new chat information. It leverages the
        provided database instance to execute the update operation. The chat_info tuple contains the necessary data
        for the update, structured according to the expectations of the underlying SQL operation managed by the
        DatabaseManager.

        Args:
            chat_info (tuple): The chat information to be updated in the session metadata. This includes any relevant
                            identifiers, timestamps, or other metadata associated with the chat session.
            db_instance (DBAccessor): The database accessor instance used for executing the update operation.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating that the operation cannot proceed due to
                        a lack of a valid database connection.
        """
        if db_instance:
            DatabaseManager.update_session_metadata_with_chat_info(
                db_instance, chat_info
            )
        else:
            raise RuntimeError("db instance is not initialised.")

    # get session metadata
    @staticmethod
    def get_session_metadata(
        db_instance: DBAccessor,
    ) -> Optional[tuple]:
        """
        Fetches and returns the session metadata from the database.

        This method is tasked with retrieving the metadata of a specific session from the database. It does this by
        utilizing the provided database instance and calling a designated method in the DatabaseManager to carry out
        the operation. If the database instance is valid, the session metadata is returned. This function is vital
        for obtaining session-specific details that may be required for different application features.

        Args:
            db_instance (DBAccessor): The instance of the database accessor used to fetch the session metadata.

        Returns:
            The session metadata if it exists, None otherwise.

        Raises:
            RuntimeError: If the db_instance is not initialized, signifying that the operation cannot continue due
                        to the absence of a valid database connection.
        """
        if db_instance:
            return DatabaseManager.read_session_metadata(db_instance)
        else:
            raise RuntimeError("db instance is not initialised.")

    # get all chat metadata in a session
    @staticmethod
    def get_session_chat_metadata(db_instance: DBAccessor) -> Optional[list[tuple]]:
        """
        Retrieves all chat metadata associated with a session from the database.

        This method fetches the chat metadata for a specific session using the provided database instance. It
        leverages the DatabaseManager to execute a query that reads the chat metadata from the database. This
        functionality is essential for accessing detailed information about each chat session, including identifiers,
        timestamps, and other relevant metadata.

        Args:
            db_instance (DBAccessor): The database accessor instance used for reading the chat metadata.

        Returns:
            Optional[list[tuple]]: A list of chat metadata records if available, None otherwise.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating that the operation cannot proceed due
                        to a lack of a valid database connection.
        """
        if db_instance:
            return DatabaseManager.read_session_chat_metadata(db_instance)
        else:
            raise RuntimeError("db instance is not initialised.")

    # get all chat history for one endpoint
    @staticmethod
    def get_chat_history_for_one_endpoint(
        chat_id: str, db_instance: DBAccessor
    ) -> Optional[list[tuple]]:
        """
        Retrieves the chat history for a specific chat session from the database.

        This method is designed to fetch the entire chat history associated with a given chat ID using the provided
        database instance. It calls upon the DatabaseManager to execute the operation. If successful, it returns the
        chat history records. This functionality is crucial for reviewing past interactions within a specific chat
        session.

        Args:
            chat_id (str): The unique identifier for the chat session.
            db_instance (DBAccessor): The database accessor instance used for executing the read operation.

        Returns:
            Optional[list[tuple]]: A list of chat history records if available, None otherwise.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating that the operation cannot proceed due to
                        a lack of a valid database connection.
        """
        if db_instance:
            return DatabaseManager.read_chat_history_for_one_endpoint(
                db_instance, chat_id
            )
        else:
            raise RuntimeError("db instance is not initialised.")

    # get a chat record for the prompt
    @staticmethod
    def create_chat_record(
        chat_record_tuple: tuple,
        db_instance: DBAccessor,
        chat_id: str,
    ) -> None:
        """
        Inserts a new chat record into the database for a specific chat session.

        This method is responsible for adding a new chat record to the database, associated with a specific chat
        session identified by the chat_id. It utilizes the provided database instance to execute the
        insertion operation. The chat record data, structured as a tuple, should contain all necessary information
        that corresponds to the database schema for the chat session table.

        Args:
            chat_record_tuple (tuple): The chat record data to be inserted, structured as a tuple. This should
            include all necessary fields such as message content, timestamps, sender identifiers, etc.
            db_instance (DBAccessor): The database accessor instance used for executing the insertion operation.
            chat_id (str): The unique identifier for the chat session, which determines the specific table where
            the record will be inserted.

        Raises:
            RuntimeError: If the db_instance is not initialized, indicating that the operation cannot proceed due
            to a lack of a valid database connection.
        """
        if db_instance:
            return DatabaseManager.create_chat_record(
                db_instance, chat_record_tuple, chat_id
            )
        else:
            raise RuntimeError("db instance is not initialised.")

    @staticmethod
    def update_prompt_template(
        db_instance: DBAccessor, prompt_template_tuple: tuple
    ) -> None:
        """
        Updates the prompt template in the database.

        This method updates the prompt template in the database using the provided database instance and the prompt
        template tuple. If the database instance is valid, it calls the update_prompt_template method of the
        DatabaseManager to perform the update.

        Args:
            db_instance (DBAccessor): The database accessor instance.
            prompt_template_tuple (tuple): The tuple containing the updated prompt template information.

        Returns:
            None
        """
        if db_instance:
            DatabaseManager.update_prompt_template(db_instance, prompt_template_tuple)

    @staticmethod
    def update_context_strategy(
        db_instance: DBAccessor, context_strategy_tuple: tuple
    ) -> None:
        """
        Updates the context strategy in the database.

        This method updates the context strategy in the database using the provided database instance and the context
        strategy tuple. If the database instance is valid, it calls the update_context_strategy method of the
        DatabaseManager to perform the update.

        Args:
            db_instance (DBAccessor): The database accessor instance.
            context_strategy_tuple (tuple): The tuple containing the updated context strategy information.

        Returns:
            None
        """
        if db_instance:
            DatabaseManager.update_context_strategy(db_instance, context_strategy_tuple)
