import datetime
import glob
import os
from itertools import chain
from pathlib import Path
from typing import Iterator

from pyparsing import Generator

from moonshot.src.configs.env_variables import EnvironmentVars, EnvVariables
from moonshot.src.storage.db_accessor import DBAccessor
from moonshot.src.utils.import_modules import get_instance


class Storage:
    @staticmethod
    def create_object(
        obj_type: str,
        obj_id: str,
        obj_info: dict,
        obj_extension: str,
        obj_mod_type: str = "jsonio",
    ) -> bool:
        """
        Writes the object information to a file.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_info (dict): A dictionary containing the object information.
            obj_extension (str): The file extension (e.g., 'json', 'py').
            obj_mod_type (str, optional): The module type for object serialization. Defaults to 'json'.
        """
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension, True)
        if obj_filepath:
            obj_mod_instance = get_instance(
                obj_mod_type,
                Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
            )
            if obj_mod_instance:
                return obj_mod_instance(obj_filepath).create_file(obj_info)
            else:
                raise RuntimeError(
                    f"Unable to get defined object module instance - {obj_mod_instance}"
                )
        else:
            raise RuntimeError("Unable to create object.")

    @staticmethod
    def read_object_generator(
        obj_type: str,
        obj_id: str,
        obj_extension: str,
        item_path: str,
        obj_mod_type: str = "generatorio",
    ) -> Generator:
        """
        Returns a generator that yields items from a JSON file.

        This method uses the provided object type, object ID, and object extension to construct the file path
        of the JSON file.

        It then uses the 'jsonio' module to open the JSON file and the 'generatorio' module to create a generator
        that yields items from the JSON file.

        The item path is used to specify the path to the items in the JSON file.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').
            item_path (str): The path to the items in the JSON file.
            obj_mod_type (str, optional): The module type for object deserialization. Defaults to 'generatorio'.

        Returns:
            Callable: A generator that yields items from the JSON file.

        Raises:
            RuntimeError: If there is an error getting the object module instance or the object file module instance.
        """
        # Get jsonio object to return raw file instance
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath:
            obj_file_instance = get_instance(
                obj_mod_type,
                Storage.get_filepath(EnvVariables.IO_MODULES.name, "jsonio", "py"),
            )
            if obj_file_instance:
                obj_file_instance = obj_file_instance(obj_filepath).read_file_raw()
            else:
                raise RuntimeError(
                    f"Unable to get defined object file module instance - {obj_file_instance}"
                )
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

        # Get generator object to return gen object
        obj_mod_instance = get_instance(
            obj_mod_type,
            Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
        )
        if obj_mod_instance:
            return obj_mod_instance(obj_file_instance, item_path)
        else:
            raise RuntimeError(
                f"Unable to get defined object module instance - {obj_mod_instance}"
            )

    @staticmethod
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
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath:
            obj_mod_instance = get_instance(
                obj_mod_type,
                Storage.get_filepath(EnvVariables.IO_MODULES.name, obj_mod_type, "py"),
            )
            if obj_mod_instance:
                return obj_mod_instance(obj_filepath).read_file()
            else:
                raise RuntimeError(
                    f"Unable to get defined object module instance - {obj_mod_instance}"
                )
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    def delete_object(obj_type: str, obj_id: str, obj_extension: str) -> None:
        """
        Deletes an object.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension (e.g., 'json', 'py').
        """
        obj_filepath = Storage.get_filepath(obj_type, obj_id, obj_extension)
        if obj_filepath:
            Path(obj_filepath).unlink()
        else:
            raise RuntimeError(f"No {obj_type.lower()} found with ID: {obj_id}")

    @staticmethod
    def get_objects(obj_type: str, obj_extension: str) -> Iterator[str]:
        """
        Retrieves all the object files with the specified extension from one or more directories.

        Args:
            obj_type (str): The type of the object (e.g., 'recipe', 'cookbook').
            obj_extension (str): The file extension (e.g., 'json', 'py').

        Returns:
            Iterator[str]: An iterator that yields the filepaths of the object files.
        """
        directories = EnvironmentVars.get_file_directory(obj_type)
        return chain.from_iterable(
            glob.iglob(f"{directory}/*.{obj_extension}") for directory in directories
        )

    @staticmethod
    def get_creation_datetime(obj_type: str, obj_id: str, obj_extension: str):
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
    ) -> DBAccessor:
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
            DBAccessor: An instance of the database accessor, which can be used to interact with the database.
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
    def close_database_connection(database_instance: DBAccessor) -> None:
        """
        Closes the database connection.

        Args:
            database_instance (DBAccessor): The instance of the database accessor.

        Returns:
            None
        """
        if database_instance:
            database_instance.close_connection()
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def create_database_table(
        database_instance: DBAccessor, sql_create_table: str
    ) -> None:
        """
        Creates a table in the database.

        This method is used to create a table in the database. If the database instance is not initialised,
        it raises a RuntimeError. Otherwise, it calls the create_table method of the database instance.

        Args:
            database_instance (DBAccessor): The database accessor instance.
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
        database_instance: DBAccessor, data: tuple, sql_create_record: str
    ) -> None:
        """
        Creates a record in the database.

        This method is used to create a record in the database. If the database instance is not initialised,
        it raises a RuntimeError. Otherwise, it calls the create_record method of the database instance.

        Args:
            database_instance (DBAccessor): The database accessor instance.
            data (tuple): The data to be inserted.
            sql_create_record (str): The SQL query to create a record.

        Returns:
            None
        """
        if database_instance:
            database_instance.create_record(data, sql_create_record)
        else:
            raise RuntimeError("Database instance is not initialised.")

    @staticmethod
    def read_database_record(
        database_instance: DBAccessor, data: tuple, sql_read_record: str
    ) -> tuple | None:
        """
        Reads a record from the database.

        This method is used to retrieve a record from the database. If the database instance is not initialised,
        it raises a RuntimeError. If the database instance is initialised, it calls the read_record method of the
        database instance and returns the record if found.

        Args:
            database_instance (DBAccessor): The database accessor instance.
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
        database_instance: DBAccessor, sql_read_records: str
    ) -> list[tuple] | None:
        """
        Reads records from the database.

        This method is used to retrieve records from the database. If the database instance is not initialised,
        it raises a RuntimeError. If the database instance is initialised, it calls the read_records method of the
        database instance and returns the record if found.

        Args:
            database_instance (DBAccessor): The database accessor instance.
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
        database_instance: DBAccessor, data: tuple, sql_update_record: str
    ) -> None:
        """
        Updates a record in the database.

        This method is used to update a record in the database. If the database instance is not initialised,
        it raises a RuntimeError. Otherwise, it calls the update_record method of the database instance.

        Args:
            database_instance (DBAccessor): The database accessor instance.
            data (tuple): The data to be updated.
            sql_update_record (str): The SQL query to update a record.

        Returns:
            None
        """
        if database_instance:
            database_instance.update_record(data, sql_update_record)
        else:
            raise RuntimeError("Database instance is not initialised.")
