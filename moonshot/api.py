from typing import Callable, Union

from moonshot.src.benchmarking.cookbooks.cookbook import Cookbook
from moonshot.src.benchmarking.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.benchmarking.executors.benchmark_executor import BenchmarkExecutor
from moonshot.src.benchmarking.executors.benchmark_executor_arguments import (
    BenchmarkExecutorArguments,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)
from moonshot.src.benchmarking.metrics.metric import Metric
from moonshot.src.benchmarking.recipes.recipe import Recipe
from moonshot.src.benchmarking.recipes.recipe_arguments import RecipeArguments
from moonshot.src.benchmarking.results.result import Result
from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.connectors.connector_manager import ConnectorManager
from moonshot.src.prompt_template.prompt_template_manager import PromptTemplateManager
from moonshot.src.redteaming.context_strategy.context_strategy_manager import (
    ContextStrategyManager,
)
from moonshot.src.redteaming.session.session import Session
from moonshot.src.redteaming.session.session_manager import SessionManager


# ------------------------------------------------------------------------------
# Environment Variables APIs
# ------------------------------------------------------------------------------
def api_set_environment_variables(env_vars: dict) -> None:
    """
    Sets the environment variables for the current session.

    Args:
        env_vars (dict): A dictionary containing the environment variables to set.

    Returns:
        None
    """
    EnvironmentVars.load_env(env_vars)


# ------------------------------------------------------------------------------
# Connector APIs
# ------------------------------------------------------------------------------
def api_create_endpoint(
    name: str,
    connector_type: str,
    uri: str,
    token: str,
    max_calls_per_second: int,
    max_concurrency: int,
    params: dict,
) -> None:
    """
    Creates a new endpoint to the connector manager.

    This function creates a new connector endpoint with the specified parameters. It constructs a
    ConnectorEndpointArguments object with the provided details and then calls the ConnectorManager's create_endpoint
    method to add the new endpoint.

    Args:
        name (str): The name of the new endpoint.
        connector_type (str): The type of the connector (e.g., 'GPT-3', 'Bert', etc.).
        uri (str): The URI for the connector's API.
        token (str): The access token for the API.
        max_calls_per_second (int): The maximum number of API calls allowed per second.
        max_concurrency (int): The maximum number of concurrent API calls.
        params (dict): Additional parameters for the connector.

    Returns:
        None
    """
    # Create a new connector endpoint arguments instance.
    # We do not need to provide id and created_date.
    # This is because during creation:
    #   1. the id is slugify from the name and stored as id.
    #   2. the created_date is based on the os file created date and time.
    connector_endpoint_args = ConnectorEndpointArguments(
        id="",
        name=name,
        connector_type=connector_type,
        uri=uri,
        token=token,
        max_calls_per_second=max_calls_per_second,
        max_concurrency=max_concurrency,
        params=params,
        created_date="",
    )
    ConnectorManager.create_endpoint(connector_endpoint_args)


def api_read_endpoint(ep_id: str) -> dict:
    """
    Reads an endpoint from the connector manager.

    This function reads an endpoint from the connector manager using the provided endpoint ID.

    Args:
        ep_id (str): The ID of the endpoint to read.

    Returns:
        dict: A dictionary containing the endpoint information.
    """
    return ConnectorManager.read_endpoint(ep_id).to_dict()


def api_update_endpoint(ep_id: str, **kwargs) -> None:
    """
    Updates an existing endpoint in the connector manager.

    This function updates an existing endpoint in the connector manager using the provided endpoint details.
    It first creates a ConnectorEndpointArguments instance with the provided details, then calls the
    ConnectorManager's update_endpoint method to update the endpoint.

    Args:
        kwargs: A dictionary of arguments for the endpoint. Possible keys are:
            name (str): The name of the endpoint.
            connector_type (str): The type of the connector.
            uri (str): The URI for the connector.
            token (str): The token for the connector.
            max_calls_per_second (int): The maximum number of API calls allowed per second.
            max_concurrency (int): The maximum number of concurrent API calls.
            params (dict): Additional parameters for the connector.

    Returns:
        None
    """
    # Check if the endpoint exists
    try:
        existing_endpoint = ConnectorManager.read_endpoint(ep_id)
    except Exception:
        raise RuntimeError(f"Endpoint with ID '{ep_id}' does not exist")

    # Update the fields of the existing endpoint with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_endpoint, key):
            setattr(existing_endpoint, key, value)

    # Update the endpoint
    ConnectorManager.update_endpoint(existing_endpoint)


