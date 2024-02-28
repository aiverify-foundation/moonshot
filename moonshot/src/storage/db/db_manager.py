from typing import Union

from moonshot.src.storage.db.db_accessor import DBAccessor
from moonshot.src.storage.db.db_sql_queries import (
    sql_create_cache_records,
    sql_create_cache_table,
    sql_create_metadata_records,
    sql_create_metadata_table,
    sql_read_cache_records,
    sql_read_metadata_records,
    sql_update_metadata_records,
)
from moonshot.src.storage.db.db_sqlite import DBSqlite
from moonshot.src.storage.db.db_types import DatabaseTypes


class DatabaseManager:
    @staticmethod
    def create_benchmark_connection(
        db_filepath: str, db_type: DatabaseTypes = DatabaseTypes.SQLITE
    ) -> Union[DBAccessor, None]:
        """
        Creates a connection to the benchmark database.

        This method attempts to create a connection to the benchmark database specified by the db_filepath and
        db_type parameters.
        If the db_type is SQLITE, it creates an instance of the DBSqlite class and attempts to establish a connection.
        If the connection is successfully established, it returns the DBSqlite instance.
        If the connection fails, it returns None.
        If the db_type is not SQLITE, it also returns None.

        Args:
            db_filepath (str): The file path of the database.
            db_type (DatabaseTypes, optional): The type of the database. Defaults to DatabaseTypes.SQLITE.

        Returns:
            Union[DBAccessor, None]: The DBAccessor instance if the connection is successfully established,
            None otherwise.
        """
        if db_type is DatabaseTypes.SQLITE:
            db_instance = DBSqlite(db_filepath)
            return db_instance if db_instance.create_connection() else None
        else:
            return None

    @staticmethod
    def close_benchmark_connection(db_instance: DBAccessor) -> None:
        """
        Closes the connection to the benchmark database.

        This method attempts to close the connection to the benchmark database using the db_instance parameter.
        If the db_instance is not None, it calls the close_connection method of the db_instance.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to close the connection.

        Returns:
            None
        """
        if db_instance:
            db_instance.close_connection()

    @staticmethod
    def create_benchmark_cache_table(db_instance: DBAccessor) -> None:
        """
        Creates a cache table in the benchmark database.

        This method attempts to create a cache table in the benchmark database using the db_instance parameter.
        If the db_instance is not None, it calls the create_table method of the db_instance with the SQL query to
        create a cache table.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to create the table.

        Returns:
            None
        """
        if db_instance:
            db_instance.create_table(sql_create_cache_table)

    @staticmethod
    def create_benchmark_metadata_table(db_instance: DBAccessor) -> None:
        """
        Creates a metadata table in the benchmark database.

        This method attempts to create a metadata table in the benchmark database using the db_instance parameter.
        If the db_instance is not None, it calls the create_table method of the db_instance with the SQL query to
        create a metadata table.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to create the table.

        Returns:
            None
        """
        if db_instance:
            db_instance.create_table(sql_create_metadata_table)

    @staticmethod
    def create_benchmark_cache_record(
        db_instance: DBAccessor, cache_data: tuple
    ) -> None:
        """
        Creates a cache record in the benchmark database.

        This method attempts to create a cache record in the benchmark database using the db_instance parameter
        and cache_data.
        If the db_instance is not None, it calls the create_record method of the db_instance with the SQL query to
        create a cache record.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to create the record.
            cache_data (tuple): The data to be stored in the cache record.

        Returns:
            None
        """
        if db_instance:
            db_instance.create_record(cache_data, sql_create_cache_records)

    @staticmethod
    def create_benchmark_metadata_record(
        db_instance: DBAccessor, metadata: tuple
    ) -> None:
        """
        Creates a metadata record in the benchmark database.

        This method attempts to create a metadata record in the benchmark database using the db_instance parameter
        and metadata.
        If the db_instance is not None, it calls the create_record method of the db_instance with the SQL query to
        create a metadata record.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to create the record.
            metadata (tuple): The data to be stored in the metadata record.

        Returns:
            None
        """
        if db_instance:
            db_instance.create_record(metadata, sql_create_metadata_records)

    @staticmethod
    def read_benchmark_cache_record(
        db_instance: DBAccessor, cache_data: tuple
    ) -> Union[tuple, None]:
        """
        Reads a cache record from the benchmark database.

        This method attempts to read a cache record from the benchmark database using the db_instance parameter
        and cache_data.
        If the db_instance is not None, it calls the read_record method of the db_instance with the SQL query to
        read a cache record.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to read the record.
            cache_data (tuple): The data to be read from the cache record.

        Returns:
            Union[tuple, None]: The cache record if found, None otherwise.
        """
        if db_instance:
            return db_instance.read_record(cache_data, sql_read_cache_records)

    @staticmethod
    def read_benchmark_metadata_record(
        db_instance: DBAccessor, metadata: tuple
    ) -> Union[tuple, None]:
        """
        Reads a metadata record from the benchmark database.

        This method attempts to read a metadata record from the benchmark database using the db_instance parameter
        and metadata.
        If the db_instance is not None, it calls the read_record method of the db_instance with the SQL query to
        read a metadata record.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to read the record.
            metadata (tuple): The data to be read from the metadata record.

        Returns:
            Union[tuple, None]: The metadata record if found, None otherwise.
        """
        if db_instance:
            return db_instance.read_record(metadata, sql_read_metadata_records)

    @staticmethod
    def update_benchmark_metadata_record(
        db_instance: DBAccessor, metadata: tuple
    ) -> None:
        """
        Updates a metadata record in the benchmark database.

        This method attempts to update a metadata record in the benchmark database using the db_instance parameter
        and metadata.
        If the db_instance is not None, it calls the update_record method of the db_instance with the SQL query to
        update a metadata record.

        Args:
            db_instance (DBAccessor): The DBAccessor instance to update the record.
            metadata (tuple): The data to be updated in the metadata record.

        Returns:
            None
        """
        if db_instance:
            return db_instance.update_record(metadata, sql_update_metadata_records)
