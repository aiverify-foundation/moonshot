import datetime
import glob
import os
from itertools import chain
from pathlib import Path
from typing import Iterator

import xxhash
from pydantic import ConfigDict, validate_call

from moonshot.src.configs.env_variables import EnvironmentVars, EnvVariables
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.utils.import_modules import get_instance


class Config:
    config_dict = ConfigDict(arbitrary_types_allowed=True)


class Storage:
    @staticmethod
    @validate_call
    def create_object(
        obj_type: str,
        obj_id: str,
        obj_info: dict,
        obj_extension: str,
        obj_mod_type: str = "jsonio",
    ) -> str:
        """
        Writes the object information to a file.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_info (dict): A dictionary containing the object information.
            obj_extension (str): The file extension (e.g., 'json', 'py').
            obj_mod_type (str, optional): The module type for object serialization. Defaults to 'jsonio'.

        Returns:
            str: A filepath string of the object that has just been created.
        """
        if not hasattr(EnvironmentVars, obj_type):
            raise RuntimeError(
                f"'{obj_type}' is not a recognized EnvironmentVar value."
            )

        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension, True)
        if obj_filepath and isinstance(obj_filepath, str):
            obj_mod_instance = get_instance(
                obj_mod_type,
                Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
            )
            if obj_mod_instance and callable(obj_mod_instance):
                try:
                    obj_mod_instance(obj_filepath).create_file(obj_info)
                    return obj_filepath
                except Exception as e:
                    raise e
            else:
                raise RuntimeError(
                    f"Unable to get defined object module instance - {obj_mod_instance}"
                )
        else:
            raise RuntimeError("Unable to create object.")

    @staticmethod
    @validate_call(config=Config.config_dict)
    def create_object_with_iterator(
        obj_type: str,
        obj_id: str,
        obj_info: dict,
        obj_extension: str,
        obj_mod_type: str = "jsonio",
        iterator_keys: list[str] | None = None,
        iterator_data: Iterator[dict] | None = None,
    ) -> str:
        """
        Writes the object information to a file using iterators for specified keys.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_info (dict): A dictionary containing the object information.
            obj_extension (str): The file extension (e.g., 'json', 'py').
            obj_mod_type (str, optional): The module type for object serialization. Defaults to 'jsonio'.
            iterator_keys (list[str] | None): A list of keys for which the values will be written using iterators.
            iterator_data (Iterator[dict] | None): An iterator for the data to be written for the specified keys.

        Returns:
            str: A filepath string of the object that has just been created.
        """
        if not hasattr(EnvironmentVars, obj_type):
            raise RuntimeError(
                f"'{obj_type}' is not a recognized EnvironmentVar value."
            )

        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension, True)
        if not obj_filepath or not isinstance(obj_filepath, str):
            raise RuntimeError("Unable to create object.")

        obj_mod_instance = get_instance(
            obj_mod_type,
            Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
        )
        if not obj_mod_instance or not callable(obj_mod_instance):
            raise RuntimeError(
                f"Unable to get defined object module instance - {obj_mod_instance}"
            )

        try:
            obj_mod_instance(obj_filepath).create_file_with_iterator(
                obj_info, iterator_keys, iterator_data
            )
            return obj_filepath
        except Exception as e:
            raise e

    @staticmethod
    @validate_call
    def read_object_with_iterator(
        obj_type: str,
        obj_id: str,
        obj_extension: str,
        obj_mod_type: str = "jsonio",
        json_keys: list[str] | None = None,
        iterator_keys: list[str] | None = None,
    ) -> dict:
        """
        Retrieves object data from a file, with options to filter by specific keys for efficient data handling.

        This function reads from a file corresponding to the given object type and ID, deserializing the content
        using the specified module. It can also selectively extract values or create iterators for specified keys,
        which is useful for handling large datasets or deeply nested JSON structures.

        Args:
            obj_type (str): The category of the object to read (e.g., 'recipe', 'cookbook').
            obj_id (str): The unique identifier for the object.
            obj_extension (str): The file extension indicating the file type (e.g., 'json', 'py').
            obj_mod_type (str, optional): The deserialization module type to use. Defaults to 'jsonio'.
            json_keys (list[str] | None, optional): Keys for which to directly extract values from the file.
                If provided, only these keys will be included in the returned dictionary.
            iterator_keys (list[str] | None, optional): Keys for which to create iterators, allowing for
                streamed access to large or nested structures within the file.

        Returns:
            dict: A dictionary with the requested object data. If `json_keys` is provided, the dictionary
            will contain only the specified keys and their values. If `iterator_keys` is provided, the dictionary
            will include iterators for the specified keys, enabling streamed data access.
        """
        if not hasattr(EnvironmentVars, obj_type):
            raise RuntimeError(
                f"'{obj_type}' is not a recognized EnvironmentVar value."
            )

        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath and isinstance(obj_filepath, str):
            obj_mod_instance = get_instance(
                obj_mod_type,
                Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
            )
            if obj_mod_instance and callable(obj_mod_instance):
                return obj_mod_instance(obj_filepath).read_file_iterator(
                    json_keys, iterator_keys
                )
            else:
                raise RuntimeError(
                    f"Unable to get defined object module instance - {obj_mod_instance}"
                )
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    @validate_call
    def read_object(
        obj_type: str, obj_id: str, obj_extension: str, obj_mod_type: str = "jsonio"
    ) -> dict:
        """
        Reads the object information from a file.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').
            obj_mod_type (str, optional): The module type for object deserialization. Defaults to 'json'.

        Returns:
            dict: A dictionary containing the object information.
        """
        if not hasattr(EnvironmentVars, obj_type):
            raise RuntimeError(
                f"'{obj_type}' is not a recognized EnvironmentVar value."
            )

        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath and isinstance(obj_filepath, str):
            obj_mod_instance = get_instance(
                obj_mod_type,
                Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
            )
            if obj_mod_instance and callable(obj_mod_instance):
                return obj_mod_instance(obj_filepath).read_file()
            else:
                raise RuntimeError(
                    f"Unable to get defined object module instance - {obj_mod_instance}"
                )
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    @validate_call
    def delete_object(obj_type: str, obj_id: str, obj_extension: str) -> bool:
        """
        Deletes the specified object file.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').

        Returns:
            bool: True if the file was successfully deleted.

        Raises:
            RuntimeError: If no file is found with the specified ID and type.
        """
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath:
            Path(obj_filepath).unlink()
            return True
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    def count_objects(
        obj_type: str, obj_id: str, obj_extension: str, item_path: str
    ) -> int:
        """
        Counts the number of objects in a dataset without loading them fully into memory.

        Args:
            obj_type (str): The type of the object (e.g., 'dataset').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json').
            item_path (str): The path to the items in the JSON file.

        Returns:
            int: The count of the objects.
        """
        count = 0
        generator = Storage.read_object_with_iterator(
            obj_type, obj_id, obj_extension, iterator_keys=[item_path]
        )
        for _ in generator[item_path.split(".")[0]]:
            count += 1
        return count

    @staticmethod
    @validate_call
    def get_objects(obj_type: str, obj_extension: str) -> Iterator[str]:
        """
        Retrieves all the object files with the specified extension from one or more directories.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_extension (str): The file extension (e.g., 'json', 'py').

        Returns:
            Iterator[str]: An iterator that yields the filepaths of the object files.
        """
        if not hasattr(EnvironmentVars, obj_type):
            raise RuntimeError(
                f"'{obj_type}' is not a recognized EnvironmentVar value."
            )

        directories = EnvironmentVars.get_file_directory(obj_type)
        return chain.from_iterable(
            glob.iglob(f"{directory}/*.{obj_extension}") for directory in directories
        )

    @staticmethod
    def get_creation_datetime(
        obj_type: str, obj_id: str, obj_extension: str
    ) -> datetime.datetime:
        """
        Retrieves the creation datetime of an object.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').

        Returns:
            datetime: The creation datetime of the object.
        """
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath:
            creation_timestamp = os.path.getctime(obj_filepath)
            creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
            return creation_datetime
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    def get_file_hash(obj_type: str, obj_id: str, obj_extension: str) -> str:
        """
        Retrieves the hash of the file content for an object using the 'xxhash' library, which provides
        an extremely fast non-cryptographic hash algorithm.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').

        Returns:
            str: The hex digest of the xxHash of the file content.
        """
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath and Path(obj_filepath).exists():
            with open(obj_filepath, "rb") as file:
                file_content = file.read()
            file_hash = xxhash.xxh64(file_content).hexdigest()
            return file_hash
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    def get_filepath(
        obj_type: str, obj_id: str, obj_extension: str, ignore_existance: bool = False
    ) -> str:
        """
        Retrieves the file path for an object.

        This method uses the provided object type, object ID, and object extension to construct the file path
        of the object. If the creation flag is set to True, it returns the file path even if the file does not exist.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').
            ignore_existance (bool, optional): A flag indicating whether to return the file path
                                        even if the file does not exist. Defaults to False.

        Returns:
            str: The file path of the object.
        """
        return EnvironmentVars.get_file_path(
            obj_type, f"{obj_id}.{obj_extension}", ignore_existance
        )

    @staticmethod
    @validate_call
    def is_object_exists(obj_type: str, obj_id: str, obj_extension: str) -> bool:
        """
        Checks if the object exists.

        Args:
            obj_type (str): The type of the object (e.g., 'runner', 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').

        Returns:
            bool: True if the object exists, False otherwise.
        """
        filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if filepath:
            return Path(filepath).exists()
        else:
            return False

    @staticmethod
    def create_database_connection(
        obj_type: str, obj_id: str, obj_extension: str, db_mod_type: str = "sqlite"
    ) -> DBInterface:
        """
        Establishes a database connection for a specific object.

        Args:
            obj_type (str): The type of the object for which the database connection is to be established
            (e.g., 'runner', 'recipe', 'cookbook').

            obj_id (str): The unique identifier of the object for which the database connection is to be established.

            obj_extension (str): The file extension of the object for which the database connection is to be established
            (e.g., 'json', 'py').

            db_mod_type (str): The type of database module to use for establishing the connection (e.g., 'sqlite).
            Defaults to 'sqlite'.

        Returns:
            DBInterface: An instance of the database accessor, which can be used to interact with the database.
        """
        database_instance = get_instance(
            db_mod_type,
            Storage.get_filepath(
                EnvVariables.DATABASES_MODULES.name, db_mod_type, "py"
            ),
        )
        if database_instance:
            database_instance = database_instance(
                Path(Storage.get_filepath(obj_type, obj_id, obj_extension, True))
            )
            if database_instance.create_connection():
                return database_instance
            else:
                raise RuntimeError(f"Failed to create connection - {db_mod_type}")
        else:
            raise RuntimeError(
                f"Unable to get defined database instance - {db_mod_type}"
            )

    @staticmethod
    def close_database_connection(database_instance: DBInterface) -> None:
        """
        Closes the database connection.

        Args:
            database_instance (DBInterface): The instance of the database accessor.

        Returns:
            None
        """
        if database_instance:
            database_instance.close_connection()
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def create_database_table(
        database_instance: DBInterface, sql_create_table: str
    ) -> None:
        """
        Creates a table in the database.

        This method is used to create a table in the database. If the database instance is not initialised,
        it raises a RuntimeError. Otherwise, it calls the create_table method of the database instance.

        Args:
            database_instance (DBInterface): The database accessor instance.
            sql_create_table (str): The SQL query to create a table.

        Returns:
            None
        """
        if database_instance:
            database_instance.create_table(sql_create_table)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def create_database_record(
        database_instance: DBInterface, data: tuple, sql_create_record: str
    ) -> tuple | None:
        """
        Inserts a record into the database.

        This method is used to insert a record into the database. If the database instance is not initialised,
        it raises a RuntimeError. If the database instance is initialised, it calls the create_record method of the
        database instance with the provided data and SQL query.

        Args:
            database_instance (DBInterface): The database accessor instance.
            data (tuple): The data to be inserted into the database.
            sql_create_record (str): The SQL query to insert a record.

        Returns:
            tuple | None: The inserted record if successful, None otherwise.
        """
        if database_instance:
            return database_instance.create_record(data, sql_create_record)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def read_database_record(
        database_instance: DBInterface, data: tuple, sql_read_record: str
    ) -> tuple | None:
        """
        Reads a record from the database.

        This method is used to retrieve a record from the database. If the database instance is not initialised,
        it raises a RuntimeError. If the database instance is initialised, it calls the read_record method of the
        database instance and returns the record if found.

        Args:
            database_instance (DBInterface): The database accessor instance.
            data (tuple): The data to be matched for reading the record.
            sql_read_records (str): The SQL query to read a record.

        Returns:
            tuple | None: The record if found, None otherwise.
        """
        if database_instance:
            return database_instance.read_record(data, sql_read_record)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def read_database_records(
        database_instance: DBInterface, sql_read_records: str
    ) -> list[tuple] | None:
        """
        Reads records from the database.

        This method is used to retrieve records from the database. If the database instance is not initialised,
        it raises a RuntimeError. If the database instance is initialised, it calls the read_records method of the
        database instance and returns the record if found.

        Args:
            database_instance (DBInterface): The database accessor instance.
            data (tuple): The data to be matched for reading the record.
            sql_read_records (str): The SQL query to read a record.

        Returns:
            tuple | None: The record if found, None otherwise.
        """
        if database_instance:
            return database_instance.read_records(sql_read_records)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def update_database_record(
        database_instance: DBInterface, data: tuple, sql_update_record: str
    ) -> None:
        """
        Updates a record in the database.

        This method is used to update a record in the database. If the database instance is not initialised,
        it raises a RuntimeError. Otherwise, it calls the update_record method of the database instance.

        Args:
            database_instance (DBInterface): The database accessor instance.
            data (tuple): The data to be updated.
            sql_update_record (str): The SQL query to update a record.

        Returns:
            None
        """
        if database_instance:
            database_instance.update_record(data, sql_update_record)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def delete_database_record_in_table(
        database_instance: DBInterface, sql_delete_record: str
    ) -> None:
        """
        Deletes records from a table in the database based on a SQL condition.

        This method is used to delete records from a specific table in the database
            that meet the condition specified in the SQL delete statement.
        If the database instance is not initialised, it raises a RuntimeError.
        Otherwise, it calls the delete_records_in_table method of the database instance with the provided SQL query.

        Args:
            database_instance (DBInterface): The database accessor instance.
            sql_delete_record (str): The SQL query to delete records from a table.

        Returns:
            None
        """
        if database_instance:
            database_instance.delete_records_in_table(sql_delete_record)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def check_database_table_exists(
        database_instance: DBInterface, table_name: str
    ) -> bool | None:
        """
        Checks if a table exists in the database.

        This method checks if the specified table exists in the database. If the database instance is not initialised,
        it raises a RuntimeError.

        Args:
            database_instance (DBInterface): The database accessor instance.
            table_name (str): The name of the table to check for existence.

        Returns:
            bool | None: True if the table exists, False if it does not, None if the database
            instance is not initialised.
        """
        if database_instance:
            return database_instance.check_database_table_exists(table_name)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def delete_database_table(
        database_instance: DBInterface, sql_delete_table: str
    ) -> None:
        """
        Deletes a table from the database.

        This method is used to delete a table from the database. If the database instance is not initialised,
        it raises a RuntimeError. Otherwise, it calls the delete_database_table method of the database instance.

        Args:
            database_instance (DBInterface): The database accessor instance.
            sql_delete_table (str): The SQL query to delete a table.

        Returns:
            None
        """
        if database_instance:
            database_instance.delete_database_table(sql_delete_table)
        else:
            raise RuntimeError("Database instance is not initialised.")
