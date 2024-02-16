from __future__ import annotations

import inspect
from abc import abstractmethod
from asyncio import sleep
from typing import Any

from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.utils.import_modules import (
    create_module_spec,
    import_module_from_spec,
)


def perform_retry(func):
    """
    A decorator to perform retries on a function.

    This decorator wraps a function to enable retrying the function call
    if it fails. The number of retries and the delay between retries
    are determined by the `api_retries_times` and `api_allow_retries`
    attributes of the class instance.

    Parameters:
    - func (Callable): The function to be wrapped and retried.

    Returns:
    - Callable: A wrapper function that includes retry logic.
    """

    async def wrapper(self, *args, **kwargs):
        if self.api_allow_retries:
            retry_count = 0
            base_delay = 1
            while retry_count <= self.api_retries_times:
                # Perform the request
                try:
                    return await func(self, *args, **kwargs)
                except Exception as exc:
                    print(f"Operation failed. {str(exc)} - Retrying...")

                # Perform retry
                retry_count += 1
                if retry_count <= self.api_retries_times:
                    delay = base_delay * (2**retry_count)
                    print(f"Attempt {retry_count}, Retrying in {delay} seconds...")
                    await sleep(delay)
            # Raise an exception
            raise ConnectionError("Failed to get response.")

    return wrapper


class Connector:
    def __init__(self, ep_args: ConnectorEndpointArguments) -> None:
        self.id = None

        self.endpoint = ep_args.uri
        self.token = ep_args.token
        self.max_concurrency = ep_args.max_concurrency
        self.max_calls_per_second = ep_args.max_calls_per_second
        self.params = ep_args.params

        self.pre_prompt = ""
        self.post_prompt = ""

        # Connection timeout
        self.timeout = ep_args.params.get("timeout", 600)
        self.allow_retries = ep_args.params.get("allow_retries", True)
        self.retries_times = ep_args.params.get("num_of_retries", 3)

    @abstractmethod
    async def get_response(self, prompt: str) -> str:
        """
        Abstract method to be implemented by subclasses to get a response from the connector.

        This method should asynchronously send a prompt to the connector's API and return the response.

        Args:
            prompt (str): The input prompt to be sent to the connector.

        Returns:
            str: The response received from the connector.
        """
        pass

    @classmethod
    def load_connector(cls, ep_args: ConnectorEndpointArguments) -> Connector:
        """
        Loads a connector instance based on the provided endpoint arguments.

        This method utilizes the connector type specified in the `ep_args` to dynamically load the corresponding
        connector class. It then instantiates the connector with the provided endpoint arguments. If the
        specified connector type does not match any available connector classes, a RuntimeError is raised.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments containing the connector type and
            other necessary information.

        Returns:
            Connector: An instance of the specified connector class initialized with the given endpoint arguments.

        Raises:
            RuntimeError: If no connector class matches the specified connector type.
        """
        connector_instance = cls._get_connector_instance(ep_args.connector_type)
        if connector_instance:
            return connector_instance(ep_args)
        else:
            raise RuntimeError(
                f"Unable to get defined connector instance - {ep_args.connector_type}"
            )

    @staticmethod
    def _get_connector_instance(connector_type: str) -> Any:
        """
        Dynamically retrieves a connector class instance based on the connector type.

        This method searches for a Python module that matches the given connector type within a predefined directory.
        It then attempts to find a class within that module that corresponds to the connector type. If such a class
        is found, it is returned as the connector class instance. If no matching class is found within the module,
        or if the module does not exist, this method returns None.

        Args:
            connector_type (str): The type of the connector to retrieve, which corresponds to the module and class name.

        Returns:
            Any: An instance of the found connector class, or None if no matching class is found.
        """
        # Create the module specification
        connector_filepath = f"{EnvironmentVars.CONNECTORS}/{connector_type}.py"
        module_spec = create_module_spec(
            connector_type,
            connector_filepath,
        )

        # Check if the module specification exists
        if module_spec:
            # Import the module
            module = import_module_from_spec(module_spec)

            # Iterate through the attributes of the module
            for attr in dir(module):
                # Get the attribute object
                obj = getattr(module, attr)

                # Check if the attribute is a class and has the same module name as the connector type
                if inspect.isclass(obj) and obj.__module__ == connector_type:
                    return obj

        # Return None if no instance of the metric class is found
        return None
