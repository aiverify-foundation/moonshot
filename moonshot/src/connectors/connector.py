from __future__ import annotations

import asyncio
import time
from abc import abstractmethod
from asyncio import sleep
from functools import wraps
from pathlib import Path
from typing import Callable

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


def perform_retry(func):
    """
    A decorator to perform retries on a function.

    This decorator wraps a function to enable retrying the function call
    if it fails. The number of retries and the delay between retries
    are determined by the `retries_times` and `allow_retries`
    attributes of the class instance.

    Parameters:
    - func (Callable): The function to be wrapped and retried.

    Returns:
    - Callable: A wrapper function that includes retry logic.
    """

    async def wrapper(self, *args, **kwargs):
        if self.allow_retries:
            retry_count = 0
            base_delay = 1
            while retry_count <= self.retries_times:
                # Perform the request
                try:
                    return await func(self, *args, **kwargs)
                except Exception as exc:
                    logger.warning(f"Operation failed. {str(exc)} - Retrying...")

                # Perform retry
                retry_count += 1
                if retry_count <= self.retries_times:
                    delay = base_delay * (2**retry_count)
                    logger.warning(
                        f"Attempt {retry_count}, Retrying in {delay} seconds..."
                    )
                    await sleep(delay)
            # Raise an exception
            raise ConnectionError("Failed to get response.")

    return wrapper


