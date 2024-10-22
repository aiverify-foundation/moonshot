from operator import itemgetter
from typing import Any

from pydantic import validate_call

from moonshot.src.api.api_runner import api_get_all_runner, api_load_runner
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.session import Session
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage


# ------------------------------------------------------------------------------
# Session and Chat APIs
# ------------------------------------------------------------------------------
@validate_call
def api_load_session(runner_id: str) -> dict | None:
    """
    Loads the session details for a specific runner.

    This function calls the `Session.load` method to retrieve the session details associated with the
    specified runner ID.

    Args:
        runner_id (str): The unique identifier of the runner for which the session details are to be loaded.

    Returns:
        dict | None: A dictionary containing the session details if available, otherwise None.
    """
    return Session.load(api_load_runner(runner_id).database_instance)


@validate_call
def api_create_session(
    runner_id: str, database_instance: Any, endpoints: list[str], runner_args: dict
) -> Session:
    """
    Creates a new session for a specific runner.

    This function creates a new session by calling the `Session` constructor with the provided arguments.

    Args:
        runner_id (str): The unique identifier of the runner for which the session is to be created.
        database_instance (Any): The database instance to be used for the session.
        endpoints (list[str]): A list of endpoints for the session.
        runner_args (dict): A dictionary of arguments for the runner.

    Returns:
        Session: A new Session object.

    Raises:
        RuntimeError: If the runner_id is empty or if the database_instance is not provided.
    """
    if isinstance(database_instance, DBInterface):
        if runner_id:
            session_instance = Session(
                runner_id,
                RunnerType.REDTEAM,
                {**runner_args},
                database_instance,
                endpoints,
                Storage.get_filepath(
                    EnvVariables.RESULTS.name, runner_id, "json", True
                ),
            )
            return session_instance
        else:
            raise RuntimeError(
                "[Session] Failed to initialise Session. String should have at least 1 character."
            )
    else:
        raise RuntimeError(
            "[Session] Failed to initialise Session. No database instance provided."
        )


def api_get_all_session_names() -> list[str]:
    """
    Retrieves a list of all session names.

    This function calls the `api_get_available_session_info` method to obtain the available session information
    and returns a list of session names.

    Returns:
        list[str]: A list of strings, each denoting a session name.
    """
    session_names, _ = api_get_available_session_info()
    return session_names


def api_get_available_session_info() -> tuple[list[str], list[dict]]:
    """
    Retrieves the IDs and metadata of runners with active sessions.

    This function retrieves the IDs and metadata of runners with active sessions by querying all runners
    and checking if each runner has an active session. It returns a tuple containing a list of runner IDs and a list
    of corresponding session metadata for runners with active sessions.

    Returns:
        tuple[list[str], list[dict]]: A tuple containing a list of runner IDs and a list of corresponding session
        metadata for runners with active sessions.
    """
    runners_info = api_get_all_runner()
    runner_instances = [
        api_load_runner(str(runner_info.get("id"))) for runner_info in runners_info
    ]

    runner_ids = []
    session_metadata_list = []

    for runner_instance in runner_instances:
        if runner_instance.database_instance:
            session_metadata = Session.load(runner_instance.database_instance)
            if session_metadata is not None:
                runner_ids.append(runner_instance.id)
                session_metadata_list.append(session_metadata)
    return runner_ids, session_metadata_list


def api_get_all_session_metadata() -> list[dict]:
    """
    Retrieves metadata for all sessions.

    This function retrieves the metadata for all active sessions by calling the `api_get_available_session_info` method.

    Returns:
        list[dict]: A list containing the metadata for all active sessions, sorted by created datetime in
                    descending order.
    """
    _, session_metadata_list = api_get_available_session_info()
    return sorted(
        session_metadata_list, key=itemgetter("created_datetime"), reverse=True
    )


@validate_call
def api_update_context_strategy(runner_id: str, context_strategy: str) -> bool:
    """
    Updates the context strategy for a specific runner.

    This function updates the context strategy for a specific runner identified by the given runner_id. It calls the
    `Session.update_context_strategy` method with the runner's database instance,
    runner_id, and the new context_strategy.

    Args:
        runner_id (str): The ID of the runner for which the context strategy needs to be updated.
        context_strategy (str): The new context strategy to be set for the runner.

    Returns:
        bool: The status on whether the context strategy is updated successfully.
    """
    return Session.update_context_strategy(
        api_load_runner(runner_id).database_instance, runner_id, context_strategy
    )


