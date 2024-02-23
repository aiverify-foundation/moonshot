from abc import abstractmethod
from typing import Any, Union


class DBAccessor:
    @staticmethod
    @abstractmethod
    def create_connection(db_id: str) -> Union[Any, None]:
        """
        Creates a connection to the database.

        Args:
            db_id (str): The ID of the database.

        Returns:
            None
        """
        pass

    @staticmethod
    @abstractmethod
    def close_connection(db_conn: Any) -> None:
        """
        Closes the connection to the database.

        Args:
            db_conn (Any): The connection to the database.

        Returns:
            None
        """
        pass

    @staticmethod
    @abstractmethod
    def create_table(db_conn: Any, create_table_sql: str) -> None:
        """
        Creates a table in the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            create_table_sql (str): The SQL statement to create a table.

        Returns:
            None
        """
        pass

    @staticmethod
    @abstractmethod
    def create_record(db_conn: Any, record: tuple, create_record_sql: str) -> None:
        """
        Creates a record in the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record (tuple): The record to be inserted into the database.
            create_record_sql (str): The SQL statement to create a record.

        Returns:
            None
        """
        pass

    @staticmethod
    @abstractmethod
    def read_metadata_record(
        db_conn: Any, record_id: str, read_record_sql: str
    ) -> Union[tuple, None]:
        """
        Reads a record from the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record_id (str): The record to be read from the database.
            read_record_sql (str): The SQL statement to read a record.

        Returns:
            Union[tuple, None]: The record read from the database, or None if the record could not be found.
        """
        pass

    @staticmethod
    @abstractmethod
    def read_cache_record(
        db_conn: Any, record: tuple, read_record_sql: str
    ) -> Union[tuple, None]:
        """
        Reads a cache record from the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record (tuple): The record to be read from the database.
            read_record_sql (str): The SQL statement to read a record.

        Returns:
            Union[tuple, None]: The record read from the database, or None if the record could not be found.
        """
        pass

    @staticmethod
    @abstractmethod
    def update_record(db_conn: Any, record: tuple, update_record_sql: str) -> None:
        """
        Updates a record in the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record (tuple): The record to be updated in the database.
            update_record_sql (str): The SQL statement to update a record.

        Returns:
            None
        """
        pass
