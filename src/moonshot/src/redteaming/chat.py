import json
import time
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any

from jinja2 import Template
from slugify import slugify

from moonshot.src.common.connection import Connection, get_predictions
from moonshot.src.common.db import Database
from moonshot.src.common.db_sql_queries import (
    sql_create_chat_history_table,
    sql_create_chat_metadata_records,
    sql_create_chat_metadata_table,
    sql_read_chat_metadata_records,
    sql_update_chat_metadata_records,
)
from moonshot.src.common.env_variables import EnvironmentVars


class ChatMetadata:
    def __init__(self, endpoint: str, created_epoch: float):
        self.endpoint = endpoint
        if created_epoch:
            self.created_epoch = created_epoch
        else:
            self.created_epoch = time.time()

        datetime_now = datetime.fromtimestamp(self.created_epoch)
        self.created_datetime = datetime_now.strftime("%Y%m%d-%H%M%S")
        self.conn_instance = None
        self.db_instance = None
        self.endpoint = endpoint
        # context strategy and prompt template
        self.context_strategy = 0
        self.prompt_template = ""
        # loaded prompt template information
        self.prompt_template_info = dict()

        self.chat_id = f"chat-{slugify(endpoint)}-{self.created_datetime}"
        self.db_file = f"{EnvironmentVars.DATABASES}/{self.chat_id}.db"

    @classmethod
    def load_metadata(cls, metadata: tuple) -> Any:
        """
        Loads the chat metadata and creates an instance of the class using the provided metadata.
        Args:
            metadata (tuple): A tuple containing the following metadata:
                - chat_id (int): The ID of the chat.
                - endpoint (str): The endpoint for the chat.
                - created_epoch (int): The epoch timestamp the chat was created.
                - created_datetime (datetime): The datetime object representing the creation time.
                - context_strategy (int): The strategy for handling context.
                - prompt_template (str): The template for generating prompts.
        Returns:
            class_instance: An instance of the class with the provided metadata.
        """
        (
            chat_id,
            endpoint,
            created_epoch,
            created_datetime,
            context_strategy,
            prompt_template,
        ) = metadata

        class_instance = cls(endpoint, created_epoch)
        class_instance.created_datetime = created_datetime
        class_instance.context_strategy = context_strategy
        class_instance.prompt_template = prompt_template
        return class_instance

    def create_metadata_in_database(self) -> None:
        """
        Creates metadata records in the database. Refer to get_tuple() to see what the fields required
        for creating metadata records.
        """
        self.db_instance.create_metadata_records(
            sql_create_chat_metadata_records, self.get_tuple()
        )

    def update_metadata_in_database(self) -> None:
        """
        Updates metadata records in the database with its own context_strategy, prompt_template and chat_id.
        """
        self.db_instance.update_metadata_records(
            sql_update_chat_metadata_records,
            (
                self.context_strategy,
                self.prompt_template,
                self.chat_id,
            ),
        )

    def get_dict(self) -> dict:
        """
        Returns a dictionary containing the attributes of the current instance.

        Returns:
            dict: A dictionary with the following keys:
                - chat_id: The chat ID of the instance.
                - endpoint: The endpoint of the instance.
                - created_epoch: The epoch timestamp when the instance was created.
                - created_datetime: The datetime when the instance was created.
                - context_strategy: The context strategy of the instance.
                - prompt_template: The prompt template of the instance.
        """
        return {
            "chat_id": self.chat_id,
            "endpoint": self.endpoint,
            "created_epoch": self.created_epoch,
            "created_datetime": self.created_datetime,
            "context_strategy": self.context_strategy,
            "prompt_template": self.prompt_template,
        }

    def get_tuple(self) -> tuple:
        """
        Returns a tuple containing the chat ID, endpoint, created epoch, created datetime,
        context strategy, and prompt template.

        Returns:
            tuple: A tuple containing the chat ID, endpoint, created epoch, created datetime,
            context strategy, and prompt template.
        """
        return (
            self.chat_id,
            self.endpoint,
            self.created_epoch,
            self.created_datetime,
            self.context_strategy,
            self.prompt_template,
        )


