import asyncio
import datetime
import glob
import inspect
import json
import os
import time
from functools import partial
from pathlib import Path
from typing import Any, Callable

import aiometer
from slugify import slugify

from moonshot.src.common.env_variables import EnvironmentVars
from moonshot.src.utils.import_modules import (
    create_module_spec,
    import_module_from_spec,
)


class Connection:
    @classmethod
    def load_from_json_config(cls, endpoint_config: str) -> Any:
        """
        Loads an instance of the class from a JSON configuration.
        This class method allows loading an instance of the class from a JSON configuration stored in a file
        or a string.

        Args:
            endpoint_config (str): A JSON configuration representing the instance's parameters.

        Returns:
            An instance of the class created from the JSON configuration.
        """
        # Construct the file path
        with open(
            f"{EnvironmentVars.LLM_ENDPOINTS}/{endpoint_config}.json", "r"
        ) as json_file:
            file_info = json.load(json_file)
            return cls(
                Path(endpoint_config).stem,
                file_info["name"],
                file_info["type"],
                file_info["uri"],
                file_info["token"],
                file_info["max_calls_per_second"],
                file_info["max_concurrency"],
                file_info["params"],
            )

    def __init__(
        self,
        id: str,
        name: str,
        connection_type: str,
        uri: str,
        token: str,
        max_calls_per_second: int,
        max_concurrency: int,
        params: dict,
    ):
        self.id = id
        self.name = name
        self.connection_type = connection_type
        self.api_endpoint = uri
        self.api_token = token
        self.api_max_calls_per_second = max_calls_per_second
        self.api_max_concurrency = max_concurrency
        self.api_params = params

        # Create a new connection instance
        self.connection_instance = self._get_connection_instance()
        if self.connection_instance:
            self.connection_instance = self.connection_instance(
                self.api_endpoint, self.api_token, self.api_params
            )
        else:
            raise RuntimeError(
                f"Unable to get defined connection instance - {self.connection_type}"
            )

    def _get_connection_instance(self) -> Any:
        """
        Retrieves an instance of the connection class based on the specified connection type.

        Returns:
            Any: An instance of the Connection class.
        """
        # Create the module specification
        module_spec = create_module_spec(
            self.connection_type,
            f"{EnvironmentVars.LLM_CONNECTION_TYPES}/{self.connection_type}.py",
        )

        # Check if the module specification exists
        if module_spec:
            # Import the module
            module = import_module_from_spec(module_spec)

            # Iterate through the attributes of the module
            for attr in dir(module):
                # Get the attribute object
                obj = getattr(module, attr)

                # Check if the attribute is a class and has the same module name as the connection type
                if inspect.isclass(obj) and obj.__module__ == self.connection_type:
                    return obj

        # Return None if no instance of the metric class is found
        return None


def get_connection_types() -> list:
    """
    Gets a list of available Language Model (LLM) connection types.
    This static method retrieves a list of available LLM connection types,
    which can be used to identify and configure connections to different LLM
    models or services.

    Returns:
        list: A list of LLM connection types, where each connection type is represented as a string or identifier.
    """
    return [
        Path(fp).stem
        for fp in glob.iglob(f"{EnvironmentVars.LLM_CONNECTION_TYPES}/*.py")
        if "__" not in fp
    ]


def get_endpoints() -> list:
    """
    Gets a list of Language Model (LLM) endpoints.
    This static method retrieves a list of available Language Model (LLM) endpoints.

    Returns:
        list: A list of LLM endpoints, where each endpoint is represented as a dictionary or an object.
    """
    endpoints = []
    filepaths = glob.glob(f"{EnvironmentVars.LLM_ENDPOINTS}/*.json")
    for filepath in filepaths:
        if "__" in filepath:
            continue

        with open(filepath, "r") as json_file:
            creation_timestamp = os.path.getctime(filepath)
            creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
            endpoints_info = json.load(json_file)
            endpoints_info["created_date"] = (
                creation_datetime.replace(microsecond=0).isoformat().replace("T", " ")
            )
            endpoints.append(endpoints_info)

    return endpoints


def get_endpoint_names() -> list:
    """
    Gets a list of Language Model (LLM) endpoint names.
    This static method retrieves a list of available Language Model (LLM) endpoint names.

    Returns:
        list: A list of LLM endpoint names.
    """
    return [item["name"] for item in get_endpoints()]


