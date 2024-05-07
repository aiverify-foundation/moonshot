from operator import itemgetter

from moonshot.src.api.api_runner import api_get_all_runner, api_load_runner
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.session import Session
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage

# ------------------------------------------------------------------------------
# Session and Chat APIs
# ------------------------------------------------------------------------------


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


def api_create_session(
    runner_id: str, database_instance: DBInterface, endpoints: list, runner_args: dict
) -> dict | None:
    """
    Loads the session details for a specific runner.

    This function calls the `Session.load` method to retrieve the session details associated with the
    specified runner ID.

    Args:
        runner_id (str): The unique identifier of the runner for which the session details are to be loaded.

    Returns:
        dict | None: A dictionary containing the session details if available, otherwise None.
    """
    Session(
        runner_id,
        RunnerType.REDTEAM,
        {**runner_args},
        database_instance,
        endpoints,
        Storage.get_filepath(EnvVariables.RESULTS.name, runner_id, "json", True),
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


def api_get_available_session_info() -> tuple[list, list]:
    """
    Retrieves the IDs and database instances of runners with active sessions.

    This function retrieves the IDs and database instances of runners with active sessions by querying all runners
    and checking if each runner has an active session. It returns a tuple containing a list of runner IDs and a list
    of corresponding database instances for runners with active sessions.

    Returns:
        tuple[list[str], list[str]]: A tuple containing a list of runner IDs and a list of corresponding database
        instances for runners with active sessions.
    """
    runners_info = api_get_all_runner()
    runner_instances = [
        api_load_runner(str(runner_info.get("id"))) for runner_info in runners_info
    ]

    runner_ids = []
    runner_with_session_db_list = []

    for runner_instance in runner_instances:
        if runner_instance.database_instance:
            if Session.load(runner_instance.database_instance) is not None:
                runner_ids.append(runner_instance.id)
                runner_with_session_db_list.append(runner_instance.database_instance)
    return runner_ids, runner_with_session_db_list


def api_get_all_session_metadata() -> list:
    """
    Retrieves metadata for all sessions.

    This function retrieves the metadata for all active sessions by calling the `api_get_available_session_info` method
    and then loading the session details for each active session.

    Returns:
        list: A list containing the metadata for all active sessions.
    """
    _, runner_with_session_db_list = api_get_available_session_info()
    list_of_session_metadata = []
    for runner_with_session_db in runner_with_session_db_list:
        list_of_session_metadata.append(Session.load(runner_with_session_db))
    return sorted(
        list_of_session_metadata, key=itemgetter("created_datetime"), reverse=True
    )


def api_update_context_strategy(runner_id: str, context_strategy: str) -> None:
    """
    Updates the context strategy for a specific runner.

    This function updates the context strategy for a specific runner identified by the given runner_id. It calls the
    `Session.update_context_strategy` method with the runner's database instance,
    runner_id, and the new context_strategy.

    Args:
        runner_id (str): The ID of the runner for which the context strategy needs to be updated.
        context_strategy (str): The new context strategy to be set for the runner.

    Returns:
        None
    """
    Session.update_context_strategy(
        api_load_runner(runner_id).database_instance, runner_id, context_strategy
    )


def api_update_prompt_template(runner_id: str, prompt_template: str) -> None:
    """
    Updates the prompt template for a specific runner.

    This function updates the prompt template for a specific runner identified by the given runner_id. It calls the
    `Session.update_prompt_template` method with the runner's database instance,
    runner_id, and the new prompt_template.

    Args:
        runner_id (str): The ID of the runner for which the prompt template needs to be updated.
        prompt_template (str): The new prompt template to be set for the runner.

    Returns:
        None
    """
    Session.update_prompt_template(
        api_load_runner(runner_id).database_instance, runner_id, prompt_template
    )


def api_delete_session(runner_id: str) -> None:
    """
    Deletes the session for a specific runner.

    This function deletes the session for the runner identified by the given runner_id. It calls the
    `Session.delete_session` method with the runner's database instance.

    Args:
        runner_id (str): The ID of the runner for which the session needs to be deleted.

    Returns:
        None
    """
    Session.delete_session(api_load_runner(runner_id).database_instance)
