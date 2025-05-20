from __future__ import annotations

import asyncio
import time
from abc import abstractmethod
from functools import partial, wraps
from pathlib import Path
from typing import Callable

from tenacity import RetryCallState, retry, stop_after_attempt, wait_random_exponential

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors.connector_response import ConnectorResponse
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


def perform_retry_callback(connector_id: str, retry_state: RetryCallState) -> None:
    """
    Callback function to log retry attempts with detailed information.

    This function is called by the tenacity library before each retry attempt.
    It logs the retry attempt number, the sleep time before the next attempt,
    the error message that caused the retry, and the connector ID.

    Args:
        connector_id (str): The ID of the connector.
        retry_state (RetryCallState): The state of the retry call, which includes
            information about the current attempt, the exception raised, and the next action.
    """
    CONNECTOR_PERFORM_RETRY_CALLBACK_ERROR = "[Connector ID: {connector_id}] Attempt {attempt_no} failed due to error: {message}"  # noqa: E501

    sleep_time = retry_state.idle_for if retry_state else 0
    exception = (
        retry_state.outcome.exception() if retry_state.outcome else "Unknown exception"
    )
    logger.error(
        CONNECTOR_PERFORM_RETRY_CALLBACK_ERROR.format(
            connector_id=connector_id,
            attempt_no=retry_state.attempt_number,
            sleep=f"{sleep_time:.2f}",
            message=str(exception),
        )
    )


def perform_retry(func):
    """
    A decorator to perform retries on a function using tenacity.

    This decorator wraps an asynchronous function to enable retrying the function call
    if it fails. The number of attempts and the delay between attempts
    are determined by the `max_attempts` attribute of the class instance.

    Args:
        func (Callable): The asynchronous function to be wrapped and retried.

    Returns:
        Callable: A wrapper function that includes retry logic.
    """

    async def wrapper(self, *args, **kwargs):
        retry_decorator = retry(
            wait=wait_random_exponential(min=1, max=60),
            stop=stop_after_attempt(self.max_attempts),
            after=partial(perform_retry_callback, self.id),
            reraise=True,
        )
        return await retry_decorator(func)(self, *args, **kwargs)

    return wrapper


