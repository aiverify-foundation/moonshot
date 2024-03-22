from __future__ import annotations

from datetime import datetime
from typing import Union

from slugify import slugify

from moonshot.src.benchmarking.prompt_arguments import PromptArguments
from moonshot.src.connectors.connector_manager import ConnectorManager
from moonshot.src.prompt_template.prompt_template_manager import PromptTemplateManager
from moonshot.src.redteaming.context_strategy.context_strategy_manager import (
    ContextStrategyManager,
)
from moonshot.src.storage.db.db_accessor import DBAccessor
from moonshot.src.storage.storage_manager import StorageManager


class ChatRecord:
    def __init__(
        self,
        chat_record_id: str,
        conn_id: str,
        context_strategy: str,
        prompt_template: str,
        prompt: str,
        prepared_prompt: str,
        predicted_result: str,
        duration: str,
        prompt_time: str,
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
            "prompt": self.prompt,
            "prepared_prompt": self.prepared_prompt,
            "predicted_result": self.predicted_result,
            "duration": self.duration,
            "prompt_time": self.prompt_time,
        }


class Chat:
    def __init__(
        self,
        session_db_instance: DBAccessor,
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
            StorageManager.create_chat_history_storage(db_chat_id, session_db_instance)
            chat_meta_tuple = (
                chat_id,
                endpoint,
                created_epoch,
                created_datetime,
            )
            StorageManager.create_chat_metadata_record(
                chat_meta_tuple, session_db_instance
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

    @classmethod
    def load_chat(
        cls, session_db_instance: DBAccessor, chat_id: str, endpoint: str = ""
    ) -> Chat:
        """
        Class method to load a Chat instance for a given chat ID and optional endpoint.

        This method initializes a Chat instance using the provided database instance, chat ID, and optionally
        an endpoint. It is designed to facilitate the retrieval and manipulation of chat data associated with
        a specific chat session.

        Args:
            cls: The class from which this method is called.
            db_instance: The database instance associated with the chat session.
            chat_id (str): The unique identifier for the chat session.
            endpoint (str, optional): The endpoint associated with the chat session. Defaults to empty string.

        Returns:
            Chat: An instance of the Chat class initialized with the provided parameters.
        """
        return cls(
            session_db_instance=session_db_instance, chat_id=chat_id, endpoint=endpoint
        )

    def load_chat_history(
        self, session_db_instance: DBAccessor, chat_id: str
    ) -> list[ChatRecord]:
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
            chat_id, session_db_instance
        )
        list_of_chat_records = []
        if list_of_chat_record_tuples:
            list_of_chat_records = [
                ChatRecord(*chat_record_tuple)
                for chat_record_tuple in list_of_chat_record_tuples
            ]
        return list_of_chat_records

    @staticmethod
    async def send_prompt(
        session_db_instance: DBAccessor,
        chat_id: str,
        endpoint: str,
        user_prompt: str,
        context_strategy_name: str = "",
        prompt_template_name: str = "",
    ) -> None:
        """
        Sends a prompt message to the chat session.

        This method sends a prompt message to the chat session based on the user input prompt. It optionally
        processes the prompt with a context strategy and/or a prompt template before sending it to the endpoint.

        Args:
            session_db_instance: The database instance associated with the chat session.
            chat_id (str): The unique identifier for the chat session.
            endpoint: The endpoint to which the prompt message will be sent.
            user_prompt (str): The user input prompt message.
            context_strategy_name (str, optional): The name of the context strategy to process the prompt.
            Defaults to "".
            prompt_template_name (str, optional): The name of the prompt template to process the prompt.
            Defaults to "".
        """
        prepared_prompt = user_prompt

        # process prompt with context strategy if it is set
        if context_strategy_name:
            chat_obj = Chat.load_chat(session_db_instance, chat_id, endpoint)
            list_of_chat_records = [
                chat_record.to_dict() for chat_record in chat_obj.chat_history
            ]

            # sort the chat records by time in descending order if it's not already sorted
            sorted_list_of_chat_records_time_desc = sorted(
                list_of_chat_records, key=lambda i: i["prompt_time"], reverse=True
            )
            prepared_prompt = ContextStrategyManager.process_prompt_cs(
                prepared_prompt,
                context_strategy_name,
                sorted_list_of_chat_records_time_desc,
            )

        # process prompt with prompt template if it is set
        if prompt_template_name:
            prepared_prompt = PromptTemplateManager.process_prompt_pt(
                prepared_prompt, prompt_template_name
            )
        endpoint_instance = ConnectorManager.create_connector(
            ConnectorManager.read_endpoint(endpoint)
        )

        # put variables into PromptArguments before passing it to get_prediction
        new_prompt_info = PromptArguments(
            rec_id="",
            pt_id="",
            ds_id="",
            prompt_index=1,
            prompt=prepared_prompt,
            target="",
            conn_id="",
        )

        prompt_start_time = datetime.now()

        # sends prompt to endpoint
        prediction_response = await ConnectorManager.get_prediction(
            new_prompt_info, endpoint_instance
        )

        # stores chat prompts, predictions and its config into DB
        chat_record_tuple = (
            "",
            context_strategy_name,
            prompt_template_name,
            user_prompt,
            prepared_prompt,
            prediction_response.predicted_results,
            prediction_response.duration,
            prompt_start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        )
        StorageManager.create_chat_record(
            chat_record_tuple, session_db_instance, chat_id
        )
