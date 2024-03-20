import sqlite3
from pathlib import Path
from typing import Union

from moonshot.src.storage.db.db_accessor import DBAccessor


class DBSqlite(DBAccessor):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.sqlite_conn = None

    def create_connection(self) -> bool:
        """
        Establishes a connection to the SQLite database.

        This method attempts to create a connection to the SQLite database at the path specified during the
        object's initialization.

        If the connection is successfully established, it returns True.
        If an error occurs during the connection process, it prints an error message with the details of the
        SQLite error and returns False.

        Returns:
            bool: True if the connection is successfully established, False otherwise.
        """
        try:
            # Create directories if they don't exist
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self.sqlite_conn = sqlite3.connect(self.db_path)
            print(f"Established connection to database ({self.db_path})")
            return True

        except sqlite3.Error as sqlite3_error:
            print(
                f"Error establishing connection to database ({self.db_path}) - {str(sqlite3_error)})"
            )
            return False

    def close_connection(self) -> None:
        """
        Closes the connection to the SQLite database.

        If the connection is already established, it attempts to close it and sets the connection attribute to None.
        If an error occurs during the closing process, it prints an error message with the details of the SQLite error.

        Returns:
            None
        """
        if self.sqlite_conn:
            try:
                self.sqlite_conn.close()
                print(f"Closed connection to database ({self.db_path})")
            except sqlite3.Error as sqlite3_error:
                print(
                    f"Error closing connection to database ({self.db_path}) - {str(sqlite3_error)})"
                )
            finally:
                self.sqlite_conn = None

    def create_table(self, create_table_sql: str) -> None:
        """
        Creates a table in the SQLite database using the provided SQL query.

        This method attempts to create a table in the SQLite database using the provided SQL query.
        If the connection to the SQLite database is established, it executes the SQL query.
        If an error occurs during the table creation process, it prints an error message with the details of the
        SQLite error.

        Args:
            create_table_sql (str): The SQL query to create a table.

        Returns:
            None
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    self.sqlite_conn.execute(create_table_sql)

            except sqlite3.Error as sqlite3_error:
                print(f"Error creating table for database - {str(sqlite3_error)}")

    def create_record(
        self, record: tuple, create_record_sql: str
    ) -> Union[tuple, None]:
        """
        Inserts a new record into the SQLite database using the provided SQL query and record.

        This method attempts to insert a new record into the SQLite database using the provided SQL query and record.
        If the connection to the SQLite database is established, it executes the SQL query with the record.
        If an error occurs during the record insertion process, it prints an error message with the details of the
        SQLite error and returns None.

        Args:
            record (tuple): The record to be inserted into the database.
            create_record_sql (str): The SQL query to insert a record.

        Returns:
            tuple: The inserted record if the operation is successful, None otherwise.
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    self.sqlite_conn.execute(create_record_sql, record)

            except sqlite3.Error as sqlite3_error:
                print(f"Error inserting record into database - {str(sqlite3_error)}")

    def read_record(self, record: tuple, read_record_sql: str) -> Union[tuple, None]:
        """
        Reads a record from the SQLite database using the provided SQL query and record.

        This method attempts to read a record from the SQLite database using the provided SQL query and record.

        If the connection to the SQLite database is established, it executes the SQL query with the record and returns
        the fetched record.
        If an error occurs during the record reading process, it prints an error message with the details of the SQLite
        error and returns None.

        Args:
            record (tuple): The record to be read from the database.
            read_record_sql (str): The SQL query to read a record.

        Returns:
            tuple: The read record if the operation is successful, None otherwise.
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(read_record_sql, record)
                    return cursor.fetchone()
            except sqlite3.Error as sqlite3_error:
                print(f"Error reading record from database - {str(sqlite3_error)}")
        return None

    def update_record(self, record: tuple, update_record_sql: str) -> None:
        """
        Updates a record in the SQLite database using the provided SQL query and record.

        This method attempts to update a record in the SQLite database using the provided SQL query and record.
        If the connection to the SQLite database is established, it executes the SQL query with the record.
        If an error occurs during the record updating process, it prints an error message with the details of the
        SQLite error.

        Args:
            record (tuple): The record to be updated in the database.
            update_record_sql (str): The SQL query to update a record.

        Returns:
            None
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    self.sqlite_conn.execute(update_record_sql, record)

            except sqlite3.Error as sqlite3_error:
                print(f"Error updating record into database - {str(sqlite3_error)}")

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
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(read_table_sql)
                    return cursor.fetchall()

            except sqlite3.Error as sqlite3_error:
                print(f"Error reading table from database - {str(sqlite3_error)}")
        return None
