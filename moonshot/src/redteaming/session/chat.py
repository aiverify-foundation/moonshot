from __future__ import annotations

from typing import Union

from slugify import slugify

from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage


class ChatRecord:
    def __init__(
        self,
        chat_record_id: str,
        conn_id: str,
        context_strategy: str,
        prompt_template: str,
        attack_module: str,
        metric: str,
        prompt: str,
        prepared_prompt: str,
        system_prompt: str,
        predicted_result: str,
        duration: str,
        prompt_time: str,
    ):
        self.chat_record_id = chat_record_id
        self.conn_id = conn_id
        self.context_strategy = context_strategy
        self.prompt_template = prompt_template
        self.attack_module = attack_module
        self.metric = metric
        self.prompt = prompt
        self.prepared_prompt = prepared_prompt
        self.system_prompt = system_prompt
        self.predicted_result = predicted_result
        self.duration = duration
        self.prompt_time = prompt_time

    def to_dict(self) -> dict[str, str]:
        """
        Converts the ChatRecord instance into a dictionary.

        Returns:
            dict: A dictionary representation of the ChatRecord instance.
        """
        return {
            "chat_record_id": self.chat_record_id,
            "conn_id": self.conn_id,
            "context_strategy": self.context_strategy,
            "prompt_template": self.prompt_template,
            "attack_module": self.attack_module,
            "metric": self.metric,
            "prompt": self.prompt,
            "prepared_prompt": self.prepared_prompt,
            "system_prompt": self.system_prompt,
            "predicted_result": self.predicted_result,
            "duration": self.duration,
            "prompt_time": self.prompt_time,
        }


class Chat:
    sql_create_chat_metadata_record = """
            INSERT INTO chat_metadata_table (
            chat_id,endpoint,created_epoch,created_datetime)
            VALUES(?,?,?,?)
    """

    sql_select_n_chat_from_chat_table = (
        """SELECT * FROM {} order by prompt_time desc limit {}"""
    )

    def __init__(
        self,
        session_db_instance: DBInterface,
        endpoint: str = "",
        created_epoch: float = 0.0,
        created_datetime: str = "",
        chat_id: str = "",
    ):
        self.chat_history = []
        if chat_id:
            db_chat_id = chat_id.replace("-", "_")
            # There is an existing chat
            self.chat_id = db_chat_id
            self.endpoint = endpoint
            self.chat_history = self.load_chat_history(session_db_instance, db_chat_id)
        else:
            # No existing chat, create new chat
            created_datetime = str(created_datetime).replace("-", "_")
            chat_id = f"{slugify(endpoint)}_{created_datetime}"
            db_chat_id = chat_id.replace("-", "_")

            sql_create_chat_history_table = f"""
                CREATE TABLE IF NOT EXISTS {db_chat_id} (
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
            Storage.create_database_table(
                session_db_instance, sql_create_chat_history_table
            )

            chat_meta_tuple = (
                chat_id,
                endpoint,
                created_epoch,
                created_datetime,
            )

            Storage.create_database_record(
                session_db_instance,
                chat_meta_tuple,
                Chat.sql_create_chat_metadata_record,
            )

            self.chat_id = db_chat_id
            self.endpoint = endpoint
            self.chat_history: list[ChatRecord] = []

    def to_dict(self) -> dict[str, Union[str, list[dict[str, str]]]]:
        """
        Converts the Chat instance into a dictionary.

        This method iterates over the chat history, converting each ChatRecord instance into a dictionary
        using its `to_dict` method. It then constructs a dictionary that includes the chat ID, endpoint,
        and the list of chat history dictionaries.

        Returns:
            dict: A dictionary representation of the Chat instance, including chat ID, endpoint, and chat history.
        """
        list_of_chat_history_dict = [
            chat_record.to_dict() for chat_record in self.chat_history
        ]
        return {
            "chat_id": self.chat_id,
            "endpoint": self.endpoint,
            "chat_history": list_of_chat_history_dict,
        }

    @staticmethod
    def load_chat_history(session_db_instance: DBInterface, chat_id: str) -> list:
        """
        Loads the chat history for a specific chat ID.

        This method retrieves the chat history for a given chat ID by calling the StorageManager's method
        to get the chat history for one endpoint. It then converts the chat record tuples into ChatRecord instances
        and returns a list of ChatRecord objects.

        Args:
            db_instance: The database instance associated with the chat session.
            chat_id (str): The unique identifier for the chat session.

        Returns:
            list[ChatRecord]: A list of ChatRecord instances representing the chat history.
        """
        sql_read_chat_history_for_one_endpoint = f"""SELECT * FROM {chat_id}"""
        list_of_chat_record_tuples = Storage.read_database_records(
            session_db_instance, sql_read_chat_history_for_one_endpoint
        )

        list_of_chat_records = []
        if list_of_chat_record_tuples:
            list_of_chat_records = [
                ChatRecord(*chat_record_tuple).to_dict()
                for chat_record_tuple in list_of_chat_record_tuples
            ]
        return list_of_chat_records

    @staticmethod
    def get_n_chat_history(
        session_db_instance: DBInterface, endpoint_id: str, num_of_previous_chats: int
    ) -> list[dict]:
        """
        Loads the chat history for a specific chat ID.

        This method retrieves the chat history for a given chat ID by calling the StorageManager's method
        to get the chat history for one endpoint. It then converts the chat record tuples into ChatRecord instances
        and returns a list of ChatRecord objects.

        Args:
            db_instance: The database instance associated with the chat session.
            chat_id (str): The unique identifier for the chat session.

        Returns:
            list[ChatRecord]: A list of ChatRecord instances representing the chat history.
        """
        endpoint_id = endpoint_id.replace("-", "_")
        list_of_chat_record_tuples = Storage.read_database_records(
            session_db_instance,
            Chat.sql_select_n_chat_from_chat_table.format(
                endpoint_id, num_of_previous_chats
            ),
        )
        list_of_chat_records = []
        if list_of_chat_record_tuples:
            list_of_chat_records = [
                ChatRecord(*chat_record_tuple).to_dict()
                for chat_record_tuple in list_of_chat_record_tuples
            ]
        return list_of_chat_records
