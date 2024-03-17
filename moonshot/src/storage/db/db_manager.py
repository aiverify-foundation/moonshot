from typing import Union

from moonshot.src.storage.db.db_accessor import DBAccessor
from moonshot.src.storage.db.db_sql_queries import (
    sql_create_cache_records,
    sql_create_cache_table,
    sql_create_chat_metadata_record,
    sql_create_chat_metadata_table,
    sql_create_metadata_records,
    sql_create_metadata_table,
    sql_create_session_metadata_record,
    sql_create_session_metadata_table,
    sql_read_cache_records,
    sql_read_metadata_records,
    sql_read_session_chat_metadata,
    sql_read_session_metadata,
    sql_update_context_strategy,
    sql_update_metadata_records,
    sql_update_prompt_template,
    sql_update_session_metadata_chat,
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

    @staticmethod
    def create_session_connection(
        db_filepath: str, db_type: DatabaseTypes = DatabaseTypes.SQLITE
    ) -> Union[DBAccessor, None]:
        """
        Creates and returns a database connection for a session based on the specified database type and filepath.

        This static method attempts to establish a database connection for managing session data. If the database type
        is SQLITE, it creates an instance of DBSqlite with the provided file path and attempts to establish a
        connection. If the connection is successfully established, the DBSqlite instance is returned. If the connection
        fails or if a database type other than SQLITE is specified, the method returns None.

        Args:
            db_filepath (str): The file path to the database.
            db_type (DatabaseTypes, optional): The type of the database, with SQLITE as the default.

        Returns:
            Union[DBAccessor, None]: An instance of the database accessor if the connection is successful,
            None otherwise.
        """
        if db_type is DatabaseTypes.SQLITE:
            db_instance = DBSqlite(db_filepath)
            return db_instance if db_instance.create_connection() else None
        else:
            return None

    @staticmethod
    def create_session_metadata_table(db_instance: DBAccessor) -> None:
        """
        Creates a session metadata table in the database.

        This static method attempts to create a session metadata table using the provided database instance.
        It calls the `create_table` method of the database instance with a predefined SQL query to create the
        session metadata table. This operation is essential for storing session-specific metadata.

        Args:
            db_instance (DBAccessor): The database accessor instance used to execute the table creation.

        Returns:
            None: This method does not return a value.
        """
        if db_instance:
            db_instance.create_table(sql_create_session_metadata_table)

    @staticmethod
    def create_session_metadata_record(
        db_instance: DBAccessor,
        session_metadata: tuple,
    ) -> None:
        """
        Creates a session metadata record in the database.

        This method inserts a new record into the session metadata table using the provided database instance
        and session metadata. It utilizes a predefined SQL query to insert the session metadata into the database.
        This operation is crucial for persisting session-specific information that can be retrieved later.

        Args:
            db_instance (DBAccessor): The database accessor instance used for database operations.
            session_metadata (tuple): The session metadata to be inserted into the database. This should match
                                    the structure expected by the SQL query used for insertion.

        Returns:
            None: This method does not return a value.
        """
        if db_instance:
            db_instance.create_record(
                session_metadata, sql_create_session_metadata_record
            )

    @staticmethod
    def create_chat_metadata_table(db_instance: DBAccessor) -> None:
        """
        Creates a chat metadata table in the database.

        This static method is responsible for creating a table specifically designed to store metadata
        related to chat sessions. It uses the provided database instance to execute a predefined SQL query
        that creates the chat metadata table. This is an essential step for organizing and storing chat-related
        information in a structured manner.

        Args:
            db_instance (DBAccessor): The database accessor instance used for executing the table creation command.

        Returns:
            None: This method does not return a value, indicating the operation's success is silent.
        """
        if db_instance:
            db_instance.create_table(sql_create_chat_metadata_table)

    @staticmethod
    def create_chat_history_table(db_instance: DBAccessor, chat_id: str) -> None:
        """
        Creates a chat history table for a specific chat ID in the database.

        This method dynamically generates and executes a SQL query to create a new table in the database,
        named after the provided chat_id. The table is designed to store various pieces of information about
        each chat interaction, including IDs, context strategy, prompt templates, prompts, prepared prompts,
        predicted results, duration, and prompt times. The table will only be created if it does not already exist.

        Args:
            db_instance (DBAccessor): The database accessor instance used for executing the table creation command.
            chat_id (str): The unique identifier for the chat session, which will be used as the table name.

        Returns:
            None: This method does not return a value, indicating the operation's success is silent.
        """
        sql_create_chat_history_table = f"""
            CREATE TABLE IF NOT EXISTS {chat_id} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_id text NOT NULL,
            context_strategy int,
            prompt_template text,
            prompt text NOT NULL,
            prepared_prompt text NOT NULL,
            predicted_result text NOT NULL,
            duration text NOT NULL,
            prompt_time text NOT NULL
            );
        """
        if db_instance:
            db_instance.create_table(sql_create_chat_history_table)

    @staticmethod
    def create_chat_metadata_record(
        db_instance: DBAccessor, chat_metadata: tuple
    ) -> None:
        """
        Inserts a new chat metadata record into the chat metadata table in the database.

        This method uses the provided database instance to insert a new record into the chat metadata table.
        The record to be inserted is specified by the chat_metadata tuple, which should contain data structured
        according to the schema of the chat metadata table. This operation is essential for tracking and managing
        metadata associated with chat sessions.

        Args:
            db_instance (DBAccessor): The database accessor instance used for database operations.
            chat_metadata (tuple): The chat metadata to be inserted into the database. This tuple should match
                                the structure expected by the SQL query used for insertion.

        Returns:
            None: This method does not return a value, indicating that the operation's success or failure is not
                explicitly communicated back to the caller.
        """
        if db_instance:
            db_instance.create_record(chat_metadata, sql_create_chat_metadata_record)

    @staticmethod
    def update_session_metadata_with_chat_info(
        db_instance: DBAccessor, chat_info: tuple[str, str]
    ) -> None:
        """
        Updates session metadata with chat information in the database.

        This method updates an existing session metadata record with new chat information. It uses the provided
        database instance and a tuple containing the chat information to execute an update operation. The specific
        fields to be updated and the criteria for the update are defined within the SQL query referenced by
        `sql_update_session_metadata_chat`.

        Args:
            db_instance (DBAccessor): The database accessor instance used for database operations.
            chat_info (tuple): A tuple containing the chat information to be updated in the session metadata.

        Returns:
            None: This method does not return a value, indicating that the operation's success or failure is not
                explicitly communicated back to the caller.
        """
        if db_instance:
            db_instance.update_record(chat_info, sql_update_session_metadata_chat)

    @staticmethod
    def read_session_metadata(
        db_instance: DBAccessor,
    ) -> Union[tuple, None]:
        """
        Reads and returns the first record of session metadata from the database.

        This static method retrieves the session metadata from the database using the provided database instance.
        It executes a predefined SQL query to read the session metadata table. If the query is successful, it returns
        the first record from the fetched results. This method is typically used to retrieve metadata for a specific
        session.

        Args:
            db_instance (DBAccessor): The database accessor instance used for reading the session metadata.

        Returns:
            The first record of session metadata if available, None otherwise.
        """
        if db_instance:
            records = db_instance.read_table(sql_read_session_metadata)
            return records[0] if records else None

    @staticmethod
    def read_session_chat_metadata(db_instance: DBAccessor) -> Union[list[tuple], None]:
        """
        Reads and returns chat metadata for a session from the database.

        This static method fetches chat metadata associated with a session from the database using the provided
        database instance. It executes a predefined SQL query to read the chat metadata table. The method returns
        all the records fetched by the query, which contain chat metadata for the session.

        Args:
            db_instance (DBAccessor): The database accessor instance used for reading the chat metadata.

        Returns:
            A list of tuples representing the chat metadata records if available, None otherwise.
        """
        if db_instance:
            return db_instance.read_table(sql_read_session_chat_metadata)
        else:
            return []

    @staticmethod
    def read_chat_history_for_one_endpoint(
        db_instance: DBAccessor, chat_id: str
    ) -> Union[list[tuple], None]:
        """
        Reads and returns the chat history for a specific chat ID from the database.

        This method constructs and executes a SQL query to fetch all records from the table corresponding to the
        given chat_id. It is designed to retrieve the entire chat history for a particular chat session, allowing
        for analysis or display of past interactions.

        Args:
            db_instance (DBAccessor): The database accessor instance used for executing the read operation.
            chat_id (str): The unique identifier for the chat session, which corresponds to the table name.

        Returns:
            A list of tuples representing the chat history records if available, None otherwise.
        """
        sql_read_chat_history_for_one_endpoint = f"""SELECT * FROM {chat_id}"""
        if db_instance:
            return db_instance.read_table(sql_read_chat_history_for_one_endpoint)

    @staticmethod
    def create_chat_record(
        db_instance: DBAccessor,
        chat_record_tuple: tuple,
        chat_id: str,
    ) -> None:
        """
        Inserts a new chat record into the specified chat history table in the database.

        This method constructs and executes a SQL query to insert a new chat record into the table identified by
        the provided chat_id. The chat record data is specified by the chat_record_tuple, which should contain all
        necessary information in the correct order as expected by the SQL insert statement.

        Args:
            db_instance (DBAccessor): The database accessor instance used for database operations.
            chat_record_tuple (tuple): The chat record data to be inserted, structured as a tuple.
            chat_id (str): The unique identifier for the chat session, used to determine the correct table.

        Returns:
            None: This method does not return a value, indicating that the operation's success or failure is not
                explicitly communicated back to the caller.
        """
        sql_create_chat_record = f"""
            INSERT INTO {chat_id} (connection_id,context_strategy,prompt_template,prompt,
            prepared_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?)
            """
        if db_instance:
            return db_instance.create_record(chat_record_tuple, sql_create_chat_record)

    @staticmethod
    def update_prompt_template(
        db_instance: DBAccessor, prompt_template_tuple: tuple[str, str]
    ) -> None:
        """
        Updates the prompt template in the database.

        This method updates the prompt template in the database using the provided database instance and the prompt
        template tuple. If the database instance is valid, it calls the update_record method of the database instance
        with the SQL query to update the prompt template.

        Args:
            db_instance (DBAccessor): The database accessor instance.
            prompt_template_tuple (tuple): The tuple containing the updated prompt template information.

        Returns:
            None
        """
        if db_instance:
            db_instance.update_record(prompt_template_tuple, sql_update_prompt_template)

    @staticmethod
    def update_context_strategy(
        db_instance: DBAccessor, context_strategy_tuple: tuple[str, str]
    ) -> None:
        """
        Updates the context strategy in the database.

        This method updates the context strategy in the database using the provided database instance and the context
        strategy tuple. If the database instance is valid, it calls the update_record method of the database instance
        with the SQL query to update the context strategy.

        Args:
            db_instance (DBAccessor): The database accessor instance.
            context_strategy_tuple (tuple): The tuple containing the updated context strategy information.

        Returns:
            None
        """
        if db_instance:
            db_instance.update_record(
                context_strategy_tuple, sql_update_context_strategy
            )