def get_predictions(
    prompts_template_info: dict, connection: Connection, prompt_callback: Callable
) -> list:
    """
    Performs predictions using the prompt. It appends contents of the prompt templates to the prompt first.

    Args:
        prompts_template_info (dict): A dictionary containing information about the prompts template.
        connection (Connection): An instance of the Connection class.
        prompt_callback (Callable): A callback function to handle prompts.

    Returns:
        list: A list of prediction results.
    """
    print("Performing predictions")

    # Store all the needed tasks
    prompts_tasks = [
        partial(
            get_async_predictions_helper,
            prompt_index,
            prompt_info,
            connection,
            prompt_callback,
        )
        for prompt_index, prompt_info in enumerate(prompts_template_info["data"])
    ]

    # Run predictions async
    print(
        f"Total number of prompts {len(prompts_tasks)} "
        f"and concurrency {connection.api_max_concurrency} "
        f"and calls per second {connection.api_max_calls_per_second}"
    )
    prediction_results = asyncio.run(
        get_async_predictions(
            prompts_tasks,
            connection.api_max_concurrency,
            connection.api_max_calls_per_second,
        )
    )

    # Return results
    return prediction_results


async def get_async_predictions_helper(
    prompt_index: int,
    prompt_info: dict,
    connection: Connection,
    prompt_callback: Callable,
) -> dict:
    """
    Helper function to asynchronously perform predictions for a given prompt.

    Args:
        prompt_index (int): The index of the prompt.
        prompt_info (dict): Information about the prompt.
        connection (Connection): The connection object.
        prompt_callback (Callable): The callback function to be called with the prompt info and connection id.

    Returns:
        dict: The updated prompt info with the predicted results and duration.
    """
    if "predicted_result" not in prompt_info:
        print(f"Predicting prompt {prompt_index} [{connection.id}]")
        start_time = time.perf_counter()

        predicted_result = await connection.connection_instance.get_response(
            prompt_info["prompt"]
        )
        duration = time.perf_counter() - start_time
        print(f"[Prompt {prompt_index}] took {duration:.4f}s")

        # Update prompt info
        prompt_info.update(
            {
                "predicted_result": predicted_result,
                "duration": duration,
            }
        )

        # Call prompt callback
        prompt_callback(prompt_info, connection.id)

    return prompt_info


async def get_async_predictions(
    prompts_tasks: list, max_at_once: int, max_calls_per_second: int
) -> list[Any]:
    """
    Asynchronously performs predictions for a list of prompt tasks.

    Args:
        prompts_tasks (list): A list of prompts tasks.
        max_at_once (int): The maximum number of tasks to run at once.
        max_calls_per_second (int): The maximum number of function calls per second.

    Returns:
        list: A list of prediction results.
    """
    return await aiometer.run_all(
        prompts_tasks, max_at_once=max_at_once, max_per_second=max_calls_per_second
    )


def add_new_endpoint(
    connector_type: str,
    name: str,
    uri: str,
    token: str,
    max_calls_per_second: int,
    max_concurrency: int,
    params: dict,
) -> None:
    """
    Adds an endpoint for a Language Model (LLM) connector.
    This static method allows adding an endpoint for a Language Model (LLM) connector. The endpoint is identified by
    its name and associated with the specified connector type. It requires the URI and access token for the
    LLM connector's API.

    Args:
        connector_type (str): The type of the LLM connector (e.g., 'GPT-3', 'Bert', etc.).
        name (str): The name or identifier for the endpoint.
        uri (str): The URI (Uniform Resource Identifier) for the LLM connector's API.
        token (str): The access token required to authenticate and access the LLM connector's API.
        max_calls_per_second (int): The number of api calls per second
        max_concurrency (int): The number of concurrent api calls
        params (dict): A dictionary that contains connection specified parameters
    """
    endpoint_info = {
        "type": connector_type,
        "name": name,
        "uri": uri,
        "token": token,
        "max_calls_per_second": max_calls_per_second,
        "max_concurrency": max_concurrency,
        "params": params,
    }
    endpoint_filename = slugify(name)
    with open(
        f"{EnvironmentVars.LLM_ENDPOINTS}/{endpoint_filename}.json", "w"
    ) as json_file:
        json.dump(endpoint_info, json_file, indent=2)