class Connector:
    def __init__(self, ep_args: ConnectorEndpointArguments) -> None:
        self.id = ep_args.id

        self.endpoint = ep_args.uri
        self.token = ep_args.token
        self.max_concurrency = ep_args.max_concurrency
        self.max_calls_per_second = ep_args.max_calls_per_second
        self.params = ep_args.params

        # Rate limiting
        self.rate_limiter = ep_args.max_calls_per_second
        # Initialize the token count to the maximum limit
        self.tokens = ep_args.max_calls_per_second
        self.updated_at = time.time()
        self.semaphore = asyncio.Semaphore(ep_args.max_concurrency)

        # Set Prompts if they exists
        self.pre_prompt = ep_args.params.get("pre_prompt", "")
        self.post_prompt = ep_args.params.get("post_prompt", "")
        self.system_prompt = ep_args.params.get("system_prompt", "")

        # Connection timeout
        self.timeout = ep_args.params.get("timeout", 600)
        self.allow_retries = ep_args.params.get("allow_retries", True)
        self.retries_times = ep_args.params.get("num_of_retries", 3)

        # Optional params
        excluded_keys = {
            "allow_retries",
            "timeout",
            "num_of_retries",
            "pre_prompt",
            "post_prompt",
            "system_prompt",
        }
        self.optional_params = {
            k: v for k, v in ep_args.params.items() if k not in excluded_keys
        }

    async def _add_tokens(self) -> None:
        """
        Replenishes the token bucket based on the elapsed time since the last update.

        This method calculates the number of tokens to add to the bucket by considering the time that has elapsed
        since the tokens were last replenished. The rate at which tokens are added is determined by the `rate_limiter`
        attribute, which defines the maximum number of tokens that can be added per second. The total number of tokens
        in the bucket will never exceed the rate limit.

        The method updates the `updated_at` attribute to the current time after tokens are added, ensuring that
        the next token addition will be calculated based on the correct elapsed time.

        Usage:
            # Assume `self` is an instance of a class with `rate_limiter`, `tokens`, and `updated_at` attributes.
            await self.add_tokens()
        """
        now = time.time()
        elapsed = now - self.updated_at
        # Add tokens based on elapsed time
        increment = elapsed * self.rate_limiter
        self.tokens = min(self.rate_limiter, self.tokens + increment)
        self.updated_at = now

    @staticmethod
    def rate_limited(func: Callable) -> Callable:
        """
        A decorator to enforce rate limiting on an asynchronous function using a token bucket strategy.

        This decorator ensures that the decorated function adheres to a rate limit specified by the `rate_limiter`
        attribute of the class instance it belongs to. It uses a token bucket mechanism where tokens are added
        to the bucket over time, and each function call consumes a token. If there are no tokens available,
        the function's execution is delayed until the next token is added.

        The decorator also uses an `asyncio.Semaphore` to control concurrency, allowing multiple instances of the
        function to run in parallel up to a limit, without exceeding the rate limit.

        Args:
            func (Callable): The asynchronous function to be decorated.

        Returns:
            Callable: The decorated function wrapped with rate limiting logic.

        Usage:
            @rate_limited
            async def some_async_function(*args, **kwargs):
                # Function implementation
        """

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            async with self.semaphore:
                # Wait for token availability
                await self._add_tokens()
                if self.tokens < 1:
                    # Calculate the time to wait until the next token is available
                    sleep_time = (1 - self.tokens) / self.rate_limiter
                    await asyncio.sleep(sleep_time)
                    # Re-check for token availability after sleeping
                    await self._add_tokens()
                # Consume a token and proceed with the function call
                self.tokens -= 1
                return await func(self, *args, **kwargs)

        return wrapper

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
    def load(cls, ep_args: ConnectorEndpointArguments) -> Connector:
        """
        This method dynamically loads a connector instance based on the provided endpoint arguments.

        The connector type specified in the `ep_args` is used to dynamically load the corresponding
        connector class. The connector is then instantiated with the provided endpoint arguments. If the
        specified connector type does not correspond to any available connector classes, a RuntimeError is raised.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments which include the connector type and
            other necessary information.

        Returns:
            Connector: An instance of the specified connector class, initialized with the given endpoint arguments.

        Raises:
            RuntimeError: If the specified connector type does not match any available connector classes.
        """
        connector_instance = get_instance(
            ep_args.connector_type,
            Storage.get_filepath(
                EnvVariables.CONNECTORS.name, ep_args.connector_type, "py"
            ),
        )
        if connector_instance:
            return connector_instance(ep_args)
        else:
            raise RuntimeError(
                f"Unable to get defined connector instance - {ep_args.connector_type}"
            )

    @staticmethod
    def create(ep_args: ConnectorEndpointArguments) -> Connector:
        """
        Creates a connector object based on the provided endpoint arguments.

        This method takes a ConnectorEndpointArguments object, which contains the necessary information
        to initialize and return a Connector object. The Connector object is created by calling the
        `load_connector` method, which dynamically loads and initializes the connector based on the
        endpoint arguments provided.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments required to create the connector.

        Returns:
            Connector: An initialized Connector object based on the provided endpoint arguments.
        """
        try:
            return Connector.load(ep_args)

        except Exception as e:
            logger.error(f"Failed to create connector: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Fetches a list of all available connector types.

        This method employs the `get_connectors` method to locate all Python files in the directory
        defined by the `EnvironmentVars.CONNECTORS` environment variable. It subsequently excludes any files that are
        not intended to be exposed as connectors (those containing "__" in their names). The method yields a list of the
        names of these connector types.

        Returns:
            list[str]: A list of strings, each denoting the name of a connector type.

        Raises:
            Exception: If an error occurs during the extraction of connector types.
        """
        try:
            return [
                Path(fp).stem
                for fp in Storage.get_objects(EnvVariables.CONNECTORS.name, "py")
                if "__" not in fp
            ]

        except Exception as e:
            logger.error(f"Failed to get available connectors: {str(e)}")
            raise e

    @staticmethod
    async def get_prediction(
        generated_prompt: ConnectorPromptArguments,
        connector: Connector,
        prompt_callback: Callable | None = None,
    ) -> ConnectorPromptArguments:
        """
        Generates a prediction for a given prompt using a specified connector.

        This method takes a `generated_prompt` object, which contains the prompt to be predicted, and a `connector`
        object, which is used to generate the prediction. The method also optionally takes a `prompt_callback` function,
        which is called after the prediction is generated.

        The method first prints a message indicating that it is predicting the prompt. It then records the start time
        and uses the `connector` to generate a prediction for the `generated_prompt`. The duration of the prediction
        is calculated and stored in the `generated_prompt`.

        If a `prompt_callback` function is provided, it is called with the `generated_prompt` and `connector.id` as
        arguments.

        The method then returns the `generated_prompt` with the generated prediction and duration.

        Args:
            generated_prompt (ConnectorPromptArguments): The prompt to be predicted.
            connector (Connector): The connector to be used for prediction.
            prompt_callback (Callable | None): An optional callback function to be called after prediction.

        Returns:
            ConnectorPromptArguments: The `generated_prompt` with the generated prediction and duration.

        Raises:
            Exception: If there is an error during prediction.
        """
        try:
            logger.info(
                f"Predicting prompt {generated_prompt.prompt_index} [{connector.id}]"
            )

            start_time = time.perf_counter()
            generated_prompt.predicted_results = await connector.get_response(
                generated_prompt.prompt
            )
            generated_prompt.duration = time.perf_counter() - start_time
            logger.debug(
                f"[Prompt {generated_prompt.prompt_index}] took {generated_prompt.duration:.4f}s"
            )

            # Call prompt callback
            if prompt_callback:
                prompt_callback(generated_prompt, connector.id)

            # Return the updated prompt
            return generated_prompt

        except Exception as e:
            logger.error(f"Failed to get prediction: {str(e)}")
            raise e

    def set_system_prompt(self, system_prompt: str) -> None:
        """
        Assigns a new system prompt to this connector instance.

        The system prompt serves as a preconfigured command or message that the connector can use to initiate
        interactions or execute specific operations.

        Parameters:
            system_prompt (str): The new system prompt to set for this connector.
        """
        self.system_prompt = system_prompt