def api_delete_endpoint(ep_id: str) -> None:
    """
    Deletes an existing endpoint in the connector manager.

    This function deletes an existing endpoint in the connector manager using the provided endpoint ID.
    It calls the ConnectorManager's delete_endpoint method to delete the endpoint.

    Args:
        ep_id (str): The ID of the endpoint to be deleted.

    Returns:
        None
    """
    ConnectorManager.delete_endpoint(ep_id)


def api_get_all_endpoint() -> list[dict]:
    """
    Retrieves a list of all available endpoints.

    This function calls the ConnectorManager's get_available_endpoints method to retrieve a list of all available
    endpoints and their details. It then converts each ConnectorEndpointArguments object into a dictionary for easier
    consumption by the caller.

    Returns:
        list[dict]: A list of dictionaries, each representing an endpoint's details.
    """
    _, endpoints = ConnectorManager.get_available_endpoints()
    return [endpoint.to_dict() for endpoint in endpoints]


def api_get_all_endpoint_name() -> list[str]:
    """
    Retrieves a list of all endpoint names.

    This function calls the ConnectorManager's get_available_endpoints method to retrieve a list of all available
    endpoint names. It extracts the names from the tuple returned by get_available_endpoints, which contains a list
    of endpoint names and a list of ConnectorEndpointArguments objects.

    Returns:
        list[str]: A list of endpoint names.
    """
    endpoints_names, _ = ConnectorManager.get_available_endpoints()
    return endpoints_names


def api_create_connector(ep_id: str) -> Connector:
    """
    Creates a connector based on the provided endpoint ID.

    This function retrieves the endpoint arguments using the provided endpoint ID and then creates a connector
    based on those arguments. It utilizes the ConnectorManager's read_endpoint method to fetch the endpoint
    arguments and then calls the create_connector method to initialize and return the connector.

    Args:
        ep_id (str): The ID of the endpoint for which to create a connector.

    Returns:
        Connector: An initialized Connector object.
    """
    return ConnectorManager.create_connector(ConnectorManager.read_endpoint(ep_id))


def api_create_connectors(ep_ids: list[str]) -> list[Connector]:
    """
    Creates connectors for multiple endpoints based on their IDs.

    This function takes a list of endpoint IDs, retrieves the corresponding endpoint arguments for each ID, and then
    creates and returns a list of connector objects based on those arguments. It utilizes the ConnectorManager's
    read_endpoint method to fetch the endpoint arguments and the create_connector method to initialize the connectors.

    Args:
        ep_ids (list[str]): A list of endpoint IDs for which connectors are to be created.

    Returns:
        list[Connector]: A list of initialized Connector objects.
    """
    return [
        ConnectorManager.create_connector(ConnectorManager.read_endpoint(ep_id))
        for ep_id in ep_ids
    ]


def api_get_all_connector_type() -> list[str]:
    """
    Retrieves a list of all available connector types.

    This function calls the ConnectorManager's get_available_connector_types method to retrieve a list of all available
    connector types. It returns the list of connector types.

    Returns:
        list[str]: A list of connector types.
    """
    return ConnectorManager.get_available_connector_types()


# ------------------------------------------------------------------------------
# Cookbook APIs
# ------------------------------------------------------------------------------
def api_create_cookbook(name: str, description: str, recipes: list[str]) -> None:
    """
    Creates a new cookbook.

    This function takes the name, description, and recipes for a new cookbook as input. It then creates a new
    CookbookArguments object with these details and an empty id. The id is left empty because it will be generated
    from the name during the creation process. The function then calls the Cookbook's create_cookbook method to
    create the new cookbook.

    Args:
        name (str): The name of the new cookbook.
        description (str): A brief description of the new cookbook.
        recipes (list[str]): A list of recipes to be included in the new cookbook.
    """
    # Create a new cookbook
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    cb_args = CookbookArguments(
        id="",
        name=name,
        description=description,
        recipes=recipes,
    )
    Cookbook.create_cookbook(cb_args)


