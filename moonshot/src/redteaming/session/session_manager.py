import glob
from pathlib import Path

from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.redteaming.session.chat import Chat
from moonshot.src.redteaming.session.session import Session, SessionMetadata


class SessionManager:
    def __init__(self):
        pass

    @staticmethod
    def create_session(
        name: str,
        description: str,
        endpoints: list[str],
        context_strategy: str = "",
        prompt_template: str = "",
    ) -> Session:
        """
        Creates and returns a new Session instance with the specified parameters.

        This method initializes a new Session object using the provided name, description, endpoints, context strategy,
        and prompt template. It is a factory method that simplifies the creation of Session objects by encapsulating
        the instantiation logic and allowing for default values for context strategy and prompt template.

        Args:
            name (str): The name of the session.
            description (str): A brief description of the session.
            endpoints (list): A list of endpoints associated with the session.
            context_strategy (str, optional): The strategy for context management within the session.
            prompt_template (str, optional): The template for prompts to be used in the session.

        Returns:
            Session
        """
        return Session(
            name, description, endpoints, "", prompt_template, context_strategy
        )

    @staticmethod
    def get_session_chats_by_session_id(session_id: str) -> list[Chat]:
        """
        Retrieves and returns all chat sessions associated with a specific session ID.

        This method acts as a proxy to the `Session.get_session_chats_by_session_id` method, facilitating the retrieval
        of all chat sessions linked to the given session ID. It is designed to abstract the process of fetching chat
        session details, making it accessible through the SessionManager.

        Args:
            session_id (str): The unique identifier for the session whose chat sessions are to be retrieved.

        Returns:
            list: A list of Chat instances, each representing a chat session associated with the specified session ID.
        """
        return Session.get_session_chats_by_session_id(session_id)

    @staticmethod
    def get_all_session_details() -> list[SessionMetadata]:
        """
        Retrieves and returns the metadata for all sessions.

        This method compiles a list of all session names (IDs) by invoking `SessionManager.get_all_session_names()`
        and then fetches the metadata for each session by calling `Session.get_session_metadata_by_id`
        for each session name. It effectively aggregates the metadata for all sessions, providing
        a comprehensive overview of all sessions managed by the SessionManager.

        Returns:
            list: A list of SessionMetadata instances, each containing the metadata for a specific session.
        """
        return [
            Session.get_session_metadata_by_id(session_name)
            for session_name in SessionManager.get_all_session_names()
        ]

    @staticmethod
    def get_all_session_names() -> list[str]:
        """
        Retrieves the names of all session files stored in the predefined session database directory.
        This method searches for all `.db` files within the session path, excluding any files that contain
        double underscores in their names. It returns a list of the file names
        (without the `.db` extension) of the found session files.

        Returns:
            list: A list of strings, each representing the name of a session
            file found in the session database directory.
        """
        session_file_path = f"{EnvironmentVars.SESSIONS}"
        filepaths = [
            Path(fp).stem
            for fp in glob.iglob(f"{session_file_path}/*.db")
            if "__" not in fp
        ]
        return filepaths

    @staticmethod
    def delete_session(session_id: str) -> None:
        """
        Deletes a session and its associated data based on the session ID.

        This method delegates the task of deleting a session, including all its related chats and metadata, to the
        `Session.delete_session` method. It provides a straightforward way to remove a session from the system using
        its unique identifier.

        Args:
            session_id (str): The unique identifier for the session to be deleted.

        Returns:
            None: This method does not return a value.
        """
        Session.delete_session(session_id)

    @staticmethod
    async def send_prompt(session_id: str, user_prompt: str) -> None:
        await Session.send_prompt(session_id, user_prompt)

    @staticmethod
    def update_prompt_template(session_id: str, prompt_template_name: str) -> None:
        """
        Updates the prompt template for a specific session.

        This method delegates the task of updating the prompt template for a session to the
        `Session.update_prompt_template` method. It allows for modifying the prompt template
        associated with the specified session ID using the provided prompt template tuple.

        Args:
            session_id (str): The unique identifier of the session for which the prompt template is to be updated.
            prompt_template (str): The new prompt template tuple to be assigned to the session.

        Returns:
            None: This method does not return a value but updates the prompt template for the specified session.
        """
        Session.update_prompt_template(session_id, prompt_template_name)

    @staticmethod
    def update_context_strategy(session_id: str, context_strategy_name: str) -> None:
        """
        Updates the context strategy for a specific session.

        This method delegates the task of updating the context strategy for a session to the
        `Session.update_context_strategy` method. It allows for modifying the context strategy
        associated with the specified session ID using the provided context strategy name.

        Args:
            session_id (str): The unique identifier of the session for which the context strategy is to be updated.
            context_strategy_name (str): The new context strategy name to be assigned to the session.

        Returns:
            None: This method does not return a value but updates the context strategy for the specified session.
        """
        Session.update_context_strategy(session_id, context_strategy_name)
