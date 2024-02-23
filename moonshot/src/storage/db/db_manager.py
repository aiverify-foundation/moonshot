from typing import Union

from pyparsing import Any

from moonshot.src.storage.db.db_sql_queries import (
    sql_create_cache_records,
    sql_create_cache_table,
    sql_create_metadata_records,
    sql_create_metadata_table,
    sql_read_cache_records,
    sql_read_metadata_records,
    sql_update_metadata_records,
)
from moonshot.src.storage.db.db_sqlite import DbSqlite


class DatabaseManager:
    @staticmethod
    def create_benchmark_connection(db_filepath: str) -> Any:
        """
        Creates a connection to the benchmark database.

        Args:
            db_filepath (str): The database filepath.

        Returns:
            Union[Any, None]: The connection to the database, or None if the connection could not be established.
        """
        return DbSqlite.create_connection(db_filepath)

    @staticmethod
    def close_benchmark_connection(db_conn: Any) -> None:
        """
        Closes the connection to the database.

        Args:
            db_conn (Any): The connection to the database.

        Returns:
            None
        """
        DbSqlite.close_connection(db_conn)

    @staticmethod
    def create_benchmark_cache_table(db_conn: Any) -> None:
        """
        Creates a cache table in the benchmark database.

        Args:
            db_conn (Any): The connection to the database.

        Returns:
            None
        """
        DbSqlite.create_table(db_conn, sql_create_cache_table)

    @staticmethod
    def create_benchmark_metadata_table(db_conn: Any) -> None:
        """
        Creates a metadata table in the benchmark database.

        Args:
            db_conn (Any): The connection to the database.

        Returns:
            None
        """
        DbSqlite.create_table(db_conn, sql_create_metadata_table)

    @staticmethod
    def create_benchmark_metadata_record(db_conn: Any, metadata: tuple) -> None:
        """
        Creates a metadata record in the benchmark database.

        Args:
            db_conn (Any): The connection to the database.
            metadata (tuple): The metadata to be inserted into the database.

        Returns:
            None
        """
        DbSqlite.create_record(db_conn, metadata, sql_create_metadata_records)

    @staticmethod
    def create_benchmark_cache_record(db_conn: Any, cache_data: tuple) -> None:
        """
        Creates a cache record in the benchmark database.

        Args:
            db_conn (Any): The connection to the database.
            cache_data (tuple): The cache data to be inserted into the database.

        Returns:
            None
        """
        DbSqlite.create_record(db_conn, cache_data, sql_create_cache_records)

    @staticmethod
    def read_benchmark_metadata_record(
        db_conn: Any, record_id: str
    ) -> Union[tuple, None]:
        """
        Reads a metadata record from the benchmark database.

        Args:
            db_conn (Any): The connection to the database.
            record_id (str): The metadata record to be read from the database.

        Returns:
            Union[tuple, None]: The metadata record read from the database, or None if the record could not be found.
        """
        return DbSqlite.read_metadata_record(
            db_conn, record_id, sql_read_metadata_records
        )

    @staticmethod
    def read_benchmark_cache_record(
        db_conn: Any, cache_record: tuple
    ) -> Union[tuple, None]:
        """
        Reads a cache record from the benchmark database.

        Args:
            db_conn (Any): The connection to the database.
            cache_record (tuple): The cache record to be read from the database.

        Returns:
            Union[tuple, None]: The cache record read from the database, or None if the record could not be found.
        """
        return DbSqlite.read_cache_record(db_conn, cache_record, sql_read_cache_records)

    @staticmethod
    def update_benchmark_metadata_record(db_conn: Any, metadata: tuple) -> None:
        """
        Updates a metadata record in the benchmark database.

        Args:
            db_conn (Any): The connection to the database.
            metadata (tuple): The metadata to be updated in the database.

        Returns:
            None
        """
        DbSqlite.update_record(db_conn, metadata, sql_update_metadata_records)