class Connector:
    CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be an instance of ConnectorEndpointArguments and not None."  # noqa: E501
    CONNECTOR_CREATE_ERROR = "[Connector] Failed to create connector: {message}"
    CONNECTOR_GET_AVAILABLE_ITEMS_ERROR = (
        "[Connector] Failed to get available connectors: {message}"
    )
    CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR = "[Connector] The 'connector' argument must be an instance of Connector and not None."  # noqa: E501
    CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR = "[Connector] The 'generated_prompt' argument must be an instance of ConnectorPromptArguments and not None."  # noqa: E501
    CONNECTOR_GET_PREDICTION_ERROR = "[Connector ID: {connector_id}] Prompt Index {prompt_index} failed to get prediction: {message}"  # noqa: E501
    CONNECTOR_GET_PREDICTION_INFO = (
        "[Connector ID: {connector_id}] Predicting Prompt Index {prompt_index}."
    )
    CONNECTOR_GET_PREDICTION_TIME_TAKEN_INFO = "[Connector ID: {connector_id}] Prompt Index {prompt_index} took {prompt_duration}s."  # noqa: E501
    CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be an instance of ConnectorEndpointArguments and not None."  # noqa: E501
    CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR = (
        "[Connector] Failed to get connector instance: {message}"
    )
    CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR = "[Connector] The 'system_prompt' argument must be an instance of string and not None."  # noqa: E501

    def __init__(self, ep_args: ConnectorEndpointArguments) -> None:
        self.id = ep_args.id

        self.endpoint = ep_args.uri
        self.token = ep_args.token
        self.max_concurrency = ep_args.max_concurrency
        self.max_calls_per_second = ep_args.max_calls_per_second
        self.model = ep_args.model
        self.params = ep_args.params

        # Rate limiting
        self.rate_limiter = ep_args.max_calls_per_second
        # Initialize the token count to the maximum limit
        self.tokens = ep_args.max_calls_per_second
        self.updated_at = time.time()
        self.semaphore = asyncio.Semaphore(ep_args.max_concurrency)

        # Set Prompts if they exist
        self.pre_prompt = ep_args.params.get("pre_prompt", "")
        self.post_prompt = ep_args.params.get("post_prompt", "")
        self.system_prompt = ep_args.params.get("system_prompt", "")

        # Connection timeout
        self.timeout = ep_args.params.get("timeout", 600)
        self.max_attempts = ep_args.params.get("max_attempts", 3)

        # Optional params
        excluded_keys = {
            "timeout",
            "max_attempts",
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
    async def get_response(self, prompt: str) -> ConnectorResponse:
        """
        Abstract method to be implemented by subclasses to obtain a response from the connector.

        This method should asynchronously send a prompt to the connector's API and return the response.

        Args:
            prompt (str): The input prompt to be sent to the connector.

        Returns:
            ConnectorResponse: An instance containing the response received from the connector and any
            additional metadata.
        """
        pass

    @classmethod
    def load(cls, ep_args: ConnectorEndpointArguments) -> Connector:
        """
        Dynamically loads a connector instance based on the provided endpoint arguments.

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
        if ep_args is None or not isinstance(ep_args, ConnectorEndpointArguments):
            raise ValueError(
                Connector.CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR
            )

        connector_instance = get_instance(
            ep_args.connector_type,
            Storage.get_filepath(
                EnvVariables.CONNECTORS.name, ep_args.connector_type, "py"
            ),
        )
        if connector_instance and isinstance(connector_instance, Callable):
            return connector_instance(ep_args)
        else:
            raise RuntimeError(
                Connector.CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR.format(
                    message=ep_args.connector_type
                )
            )

    @staticmethod
    def create(ep_args: ConnectorEndpointArguments) -> Connector:
        """
        Creates a connector object based on the provided endpoint arguments.

        This method takes a ConnectorEndpointArguments object, which contains the necessary information
        to initialize and return a Connector object. The Connector object is created by calling the
        `load` method, which dynamically loads and initializes the connector based on the
        endpoint arguments provided.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments required to create the connector.

        Returns:
            Connector: An initialized Connector object based on the provided endpoint arguments.

        Raises:
            ValueError: If the provided endpoint arguments are invalid.
            Exception: If there is an error during the creation of the connector.
        """
        try:
            if ep_args is None or not isinstance(ep_args, ConnectorEndpointArguments):
                raise ValueError(
                    Connector.CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR
                )
            return Connector.load(ep_args)

        except Exception as e:
            logger.error(Connector.CONNECTOR_CREATE_ERROR.format(message=str(e)))
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Fetches a list of all available connector types.

        This method employs the `get_connectors` method to locate all Python files in the directory
        defined by the `EnvVariables.CONNECTORS` environment variable. It subsequently excludes any files that are
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
            logger.error(
                Connector.CONNECTOR_GET_AVAILABLE_ITEMS_ERROR.format(message=str(e))
            )
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

        The method logs a message indicating that it is predicting the prompt. It then records the start time
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
        if generated_prompt is None or not isinstance(
            generated_prompt, ConnectorPromptArguments
        ):
            raise ValueError(
                Connector.CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR
            )

        if connector is None or not isinstance(connector, Connector):
            raise ValueError(
                Connector.CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR
            )

        try:
            logger.info(
                Connector.CONNECTOR_GET_PREDICTION_INFO.format(
                    connector_id=connector.id,
                    prompt_index=generated_prompt.prompt_index,
                )
            )

            start_time = time.perf_counter()
            generated_prompt.predicted_results = await connector.get_response(
                generated_prompt.prompt
            )
            generated_prompt.duration = time.perf_counter() - start_time
            logger.debug(
                Connector.CONNECTOR_GET_PREDICTION_TIME_TAKEN_INFO.format(
                    connector_id=connector.id,
                    prompt_index=generated_prompt.prompt_index,
                    prompt_duration=f"{generated_prompt.duration:.4f}",
                )
            )

            # Call prompt callback
            if prompt_callback:
                prompt_callback(generated_prompt, connector.id)

            # Return the updated prompt
            return generated_prompt

        except Exception as e:
            logger.error(
                Connector.CONNECTOR_GET_PREDICTION_ERROR.format(
                    connector_id=connector.id,
                    prompt_index=generated_prompt.prompt_index,
                    message=str(e),
                )
            )
            raise e

    def set_system_prompt(self, system_prompt: str) -> None:
        """
        Sets a new system prompt for this connector instance.

        The system prompt is a predefined message or command that the connector can use to start interactions
        or perform specific tasks.

        Args:
            system_prompt (str): The new system prompt to set for this connector.

        Raises:
            ValueError: If the provided system prompt is not a string or is None.
        """
        if system_prompt is None or not isinstance(system_prompt, str):
            raise ValueError(Connector.CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR)
        self.system_prompt = system_prompt
