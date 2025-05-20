import asyncio
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from tenacity import RetryCallState

from moonshot.src.connectors.connector import (
    Connector,
    perform_retry,
    perform_retry_callback,
)
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)

CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be an instance of ConnectorEndpointArguments and not None."  # noqa: E501
CONNECTOR_CREATE_ERROR = "[Connector] Failed to create connector: {message}"
CONNECTOR_GET_AVAILABLE_ITEMS_ERROR = (
    "[Connector] Failed to get available connectors: {message}"
)
CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR = "[Connector] The 'connector' argument must be an instance of Connector and not None."  # noqa: E501
CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR = "[Connector] The 'generated_prompt' argument must be an instance of ConnectorPromptArguments and not None."  # noqa: E501
CONNECTOR_GET_PREDICTION_ERROR = "[Connector ID: {connector_id}] Prompt Index {prompt_index} failed to get prediction: {message}"  # noqa: E501
CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be an instance of ConnectorEndpointArguments and not None."  # noqa: E501
CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR = (
    "[Connector] Failed to get connector instance: {message}"
)
CONNECTOR_PERFORM_RETRY_CALLBACK_ERROR = "[Connector ID: {connector_id}] Attempt {attempt_no} failed due to error: {message}"  # noqa: E501
CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR = "[Connector] The 'system_prompt' argument must be an instance of string and not None."  # noqa: E501

from moonshot.src.storage.storage import Storage


@pytest.fixture
def connector():
    ep_args = ConnectorEndpointArguments(
        id="SampleId",
        name="SampleName",
        connector_type="SampleConnector",
        uri="",
        token="",
        max_calls_per_second=1,
        max_concurrency=1,
        model="my-model",
        params={},
        created_date="",
    )
    return Connector(ep_args)


@pytest.fixture
def generated_prompt():
    return ConnectorPromptArguments(prompt="Test prompt", prompt_index=1, target="")


class MockConnector:
    def __init__(self, max_attempts=3):
        self.id = "mock-connector"
        self.system_prompt = ""
        self.max_attempts = max_attempts
        self.attempt = 0

    # Create a mock function that will always fail
    @perform_retry
    async def mock_func_perm_failure(self, *args, **kwargs):
        self.attempt += 1
        raise Exception("Permanent failure")

    @perform_retry
    async def mock_func(self, *args, **kwargs):
        """
        Mock function that will fail a few times before succeeding.

        This function simulates a task that may fail a few times before eventually succeeding.
        It raises an exception if the current attempt number is less than the specified number
        of attempts, otherwise it returns "Success".

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            Exception: If the current attempt number is less than the specified number of attempts.

        Returns:
            str: "Success" if the function does not raise an exception.
        """
        self.attempt += 1
        if self.attempt < self.max_attempts:
            raise Exception("Temporary failure")
        return "Success"


class TestConnector(Connector):
    def __init__(self, ep_args, rate_limiter, tokens):
        super().__init__(ep_args)
        self.rate_limiter = rate_limiter
        self.tokens = tokens
        self.semaphore = asyncio.Semaphore(2)
        self._add_tokens = AsyncMock()

    async def get_response(self, prompt: str):
        return "response"


