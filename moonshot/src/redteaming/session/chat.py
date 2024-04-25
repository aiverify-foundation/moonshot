from __future__ import annotations

from datetime import datetime
from typing import Union

from slugify import slugify

from moonshot.api import api_create_connector_from_endpoint
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.prompt_templates.prompt_template import PromptTemplate
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

    @classmethod
    def load_chat(
        cls, session_db_instance: DBInterface, chat_id: str, endpoint: str = ""
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
        self, session_db_instance: DBInterface, chat_id: str
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
        sql_read_chat_history_for_one_endpoint = f"""SELECT * FROM {chat_id}"""
        list_of_chat_record_tuples = Storage.read_database_records(
            session_db_instance, sql_read_chat_history_for_one_endpoint
        )

        list_of_chat_records = []
        if list_of_chat_record_tuples:
            list_of_chat_records = [
                ChatRecord(*chat_record_tuple)
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

    @staticmethod
    async def send_prompt(
        session_db_instance: DBInterface,
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

        # process prompt with prompt template if it is set
        if prompt_template_name:
            prepared_prompt = PromptTemplate.process_prompt_pt(
                prepared_prompt, prompt_template_name
            )
        endpoint_instance = api_create_connector_from_endpoint(endpoint)

        # put variables into PromptArguments before passing it to get_prediction
        new_prompt_info = ConnectorPromptArguments(
            prompt_index=1, prompt=prepared_prompt, target=""
        )

        prompt_start_time = datetime.now()

        # sends prompt to endpoint
        prediction_response = await Connector.get_prediction(
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

        sql_create_chat_record = f"""
            INSERT INTO {chat_id} (connection_id,context_strategy,prompt_template,prompt,
            prepared_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?)
            """
        Storage.create_database_record(
            session_db_instance, chat_record_tuple, sql_create_chat_record
        )