def api_read_cookbook(cb_id: str) -> dict:
    """
    Retrieves a cookbook based on the provided cookbook ID.

    This function reads a cookbook using the `read_cookbook` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.

    Args:
        cb_id (str): A cookbook ID.

    Returns:
        dict: A dictionary representing a cookbook.
    """
    return Cookbook.read_cookbook(cb_id).to_dict()


def api_read_cookbooks(cb_ids: list[str]) -> list[dict]:
    """
    Retrieves a list of cookbooks based on the provided list of cookbook IDs.

    This function iterates over the list of cookbook IDs, reads each cookbook using the `read_cookbook` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.
    It returns a list of these dictionaries.

    Args:
        cb_ids (list[str]): A list of cookbook IDs.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookbook.
    """
    return [Cookbook.read_cookbook(cb_id).to_dict() for cb_id in cb_ids]


def api_update_cookbook(cb_id: str, **kwargs) -> None:
    """
    Updates an existing cookbook in the cookbook manager.

    This function updates an existing cookbook in the cookbook manager using the provided cookbook details.
    It first checks if the cookbook exists, then updates the fields of the existing cookbook with the provided kwargs,
    and finally calls the Cookbook's update_cookbook method to update the cookbook.

    Args:
        cb_id (str): The ID of the cookbook to update.
        kwargs: A dictionary of arguments for the cookbook. Possible keys are:
            name (str): The name of the cookbook.
            description (str): The description of the cookbook.
            recipes (list[str]): The list of recipes in the cookbook.

    Raises:
        RuntimeError: If the cookbook with the provided ID does not exist.

    Returns:
        None
    """
    # Check if the cookbook exists
    try:
        existing_cookbook = Cookbook.read_cookbook(cb_id)
    except Exception:
        raise RuntimeError(f"Cookbook with ID '{cb_id}' does not exist")

    # Update the fields of the existing cookbook with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_cookbook, key):
            setattr(existing_cookbook, key, value)

    # Update the cookbook
    Cookbook.update_cookbook(existing_cookbook)


def api_delete_cookbook(cb_id: str) -> None:
    """
    Deletes a cookbook.

    This function calls the `delete_cookbook` method of the `Cookbook` class, which deletes the cookbook
    corresponding to the provided ID.

    Args:
        cb_id (str): The ID of the cookbook to delete.
    """
    Cookbook.delete_cookbook(cb_id)


def api_get_all_cookbook() -> list[dict]:
    """
    Retrieves all available cookbooks.

    This function calls the `get_available_cookbooks` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns a list
    of dictionaries, each representing a cookbook.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookbook.
    """
    _, cookbooks = Cookbook.get_available_cookbooks()
    return [cookbook.to_dict() for cookbook in cookbooks]


def api_get_all_cookbook_name() -> list[str]:
    """
    Retrieves the names of all available cookbooks.

    This function calls the `get_available_cookbooks` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns the
    list of cookbook IDs, which are the names of the cookbooks.

    Returns:
        list[str]: A list of cookbook names.
    """
    cookbooks_names, _ = Cookbook.get_available_cookbooks()
    return cookbooks_names


# ------------------------------------------------------------------------------
# Recipe APIs
# ------------------------------------------------------------------------------
def api_create_recipe(
    name: str,
    description: str,
    tags: list[str],
    datasets: list[str],
    prompt_templates: list[str],
    metrics: list[str],
) -> None:
    """
    Creates a new recipe.

    This function takes a name, description, tags, datasets, prompt templates, and metrics as input, and creates a
    new recipe. It constructs a RecipeArguments object with the provided details and then calls the Recipe's
    create_recipe method to add the new recipe.

    Args:
        name (str): The name of the new recipe.
        description (str): The description of the recipe.
        tags (list[str]): The tags associated with the recipe.
        datasets (list[str]): The datasets used in the recipe.
        prompt_templates (list[str]): The prompt templates used in the recipe.
        metrics (list[str]): The metrics used in the recipe.

    Returns:
        None
    """
    # Create a new recipe
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    rec_args = RecipeArguments(
        id="",
        name=name,
        description=description,
        tags=tags,
        datasets=datasets,
        prompt_templates=prompt_templates,
        metrics=metrics,
    )
    Recipe.create_recipe(rec_args)


