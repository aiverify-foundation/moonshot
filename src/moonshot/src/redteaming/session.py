from __future__ import annotations

import glob
import json
import time
from datetime import datetime
from pathlib import Path

from slugify import slugify

from moonshot.src.common.env_variables import EnvironmentVars
from moonshot.src.redteaming.chat import Chat
from moonshot.src.utils.write_file import write_json_file


class SessionMetadata:
    def __init__(
        self,
        session_id: str,
        name: str,
        description: str,
        created_epoch: float,
        endpoints: list,
        metadata_file: str,
        chats: list,
        prompt_template: str,
        context_strategy: int,
    ):
        self.session_id = session_id
        self.name = name
        self.description = description
        self.created_epoch = created_epoch
        self.created_datetime = datetime.fromtimestamp(created_epoch).strftime(
            "%Y%m%d-%H%M%S"
        )
        self.endpoints = endpoints
        self.metadata_file = metadata_file
        self.chats = chats
        self.prompt_template = prompt_template
        self.context_strategy = context_strategy

    @classmethod
    def load_metadata(cls, session_id: str) -> SessionMetadata:
        """
        Load an instance of the class from a JSON configuration.
        This class method allows loading an instance of the class from a JSON configuration stored in a file
        or a string.

        Args:
            session_id (str): The target session's ID.

        Returns:
            SessionMetadata: An instance of the class created from the JSON configuration.
        """
        try:
            with open(
                f"{EnvironmentVars.SESSIONS}/{session_id}.json", "r"
            ) as json_file:
                file_info = json.load(json_file)
                return cls(
                    file_info["session_id"],
                    file_info["name"],
                    file_info["description"],
                    file_info["created_epoch"],
                    file_info["endpoints"],
                    file_info["metadata_file"],
                    file_info["chats"],
                    file_info["prompt_template"],
                    file_info["context_strategy"],
                )
        except OSError:
            print(
                "Unable to find Session configuration file. Ensure that session configuration file exists."
            )

    def create_metadata_file(self) -> None:
        """
        This function creates a metadata file and saves the session metadata to it.
        """
        # Save the session metadata
        metadata_dict = self.get_dict()
        metadata_dict["chats"] = [chat.get_id() for chat in self.chats]
        write_json_file(
            metadata_dict,
            self.metadata_file,
        )

    def get_dict(self) -> dict:
        """
        Returns a dictionary containing the session ID, name, description, created epoch, created datetime,
        endpoints, metadata file, chats, prompt template, and context strategy of the object.
        Returns:
            dict: A dictionary with the following keys:
                - session_id (str): The session ID.
                - name (str): The name of the session.
                - description (str): The description of the session.
                - created_epoch (int): The creation time of the session in epoch.
                - created_datetime (datetime): The creation time of the session in datetime.
                - endpoints (list): The list of endpoints.
                - metadata_file (str): The metadata file.
                - chats (list): The list of chats.
                - prompt_template (str): The prompt template name.
                - context_strategy (str): The context strategy.
        """
        return {
            "session_id": self.session_id,
            "name": self.name,
            "description": self.description,
            "created_epoch": self.created_epoch,
            "created_datetime": self.created_datetime,
            "endpoints": self.endpoints,
            "metadata_file": self.metadata_file,
            "chats": self.chats,
            "prompt_template": self.prompt_template,
            "context_strategy": self.context_strategy,
        }


