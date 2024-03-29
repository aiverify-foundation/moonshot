from typing import Callable

from moonshot.src.runners.runner import Runner
from moonshot.src.runners.runner_arguments import RunnerArguments
from moonshot.src.runners.runner_type import RunnerType


# ------------------------------------------------------------------------------
# Runner APIs
# ------------------------------------------------------------------------------
def api_create_recipe_runner(
    name: str,
    recipes: list[str],
    endpoints: list[str],
    num_of_prompts: int,
    progress_callback_func: Callable | None = None,
) -> Runner:
    """
    Creates a new recipe runner.

    This function takes a variety of parameters, including the name, recipes, endpoints,
    number of prompts, and a progress callback function. It then creates a new RunnerArguments
    object with these parameters, and calls the Runner.create method to create a new recipe runner.

    Note: The id of the runner is generated from the name of the runner using the slugify function,
    so it does not need to be provided.

    Args:
        name (str): The name of the runner.
        recipes (list[str]): The recipes to be used by the runner.
        endpoints (list[str]): The endpoints to be used by the runner.
        num_of_prompts (int): The number of prompts to be used by the runner.
        progress_callback_func (Callable | None): The progress callback function to be used by the runner.

    Returns:
        Runner: A new Runner object.
    """
    # Create a new recipe runner
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    runner_args = RunnerArguments(
        id="",
        name=name,
        run_type=RunnerType.RECIPE,
        recipes=recipes,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
        progress_callback_func=progress_callback_func,
    )
    return Runner.create(runner_args)


def api_create_cookbook_runner(
    name: str,
    cookbooks: list[str],
    endpoints: list[str],
    num_of_prompts: int,
    progress_callback_func: Callable | None = None,
) -> Runner:
    """
    Creates a new cookbook runner.

    This function takes a variety of parameters, including the name, cookbooks, endpoints,
    number of prompts, and a progress callback function. It then creates a new RunnerArguments
    object with these parameters, and calls the Runner.create method to create a new cookbook runner.

    Note: The id of the runner is generated from the name of the runner using the slugify function,
    so it does not need to be provided.

    Args:
        name (str): The name of the runner.
        cookbooks (list[str]): The cookbooks to be used by the runner.
        endpoints (list[str]): The endpoints to be used by the runner.
        num_of_prompts (int): The number of prompts to be used by the runner.
        progress_callback_func (Callable | None): The progress callback function to be used by the runner.

    Returns:
        Runner: A new Runner object.
    """
    # Create a new cookbook runner
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    runner_args = RunnerArguments(
        id="",
        name=name,
        run_type=RunnerType.COOKBOOK,
        cookbooks=cookbooks,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
        progress_callback_func=progress_callback_func,
    )
    return Runner.create(runner_args)


def api_load_runner(
    runner_id: str, progress_callback_func: Callable | None = None
) -> Runner:
    """
    Loads a runner based on the provided runner ID.

    This function retrieves the runner using the provided runner ID and then loads it.
    It utilizes the Runner's load method to fetch and return the runner.

    Args:
        runner_id (str): The ID of the runner to be loaded.
        progress_callback_func (Callable | None): The progress callback function to be used by the runner.

    Returns:
        Runner: An initialized Runner object.
    """
    return Runner.load(runner_id, progress_callback_func)


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


def api_delete_runner(runner_id: str) -> None:
    """
    Deletes a runner based on the provided runner ID.

    This function takes a runner ID as input and deletes the corresponding runner.

    Args:
        runner_id (str): The ID of the runner to be deleted.

    Returns:
        None
    """
    Runner.delete(runner_id)


def api_get_all_runner() -> list[dict]:
    """
    Retrieves all available runners.

    This function calls the get_available_items method to retrieve all available runners. It then converts each
    runner into a dictionary using the to_dict method and returns a list of these dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing a runner.
    """
    _, runners = Runner.get_available_items()
    return [runner.to_dict() for runner in runners]


def api_get_all_runner_name() -> list[str]:
    """
    Retrieves all available runner names.

    This function calls the get_available_items method to retrieve all available runners. It then extracts the names of
    each runner and returns a list of these names.

    Returns:
        list[str]: A list of runner names.
    """
    runners_names, _ = Runner.get_available_items()
    return runners_names