def api_read_recipe(rec_id: str) -> dict:
    """
    Reads a recipe and returns its information.

    This function takes a recipe ID as input, reads the corresponding recipe,
    and returns a dictionary containing the recipe's information.

    Args:
        rec_id (str): The ID of the recipe.

    Returns:
        dict: A dictionary containing the recipe's information.
    """
    return Recipe.read_recipe(rec_id).to_dict()


def api_read_recipes(rec_ids: list[str]) -> list[dict]:
    """
    Reads multiple recipes and returns their information.

    This function takes a list of recipe IDs as input, reads the corresponding recipes,
    and returns a list of dictionaries containing each recipe's information.

    Args:
        rec_ids (list[str]): The IDs of the recipes.

    Returns:
        list[dict]: A list of dictionaries, each containing a recipe's information.
    """
    # This function uses list comprehension to iterate over the list of recipe IDs,
    # calling the read_recipe method for each ID and converting the result to a dictionary.
    # The resulting list of dictionaries is then returned.
    return [Recipe.read_recipe(rec_id).to_dict() for rec_id in rec_ids]


def api_update_recipe(rec_id: str, **kwargs) -> None:
    """
    Updates an existing recipe in the recipe manager.

    This function updates an existing recipe in the recipe manager using the provided recipe details.
    It first checks if the recipe exists, then updates the fields of the existing recipe with the provided kwargs,
    and finally calls the Recipe's update_recipe method to update the recipe.

    Args:
        rec_id (str): The ID of the recipe to update.
        kwargs: A dictionary of arguments for the recipe. Possible keys are:
            name (str): The name of the recipe.
            description (str): The description of the recipe.
            tags (list[str]): The tags associated with the recipe.
            datasets (list[str]): The datasets used in the recipe.
            prompt_templates (list[str]): The prompt templates used in the recipe.
            metrics (list[str]): The metrics used in the recipe.

    Raises:
        RuntimeError: If the recipe with the provided ID does not exist.

    Returns:
        None
    """
    # Check if the recipe exists
    try:
        existing_recipe = Recipe.read_recipe(rec_id)
    except Exception:
        raise RuntimeError(f"Recipe with ID '{rec_id}' does not exist")

    # Update the fields of the existing recipe with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_recipe, key):
            setattr(existing_recipe, key, value)

    # Update the endpoint
    Recipe.update_recipe(existing_recipe)


def api_delete_recipe(rec_id: str) -> None:
    """
    Deletes a recipe.

    This method takes a recipe ID as input, deletes the corresponding JSON file from the directory specified by
    `EnvironmentVars.RECIPES`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        rec_id (str): The ID of the recipe to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    Recipe.delete_recipe(rec_id)


def api_get_all_recipe() -> list[dict]:
    """
    Retrieves all available recipes.

    This function calls the get_available_recipes method to retrieve all available recipes. It then converts each
    recipe into a dictionary using the to_dict method and returns a list of these dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing a recipe.
    """
    _, recipes = Recipe.get_available_recipes()
    return [recipe.to_dict() for recipe in recipes]


def api_get_all_recipe_name() -> list[str]:
    """
    Retrieves all available recipe names.

    This function calls the get_available_recipes method to retrieve all available recipes. It then extracts the names
    of each recipe and returns a list of these names.

    Returns:
        list[str]: A list of strings, each representing a recipe name.
    """
    recipes_names, _ = Recipe.get_available_recipes()
    return recipes_names


# ------------------------------------------------------------------------------
# Metrics APIs
# ------------------------------------------------------------------------------
def api_delete_metric(met_id: str) -> None:
    """
    Deletes a metric.

    This method takes a metric ID as input, deletes the corresponding JSON file from the directory specified by
    `EnvironmentVars.METRICS`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        met_id (str): The ID of the metric to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    Metric.delete_metric(met_id)


def api_get_all_metric() -> list[str]:
    """
    Retrieves all available metrics.

    This function calls the get_available_metrics method to retrieve all available metrics.
    It then returns a list of these metrics.

    Returns:
        list[str]: A list of strings, each representing a metric.
    """
    return Metric.get_available_metrics()


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
    return BenchmarkExecutor.create_executor(be_args)


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
    return BenchmarkExecutor.create_executor(be_args)


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
    return BenchmarkExecutor.load_executor(be_id, progress_callback_func)


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
    return BenchmarkExecutor.read_executor_arguments(be_id).to_dict()


