import sqlite3

from moonshot.src.storage.db_interface import DBInterface


class SQLite(DBInterface):
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

    def create_record(self, record: tuple, create_record_sql: str) -> tuple | None:
        """
        Inserts a new record into the SQLite database using the provided SQL query and record data.

        This method attempts to insert a new record into the SQLite database using the provided SQL query
        and record data.

        If the connection to the SQLite database is established, it executes the SQL query with the record data.

        If the operation is successful, it commits the transaction and returns the ID of the inserted record along
        with the record data.

        If an error occurs during the record insertion process, it prints an error message with the details of the
        SQLite error and returns None.

        Args:
            record (tuple): The data of the record to be inserted.
            create_record_sql (str): The SQL query to insert a new record.

        Returns:
            tuple | None: A tuple containing the ID of the inserted record and the record data if the operation
            is successful, None otherwise.
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(create_record_sql, record)
                    self.sqlite_conn.commit()
                    # Fetch the lastrowid (auto-incremented ID)
                    inserted_id = cursor.lastrowid
                    # Return the complete record including the inserted_id
                    return (inserted_id,) + record

            except sqlite3.Error as sqlite3_error:
                print(f"Error inserting record into database - {str(sqlite3_error)}")
        return None

    def read_record(self, record: tuple, read_record_sql: str) -> tuple | None:
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

    def read_records(self, read_records_sql: str) -> list[tuple] | None:
        """
        Executes a SQL query to read data from a table and returns the results.

        This method attempts to execute a provided SQL query to read data from a table within the SQLite database.
        If the connection to the database is established, it executes the query and returns all fetched rows as a list.
        In case of an error during the execution of the query, it prints an error message detailing the issue.

        Args:
            read_records_sql (str): The SQL query string used to read data from a table.

        Returns:
            list | None: A list of tuples representing the rows fetched by the query if successful.
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(read_records_sql)
                    return cursor.fetchall()

            except sqlite3.Error as sqlite3_error:
                print(f"Error reading records from database - {str(sqlite3_error)}")
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

    def delete_record_by_id(self, record_id: int, delete_record_sql: str) -> None:
        """
        Deletes a record from the SQLite database using the provided SQL query and record ID.

        This method attempts to delete a record from the SQLite database using the provided SQL query and record ID.
        If the connection to the SQLite database is established, it executes the SQL query with the record ID.
        If an error occurs during the record deletion process, it prints an error message with the details of the
        SQLite error.

        Args:
            record_id (int): The ID of the record to be deleted.
            delete_record_sql (str): The SQL query to delete a record by ID.

        Returns:
            None
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(delete_record_sql, (record_id,))
                    self.sqlite_conn.commit()
            except sqlite3.Error as sqlite3_error:
                print(f"Error deleting record from database - {str(sqlite3_error)}")

    def delete_records_in_table(self, delete_record_sql: str) -> None:
        """
        Deletes all records from a table in the SQLite database using the provided SQL query.

        This method attempts to delete all records from a specific table in the SQLite database using the provided SQL query.
        If the connection to the SQLite database is established, it executes the SQL query to delete the records.
        If an error occurs during the deletion process, it prints an error message with the details of the SQLite error.

        Args:
            delete_record_sql (str): The SQL query to delete all records from a table.

        Returns:
            None
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(delete_record_sql)
                    self.sqlite_conn.commit()
            except sqlite3.Error as sqlite3_error:
                print(f"Error deleting records from database - {str(sqlite3_error)}")


    def check_database_table_exists(self, table_name: str) -> bool | None:
        """
        Checks if a table exists in the SQLite database.

        This method attempts to check if a table with the given name exists in the SQLite database.
        If the connection to the database is established, it executes the query to check for the table's existence.
        If the table exists, it returns True; otherwise, it returns False.

        Args:
            table_name (str): The name of the table to check for existence.

        Returns:
            bool | None: True if the table exists, False if it does not, or None if an error occurs.
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(
                        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
                    )
                    result = cursor.fetchone()
                    if result is not None:
                        return True
                    return False
            except sqlite3.Error as sqlite3_error:
                print(f"Error checking table existence - {str(sqlite3_error)}")
        return None

    def delete_database_table(self, delete_table_sql: str) -> None:
        """
        Deletes a table from the SQLite database using the provided SQL query.

        This method attempts to delete a table from the SQLite database using the provided SQL query.
        If the connection to the SQLite database is established, it executes the SQL query to delete the table.
        If an error occurs during the table deletion process, it prints an error message with the details of the
        SQLite error.

        Args:
            delete_table_sql (str): The SQL query to delete a table.

        Returns:
            None
        """
        if self.sqlite_conn:
            try:
                with self.sqlite_conn:
                    cursor = self.sqlite_conn.cursor()
                    cursor.execute(delete_table_sql)
            except sqlite3.Error as sqlite3_error:
                print(f"Error deleting table from database - {str(sqlite3_error)}")
        return None