@validate_call
def api_update_cs_num_of_prev_prompts(runner_id: str, num_of_prev_prompts: int) -> bool:
    """
    Updates the number of previous prompts used in a context strategy for a specific runner.

    This function updates the number of previous prompts used in a context strategy for a specific runner identified by
    the given runner_id. It calls the `Session.update_cs_num_of_prev_prompts` method with the runner's database
    instance, runner_id, and the new num_of_prev_prompts.

    Args:
        runner_id (str): The ID of the runner for which the number of previous prompts needs to be updated.
        num_of_prev_prompts (int): The new number of previous prompts to be set for the runner.

    Returns:
        bool: The status on whether the number of prompts for context strategy is updated successfully.
    """
    return Session.update_cs_num_of_prev_prompts(
        api_load_runner(runner_id).database_instance, runner_id, num_of_prev_prompts
    )


@validate_call
def api_update_prompt_template(runner_id: str, prompt_template: str) -> bool:
    """
    Updates the prompt template for a specific runner.

    This function updates the prompt template for a specific runner identified by the given runner_id. It calls the
    `Session.update_prompt_template` method with the runner's database instance,
    runner_id, and the new prompt_template.

    Args:
        runner_id (str): The ID of the runner for which the prompt template needs to be updated.
        prompt_template (str): The new prompt template to be set for the runner.

    Returns:
        bool: The status on whether the prompt template is updated successfully.
    """
    return Session.update_prompt_template(
        api_load_runner(runner_id).database_instance, runner_id, prompt_template
    )


@validate_call
def api_update_metric(runner_id: str, metric_id: str) -> bool:
    """
    Updates the metric for a specific runner.

    This function updates the metric for a specific runner identified by the given runner_id. It calls the
    `Session.update_metric` method with the runner's database instance,
    runner_id, and the new metric_id.

    Args:
        runner_id (str): The ID of the runner for which the metric needs to be updated.
        metric_id (str): The new metric to be set for the runner.

    Returns:
        bool: The status on whether the metric is updated successfully.
    """
    return Session.update_metric(
        api_load_runner(runner_id).database_instance, runner_id, metric_id
    )


@validate_call
def api_update_system_prompt(runner_id: str, system_prompt: str) -> bool:
    """
    Updates the system prompt for a specific runner.

    This function updates the system prompt for a specific runner identified by the given runner_id. It calls the
    `Session.update_system_prompt` method with the runner's database instance,
    runner_id, and the new system_prompt.

    Args:
        runner_id (str): The ID of the runner for which the system prompt needs to be updated.
        system_prompt (str): The new system prompt to be set for the runner.

    Returns:
        bool: The status on whether the system prompt is updated successfully.
    """
    return Session.update_system_prompt(
        api_load_runner(runner_id).database_instance, runner_id, system_prompt
    )


@validate_call
def api_update_attack_module(runner_id: str, attack_module_id: str) -> bool:
    """
    Updates the attack module for a specific runner.

    This function updates the attack module for a specific runner identified by the given runner_id. It calls the
    `Session.update_attack_module` method with the runner's database instance,
    runner_id, and the new attack_module_id.

    Args:
        runner_id (str): The ID of the runner for which the attack module needs to be updated.
        attack_module_id (str): The new attack module to be set for the runner.

    Returns:
        bool: The status on whether the attack module is updated successfully.
    """
    return Session.update_attack_module(
        api_load_runner(runner_id).database_instance, runner_id, attack_module_id
    )


@validate_call
def api_delete_session(runner_id: str) -> bool:
    """
    Deletes the session for a specific runner.

    This function deletes the session for the runner identified by the given runner_id. It calls the
    `Session.delete` method with the runner's database instance.

    Args:
        runner_id (str): The ID of the runner for which the session needs to be deleted.

    Returns:
        bool: The status on whether the session is deleted successfully.
    """
    return Session.delete(api_load_runner(runner_id).database_instance)


@validate_call
def api_get_all_chats_from_session(runner_id: str) -> dict | None:
    """
    Retrieves all chat messages from a specific session.

    This function retrieves all chat messages from the session associated with the specified runner ID.
    It calls the `Session.get_session_chats` method with the runner's database instance.

    Args:
        runner_id (str): The unique identifier of the runner for which the chat messages are to be retrieved.

    Returns:
        dict | None: A dictionary containing all chat messages if available, otherwise None.
    """
    return Session.get_session_chats(api_load_runner(runner_id).database_instance)
