import sqlite3
from pathlib import Path
from typing import Union

from moonshot.src.storage.db.db_accessor import DBAccessor


class DbSqlite(DBAccessor):
    @staticmethod
    def create_connection(db_path: str) -> Union[sqlite3.Connection, None]:
        """
        Creates a connection to the database.

        Args:
            db_path (str): The database path.

        Returns:
            None
        """
        try:
            # Create directories if they don't exist
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            sqlite_conn = sqlite3.connect(db_path)
            print(f"Established connection to database ({db_path})")
            return sqlite_conn

        except sqlite3.Error as sqlite3_error:
            print(
                f"Error establishing connection to database ({db_path}) - {str(sqlite3_error)})"
            )
            return None

    @staticmethod
    def close_connection(db_conn: sqlite3.Connection) -> None:
        """
        Closes the connection to the database.

        Args:
            db_conn (Any): The connection to the database.

        Returns:
            None
        """
        if db_conn:
            db_conn.close()

    @staticmethod
    def create_table(db_conn: sqlite3.Connection, create_table_sql: str) -> None:
        """
        Creates a table in the database using the provided SQL statement.

        Args:
            create_table_sql (str): The SQL statement to create a table.

        Returns:
            None
        """
        if db_conn:
            try:
                with db_conn:
                    db_conn.execute(create_table_sql)

            except sqlite3.Error as sqlite3_error:
                print(f"Error creating table for database - {str(sqlite3_error)})")

    @staticmethod
    def create_record(
        db_conn: sqlite3.Connection, record: tuple, create_record_sql: str
    ) -> None:
        """
        Creates a record in the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record (tuple): The record to be inserted into the database.
            create_record_sql (str): The SQL statement to create a record.

        Returns:
            None
        """
        if db_conn:
            try:
                with db_conn:
                    db_conn.execute(create_record_sql, record)

            except sqlite3.Error as sqlite3_error:
                print(f"Error inserting record into database - {str(sqlite3_error)})")

    @staticmethod
    def read_metadata_record(
        db_conn: sqlite3.Connection, record_id: str, read_record_sql: str
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
        if db_conn:
            try:
                with db_conn:
                    cursor = db_conn.cursor()
                    cursor.execute(read_record_sql, (record_id,))
                    return cursor.fetchone()

            except sqlite3.Error as sqlite3_error:
                print(f"Error reading record from database - {str(sqlite3_error)}")
        return None

    @staticmethod
    def read_cache_record(
        db_conn: sqlite3.Connection, record: tuple, read_record_sql: str
    ) -> Union[tuple, None]:
        """
        Reads a record from the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record (tuple): The record to be read from the database.
            read_record_sql (str): The SQL statement to read a record.

        Returns:
            Union[tuple, None]: The record read from the database, or None if the record could not be found.
        """
        if db_conn:
            try:
                with db_conn:
                    cursor = db_conn.cursor()
                    cursor.execute(read_record_sql, record)
                    return cursor.fetchone()

            except sqlite3.Error as sqlite3_error:
                print(f"Error reading record from database - {str(sqlite3_error)}")
        return None

    @staticmethod
    def update_record(
        db_conn: sqlite3.Connection, record: tuple, update_record_sql: str
    ) -> None:
        """
        Updates a record in the database using the provided SQL statement.

        Args:
            db_conn (Any): The connection to the database.
            record (tuple): The record to be updated in the database.
            update_record_sql (str): The SQL statement to update a record.

        Returns:
            None
        """
        if db_conn:
            try:
                with db_conn:
                    db_conn.execute(update_record_sql, record)
            except sqlite3.Error as sqlite3_error:
                print(f"Error updating record into database - {str(sqlite3_error)}")