class Chat:
    def __init__(self, endpoint: str, created_epoch: float = None, chat_id: str = ""):
        if chat_id:
            # There is an existing chat
            chat_db_file = f"{EnvironmentVars.DATABASES}/{chat_id}.db"
            if Path(chat_db_file).exists():
                # Load the db instance
                db_instance = Database(chat_db_file)
                db_instance.create_connection()

                # Load the metadata by reading the info from the db
                self.chat_metadata = ChatMetadata.load_metadata(
                    db_instance.read_metadata_records(
                        sql_read_chat_metadata_records, chat_id
                    )
                )

                # Update metadata with the db instance
                self.chat_metadata.db_instance = db_instance

                # Resume the existing chats
                self.resume_existing_chat()
            else:
                raise RuntimeError("Invalid chat id")

        else:
            # Create a new chat
            self.chat_metadata = ChatMetadata(endpoint, created_epoch)
            self.create_new_chat()

    @classmethod
    def load_chat(cls, chat_id: str) -> Any:
        """
        Loads an existing chat using the provided chat_id.

        Args:
            chat_id (str): The ID of the chat to be loaded.

        Returns:
            Chat: The loaded Chat object.
        """
        # Trigger loading existing file using chat_id
        return cls("", None, chat_id)

    def create_new_chat(self) -> None:
        """
        Creates a Connection instance, DB instance and DB metadata entry using information from ChatMetadata endpoint.
        """
        # create a connection instance
        self.chat_metadata.conn_instance = Connection.load_from_json_config(
            self.chat_metadata.endpoint
        )

        # create a db instance
        self.chat_metadata.db_instance = Database(self.chat_metadata.db_file)
        self.chat_metadata.db_instance.create_connection()
        self.chat_metadata.db_instance.create_table(sql_create_chat_metadata_table)
        self.chat_metadata.db_instance.create_table(sql_create_chat_history_table)

        # Create database metadata entry
        self.chat_metadata.create_metadata_in_database()

    def resume_existing_chat(self) -> None:
        """
        Resumes an existing chat by loading the configuration from ChatMetadata endpoint.
        """
        # create a connection instance
        self.chat_metadata.conn_instance = Connection.load_from_json_config(
            self.chat_metadata.endpoint
        )

    def get_chat_settings(self) -> dict:
        """
        Retrieves the chat settings.

        Returns:
            dict: A dictionary containing the chat settings with the following keys:
                  - "context_strategy" (int): The context strategy used in the chat.
                  - "prompt_template" (str): The prompt template used in the chat.
        """
        return {
            "context_strategy": self.chat_metadata.context_strategy,
            "prompt_template": self.chat_metadata.prompt_template,
        }

    def get_id(self) -> str:
        """
        Returns the chat ID associated with the current chat metadata.

        Returns:
            str: The chat ID.
        """
        return self.chat_metadata.chat_id

    def get_previous_prompts(self, num_of_previous_prompts: int) -> list:
        """
        Retrieves a list of previous prompts from the chat metadata database.

        Args:
            num_of_previous_prompts (int): The number of previous prompts to retrieve.

        Returns:
            list: A list of dictionaries representing the previous prompts.
        """
        if num_of_previous_prompts > 0:
            prev_prompts = self.chat_metadata.db_instance.read_chat_records(
                num_of_previous_prompts
            )
            return [self._convert_tuple_to_dict(chat) for chat in prev_prompts]
        else:
            return list()

    def _convert_tuple_to_dict(self, chat_records_tuple: tuple) -> dict:
        """
        Converts a tuple of chat records into a dictionary.

        Args:
            chat_records_tuple (tuple): A tuple containing the following chat records:
                - chat_id (int): The ID of the chat.
                - connection_id (int): The ID of the connection.
                - context_strategy (int): The strategy used for context.
                - prompt_template (str): The template for the prompt.
                - prompt (str): The prompt for the chat.
                - prepared_prompt (str): The prepared prompt for the chat.
                - predicted_result (str): The predicted result of the chat.
                - duration (float): The duration of the chat.

        Returns:
            dict: A dictionary representation of the chat records with the following keys:
                - "chat_id" (int): The ID of the chat.
                - "connection_id" (int): The ID of the connection.
                - "context_strategy" (int): The strategy used for context.
                - "prompt_template" (str): The template for the prompt.
                - "prompt" (str): The prompt for the chat.
                - "prepared_prompt" (str): The prepared prompt for the chat.
                - "predicted_result" (str): The predicted result of the chat.
                - "duration" (float): The duration of the chat.
        """
        (
            chat_id,
            connection_id,
            context_strategy,
            prompt_template,
            prompt,
            prepared_prompt,
            predicted_result,
            duration,
        ) = chat_records_tuple
        return {
            "chat_id": chat_id,
            "connection_id": connection_id,
            "context_strategy": context_strategy,
            "prompt_template": prompt_template,
            "prompt": prompt,
            "prepared_prompt": prepared_prompt,
            "predicted_result": predicted_result,
            "duration": duration,
        }

    def set_context_strategy(self, context_strategy: int) -> None:
        """
        Sets the context strategy for the chat.

        Args:
            context_strategy (int): The context strategy to be set. (number of previous prompts to be used)
        """
        # Store context strategy and Update the chat metadata
        if context_strategy >= 0:
            self.chat_metadata.context_strategy = context_strategy
            self.chat_metadata.update_metadata_in_database()

    def get_context_strategy(self) -> int:
        """
        Retrieves the context strategy.

        Returns:
            int: The context strategy (number of previous prompts to be used).
        """
        # Retrieve the context strategy
        return self.chat_metadata.context_strategy

    def set_prompt_template(self, prompt_template: str) -> None:
        """
        Sets the prompt template for the chat.

        Args:
            prompt_template (str): The name of the prompt template.
        """
        if prompt_template:
            # Store prompt template
            self.chat_metadata.prompt_template = prompt_template

            # Load prompt template info
            with open(
                f"{EnvironmentVars.PROMPT_TEMPLATES}/{prompt_template}.json", "r"
            ) as json_file:
                self.chat_metadata.prompt_template_info = json.load(json_file)
        else:
            # Store prompt template
            self.chat_metadata.prompt_template = ""

        # Update the chat metadata
        self.chat_metadata.update_metadata_in_database()

    def send_prompt(self, prompt: str) -> str:
        """
        Sends a prompt to the model for prediction and returns the first prediction response.

        Args:
            prompt (str): The prompt to be sent for prediction.

        Returns:
            str: The first prediction response if available, otherwise None.
        """
        # prepare the prompt for the prediction
        prepared_prompt = self.prepare_prompt(prompt)

        # prepare the prompt info for the prediction
        prompt_info = {"data": [{"prompt": prepared_prompt}]}

        # make the prediction and write to database through callback
        predictions_response = get_predictions(
            prompt_info,
            self.chat_metadata.conn_instance,
            partial(
                self.chat_metadata.db_instance.create_chat_records,
                self.get_chat_settings(),
                prompt,
            ),
        )

        # return the first prediction response
        if predictions_response:
            return predictions_response[0]
        else:
            return predictions_response

    def process_context_prompts(
        self, current_prompt: str, context_strategy: int
    ) -> str:
        """
        Append the user's prompts with context strategy (previous prompts to be used as context).

        Args:
            current_prompt (str): The current prompt.
            context_strategy (int): The context strategy (number of previous prompts to be used).

        Returns:
            str or None: The processed context prompts or None if there are no previous prompts.
        """
        previous_prompts = self.get_previous_prompts(context_strategy)
        if previous_prompts:
            final_prompt = ""
            for previous_prompt in previous_prompts:
                final_prompt += previous_prompt["prompt"]
                final_prompt += " " + previous_prompt["predicted_result"]
            final_prompt += f"Current prompt:{current_prompt}"
            final_prompt = "Previous prompt:" + final_prompt
            return final_prompt
        return None

    def prepare_prompt(self, prompt: str) -> str:
        """
        Prepare the final prompt to be sent by checking if the prompt needs to be modified
        to add prompt template contents and context.

        Args:
            prompt (str): The original prompt.

        Returns:
            str: The prepared final prompt.
        """
        context_strategy = self.get_context_strategy()
        new_prompt = prompt
        if (
            self.chat_metadata.prompt_template
            or self.chat_metadata.prompt_template != ""
        ):
            prompt_template_file = f"{EnvironmentVars.PROMPT_TEMPLATES}/{self.chat_metadata.prompt_template}.json"
            with open(prompt_template_file, "r") as json_file:
                prompt_template_details = json.load(json_file)
                template = prompt_template_details["template"]
                jinja_template = Template(template)
                new_prompt = jinja_template.render({"prompt": prompt})

        if context_strategy > 0:
            prompt_with_context = self.process_context_prompts(
                new_prompt, context_strategy
            )
            if prompt_with_context:
                return prompt_with_context
            # no previous prompt
            return new_prompt
        else:
            return new_prompt