class Session:
    current_session = None

    def __init__(
        self,
        name: str,
        description: str,
        endpoints: list,
        session_id: str = "",
    ):
        if session_id:
            # There is an existing session
            self.metadata = SessionMetadata.load_metadata(session_id)
            if Path(self.metadata.metadata_file).exists():
                # There is an existing session
                self.resume_existing_session()
            else:
                print("Unable to resume existing session. Please create a new session.")
        else:
            # Create a new session
            session_id = slugify(name, lowercase=False)
            self.metadata = SessionMetadata(
                session_id,
                name,
                description,
                time.time(),
                endpoints,
                f"{EnvironmentVars.SESSIONS}/{session_id}.json",
                [],
                "",
                0,
            )
            # There is no existing session, create new session
            self.create_new_session()

    @classmethod
    def load_session(cls, session_id: str) -> Session:
        """
        A class method that loads a session based on a given session ID.
        Args:
            session_id (str): The ID of the session to be loaded.
        Returns:
            Session: An instance of the class with the specified session ID.
        """
        # Trigger loading existing file using session_id
        return cls("", "", [], session_id)

    def create_new_session(self) -> None:
        """
        Creates a new session. For each endpoint in this session, create a chat to track the history.
        """
        # Create new session chats with provided endpoints
        self.metadata.chats = [
            Chat(endpoint, self.metadata.created_epoch)
            for endpoint in self.metadata.endpoints
        ]

        # Save session metadata
        self.metadata.create_metadata_file()

    def resume_existing_session(self) -> None:
        """
        Resumes an existing session. This function loads all the chats from the metadata and assigns them to the
        'chats_instances' variable. It then updates the prompt templates and context strategy based on the metadata.
        """
        self.metadata.chats = [
            Chat.load_chat(chat_id) for chat_id in self.metadata.chats
        ]

        # Update the prompt templates and context strategy
        self.set_context_strategy(self.metadata.context_strategy)
        self.set_prompt_template(self.metadata.prompt_template)

    def set_context_strategy(self, new_context_strategy: int) -> None:
        """
        Set the context strategy for the session and chats.

        Args:
            new_context_strategy (int): The new context strategy to be set.
        """
        # Set session and chats context strategy
        self.metadata.context_strategy = new_context_strategy
        for chat in self.metadata.chats:
            chat.set_context_strategy(new_context_strategy)

        # Save session metadata
        self.metadata.create_metadata_file()

    def set_prompt_template(self, new_prompt_template: str = "") -> None:
        """
        Sets the prompt template for this session and the chats in this session.

        Args:
            new_prompt_template (str): The name of the new prompt template to be set.
        """
        # Set session and chats prompt template
        self.metadata.prompt_template = new_prompt_template
        for chat in self.metadata.chats:
            chat.set_prompt_template(new_prompt_template)

        # Save session metadata
        self.metadata.create_metadata_file()

    def send_prompt(self, user_prompt) -> None:
        """
        Sends a user prompt to all the chats in the metadata.

        Args:
            user_prompt (str): The user prompt to be sent.
        """
        for chat in self.metadata.chats:
            chat.send_prompt(user_prompt)

    def get_session_id(self) -> str:
        """
        Retrieves the session ID.

        Returns:
            str: The session ID associated with the current session.
        """
        return self.metadata.session_id

    def get_session_chats(self) -> list:
        """
        Gets the chats associated with the current session.

        Returns:
            list: The list of chats associated with the current session.
        """
        return self.metadata.chats

    def get_session_previous_prompts(self, number_of_previous_prompts: int) -> list:
        """
        Retrieves a list of previous prompts from the session's metadata.

        Args:
            number_of_previous_prompts (int): The number of previous prompts to retrieve.

        Returns:
            list: A list of dictionaries representing the previous prompts.
        """
        return [
            chat.get_previous_prompts(number_of_previous_prompts)
            for chat in self.metadata.chats
        ]

    def get_session_context_strategy(self) -> int:
        """
        Returns the current session's context strategy.

        Returns:
            int: The current session's context strategy.
        """
        return self.metadata.context_strategy

    def get_session_prompt_template(self) -> str:
        """
        Returns the name of the prompt template for the current session.

        Returns:
            str: The name of the prompt template for the current session.
        """
        return self.metadata.prompt_template


def get_all_sessions() -> list:
    """
    This method retrieves a list of available sessions.

    Returns:
        list: A list of available sessions. Each item in the list represents a session.
    """
    filepaths = [
        Path(fp).stem
        for fp in glob.iglob(f"{EnvironmentVars.SESSIONS}/*.json")
        if "__" not in fp
    ]
    return get_sessions(filepaths)


def get_all_session_names() -> list:
    """
    This method retrieves a list of available session names.

    Returns:
        list: A list of available session names.
    """
    return [item["session_id"] for item in get_all_sessions()]


def get_sessions(desired_sessions: list) -> list:
    """
    This method retrieves a list of desired sessions.

    Args:
        desired_sessions (list): A list of session names to retrieve more information on.

    Returns:
        list: A list of desired sessions, where each session is represented as a dictionary or an object.
    """
    sessions = []
    for session_name in desired_sessions:
        session_filename = slugify(session_name, lowercase=False)
        filepath = f"{EnvironmentVars.SESSIONS}/{session_filename}.json"

        with open(filepath, "r") as json_file:
            session_info = json.load(json_file)
            session_info["filename"] = Path(filepath).stem
            sessions.append(session_info)

    return sessions