def api_delete_executor(be_id: str) -> None:
    """
    This function takes an executor id as input and deletes the corresponding executor.

    Args:
        be_id (str): The id of the executor to be deleted.
    """
    BenchmarkExecutor.delete_executor(be_id)


def api_get_all_executor() -> list[dict]:
    """
    This function retrieves all available executors and returns them as a list of dictionaries. Each dictionary
    represents an executor and contains its information.

    Returns:
        list[dict]: A list of dictionaries, each representing an executor.
    """
    _, executors = BenchmarkExecutor.get_available_executors()
    return [executor.to_dict() for executor in executors]


def api_get_all_executor_name() -> list[str]:
    """
    This function retrieves all available executor names and returns them as a list.

    Returns:
        list[str]: A list of executor names.
    """
    executors_names, _ = BenchmarkExecutor.get_available_executors()
    return executors_names


# ------------------------------------------------------------------------------
# Results APIs
# ------------------------------------------------------------------------------
def api_read_result(res_id: str) -> dict:
    """
    Reads a result and returns its information.

    This function takes a result ID as input, reads the corresponding database file from the storage manager,
    and returns a dictionary containing the result's information.

    Args:
        res_id (str): The ID of the result.

    Returns:
        dict: A dictionary containing the result's information.
    """
    return Result.read_result(res_id).to_dict()


def api_read_results(res_ids: list[str]) -> list[dict]:
    """
    This function takes a list of result ids as input and reads the corresponding results.

    Args:
        res_ids (list[str]): The list of ids of the results to be read.

    Returns:
        list[dict]: A list of dictionaries, each representing a result.
    """
    return [Result.read_result(res_id).to_dict() for res_id in res_ids]


def api_delete_result(res_id: str) -> None:
    """
    This function takes a result id as input and deletes the corresponding result.

    Args:
        res_id (str): The id of the result to be deleted.
    """
    Result.delete_result(res_id)


def api_get_all_result() -> list[dict]:
    """
    This function retrieves all available results and returns them as a list of dictionaries. Each dictionary
    represents a result and contains its information.

    Returns:
        list[dict]: A list of dictionaries, each representing a result.
    """
    _, results = Result.get_available_results()
    return [result.to_dict() for result in results]


def api_get_all_result_name() -> list[str]:
    """
    This function retrieves all available result names and returns them as a list.

    Returns:
        list[str]: A list of result names.
    """
    results_name, _ = Result.get_available_results()
    return results_name


def api_get_all_prompt_template_detail() -> list[dict]:
    """
    Retrieves all available prompt template details and returns them as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing the details of a prompt template.
    """
    return PromptTemplateManager.get_all_prompt_template_details()


def api_get_all_prompt_template_name() -> list[str]:
    """
    Retrieves all available prompt template names and returns them as a list.

    Returns:
        list[str]: A list of prompt template names.
    """
    return PromptTemplateManager.get_all_prompt_template_names()


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


# ------------------------------------------------------------------------------
# Context Strategy APIs
# ------------------------------------------------------------------------------


def api_get_all_context_strategy_name() -> list[str]:
    """
    Retrieves and returns the names of all context strategies currently available.

    This API endpoint interfaces with the `ContextStrategyManager.get_all_context_strategy_names` method to fetch a list
    of all context strategy names. It's designed for clients that need to know what context strategies are available for
    use in sessions or other components of the system.

    Returns:
        list[str]: A list of strings, each representing the name of a context strategy.
    """
    return ContextStrategyManager.get_all_context_strategy_names()


def api_delete_context_strategy(context_strategy_name: str) -> None:
    """
    Deletes a context strategy based on the provided name.

    This API endpoint interfaces with the `ContextStrategyManager.delete_context_strategy` method, facilitating the
    removal of a specified context strategy from the system. It is particularly useful for managing the lifecycle of
    context strategies, allowing for the deletion of strategies that are no longer needed or relevant.

    Args:
        context_strategy_name (str): The name of the context strategy to be deleted

    Returns:
        None: This method does not return a value, but it will remove the specified context strategy from the system.
    """
    ContextStrategyManager.delete_context_strategy(context_strategy_name)


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
