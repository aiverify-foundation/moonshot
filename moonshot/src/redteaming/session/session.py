import time
from slugify import slugify
from datetime import datetime
import os
from ast import literal_eval
from pathlib import Path

from moonshot.src.storage.storage_manager import StorageManager
from moonshot.src.redteaming.session.chat import Chat
from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.storage.db.db_accessor import DBAccessor


class SessionMetadata:
    def __init__(
        self,
        session_id: str = "",
        name: str = "",
        description: str = "",
        endpoints: str = "",
        created_epoch: str = "",
        created_datetime: str = "",
        context_strategy: str = "",
        prompt_template: str = "",
        chat_ids="",
    ):
        self.session_id = session_id
        self.name = name
        self.description = description
        self.endpoints = endpoints
        self.created_epoch = created_epoch
        self.created_datetime = created_datetime
        self.context_strategy = context_strategy
        self.prompt_template = prompt_template
        self.chat_ids = chat_ids

    def to_dict(self) -> dict:
        """
        Converts the SessionMetadata instance into a dictionary.

        Returns:
            dict: A dictionary representation of the SessionMetadata instance.
        """
        return {
            "session_id": self.session_id,
            "name": self.name,
            "description": self.description,
            "endpoints": self.endpoints,
            "created_epoch": self.created_epoch,
            "created_datetime": self.created_datetime,
            "context_strategy": self.context_strategy,
            "prompt_template": self.prompt_template,
            "chat_ids": self.chat_ids,
        }