@pytest.mark.asyncio
class TestCollectionConnector:
    # ------------------------------------------------------------------------------
    # Test perform_retry_callback functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "attempt_number, idle_for, outcome_exception, expected_sleep, expected_message",
        [
            (
                3,
                2.5,
                Exception("Test exception"),
                "2.50",
                "Test exception",
            ),  # Normal case
            (
                3,
                None,
                Exception("Test exception"),
                "0.00",
                "Test exception",
            ),  # No idle_for
            (3, 2.5, None, "2.50", "Unknown exception"),  # No outcome
            (
                3,
                2.5,
                "no_exception_method",
                "2.50",
                "Unknown exception",
            ),  # No exception method
            (3, None, None, "0.00", "Unknown exception"),  # No idle_for and outcome
        ],
    )
    def test_perform_retry_callback(
        self,
        mocker,
        attempt_number,
        idle_for,
        outcome_exception,
        expected_sleep,
        expected_message,
    ):
        mock_logger = mocker.patch("moonshot.src.connectors.connector.logger")

        mock_retry_state = Mock(spec=RetryCallState)
        mock_retry_state.attempt_number = attempt_number

        if idle_for is not None:
            mock_retry_state.idle_for = idle_for
        else:
            mock_retry_state.idle_for = 0

        if outcome_exception == "no_exception_method":
            mock_retry_state.outcome = None
        elif outcome_exception is not None:
            mock_retry_state.outcome = Mock()
            mock_retry_state.outcome.exception.return_value = outcome_exception
        else:
            mock_retry_state.outcome = None

        perform_retry_callback("test_connector_id", mock_retry_state)

        mock_logger.error.assert_called_once_with(
            CONNECTOR_PERFORM_RETRY_CALLBACK_ERROR.format(
                connector_id="test_connector_id",
                attempt_no=attempt_number,
                sleep=expected_sleep,
                message=expected_message,
            )
        )

    # ------------------------------------------------------------------------------
    # Test perform_retry functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "max_attempts, expected_attempts, should_succeed",
        [
            (-1, 1, True),  # succeeds immediately
            (0, 1, True),  # succeeds immediately
            (1, 1, True),  # succeeds after 1 attempt
            (2, 2, True),  # succeeds after 2 attempts
            (3, 3, True),  # succeeds after 3 attempts
        ],
    )
    async def test_perform_retry(self, max_attempts, expected_attempts, should_succeed):
        """
        Test the perform_retry decorator with various configurations.

        This test verifies the behavior of the perform_retry decorator by simulating different
        scenarios where retries are allowed or not, and where the number of attempts varies.
        It checks whether the function succeeds or fails as expected and whether the number
        of attempts matches the expected value.

        Args:
            max_attempts (int): The number of attempts before succeeding.
            expected_attempts (int): The expected number of attempts.
            should_succeed (bool): Whether the function should succeed.

        Raises:
            Exception: If the function is expected to fail.
        """
        # Create an instance with the given parameters
        instance = MockConnector(max_attempts=max_attempts)

        if should_succeed:
            # If the function is expected to succeed, call the mock function
            result = await instance.mock_func()
            assert result == "Success"
            assert instance.attempt == expected_attempts
        else:
            # If the function is expected to fail, call the mock function and check for an exception
            with pytest.raises(Exception) as excinfo:
                result = await instance.mock_func()
            assert str(excinfo.value) == "Temporary failure"
            assert instance.attempt == expected_attempts

    @pytest.mark.parametrize(
        "max_attempts",
        [
            2,  # exceeds retry limit
        ],
    )
    async def test_perform_retry_exceeds_retries(self, max_attempts):
        """
        Test the perform_retry decorator when the retry limit is exceeded.

        This test verifies that the perform_retry decorator correctly raises an exception
        when the maximum number of retry attempts is exceeded.

        Args:
            max_attempts (int): The maximum number of attempts before giving up.

        Raises:
            Exception: If the function fails permanently.
        """
        # Create an instance with the given parameters
        instance = MockConnector(max_attempts=max_attempts)

        with pytest.raises(Exception) as excinfo:
            _ = await instance.mock_func_perm_failure()
        assert str(excinfo.value) == "Permanent failure"
        assert instance.attempt == max_attempts

    # ------------------------------------------------------------------------------
    # Test rate_limited functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "tokens, rate_limiter, expected_sleep_called, expected_result",
        [
            (1, 1, False, "success"),  # Tokens available
            (0, 1, True, "success"),  # No tokens available, should sleep
            (-1, 1, True, "success"),  # Negative tokens, should sleep
            (1, 2, False, "success"),  # Tokens available, higher rate limiter
        ],
    )
    async def test_rate_limited(
        mocker, tokens, rate_limiter, expected_sleep_called, expected_result
    ):
        """
        Test the rate_limited decorator with various configurations.

        This test verifies the behavior of the rate_limited decorator by simulating different
        scenarios where tokens are available or not, and where the rate limiter varies.
        It checks whether the function succeeds as expected and whether the sleep function
        is called when tokens are not available.

        Args:
            mocker: The mocker object for patching.
            tokens (int): The number of tokens available.
            rate_limiter (int): The rate limiter value.
            expected_sleep_called (bool): Whether the sleep function is expected to be called.
            expected_result (str): The expected result of the decorated function.
        """
        # Create an example ConnectorEndpointArguments
        ep_args = ConnectorEndpointArguments(
            id="SampleId",
            name="SampleName",
            connector_type="SampleConnector",
            uri="",
            token="",
            max_calls_per_second=1,
            max_concurrency=1,
            model="my-model",
            params={},
            created_date="",
        )

        # Create a mock instance of the Connector class
        mock_connector = TestConnector(
            ep_args, rate_limiter=rate_limiter, tokens=tokens
        )

        # Mock the function to be decorated
        async def mock_func(self, *args, **kwargs):
            return "success"

        # Apply the decorator
        decorated_func = Connector.rate_limited(mock_func)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            result = await decorated_func(mock_connector)
            assert result == expected_result
            assert mock_connector._add_tokens.called
            assert mock_sleep.called == expected_sleep_called

    @pytest.mark.parametrize(
        "tokens, rate_limiter, expected_results, expected_sleep_calls",
        [
            (2, 1, ["success", "success"], 1),  # Tokens available
            (2, 2, ["success", "success"], 0),  # Tokens available
            (0, 1, ["success", "success"], 2),  # No tokens available, should sleep
            (1, 1, ["success", "success"], 1),  # Tokens available
            (1, 2, ["success", "success"], 1),  # Tokens available, higher rate limiter
            (-1, 1, ["success", "success"], 2),  # Negative tokens, should sleep
        ],
    )
    async def test_rate_limited_concurrent(
        mocker, tokens, rate_limiter, expected_results, expected_sleep_calls
    ):
        """
        Test the rate_limited decorator with concurrent calls.

        This test verifies the behavior of the rate_limited decorator when multiple
        concurrent calls are made. It simulates different scenarios where tokens are
        available or not, and where the rate limiter varies. It checks whether the
        function succeeds as expected and whether the sleep function is called the
        expected number of times.

        Args:
            mocker: The mocker object for patching.
            tokens (int): The number of tokens available.
            rate_limiter (int): The rate limiter value.
            expected_results (list): The expected results of the decorated function.
            expected_sleep_calls (int): The expected number of sleep function calls.
        """
        # Create an example ConnectorEndpointArguments
        ep_args = ConnectorEndpointArguments(
            id="SampleId",
            name="SampleName",
            connector_type="SampleConnector",
            uri="",
            token="",
            max_calls_per_second=1,
            max_concurrency=1,
            model="my-model",
            params={},
            created_date="",
        )

        # Create a mock instance of the Connector class
        mock_connector = Connector(ep_args)
        mock_connector.rate_limiter = rate_limiter
        mock_connector.tokens = tokens
        mock_connector.semaphore = asyncio.Semaphore(2)

        # Mock the function to be decorated
        async def mock_func(self, *args, **kwargs):
            return "success"

        # Apply the decorator
        decorated_func = Connector.rate_limited(mock_func)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            # Test the decorated function with concurrency
            results = await asyncio.gather(
                decorated_func(mock_connector), decorated_func(mock_connector)
            )
            assert results == expected_results
            assert mock_sleep.call_count == expected_sleep_calls

    # ------------------------------------------------------------------------------
    # Test load functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_args, filepath_return_val, connector_return_val",
        [
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "my-connector-type.py",
                MockConnector,
            )
        ],
    )
    def test_load_success(self, ep_args, filepath_return_val, connector_return_val):
        """
        Test the successful loading of a connector.

        This test verifies that the Connector.load method successfully loads a connector
        instance when provided with valid endpoint arguments and a valid connector type.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments for the connector.
            filepath_return_val (str): The expected filepath return value.
            connector_return_val (type): The expected connector return value.
        """
        with patch(
            "moonshot.src.connectors.connector.get_instance"
        ) as mock_get_instance, patch(
            "moonshot.src.connectors.connector.Storage.get_filepath"
        ) as mock_get_filepath:
            mock_get_filepath.return_value = filepath_return_val
            mock_get_instance.return_value = connector_return_val

            connector = Connector.load(ep_args)
            assert connector is not None
            assert isinstance(connector, connector_return_val)

    @pytest.mark.parametrize(
        "ep_args, filepath_return_val, connector_return_val, expected_exception, expected_exception_error_message",
        [
            (
                None,
                "my-connector-type.py",
                MockConnector,
                ValueError,
                CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                1234,
                "my-connector-type.py",
                MockConnector,
                ValueError,
                CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                [],
                "my-connector-type.py",
                MockConnector,
                ValueError,
                CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                (),
                "my-connector-type.py",
                MockConnector,
                ValueError,
                CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                {},
                "my-connector-type.py",
                MockConnector,
                ValueError,
                CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            # Invalid get_instance value
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "my-connector-type.py",
                None,
                RuntimeError,
                CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR.format(
                    message="my-connector-type"
                ),
            ),
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "my-connector-type.py",
                1234,
                RuntimeError,
                CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR.format(
                    message="my-connector-type"
                ),
            ),
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "my-connector-type.py",
                (),
                RuntimeError,
                CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR.format(
                    message="my-connector-type"
                ),
            ),
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "my-connector-type.py",
                [],
                RuntimeError,
                CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR.format(
                    message="my-connector-type"
                ),
            ),
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "my-connector-type.py",
                {},
                RuntimeError,
                CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR.format(
                    message="my-connector-type"
                ),
            ),
        ],
    )
    def test_load_error(
        self,
        ep_args,
        filepath_return_val,
        connector_return_val,
        expected_exception,
        expected_exception_error_message,
    ):
        """
        Test the error handling of the Connector.load method.

        This test verifies that the Connector.load method raises the appropriate exceptions
        and error messages when provided with invalid endpoint arguments or an invalid
        connector type.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments for the connector.
            filepath_return_val (str): The expected filepath return value.
            connector_return_val (type): The expected connector return value.
            expected_exception (type): The expected exception type.
            expected_exception_error_message (str): The expected exception error message.
        """
        with patch(
            "moonshot.src.connectors.connector.get_instance"
        ) as mock_get_instance, patch(
            "moonshot.src.connectors.connector.Storage.get_filepath"
        ) as mock_get_filepath:
            mock_get_filepath.return_value = filepath_return_val
            mock_get_instance.return_value = connector_return_val

            with pytest.raises(expected_exception) as exc_info:
                _ = Connector.load(ep_args)

            # Assert the exception message
            assert (
                str(exc_info.value) == expected_exception_error_message
            ), "The exception message should match the expected message."

    # ------------------------------------------------------------------------------
    # Test create functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_args, load_return_val",
        [
            (
                ConnectorEndpointArguments(
                    id="test_id",
                    name="new_name",
                    uri="",
                    token="test_token",
                    max_concurrency=5,
                    max_calls_per_second=10,
                    model="my-model",
                    params={},
                    connector_type="my-connector-type",
                ),
                "success",
            )
        ],
    )
    def test_create_success(self, ep_args, load_return_val):
        """
        Test the successful creation of a connector.

        This test verifies that the Connector.create method successfully creates a connector
        instance when provided with valid endpoint arguments and a valid load return value.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments for the connector.
            load_return_val (str): The expected load return value.
        """
        with patch("moonshot.src.connectors.connector.Connector.load") as mock_load:
            mock_load.return_value = load_return_val
            connector = Connector.create(ep_args)
            assert connector is not None
            assert connector == load_return_val

    @pytest.mark.parametrize(
        "ep_args, load_return_val, expected_exception, expected_exception_error_message",
        [
            (
                None,
                "success",
                ValueError,
                CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                1234,
                "success",
                ValueError,
                CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                [],
                "success",
                ValueError,
                CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                (),
                "success",
                ValueError,
                CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
            (
                {},
                "success",
                ValueError,
                CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR,
            ),
        ],
    )
    def test_create_error(
        self,
        ep_args,
        load_return_val,
        expected_exception,
        expected_exception_error_message,
    ):
        with patch("moonshot.src.connectors.connector.Connector.load") as mock_load:
            mock_load.return_value = load_return_val
            with pytest.raises(expected_exception) as exc_info:
                _ = Connector.create(ep_args)

            # Assert the exception message
            assert (
                str(exc_info.value) == expected_exception_error_message
            ), "The exception message should match the expected message."

    def test_create_load_exception(self, mocker):
        # Arrange
        ep_args = MagicMock(spec=ConnectorEndpointArguments)
        _ = mocker.patch(
            "moonshot.src.connectors.connector.Connector.load",
            side_effect=RuntimeError("Load error"),
        )
        mock_logger = mocker.patch("moonshot.src.connectors.connector.logger")

        # Act & Assert
        with pytest.raises(RuntimeError) as excinfo:
            Connector.create(ep_args)

        assert str(excinfo.value) == "Load error"
        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][0] == CONNECTOR_CREATE_ERROR.format(
            message="Load error"
        )

    # ------------------------------------------------------------------------------
    # Test get_available items functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mocked_files, expected_result",
        [
            (
                [
                    "connector1.py",
                    "connector2.py",
                    "__init__.py",
                    "connector3.py",
                    "connector4.py",
                ],
                ["connector1", "connector2", "connector3", "connector4"],
            ),
            (["__init__.py"], []),
            ([], []),
        ],
    )
    @patch.object(Storage, "get_objects")
    def test_get_available_items(self, mock_get_objects, mocked_files, expected_result):
        # Mock the return value of Storage.get_objects
        mock_get_objects.return_value = mocked_files

        # Call the method
        result = Connector.get_available_items()

        # Assert the result
        assert result == expected_result

    @pytest.mark.parametrize(
        "exception, log_message",
        [
            (
                Exception("Test Exception"),
                "Failed to get available items: Test Exception",
            ),
        ],
    )
    @patch.object(Storage, "get_objects")
    @patch("moonshot.src.connectors.connector.logger")
    def test_get_available_items_exception(
        self, mock_logger, mock_get_objects, exception, log_message
    ):
        # Mock the get_objects method to raise an exception
        mock_get_objects.side_effect = exception

        # Call the method and assert it raises the exception
        with pytest.raises(Exception) as excinfo:
            Connector.get_available_items()

        # Assert the logger error was called with the correct message
        assert str(excinfo.value) == "Test Exception"
        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][
            0
        ] == CONNECTOR_GET_AVAILABLE_ITEMS_ERROR.format(message="Test Exception")

    # ------------------------------------------------------------------------------
    # Test get_prediction functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "generated_prompt, connector, predicted_results, prompt_callback, exception",
        [
            (
                ConnectorPromptArguments(
                    prompt="prompt 1", prompt_index=1, target="target 1"
                ),
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                None,
                None,
            ),
            # Invalid ConnectorPromptArguments
            (
                None,
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR,
            ),
            (
                1234,
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR,
            ),
            (
                {},
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR,
            ),
            (
                [],
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR,
            ),
            (
                (),
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR,
            ),
            # Invalid ConnectorResponse
            (
                ConnectorPromptArguments(
                    prompt="prompt 2", prompt_index=2, target="target 2"
                ),
                None,
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR,
            ),
            (
                ConnectorPromptArguments(
                    prompt="prompt 2", prompt_index=2, target="target 2"
                ),
                1234,
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR,
            ),
            (
                ConnectorPromptArguments(
                    prompt="prompt 2", prompt_index=2, target="target 2"
                ),
                {},
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR,
            ),
            (
                ConnectorPromptArguments(
                    prompt="prompt 2", prompt_index=2, target="target 2"
                ),
                [],
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR,
            ),
            (
                ConnectorPromptArguments(
                    prompt="prompt 2", prompt_index=2, target="target 2"
                ),
                (),
                ["predicted result 1", "predicted result 2"],
                None,
                CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR,
            ),
            # Valid ConnectorPromptArguments and Connector with a callback function
            (
                ConnectorPromptArguments(
                    prompt="prompt 3", prompt_index=3, target="target 3"
                ),
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                ["predicted result 1", "predicted result 2"],
                MagicMock(),
                None,
            ),
        ],
    )
    async def test_get_prediction(
        self, generated_prompt, connector, predicted_results, prompt_callback, exception
    ):
        with patch(
            "moonshot.src.connectors.connector.Connector.get_response",
            return_value=predicted_results,
        ):
            with patch(
                "moonshot.src.connectors.connector.time.perf_counter",
                side_effect=[0, 0.5],
            ):
                if exception:
                    with pytest.raises(Exception) as exc_info:
                        await Connector.get_prediction(
                            generated_prompt, connector, prompt_callback
                        )
                    assert str(exc_info.value) == str(exception)
                else:
                    result = await Connector.get_prediction(
                        generated_prompt, connector, prompt_callback
                    )
                    assert result.predicted_results == predicted_results
                    assert result.duration == 0.5
                    if prompt_callback:
                        prompt_callback.assert_called_once_with(
                            generated_prompt, connector.id
                        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "generated_prompt, connector, predicted_results, prompt_callback, exception, expected_log_message",
        [
            # Valid ConnectorPromptArguments and Connector with an exception raised during prediction
            (
                ConnectorPromptArguments(
                    prompt="prompt 4", prompt_index=4, target="target 4"
                ),
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                None,
                None,
                Exception("prediction error"),
                CONNECTOR_GET_PREDICTION_ERROR.format(
                    connector_id="test_connector",
                    prompt_index=4,
                    message="prediction error",
                ),
            ),
            # Valid ConnectorPromptArguments and Connector with a callback function and an exception
            # raised during prediction
            (
                ConnectorPromptArguments(
                    prompt="prompt 5", prompt_index=5, target="target 5"
                ),
                Connector(
                    ConnectorEndpointArguments(
                        id="test_connector",
                        name="test connector",
                        connector_type="",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="model",
                        params={},
                    )
                ),
                None,
                MagicMock(),
                Exception("prediction error"),
                CONNECTOR_GET_PREDICTION_ERROR.format(
                    connector_id="test_connector",
                    prompt_index=5,
                    message="prediction error",
                ),
            ),
            # Valid ConnectorPromptArguments and Connector with an exception raised during prediction and logger check
            (
                ConnectorPromptArguments(
                    prompt="Test prompt", prompt_index=1, target=""
                ),
                Connector(
                    ConnectorEndpointArguments(
                        id="SampleId",
                        name="SampleName",
                        connector_type="SampleConnector",
                        uri="",
                        token="",
                        max_calls_per_second=1,
                        max_concurrency=1,
                        model="my-model",
                        params={},
                    )
                ),
                None,
                None,
                Exception("Test Exception"),
                CONNECTOR_GET_PREDICTION_ERROR.format(
                    connector_id="SampleId", prompt_index=1, message="Test Exception"
                ),
            ),
        ],
    )
    async def test_get_prediction_exception(
        self,
        generated_prompt,
        connector,
        predicted_results,
        prompt_callback,
        exception,
        expected_log_message,
    ):
        connector.get_response = AsyncMock(return_value=predicted_results)

        if exception:
            connector.get_response.side_effect = exception

        with patch(
            "moonshot.src.connectors.connector.time.perf_counter", side_effect=[0, 0.5]
        ):
            with patch("moonshot.src.connectors.connector.logger") as mock_logger:
                if exception:
                    with pytest.raises(Exception) as exc_info:
                        await Connector.get_prediction(
                            generated_prompt, connector, prompt_callback
                        )
                    assert str(exc_info.value) == str(exception)
                    mock_logger.error.assert_called_once()
                    assert mock_logger.error.call_args[0][0] == expected_log_message
                else:
                    result = await Connector.get_prediction(
                        generated_prompt, connector, prompt_callback
                    )
                    assert result.predicted_results == predicted_results
                    assert result.duration == 0.5
                    if prompt_callback:
                        prompt_callback.assert_called_once_with(
                            generated_prompt, connector.id
                        )

    # ------------------------------------------------------------------------------
    # Test set_system_prompt functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "system_prompt",
        [
            "New system prompt",
            "",
            "Another prompt with special characters !@#$%^&*()",
        ],
    )
    def test_set_system_prompt_success(self, system_prompt):
        # Mock Connector
        connector = Connector(
            ConnectorEndpointArguments(
                id="test_id",
                name="new_name",
                uri="",
                token="test_token",
                max_concurrency=5,
                max_calls_per_second=10,
                model="my-model",
                params={},
                connector_type="my-connector-type",
            )
        )

        # Call the method
        connector.set_system_prompt(system_prompt)

        # Assert the system prompt is set correctly
        assert connector.system_prompt == system_prompt

    @pytest.mark.parametrize(
        "system_prompt, expected_exception, expected_exception_error_message",
        [
            (None, ValueError, CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR),
            (123, ValueError, CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR),
            ([], ValueError, CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR),
            ((), ValueError, CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR),
            ({}, ValueError, CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR),
        ],
    )
    def test_set_system_prompt_error(
        self, system_prompt, expected_exception, expected_exception_error_message
    ):
        # Mock Connector
        connector = Connector(
            ConnectorEndpointArguments(
                id="test_id",
                name="new_name",
                uri="",
                token="test_token",
                max_concurrency=5,
                max_calls_per_second=10,
                model="my-model",
                params={},
                connector_type="my-connector-type",
            )
        )

        # Call the method
        with pytest.raises(expected_exception) as exc_info:
            connector.set_system_prompt(system_prompt)

            # Assert the exception message
            assert (
                str(exc_info.value) == expected_exception_error_message
            ), "The exception message should match the expected message."
