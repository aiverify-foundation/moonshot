import sqlite3
from pathlib import Path
from sqlite3 import Error

from moonshot.src.common.db_sql_queries import (
    sql_create_cache_records,
    sql_create_chat_history_records,
    sql_read_cache_records,
    sql_read_chat_history_records,
)
from moonshot.src.utils.timeit import timeit


class Database:
    @timeit
    def __init__(self, db_file: str):
        self.conn = None
        self.db_file = db_file
        self.cache_records = list()

    def __del__(self):
        """
        Cleans up the object by writing cache records and closing the database connection.

        This method is automatically called when the object is destroyed.
        """
        # Write cache records
        self.write_cache_records()

        # Close database connection
        self.close_connection()

    def create_connection(self) -> None:
        """
        Creates a connection to the database.
        """
        try:
            # Create directories if they don't exist
            Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_file)
            print(f"Established connection to database ({self.db_file})")
        except Error as sqlite3_error:
            print(
                f"Error establishing connection to database ({self.db_file}) - {str(sqlite3_error)})"
            )

    @timeit
    def create_table(self, create_table_sql: str) -> None:
        """
        Executes a SQL query to create a table in the SQLite database.

        Args:
            create_table_sql (str): The SQL statement to create the table.
        """
        if self.conn:
            try:
                with self.conn:
                    self.conn.execute(create_table_sql)
            except Error as sqlite3_error:
                print(
                    f"Error creating table for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    @timeit
    def create_metadata_records(self, sql_statement: str, metadata: tuple) -> None:
        """
        Executes a SQL statement to create metadata records in the database.

        Args:
            sql_statement (str): The SQL statement to execute.
            metadata (tuple): The tuple of metadata records to insert into the database.
        """
        if self.conn:
            try:
                with self.conn:
                    self.conn.execute(sql_statement, metadata)
            except Error as sqlite3_error:
                print(
                    f"Error inserting metadata records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    @timeit
    def update_metadata_records(self, sql_statement: str, metadata: tuple) -> None:
        """
        Updates metadata records in the database using the provided SQL statement and metadata.

        Args:
            sql_statement (str): The SQL statement to execute.
            metadata (tuple): The tuple of metadata to be updated.
        """
        if self.conn:
            try:
                with self.conn:
                    self.conn.execute(sql_statement, metadata)
            except Error as sqlite3_error:
                print(
                    f"Error updating metadata records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    @timeit
    def read_metadata_records(self, sql_statement: str, id: str) -> tuple:
        """
        Retrieves metadata records from the database using the provided SQL statement and ID.

        Args:
            sql_statement (str): The SQL statement to execute.
            id (str): The ID of the metadata record to pass to the SQL statement.

        Returns:
            tuple: A tuple of metadata records.
        """
        if self.conn:
            try:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(sql_statement, (id,))
                    return cursor.fetchone()
            except Error as sqlite3_error:
                print(
                    f"Error updating metadata records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    def create_chat_records(
        self, chat_settings: dict, prompt, prompt_info: dict, connection_id: str
    ) -> None:
        """
        Creates chat records in the database.

        Args:
            chat_settings (dict): A dictionary containing the chat settings.
            prompt: The user's prompt to the LLM.
            prompt_info (dict): A dictionary containing information about the prompt.
            connection_id (str): The ID of the connection.
        """

        if self.conn:
            try:
                # Prepare cache tuple
                cache_tuple = (
                    connection_id,
                    chat_settings["context_strategy"],
                    chat_settings["prompt_template"],
                    prompt,
                    prompt_info["prompt"],
                    prompt_info["predicted_result"],
                    prompt_info["duration"],
                )
                with self.conn:
                    self.conn.execute(sql_create_chat_history_records, cache_tuple)
            except Error as sqlite3_error:
                print(
                    f"Error inserting chat records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    @timeit
    def read_chat_records(self, number_of_records: int) -> list:
        """
        Retrieves the specified number of chat records from the database.

        Args:
            number_of_records (int): The number of chat records to retrieve.

        Returns:
            list: A list of chat records.
        """
        if self.conn:
            try:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(sql_read_chat_history_records, (number_of_records,))
                    return cursor.fetchall()
            except Error as sqlite3_error:
                print(
                    f"Error reading chat records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    def append_cache_records(
        self,
        recipe_id: str,
        prompt_template_name: str,
        prompt_info: dict,
        connection_id: str,
    ) -> None:
        """
        Appends cache records to the cache records list.

        Args:
            recipe_id (str): The ID of the recipe.
            prompt_template_name (str): The name of the prompt template.
            prompt_info (dict): Information about the prompt.
            connection_id (str): The ID of the connection.
        """
        self.cache_records.append(
            (recipe_id, prompt_template_name, prompt_info, connection_id)
        )
        print("CACHE RECORDS", self.cache_records)

    @timeit
    def create_cache_records(self) -> None:
        """
        Retrieves a cache tuple by iterating over the self.cache_records list. Then, insert them into the database.
        """
        if self.conn:
            try:
                # Prepare cache tuple
                cache_tuple = [
                    (
                        connection_id,
                        recipe_id,
                        prompt_template_name,
                        prompt_info["prompt"],
                        prompt_info["target"],
                        prompt_info["predicted_result"],
                        prompt_info["duration"],
                    )
                    for recipe_id, prompt_template_name, prompt_info, connection_id in self.cache_records
                ]
                with self.conn:
                    self.conn.executemany(sql_create_cache_records, cache_tuple)
            except Error as sqlite3_error:
                print(
                    f"Error inserting cache records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    @timeit
    def read_cache_records(self, recipe_id: str, connection_id: str) -> list:
        """
        Reads cache records from the database based on the recipe ID and connection ID.

        Args:
            recipe_id (str): The ID of the recipe to retrieve cache records for.
            connection_id (str): The ID of the connection to retrieve cache records for.

        Returns:
            list: A list of cache records retrieved from the database.
        """
        if self.conn:
            try:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(sql_read_cache_records, (recipe_id, connection_id))
                    return cursor.fetchall()
            except Error as sqlite3_error:
                print(
                    f"Error reading cache records for database ({self.db_file}) - {str(sqlite3_error)})"
                )

    @timeit
    def write_cache_records(self) -> None:
        """
        Writes cache records to the database.
        """
        if len(self.cache_records) > 0:
            print(f"Committing all {len(self.cache_records)} cache records...")
            self.create_cache_records()

            # Clear cache records
            self.cache_records = list()

    @timeit
    def close_connection(self) -> None:
        """
        Closes the connection to the database.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
