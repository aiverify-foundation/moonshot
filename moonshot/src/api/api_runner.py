from typing import Callable

from pydantic import validate_call

from moonshot.src.runners.runner import Runner
from moonshot.src.runners.runner_arguments import RunnerArguments


# ------------------------------------------------------------------------------
# Runner APIs
# ------------------------------------------------------------------------------
@validate_call
def api_create_runner(
    name: str,
    endpoints: list[str],
    description: str = "",
    progress_callback_func: Callable | None = None,
) -> Runner:
    """
    Creates a new runner.

    This function takes the name, endpoints, and an optional progress callback function to create a new Runner instance.
    The ID of the runner is generated from the name of the runner using the slugify function,
    so it does not need to be provided.

    Args:
        name (str): The name of the runner.
        endpoints (list[str]): A list of endpoint identifiers for the runner.
        description (str, optional): A brief description of the runner. Defaults to an empty string.
        progress_callback_func (Callable | None, optional): An optional callback function for progress updates.
        Defaults to None.

    Returns:
        Runner: A new Runner object.
    """
    # Create a new recipe runner
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    # Validate arguments
    if not name.strip():
        raise ValueError("Runner name must not be empty.")

    if not endpoints or not isinstance(endpoints, list) \
            or not all([e.strip() for e in endpoints]):
        raise ValueError("Endpoints must be a non-empty list of strings.")

    runner_args = RunnerArguments(
        id="",
        name=name,
        endpoints=endpoints,
        description=description,
        progress_callback_func=progress_callback_func,
    )
    return Runner.create(runner_args)


@validate_call
def api_load_runner(
    runner_id: str, progress_callback_func: Callable | None = None
) -> Runner:
    """
    Loads a runner based on the provided runner ID.

    This function retrieves the runner using the provided runner ID and then loads it.
    It utilizes the Runner's load method to fetch and return the runner.

    Args:
        runner_id (str): The ID of the runner to be loaded.
        progress_callback_func (Callable | None, optional): An optional progress callback function for the runner.
        Defaults to None.

    Returns:
        Runner: An initialized Runner object.
    """
    return Runner.load(runner_id, progress_callback_func)


@validate_call
def api_read_runner(runner_id: str) -> dict:
    """
    Reads a runner and returns its information.

    This function takes a runner ID as input, reads the corresponding runner,
    and returns a dictionary containing the runner's information.

    Args:
        runner_id (str): The ID of the runner.

    Returns:
        dict: A dictionary containing the runner's information.
    """
    return Runner.read(runner_id).to_dict()


@validate_call
def api_delete_runner(runner_id: str) -> bool:
    """
    Deletes a runner by its identifier.

    This function takes a runner ID as input and calls the delete method from the Runner class
    to remove the specified runner from storage.

    Args:
        runner_id (str): The unique identifier of the runner to be deleted.

    Returns:
        bool: True if the runner was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return Runner.delete(runner_id)


def api_get_all_runner() -> list[dict]:
    """
    Retrieves all available runners.

    This function calls the get_available_items method from the Runner class to retrieve all available runners.
    It then converts each runner into a dictionary using the to_dict method and returns a list of these dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing a runner.
    """
    _, runners = Runner.get_available_items()
    return [runner.to_dict() for runner in runners]


def api_get_all_runner_name() -> list[str]:
    """
    Retrieves all available runner names.

    This function calls the get_available_items method from the Runner class to retrieve all available runners.
    It then extracts the names of each runner and returns a list of these names.

    Returns:
        list[str]: A list of runner names.
    """
    runners_names, _ = Runner.get_available_items()
    return runners_names
