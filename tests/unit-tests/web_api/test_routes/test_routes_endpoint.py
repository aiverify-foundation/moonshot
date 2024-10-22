import pytest

from moonshot.integrations.web_api.schemas.endpoint_response_model import (
    EndpointDataModel,
)
from moonshot.integrations.web_api.services.utils.exceptions_handler import (
    ServiceException,
)


@pytest.mark.parametrize(
    "endpoint_data, exception, expected_status, expected_response",
    [
        # Success Scenario
        (
            {
                "name": "test-endpoint",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "HIDDEN_TOKEN",
                "max_calls_per_second": 10,
                "max_concurrency": 1,
                "model": "gpt-3.5-turbo",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
            },
            None,
            200,
            {"message": "Endpoint added successfully"},
        ),
        # Exception Scenario
        (
            {
                "name": "test-endpoint",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "HIDDEN_TOKEN",
                "max_calls_per_second": 10,
                "max_concurrency": 1,
                "model": "gpt-3.5-turbo",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
            },
            ServiceException(
                "A file not found error occurred", "add_endpoint", "FileNotFound"
            ),
            404,
            None,
        ),
        (
            {
                "name": "test-endpoint",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "HIDDEN_TOKEN",
                "max_calls_per_second": 10,
                "max_concurrency": 1,
                "model": "gpt-3.5-turbo",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
            },
            ServiceException(
                "A validation error occurred", "add_endpoint", "ValidationError"
            ),
            400,
            None,
        ),
        (
            {
                "name": "test-endpoint",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "HIDDEN_TOKEN",
                "max_calls_per_second": 10,
                "max_concurrency": 1,
                "model": "gpt-3.5-turbo",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
            },
            ServiceException(
                "An unexpected error occurred", "add_endpoint", "UnknownError"
            ),
            500,
            None,
        ),
    ],
)
def test_create_endpoint(
    test_client,
    mock_endpoint_service,
    endpoint_data,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.add_endpoint.side_effect = exception
    else:
        mock_endpoint_service.add_endpoint.return_value = endpoint_data

    response = test_client.post("/api/v1/llm-endpoints", json=endpoint_data)

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        if expected_status != 422:
            assert response.json() == expected_response


@pytest.mark.parametrize(
    "mock_response, exception, expected_status, expected_response",
    [
        # Success Scenario
        (
            [
                {
                    "id": "test-endpoint-1",
                    "name": "test-endpoint-1",
                    "connector_type": "openai-connector",
                    "uri": "",
                    "token": "HIDDEN_TOKEN",
                    "max_calls_per_second": 10,
                    "max_concurrency": 1,
                    "model": "gpt-3.5-turbo",
                    "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
                    "created_date": "2024-05-20 17:13:35",
                },
                {
                    "id": "test-endpoint-2",
                    "name": "test-endpoint-2",
                    "connector_type": "openai-connector",
                    "uri": "",
                    "token": "HIDDEN_TOKEN",
                    "max_calls_per_second": 10,
                    "max_concurrency": 1,
                    "model": "gpt-3.5-turbo",
                    "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
                    "created_date": "2024-05-20 17:13:35",
                },
            ],
            None,
            200,
            [
                {
                    "id": "test-endpoint-1",
                    "name": "test-endpoint-1",
                    "connector_type": "openai-connector",
                    "uri": "",
                    "token": "HIDDEN_TOKEN",
                    "max_calls_per_second": 10,
                    "max_concurrency": 1,
                    "model": "gpt-3.5-turbo",
                    "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
                    "created_date": "2024-05-20 17:13:35",
                },
                {
                    "id": "test-endpoint-2",
                    "name": "test-endpoint-2",
                    "connector_type": "openai-connector",
                    "uri": "",
                    "token": "HIDDEN_TOKEN",
                    "max_calls_per_second": 10,
                    "max_concurrency": 1,
                    "model": "gpt-3.5-turbo",
                    "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
                    "created_date": "2024-05-20 17:13:35",
                },
            ],
        ),
        # Exception cases
        (
            None,
            ServiceException(
                "A file not found error occurred", "get_all_endpoints", "FileNotFound"
            ),
            404,
            None,
        ),
        (
            None,
            ServiceException(
                "A validation error occurred", "get_all_endpoints", "ValidationError"
            ),
            400,
            None,
        ),
        (
            None,
            ServiceException(
                "An value error occurred", "get_all_endpoints", "ValueError"
            ),
            500,
            None,
        ),
    ],
)
def test_get_all_endpoints(
    test_client,
    mock_endpoint_service,
    mock_response,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.get_all_endpoints.side_effect = exception
    else:
        mock_response_model = [EndpointDataModel(**data) for data in mock_response]
        mock_endpoint_service.get_all_endpoints.return_value = mock_response_model

    response = test_client.get("/api/v1/llm-endpoints")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        expected_response_model = [
            EndpointDataModel(**data) for data in expected_response
        ]
        for model in expected_response_model:
            model.mask_token()
        expected_response_dicts = [model.dict() for model in expected_response_model]
        assert response.json() == expected_response_dicts


@pytest.mark.parametrize(
    "mock_response, exception, expected_status, expected_response",
    [
        # Success Scenario
        (
            ["test-endpoint-1", "test-endpoint-2"],
            None,
            200,
            ["test-endpoint-1", "test-endpoint-2"],
        ),
        # Exception cases
        (
            None,
            ServiceException(
                "A file not found error occurred",
                "get_all_endpoints_names",
                "FileNotFound",
            ),
            404,
            None,
        ),
        (
            None,
            ServiceException(
                "A validation error occurred",
                "get_all_endpoints_names",
                "ValidationError",
            ),
            400,
            None,
        ),
        (
            None,
            ServiceException(
                "An value error occurred", "get_all_endpoints_names", "ValueError"
            ),
            500,
            None,
        ),
    ],
)
def test_get_all_endpoints_name(
    test_client,
    mock_endpoint_service,
    mock_response,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.get_all_endpoints_names.side_effect = exception
    else:
        mock_endpoint_service.get_all_endpoints_names.return_value = mock_response

    response = test_client.get("/api/v1/llm-endpoints/name")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "endpoint_id, mock_response, exception, expected_status, expected_response",
    [
        # Success Scenario
        (
            "test-endpoint-1",
            {
                "id": "test-endpoint-1",
                "name": "test-endpoint-1",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "HIDDEN_TOKEN",
                "max_calls_per_second": 10,
                "max_concurrency": 1,
                "model": "gpt-3.5-turbo",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
                "created_date": "2024-05-20 17:13:35",
            },
            None,
            200,
            {
                "id": "test-endpoint-1",
                "name": "test-endpoint-1",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "HIDDEN_TOKEN",
                "max_calls_per_second": 10,
                "max_concurrency": 1,
                "model": "gpt-3.5-turbo",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
                "created_date": "2024-05-20 17:13:35",
            },
        ),
        # Exception cases
        (
            "test-endpoint-1",
            None,
            ServiceException(
                "A file not found error occurred", "get_endpoint", "FileNotFound"
            ),
            404,
            None,
        ),
        (
            "test-endpoint-1",
            None,
            ServiceException(
                "A validation error occurred", "get_endpoint", "ValidationError"
            ),
            400,
            None,
        ),
        (
            "test-endpoint-1",
            None,
            ServiceException("An value error occurred", "get_endpoint", "ValueError"),
            500,
            None,
        ),
    ],
)
def test_get_endpoint(
    test_client,
    mock_endpoint_service,
    endpoint_id,
    mock_response,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.get_endpoint.side_effect = exception
    else:
        mock_response_model = EndpointDataModel(**mock_response)
        mock_endpoint_service.get_endpoint.return_value = mock_response_model

    response = test_client.get(f"/api/v1/llm-endpoints/{endpoint_id}")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        expected_response_model = EndpointDataModel(**expected_response)
        expected_response_model.mask_token()
        expected_dict = expected_response_model.dict()
        assert response.json() == expected_dict


@pytest.mark.parametrize(
    "endpoint_id, mock_response, exception, expected_status, expected_response",
    [
        # Success Scenario
        (
            "test-endpoint-1",
            {"uri": "updated-test-endpoint-1"},
            None,
            200,
            {"message": "Endpoint updated successfully"},
        ),
        # Exception cases
        (
            "test-endpoint-1",
            {"uri": "updated-test-endpoint-1"},
            ServiceException(
                "A file not found error occurred", "update_endpoint", "FileNotFound"
            ),
            404,
            None,
        ),
        (
            "test-endpoint-1",
            {"uri": "updated-test-endpoint-1"},
            ServiceException(
                "A validation error occurred", "update_endpoint", "ValidationError"
            ),
            400,
            None,
        ),
        (
            "test-endpoint-1",
            {"uri": "updated-test-endpoint-1"},
            ServiceException(
                "An value error occurred", "update_endpoint", "ValueError"
            ),
            500,
            None,
        ),
    ],
)
def test_update_endpoint(
    test_client,
    mock_endpoint_service,
    endpoint_id,
    mock_response,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.update_endpoint.side_effect = exception
    else:
        mock_endpoint_service.update_endpoint.return_value = mock_response

    response = test_client.put(
        f"/api/v1/llm-endpoints/{endpoint_id}", json=mock_response
    )

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "endpoint_id, exception, expected_status, expected_response",
    [
        # Success Scenario
        ("test-endpoint-1", None, 200, {"message": "Endpoint deleted successfully"}),
        # Exception cases
        (
            "test-endpoint-1",
            ServiceException(
                "A file not found error occurred", "delete_endpoint", "FileNotFound"
            ),
            404,
            None,
        ),
        (
            "test-endpoint-1",
            ServiceException(
                "A validation error occurred", "delete_endpoint", "ValidationError"
            ),
            400,
            None,
        ),
        (
            "test-endpoint-1",
            ServiceException(
                "An value error occurred", "delete_endpoint", "ValueError"
            ),
            500,
            None,
        ),
    ],
)
def test_delete_endpoint(
    test_client,
    mock_endpoint_service,
    endpoint_id,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.delete_endpoint.side_effect = exception

    response = test_client.delete(f"/api/v1/llm-endpoints/{endpoint_id}")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "mock_response, exception, expected_status, expected_response",
    [
        # Success Scenario
        (
            [
                "together-connector",
                "openai-connector",
                "claude2-connector",
                "huggingface-connector",
            ],
            None,
            200,
            [
                "together-connector",
                "openai-connector",
                "claude2-connector",
                "huggingface-connector",
            ],
        ),
        # Exception cases
        (
            None,
            ServiceException(
                "A file not found error occurred", "get_all_connectors", "FileNotFound"
            ),
            404,
            None,
        ),
        (
            None,
            ServiceException(
                "A validation error occurred", "get_all_connectors", "ValidationError"
            ),
            400,
            None,
        ),
        (
            None,
            ServiceException(
                "An value error occurred", "get_all_connectors", "ValueError"
            ),
            500,
            None,
        ),
    ],
)
def test_get_connectors(
    test_client,
    mock_endpoint_service,
    mock_response,
    expected_status,
    exception,
    expected_response,
):
    if exception:
        mock_endpoint_service.get_all_connectors.side_effect = exception
    else:
        mock_endpoint_service.get_all_connectors.return_value = mock_response

    response = test_client.get("/api/v1/connectors")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response
