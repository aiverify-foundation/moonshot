from moonshot.src.redteaming.session.session import Session
from moonshot.src.redteaming.session.session_manager import SessionManager


# ------------------------------------------------------------------------------
# Session and Chat APIs
# ------------------------------------------------------------------------------
def api_get_all_session_name() -> list[str]:
    """
    Retrieves and returns the names (IDs) of all sessions currently managed.

    This API endpoint wraps around the `SessionManager.get_all_session_names` method, providing an interface
    to fetch a list of all session names (or IDs). It's useful for clients needing to enumerate all sessions
    without requiring the details of each session.

    Returns:
        list[str]: A list of strings, each representing the unique name (ID) of a session.
    """
    return SessionManager.get_all_session_names()


def api_get_all_session_detail() -> list[dict]:
    """
    Retrieves and returns detailed metadata for all sessions currently managed.

    This API endpoint leverages the `SessionManager.get_all_session_details` method to obtain metadata for all sessions.
    It then converts each session's metadata into a dictionary format for easy consumption by clients. This method
    is particularly useful for clients that require comprehensive details about each session, including names,
    descriptions, endpoints, and other relevant metadata.

    Returns:
        list[dict]: A list of dictionaries, each representing the detailed metadata of a session.
    """

    return [
        session_metadata.to_dict()
        for session_metadata in SessionManager.get_all_session_details()
    ]


def api_get_session_chats_by_session_id(session_id: str) -> list[dict]:
    """
    Retrieves and returns the chat sessions associated with a specific session ID as a list of dictionaries.

    This API endpoint calls the `SessionManager.get_session_chats_by_session_id` method to fetch all chat sessions
    related to the specified session ID. Each chat session object is then converted to a dictionary for easy JSON
    serialization and client consumption. This is particularly useful for clients that need to display or process
    the details of chat sessions within a specific session.

    Args:
        session_id (str): The unique identifier for the session whose chat sessions are to be retrieved.

    Returns:
        list[dict]: A list of dictionaries, each representing a chat session associated with the specified session ID.
    """
    return [
        chat_object.to_dict()
        for chat_object in SessionManager.get_session_chats_by_session_id(session_id)
    ]


def api_create_session(
    name: str,
    description: str,
    endpoints: list[str],
    context_strategy: str = "",
    prompt_template: str = "",
) -> Session:
    """
    Creates a new session with the specified parameters and returns the session instance.
    This API endpoint facilitates the creation of a new session by wrapping around the `SessionManager.create_session`
    method. It allows clients to specify session details such as name, description, associated endpoints,
    context strategy, and prompt template. This method is particularly useful for initializing sessions with custom
    configurations for red teaming exercises or other operational scenarios.

    Args:
        name (str): The name of the new session.
        description (str): A brief description of the session.
        endpoints (list): A list of endpoints that the session will interact with.
        context_strategy (str, optional): The strategy for managing context within the session.
        prompt_template (str, optional): The template for generating prompts within the session.

    Returns:
        Session: The newly created session instance.
    """
    return SessionManager.create_session(
        name, description, endpoints, context_strategy, prompt_template
    )


def api_get_session(session_id: str) -> Session:
    """
    Retrieves and returns a session object based on the provided session ID.

    This API endpoint fetches a session object identified by the session ID and returns it to the caller.
    It is useful for obtaining detailed information about a specific session within the system.

    Args:
        session_id (str): The unique identifier of the session to retrieve.

    Returns:
        Session: The session object associated with the specified session ID.
    """
    return Session(session_id=session_id)


def api_delete_session(session_id: str) -> None:
    """
    Deletes a session based on the provided session ID.

    This API endpoint wraps around the `SessionManager.delete_session` method, offering a straightforward way to remove
    a session from the system using its unique identifier. It is particularly useful for cleaning up sessions that are
    no longer needed or for managing session lifecycles in a dynamic environment.

    Args:
        session_id (str): The unique identifier of the session to be deleted.

    Returns:
        None: This method does not return a value, but it will remove the specified session from the system.
    """
    SessionManager.delete_session(session_id)


async def api_send_prompt(session_id: str, user_prompt: str) -> None:
    """
    Sends a user-defined prompt to a specific session.

    This API endpoint allows for sending a prompt, defined by the user, to a session identified by the session ID.
    It leverages the `SessionManager.send_prompt` method to facilitate the interaction between the user and the session,
    enabling dynamic input and further customization of the session's behavior based on user input.

    Args:
        session_id (str): The unique identifier of the session to which the prompt is to be sent.
        user_prompt (str): The prompt text defined by the user to be sent to the session.

    Returns:
        None: This method does not return a value but triggers the sending of the user prompt to the specified session.
    """
    await SessionManager.send_prompt(session_id, user_prompt)


def api_update_context_strategy(session_id: str, context_strategy_name: str) -> None:
    """
    Updates the context strategy for a specific session.

    This API endpoint calls the `SessionManager.update_context_strategy` method to update the context strategy
    associated with the specified session ID. It allows clients to modify the context strategy for a session,
    enabling dynamic changes in how context is managed within the session.

    Args:
        session_id (str): The unique identifier of the session for which the context strategy is to be updated.
        context_strategy_name (str): The new context strategy name to be assigned to the session.

    Returns:
        None: This method does not return a value but updates the context strategy for the specified session.
    """
    SessionManager.update_context_strategy(session_id, context_strategy_name)


def api_update_prompt_template(session_id: str, prompt_template_name: str) -> None:
    """
    Updates the prompt template for a specific session.

    This API endpoint calls the `SessionManager.update_prompt_template` method to update the prompt template
    associated with the specified session ID. It allows clients to modify the prompt template for a session,
    enabling dynamic changes in the prompts generated within the session.

    Args:
        session_id (str): The unique identifier of the session for which the prompt template is to be updated.
        prompt_template_name (str): The new prompt template name to be assigned to the session.

    Returns:
        None: This method does not return a value but updates the prompt template for the specified session.
    """
    SessionManager.update_prompt_template(session_id, prompt_template_name)
