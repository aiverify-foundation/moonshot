import copy
from datetime import datetime
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage import Storage

CONNECTOR_ENDPOINT_CREATE_ERROR = (
    "[ConnectorEndpoint] Failed to create connector endpoint: {message}"
)
CONNECTOR_ENDPOINT_GET_AVAILABLE_ITEMS_ERROR = (
    "[ConnectorEndpoint] Failed to get available connector endpoints: {message}"
)
CONNECTOR_ENDPOINT_UPDATE_ERROR = (
    "[ConnectorEndpoint] Failed to update connector endpoint: {message}"
)

class TestCollectionConnectorEndpoint:
    # ------------------------------------------------------------------------------
    # CONNECTOR ENDPOINT - create
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_args, expected_ep_id",
        [
            (
                ConnectorEndpointArguments(
                    id="",
                    name="Test Endpoint",
                    connector_type="type1",
                    uri="http://example.com",
                    token="token123",
                    max_calls_per_second=10,
                    max_concurrency=5,
                    model="model1",
                    params={"param1": "value1"},
                ),
                "test-endpoint",
            ),
            (
                ConnectorEndpointArguments(
                    id="",
                    name="Another Endpoint",
                    connector_type="type2",
                    uri="http://example.org",
                    token="token456",
                    max_calls_per_second=20,
                    max_concurrency=10,
                    model="model2",
                    params={"param2": "value2"},
                ),
                "another-endpoint",
            ),
            (
                {
                    "id": "",
                    "name": "Test Endpoint",
                    "connector_type": "type1",
                    "uri": "http://example.com",
                    "token": "token123",
                    "max_calls_per_second": 10,
                    "max_concurrency": 5,
                    "model": "model1",
                    "params": {"param1": "value1"},
                },
                "test-endpoint",
            ),
        ],
    )
    @patch.object(Storage, "create_object")
    def test_create_success(self, mock_create_object, ep_args, expected_ep_id):
        result = ConnectorEndpoint.create(ep_args)
        assert result == expected_ep_id
        if isinstance(ep_args, ConnectorEndpointArguments):
            mock_create_object.assert_called_once_with(
                EnvVariables.CONNECTORS_ENDPOINTS.name,
                expected_ep_id,
                {
                    "name": ep_args.name,
                    "connector_type": ep_args.connector_type,
                    "uri": ep_args.uri,
                    "token": ep_args.token,
                    "max_calls_per_second": ep_args.max_calls_per_second,
                    "max_concurrency": ep_args.max_concurrency,
                    "model": ep_args.model,
                    "params": ep_args.params,
                },
                "json",
            )
        elif isinstance(ep_args, dict):
            mock_create_object.assert_called_once_with(
                EnvVariables.CONNECTORS_ENDPOINTS.name,
                expected_ep_id,
                {
                    "name": ep_args["name"],
                    "connector_type": ep_args["connector_type"],
                    "uri": ep_args["uri"],
                    "token": ep_args["token"],
                    "max_calls_per_second": ep_args["max_calls_per_second"],
                    "max_concurrency": ep_args["max_concurrency"],
                    "model": ep_args["model"],
                    "params": ep_args["params"],
                },
                "json",
            )
        else:
            assert False

    @pytest.mark.parametrize(
        "ep_args, expected_exception, expected_result",
        [
            (
                None,
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            (
                1234,
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            (
                [],
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            ({}, ValidationError, "Field required"),
            (
                (),
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            (
                True,
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
        ],
    )
    @patch.object(Storage, "create_object")
    def test_create_invalid_values(
        self, mock_create_object, ep_args, expected_exception, expected_result
    ):
        with pytest.raises(expected_exception) as excinfo:
            _ = ConnectorEndpoint.create(ep_args)
        assert expected_result in excinfo.value.errors()[0]["msg"]

    @pytest.mark.parametrize(
        "ep_args, exception_message",
        [
            (
                ConnectorEndpointArguments(
                    id="",
                    name="Failing Endpoint",
                    connector_type="type3",
                    uri="http://example.fail",
                    token="token789",
                    max_calls_per_second=30,
                    max_concurrency=15,
                    model="model3",
                    params={"param3": "value3"},
                ),
                "Storage error",
            ),
        ],
    )
    @patch.object(Storage, "create_object", side_effect=Exception("Storage error"))
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.logger")
    def test_create_failure(
        self, mock_logger, mock_create_object, ep_args, exception_message
    ):
        with pytest.raises(Exception) as excinfo:
            ConnectorEndpoint.create(ep_args)
        assert str(excinfo.value) == exception_message
        mock_logger.error.assert_called_once_with(
            CONNECTOR_ENDPOINT_CREATE_ERROR.format(message=exception_message)
        )

    # ------------------------------------------------------------------------------
    # CONNECTOR ENDPOINT - read
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_id, mock_return_value, expected_result",
        [
            (
                "test-endpoint",
                {
                    "name": "Test Endpoint",
                    "connector_type": "Test Type",
                    "uri": "http://test.uri",
                    "token": "test_token",
                    "max_calls_per_second": 10,
                    "max_concurrency": 5,
                    "model": "test_model",
                    "params": {},
                },
                ConnectorEndpointArguments(
                    id="test-endpoint",
                    name="Test Endpoint",
                    connector_type="Test Type",
                    uri="http://test.uri",
                    token="test_token",
                    max_calls_per_second=10,
                    max_concurrency=5,
                    model="test_model",
                    params={},
                    created_date="2023-10-01 12:00:00",
                ),
            ),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.read_object")
    @patch(
        "moonshot.src.connectors_endpoints.connector_endpoint.Storage.get_creation_datetime"
    )
    def test_read_success(
        self,
        mock_get_creation_datetime,
        mock_read_object,
        ep_id,
        mock_return_value,
        expected_result,
    ):
        mock_read_object.return_value = mock_return_value
        mock_get_creation_datetime.return_value = datetime(2023, 10, 1, 12, 0, 0)

        result = ConnectorEndpoint.read(ep_id)

        assert isinstance(result, ConnectorEndpointArguments)
        assert result == expected_result

    @pytest.mark.parametrize(
        "ep_id, expected_exception, expected_result",
        [
            (None, ValidationError, "Input should be a valid string"),
            (1234, ValidationError, "Input should be a valid string"),
            ([], ValidationError, "Input should be a valid string"),
            ({}, ValidationError, "Input should be a valid string"),
            ((), ValidationError, "Input should be a valid string"),
            (True, ValidationError, "Input should be a valid string"),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.read_object")
    def test_read_invalid_values(
        self, mock_read_object, ep_id, expected_exception, expected_result
    ):
        with pytest.raises(expected_exception) as excinfo:
            _ = ConnectorEndpoint.read(ep_id)
        assert expected_result in excinfo.value.errors()[0]["msg"]

    @pytest.mark.parametrize(
        "ep_id, expected_exception_message",
        [
            (
                "test-endpoint",
                "[ConnectorEndpoint] Failed to read connector endpoint: Invalid connector endpoint id - test-endpoint",
            ),
            (
                "test1-endpoint",
                "[ConnectorEndpoint] Failed to read connector endpoint: Invalid connector endpoint id - test1-endpoint",
            ),
        ],
    )
    @patch(
        "moonshot.src.connectors_endpoints.connector_endpoint.ConnectorEndpoint._read_endpoint"
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.logger")
    def test_read_endpoint_returns_none(
        self, mock_logger, mock_read_endpoint, ep_id, expected_exception_message
    ):
        mock_read_endpoint.return_value = None

        with pytest.raises(RuntimeError):
            ConnectorEndpoint.read(ep_id)
        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][0] == expected_exception_message

    @pytest.mark.parametrize(
        "ep_id, exception_message, expected_exception_message",
        [
            (
                "test-endpoint",
                "Read endpoint error",
                "[ConnectorEndpoint] Failed to read connector endpoint: Read endpoint error",
            ),
            (
                "another-endpoint",
                "Another read endpoint error",
                "[ConnectorEndpoint] Failed to read connector endpoint: Another read endpoint error",
            ),
        ],
    )
    @patch(
        "moonshot.src.connectors_endpoints.connector_endpoint.ConnectorEndpoint._read_endpoint"
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.logger")
    def test_read_endpoint_throws_exception(
        self,
        mock_logger,
        mock_read_endpoint,
        ep_id,
        exception_message,
        expected_exception_message,
    ):
        mock_read_endpoint.side_effect = RuntimeError(exception_message)

        with pytest.raises(RuntimeError):
            ConnectorEndpoint.read(ep_id)
        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][0] == expected_exception_message

    # ------------------------------------------------------------------------------
    # CONNECTOR ENDPOINT - update
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_args, expected_result",
        [
            (
                ConnectorEndpointArguments(
                    id="valid_endpoint_id",
                    name="Endpoint 1",
                    connector_type="type1",
                    uri="uri1",
                    token="token1",
                    max_calls_per_second=10,
                    max_concurrency=5,
                    model="model1",
                    params={},
                ),
                True,
            ),
            (
                {
                    "id": "invalid_endpoint_id",
                    "name": "Endpoint 2",
                    "connector_type": "type2",
                    "uri": "uri2",
                    "token": "token2",
                    "max_calls_per_second": 20,
                    "max_concurrency": 10,
                    "model": "model2",
                    "params": {},
                },
                True,
            ),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.create_object")
    def test_update_success(self, mock_create_object, ep_args, expected_result):
        mock_create_object.return_value = None  # Mocking successful update

        result = ConnectorEndpoint.update(ep_args)
        assert result == expected_result

        if isinstance(ep_args, ConnectorEndpointArguments):
            ep_info = ep_args.to_dict()
            ep_info.pop("id", None)
            ep_info.pop("created_date", None)
            mock_create_object.assert_called_once_with(
                EnvVariables.CONNECTORS_ENDPOINTS.name, ep_args.id, ep_info, "json"
            )
        elif isinstance(ep_args, dict):
            ep_info = copy.deepcopy(ep_args)
            ep_info.pop("id", None)
            ep_info.pop("created_date", None)
            mock_create_object.assert_called_once_with(
                EnvVariables.CONNECTORS_ENDPOINTS.name, ep_args["id"], ep_info, "json"
            )
        else:
            assert False

    @pytest.mark.parametrize(
        "ep_args, mocked_exception",
        [
            (
                ConnectorEndpointArguments(
                    id="invalid_endpoint_id",
                    name="Endpoint 2",
                    connector_type="type2",
                    uri="uri2",
                    token="token2",
                    max_calls_per_second=20,
                    max_concurrency=10,
                    model="model2",
                    params={},
                ),
                Exception("Update error"),
            ),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.create_object")
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.logger")
    def test_update_exception(
        self, mock_logger, mock_create_object, ep_args, mocked_exception
    ):
        mock_create_object.side_effect = mocked_exception

        with pytest.raises(Exception) as excinfo:
            ConnectorEndpoint.update(ep_args)

        assert str(excinfo.value) == str(mocked_exception)
        ep_info = ep_args.to_dict()
        ep_info.pop("id", None)
        ep_info.pop("created_date", None)
        mock_create_object.assert_called_once_with(
            EnvVariables.CONNECTORS_ENDPOINTS.name, ep_args.id, ep_info, "json"
        )
        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][
            0
        ] == CONNECTOR_ENDPOINT_UPDATE_ERROR.format(message=str(mocked_exception))

    @pytest.mark.parametrize(
        "invalid_ep_args,expected_exception,expected_result",
        [
            (
                None,
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            (
                "",
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            ({}, ValidationError, "Field required"),
            (
                [],
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            (
                (),
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
            (
                1234,
                ValidationError,
                "Input should be a valid dictionary or instance of ConnectorEndpointArguments",
            ),
        ],
    )
    def test_update_invalid_arguments(
        self, invalid_ep_args, expected_exception, expected_result
    ):
        with pytest.raises(expected_exception) as excinfo:
            ConnectorEndpoint.update(invalid_ep_args)
        assert expected_result in excinfo.value.errors()[0]["msg"]

    # ------------------------------------------------------------------------------
    # CONNECTOR ENDPOINT - delete
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_id, expected_result",
        [
            ("valid_endpoint_id", True),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.delete_object")
    def test_delete_success(self, mock_delete_object, ep_id, expected_result):
        mock_delete_object.return_value = None  # Mocking successful deletion

        result = ConnectorEndpoint.delete(ep_id)

        assert result == expected_result
        mock_delete_object.assert_called_once_with(
            EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json"
        )

    @pytest.mark.parametrize(
        "invalid_ep_id,expected_result",
        [
            (None, "Input should be a valid string"),
            ({}, "Input should be a valid string"),
            ([], "Input should be a valid string"),
            ((), "Input should be a valid string"),
            (1234, "Input should be a valid string"),
        ],
    )
    def test_delete_invalid_arguments(self, invalid_ep_id, expected_result):
        with pytest.raises(ValidationError) as excinfo:
            ConnectorEndpoint.delete(invalid_ep_id)
        assert expected_result in excinfo.value.errors()[0]["msg"]

    @pytest.mark.parametrize(
        "ep_id, mocked_exception",
        [
            ("invalid_endpoint_id", Exception("Deletion error")),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.delete_object")
    def test_delete_exception(self, mock_delete_object, ep_id, mocked_exception):
        mock_delete_object.side_effect = mocked_exception

        with pytest.raises(Exception) as excinfo:
            ConnectorEndpoint.delete(ep_id)

        assert str(excinfo.value) == str(mocked_exception)
        mock_delete_object.assert_called_once_with(
            EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json"
        )

    # ------------------------------------------------------------------------------
    # CONNECTOR ENDPOINT - get_available_items
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mocked_eps, expected_ids, expected_eps",
        [
            (
                ["endpoint1.json", "endpoint2.json"],
                ["endpoint1", "endpoint2"],
                [
                    ConnectorEndpointArguments(
                        id="endpoint1",
                        name="Endpoint 1",
                        connector_type="type1",
                        uri="uri1",
                        token="token1",
                        max_calls_per_second=10,
                        max_concurrency=5,
                        model="model1",
                        params={},
                    ),
                    ConnectorEndpointArguments(
                        id="endpoint2",
                        name="Endpoint 2",
                        connector_type="type2",
                        uri="uri2",
                        token="token2",
                        max_calls_per_second=20,
                        max_concurrency=10,
                        model="model2",
                        params={},
                    ),
                ],
            ),
            (
                ["__init__.json", "endpoint3.json"],
                ["endpoint3"],
                [
                    ConnectorEndpointArguments(
                        id="endpoint3",
                        name="Endpoint 3",
                        connector_type="type3",
                        uri="uri3",
                        token="token3",
                        max_calls_per_second=30,
                        max_concurrency=15,
                        model="model3",
                        params={},
                    )
                ],
            ),
            ([], [], []),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.get_objects")
    @patch(
        "moonshot.src.connectors_endpoints.connector_endpoint.ConnectorEndpoint._read_endpoint"
    )
    def test_get_available_items(
        self,
        mock_read_endpoint,
        mock_get_objects,
        mocked_eps,
        expected_ids,
        expected_eps,
    ):
        mock_get_objects.return_value = mocked_eps
        mock_read_endpoint.side_effect = lambda ep_id: {
            "id": ep_id,
            "name": f"Endpoint {ep_id[-1]}",
            "connector_type": f"type{ep_id[-1]}",
            "uri": f"uri{ep_id[-1]}",
            "token": f"token{ep_id[-1]}",
            "max_calls_per_second": int(ep_id[-1]) * 10,
            "max_concurrency": int(ep_id[-1]) * 5,
            "model": f"model{ep_id[-1]}",
            "params": {},
        }

        ids, eps = ConnectorEndpoint.get_available_items()

        assert ids == expected_ids
        assert eps == expected_eps

    @pytest.mark.parametrize(
        "mocked_exception",
        [
            (Exception("Storage error")),
        ],
    )
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.Storage.get_objects")
    @patch("moonshot.src.connectors_endpoints.connector_endpoint.logger")
    def test_get_available_items_exception(
        self, mock_logger, mock_get_objects, mocked_exception
    ):
        mock_get_objects.side_effect = mocked_exception

        with pytest.raises(Exception) as excinfo:
            ConnectorEndpoint.get_available_items()

        assert str(excinfo.value) == str(mocked_exception)
        mock_logger.error.assert_called_once()
        assert mock_logger.error.call_args[0][
            0
        ] == CONNECTOR_ENDPOINT_GET_AVAILABLE_ITEMS_ERROR.format(
            message=str(mocked_exception)
        )
