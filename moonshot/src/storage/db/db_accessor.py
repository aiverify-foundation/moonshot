from abc import abstractmethod
from typing import Any, Union


class DBAccessor:
    @abstractmethod
    def create_connection(self) -> Union[Any, None]:
        """
        This method is used to create a connection to the database. The details of the connection
        are implementation specific and should be provided by the concrete class that inherits from this abstract class.

        Returns:
            Union[Any, None]: The connection object if successful, None otherwise.
        """
        pass

    @abstractmethod
    def close_connection(self) -> None:
        """
        This method is used to close the connection to the database. The details of the operation
        are implementation specific and should be provided by the concrete class that inherits from this abstract class.
        """
        pass

    @abstractmethod
    def create_table(self, create_table_sql: str) -> None:
        """
        This method is used to create a table in the database. The details of the operation
        are implementation specific and should be provided by the concrete class that inherits from this abstract class.

        Args:
            create_table_sql (str): The SQL query to create a table.

        Returns:
            None
        """
        pass

    @abstractmethod
    def create_record(self, record: tuple, create_record_sql: str) -> None:
        """
        This method is used to create a record in the database. The details of the operation
        are implementation specific and should be provided by the concrete class that inherits from this abstract class.

        Args:
            record (tuple): The record to be created.
            create_record_sql (str): The SQL query to create a record.

        Returns:
            None
        """
        pass

    @abstractmethod
    def read_table(self, read_table_sql: str) -> Union[list[tuple], None]:
        """
        Executes a SQL query to read data from a table and returns the results.

        This method attempts to execute a provided SQL query to read data from a table within the SQLite database.
        If the connection to the database is established, it executes the query and returns all fetched rows as a list.
        In case of an error during the execution of the query, it prints an error message detailing the issue.

        Args:
            read_table_sql (str): The SQL query string used to read data from a table.

        Returns:
            Union[list, None]: A list of tuples representing the rows fetched by the query if successful.
        """
        pass

    @abstractmethod
    def read_record(self, record: tuple, read_record_sql: str) -> Union[tuple, None]:
        """
        This method is used to read a record from the database. The details of the operation
        are implementation specific and should be provided by the concrete class that inherits from this abstract class.

        Args:
            record (tuple): The record to be read.
            read_record_sql (str): The SQL query to read a record.

        Returns:
            Union[tuple, None]: The record if found, None otherwise.
        """
        pass

    @abstractmethod
    def update_record(self, record: tuple, update_record_sql: str) -> None:
        """
        This method is used to update a record in the database. The details of the operation
        are implementation specific and should be provided by the concrete class that inherits from this abstract class.

        Args:
            record (tuple): The record to be updated.
            update_record_sql (str): The SQL query to update a record.

        Returns:
            None
        """
        pass
