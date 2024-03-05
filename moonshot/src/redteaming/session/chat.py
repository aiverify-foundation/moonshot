from __future__ import annotations
from slugify import slugify
from datetime import datetime

from moonshot.src.storage.storage_manager import StorageManager


class ChatRecord:
    def __init__(
        self,
        chat_record_id,
        conn_id,
        context_strategy,
        prompt_template,
        prompt,
        prepared_prompt,
        predicted_result,
        duration,
        prompt_time,
    ):
        self.chat_record_id = chat_record_id
        self.conn_id = conn_id
        self.context_strategy = context_strategy
        self.prompt_template = prompt_template
        self.prompt = prompt
        self.prepared_prompt = prepared_prompt
        self.predicted_result = predicted_result
        self.duration = duration
        self.prompt_time = prompt_time

    def to_dict(self) -> dict:
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
            "prompt": self.prompt,
            "prepared_prompt": self.prepared_prompt,
            "predicted_result": self.predicted_result,
            "duration": self.duration,
            "prompt_time": self.prompt_time,
        }


class Chat:
    def __init__(
        self,
        session_db_instance,
        endpoint: str = None,
        created_epoch: float = None,
        created_datetime: float = None,
        chat_id: str = "",
    ):
        if chat_id:
            # There is an existing chat
            self.chat_id = chat_id
            self.endpoint = endpoint
            self.chat_history = self.load_chat_history(session_db_instance, chat_id)
        else:
            # No existing chat, create new chat
            created_datetime = created_datetime.replace("-", "_")
            chat_id = f"{slugify(endpoint)}_{created_datetime}"
            StorageManager.create_chat_history_storage(chat_id, session_db_instance)
            chat_meta_tuple = (chat_id, endpoint, created_epoch, created_datetime)
            StorageManager.create_chat_metadata_record(
                chat_meta_tuple, session_db_instance
            )

            self.chat_id = chat_id
            self.endpoint = endpoint
            self.chat_history = [ChatRecord]

    def to_dict(self) -> dict:
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

    @classmethod
    def load_chat(cls, db_instance, chat_id: str, endpoint: str = None) -> Chat:
        """
        Class method to load a Chat instance for a given chat ID and optional endpoint.

        This method initializes a Chat instance using the provided database instance, chat ID, and optionally
        an endpoint. It is designed to facilitate the retrieval and manipulation of chat data associated with
        a specific chat session.

        Args:
            cls: The class from which this method is called.
            db_instance: The database instance associated with the chat session.
            chat_id (str): The unique identifier for the chat session.
            endpoint (str, optional): The endpoint associated with the chat session. Defaults to None.

        Returns:
            Chat: An instance of the Chat class initialized with the provided parameters.
        """
        return cls(session_db_instance=db_instance, chat_id=chat_id, endpoint=endpoint)

    def load_chat_history(self, db_instance, chat_id) -> list[ChatRecord]:
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
        list_of_chat_record_tuples = StorageManager.get_chat_history_for_one_endpoint(
            chat_id, db_instance
        )
        list_of_chat_records = [
            ChatRecord(*chat_record_tuple)
            for chat_record_tuple in list_of_chat_record_tuples
        ]
        return list_of_chat_records

    @staticmethod
    def send_prompt(
        session_db_instance,
        chat_id,
        user_prompt,
        prepared_prompt,
        context_strategy,
        prompt_template,
    ) -> None:
        chat_obj = Chat(session_db_instance=session_db_instance, chat_id=chat_id)
        prepared_prompt_dict = {"data": [{"prompt": prepared_prompt}]}
        predicted_result = chat_obj.get_prediction(
            prepared_prompt_dict, "connection_object"
        )

        # TODO
        connection_id = "conn_id_123"
        duration = "2 secs"
        prompt_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # TODO callback with partial
        chat_record_tuple = (
            connection_id,
            context_strategy,
            prompt_template,
            user_prompt,
            prepared_prompt,
            predicted_result,
            duration,
            prompt_time,
        )
        StorageManager.create_chat_record(
            chat_record_tuple, session_db_instance, chat_id
        )

    def get_prediction(self, prepared_prompt, connection_object) -> str:
        # TODO
        return "predicted results"
