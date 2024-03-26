from typing import Callable, Union

from moonshot.src.benchmarking.executors.benchmark_executor import BenchmarkExecutor
from moonshot.src.benchmarking.executors.benchmark_executor_arguments import (
    BenchmarkExecutorArguments,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)


# ------------------------------------------------------------------------------
# Benchmark executor APIs
# ------------------------------------------------------------------------------
def api_create_recipe_executor(
    name: str,
    recipes: list[str],
    endpoints: list[str],
    num_of_prompts: int,
    progress_callback_func: Union[Callable, None] = None,
) -> BenchmarkExecutor:
    """
    Creates a new recipe executor.

    This function takes a name, a list of recipes, a list of endpoints, a number of prompts, and an optional progress
    callback function as input.
    It creates a new BenchmarkExecutor instance with these parameters and returns it.

    Args:
        name (str): The name of the new recipe executor.
        recipes (list[str]): A list of recipes for the new executor.
        endpoints (list[str]): A list of endpoints for the new executor.
        num_of_prompts (int): The number of prompts for the new executor.
        progress_callback_func (Union[Callable, None]): An optional progress callback function for the new executor.

    Returns:
        BenchmarkExecutor: The newly created recipe executor.
    """
    # Create a new recipe executor
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=BenchmarkExecutorTypes.RECIPE,
        recipes=recipes,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
        progress_callback_func=progress_callback_func,
    )
    return BenchmarkExecutor.create(be_args)


def api_create_cookbook_executor(
    name: str,
    cookbooks: list[str],
    endpoints: list[str],
    num_of_prompts: int,
    progress_callback_func: Union[Callable, None] = None,
) -> BenchmarkExecutor:
    """
    Creates a new cookbook executor.

    This function takes a name, a list of cookbooks, a list of endpoints, a number of prompts, and an optional progress
    callback function as input.
    It creates a new BenchmarkExecutor instance with these parameters and returns it.

    Args:
        name (str): The name of the new cookbook executor.
        cookbooks (list[str]): A list of cookbooks for the new executor.
        endpoints (list[str]): A list of endpoints for the new executor.
        num_of_prompts (int): The number of prompts for the new executor.
        progress_callback_func (Union[Callable, None]): An optional progress callback function for the new executor.

    Returns:
        BenchmarkExecutor: The newly created cookbook executor.
    """
    # Create a new cookbook executor
    # We do not need to provide the id.
    # This is because during creating:
    # 1. the id is slugify from the name and stored as id.
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=BenchmarkExecutorTypes.COOKBOOK,
        cookbooks=cookbooks,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
        progress_callback_func=progress_callback_func,
    )
    return BenchmarkExecutor.create(be_args)


def api_load_executor(
    be_id: str, progress_callback_func: Union[Callable, None] = None
) -> BenchmarkExecutor:
    """
    Loads an existing executor.

    This function takes an executor ID and an optional progress callback function as input.
    It checks if the executor's database file exists. If it does not, it raises an error.
    If the file does exist, it creates a connection to the database and reads the executor's
    information from the database. It then creates a new BenchmarkExecutor instance with the
    read information and the provided progress callback function, and returns this instance.

    Args:
        be_id (str): The ID of the executor to load.
        progress_callback_func (Union[Callable, None]): An optional progress callback function for the executor.

    Returns:
        BenchmarkExecutor: The loaded executor.

    Raises:
        RuntimeError: If the executor's database file does not exist.
        Exception: If there is an error during the loading process.
    """
    return BenchmarkExecutor.load(be_id, progress_callback_func)


def api_read_executor(be_id: str) -> dict:
    """
    Reads an executor and returns its information.

    This function takes an executor ID as input, reads the corresponding database file from the storage manager,
    and returns a dictionary containing the executor's information.

    Args:
        be_id (str): The ID of the executor.

    Returns:
        dict: A dictionary containing the executor's information.
    """
    return BenchmarkExecutor.read(be_id).to_dict()


def api_delete_executor(be_id: str) -> None:
    """
    This function takes an executor id as input and deletes the corresponding executor.

    Args:
        be_id (str): The id of the executor to be deleted.
    """
    BenchmarkExecutor.delete(be_id)


def api_get_all_executor() -> list[dict]:
    """
    This function retrieves all available executors and returns them as a list of dictionaries. Each dictionary
    represents an executor and contains its information.

    Returns:
        list[dict]: A list of dictionaries, each representing an executor.
    """
    _, executors = BenchmarkExecutor.get_available_items()
    return [executor.to_dict() for executor in executors]


def api_get_all_executor_name() -> list[str]:
    """
    This function retrieves all available executor names and returns them as a list.

    Returns:
        list[str]: A list of executor names.
    """
    executors_names, _ = BenchmarkExecutor.get_available_items()
    return executors_names