class Session:
    def __init__(
        # TODO system prompt
        self,
        name: str = "",
        description: str = "",
        endpoints: list = "",
        session_id: str = "",
        prompt_template="",
        context_strategy="",
    ):
        if session_id:
            # Check if session_id is valid
            db_filepath = f"{EnvironmentVars.SESSIONS}/{session_id}.db"
            if Path(db_filepath).exists():
                self.db_instance = StorageManager.create_session_database_connection(
                    self.session_id
                )
            else:
                print("Unable to resume existing session. Please create a new session.")
        else:
            # There is no existing session, create new session
            self.name = name
            self.description = description
            self.created_epoch = time.time()
            self.created_datetime = datetime.fromtimestamp(self.created_epoch).strftime(
                "%Y%m%d-%H%M%S"
            )
            self.endpoints = endpoints
            self.prompt_template = prompt_template
            self.context_strategy = context_strategy
            session_id = f"{slugify(name)}_{self.created_datetime}"
            self.session_id = session_id
            self.create_new_session()

    def create_new_session(self) -> None:
        """
        Creates a new session with associated metadata and initializes storage structures.

        This method performs several key operations to establish a new session:
        1. It compiles session metadata into a tuple, including session ID, name, description, endpoints, creation time,
        context strategy, and prompt template.
        2. It establishes a database connection for the session and creates necessary storage structures, including
        session and chat metadata tables.
        3. It inserts the session metadata into the database.
        4. For each endpoint associated with the session, it creates a chat instance, initializes chat tables, and
        updates the session metadata with the chat IDs.

        The method ensures that all necessary database tables and records are created for the session and its chats,
        setting up a complete environment for managing session and chat data.

        Returns:
            None: This method does not return a value.
        """
        session_meta_tuple = (
            self.session_id,
            self.name,
            self.description,
            str(self.endpoints),
            self.created_epoch,
            self.created_datetime,
            self.context_strategy,
            self.prompt_template,
        )

        # creates db, session and chat metadata tables, and insert session metadata
        session_db_instance = StorageManager.create_session_database_connection(
            self.session_id
        )
        StorageManager.create_session_storage(session_meta_tuple, session_db_instance)

        # creates chat tables, update chat metadata and update session metadata with chat ids
        list_of_chats = [
            Chat(
                session_db_instance, endpoint, self.created_epoch, self.created_datetime
            )
            for endpoint in self.endpoints
        ]
        chat_ids = [chat.chat_id for chat in list_of_chats]
        StorageManager.update_session_metata_with_chat_info(
            (str(chat_ids), self.session_id), session_db_instance
        )

    def get_session_metadata(self) -> SessionMetadata:
        """
        Retrieves session metadata from the database and returns it as a SessionMetadata instance.

        Returns:
            SessionMetadata: An instance of SessionMetadata populated with the session's metadata.
        """
        session_metadata = self.db_instance.read_session_metadata()
        return SessionMetadata(*session_metadata)

    @staticmethod
    def get_connection_instance_by_session_id(session_id: str) -> DBAccessor:
        """
        Creates and returns a database connection instance for a given session ID.

        It is used to access the database to perform operations.

        Args:
            session_id (str): The unique identifier for the session.

        Returns:
            A database connection instance specific to the session identified by session_id.
        """
        session_db_instance = StorageManager.create_session_database_connection(
            session_id
        )
        return session_db_instance

    @staticmethod
    def get_session_metadata_by_id(session_id: str) -> SessionMetadata:
        """
        Retrieves and returns the session metadata for a given session ID.

        This method fetches the session metadata from the database associated with the specified session ID. It
        establishes a database connection, retrieves the session metadata, and then constructs a SessionMetadata
        object with the retrieved data. Additionally, it converts the 'endpoints' and 'chat_ids' fields from string
        representations to their original data types using literal_eval.

        Args:
            session_id (str): The unique identifier for the session whose metadata is to be retrieved.

        Returns:
            SessionMetadata: An instance of SessionMetadata populated with the session's metadata, including
                            converted 'endpoints' and 'chat_ids' fields.
        """
        session_db_instance = StorageManager.create_session_database_connection(
            session_id
        )
        session_metadata = StorageManager.get_session_metata(session_db_instance)
        session_metadata = SessionMetadata(*session_metadata)

        # parse string of lists to lists. they are stored as string as the db does not support
        session_metadata.endpoints = literal_eval(session_metadata.endpoints)
        session_metadata.chat_ids = literal_eval(session_metadata.chat_ids)
        return session_metadata

    @staticmethod
    def get_session_chats_by_session_id(session_id) -> list[Chat]:
        """
        Retrieves and returns a list of Chat instances for all chats associated with a given session ID.

        This method establishes a database connection for the specified session ID and fetches the metadata for all
        chats associated with that session. It then creates and returns a list of Chat instances, each initialized
        with the database connection and the metadata for one of the chats. This allows for interaction with and
        manipulation of individual chat sessions within the specified session.

        Args:
            session_id (str): The unique identifier for the session whose chats are to be retrieved.

        Returns:
            list: A list of Chat instances, each representing a chat session associated with the specified session ID.
        """
        session_db_instance = StorageManager.create_session_database_connection(
            session_id
        )
        list_of_chat_metadata = StorageManager.get_session_chat_metadata(
            session_db_instance
        )
        return [
            Chat.load_chat(session_db_instance, chat_metadata[0], chat_metadata[1])
            for chat_metadata in list_of_chat_metadata
        ]

    @staticmethod
    def delete_session(session_id) -> None:
        """
        Deletes the database file associated with a given session ID.

        Args:
            session_id (str): The unique identifier for the session whose database file is to be deleted.
        """
        try:
            os.remove(f"{EnvironmentVars.SESSIONS}/{session_id}.db")
        except OSError as e:
            print(f"Failed to delete Session file: {e.filename} - {e.strerror}")
        else:
            print(f"Successfully deleted Session - {session_id}")

    @staticmethod
    def prepare_prompt(
        prompt: str, context_strategy: str = "", prompt_template: str = ""
    ) -> str:
        # TODO call CS and PT manager to prepare prompts
        if context_strategy:
            prompt += " context strategy added"
        if prompt_template:
            prompt += "prompt template added"
        return prompt

    @staticmethod
    def send_prompt(session_id: str, user_prompt: str) -> None:
        # TODO
        # get session db connection
        session_db_instance = StorageManager.create_session_database_connection(
            session_id
        )
        session_metadata = SessionMetadata(
            *StorageManager.get_session_metata(session_db_instance)
        )

        # get cs, pt and chat ids from session metadata
        context_strategy = session_metadata.context_strategy
        prompt_template = session_metadata.prompt_template
        list_of_chat_ids = literal_eval(session_metadata.chat_ids)

        # get final prompt after processing user prompt with cs and pt
        prepared_prompt = Session.prepare_prompt(
            user_prompt, context_strategy, prompt_template
        )
        for chat_id in list_of_chat_ids:
            Chat.send_prompt(
                session_db_instance,
                chat_id,
                user_prompt,
                prepared_prompt,
                context_strategy,
                prompt_template,
            )

    @staticmethod
    def update_prompt_template(session_id: str, prompt_template_name: str) -> None:
        """
        Updates the prompt template for a specific session.

        This method creates a database connection for the session identified by session_id and then calls the
        `StorageManager.update_prompt_template` method to update the prompt template with the provided name.
        It allows for changing the prompt template associated with the session, enabling customization of prompts
        used within the session.

        Args:
            session_id (str): The unique identifier of the session for which the prompt template is to be updated.
            prompt_template_name (str): The new prompt template name to be assigned to the session.

        Returns:
            None: This method does not return a value but updates the prompt template for the specified session.
        """
        session_db_instance = StorageManager.create_session_database_connection(
            session_id
        )
        StorageManager.update_prompt_template(
            session_db_instance, (prompt_template_name, session_id)
        )

    @staticmethod
    def update_context_strategy(session_id: str, context_strategy_name: str) -> None:
        """
        Updates the context strategy for a specific session.

        This method creates a database connection for the session identified by session_id and then calls the
        `StorageManager.update_context_strategy` method to update the context strategy with the provided name.
        It allows for changing the context strategy associated with the session, enabling customization of context
        management within the session.

        Args:
            session_id (str): The unique identifier of the session for which the context strategy is to be updated.
            context_strategy_name (str): The new context strategy name to be assigned to the session.

        Returns:
            None: This method does not return a value but updates the context strategy for the specified session.
        """
        session_db_instance = StorageManager.create_session_database_connection(
            session_id
        )
        StorageManager.update_context_strategy(
            session_db_instance, (context_strategy_name, session_id)
        )
