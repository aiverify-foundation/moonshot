from unittest.mock import patch

import pytest

from moonshot.integrations.web_api.schemas.endpoint_create_dto import (
    EndpointCreateDTO,
    EndpointUpdateDTO,
)
from moonshot.integrations.web_api.schemas.endpoint_response_model import (
    EndpointDataModel,
)
from moonshot.integrations.web_api.services.endpoint_service import EndpointService
from moonshot.integrations.web_api.services.utils.exceptions_handler import (
    ServiceException,
)

# Mock data for successful API calls
MOCK_ENDPOINT = {
    "id": "endpoint-1",
    "name": "Endpoint 1",
    "connector_type": "openai-connector",
    "uri": "",
    "token": "ADD_TOKEN",
    "max_calls_per_second": 10,
    "max_concurrency": 1,
    "model": "gpt-3.5-turbo",
    "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
    "created_date": "2024-05-22 17:01:37",
}

MOCK_ENDPOINTS = [MOCK_ENDPOINT]
MOCK_ENDPOINT_NAMES = [endpoint["name"] for endpoint in MOCK_ENDPOINTS]
MOCK_CONNECTOR_TYPES = [
    "together-connector",
    "openai-connector",
    "claude2-connector",
    "huggingface-connector",
]

MOCK_CREATE_ENDPOINT = EndpointCreateDTO(
    name="New Endpoint",
    connector_type="openai-connector",
    uri="",
    token="YOUR TOKEN",
    max_calls_per_second=10,
    max_concurrency=1,
    model="my-gpt-3.5-turbo",
    params={},
)
MOCK_UPDATE_ENDPOINT = EndpointUpdateDTO(
    token="UPDATE TOKEN",
)


@pytest.fixture
def endpoint_service():
    return EndpointService()


@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_get_all_endpoints_success(mock_moonshot_api, endpoint_service):
    """
    Test case for successful retrieval of all endpoints.
    """
    mock_moonshot_api.api_get_all_endpoint.return_value = MOCK_ENDPOINTS
    endpoints = endpoint_service.get_all_endpoints()
    expected_endpoints = [
        EndpointDataModel.model_validate(endpoint) for endpoint in MOCK_ENDPOINTS
    ]
    assert endpoints == expected_endpoints
    mock_moonshot_api.api_get_all_endpoint.assert_called_once()


@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_get_all_endpoints_names_success(mock_moonshot_api, endpoint_service):
    """
    Test case for successful retrieval of all endpoint names.
    """
    mock_moonshot_api.api_get_all_endpoint_name.return_value = MOCK_ENDPOINT_NAMES
    endpoint_names = endpoint_service.get_all_endpoints_names()
    assert endpoint_names == MOCK_ENDPOINT_NAMES
    mock_moonshot_api.api_get_all_endpoint_name.assert_called_once()


@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_get_all_connectors_success(mock_moonshot_api, endpoint_service):
    """
    Test case for successful retrieval of all connector types.
    """
    mock_moonshot_api.api_get_all_connector_type.return_value = MOCK_CONNECTOR_TYPES
    connector_types = endpoint_service.get_all_connectors()
    assert connector_types == MOCK_CONNECTOR_TYPES
    mock_moonshot_api.api_get_all_connector_type.assert_called_once()


# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_get_all_endpoints_exceptions(
    mock_moonshot_api, exception, error_code, endpoint_service
):
    """
    Test case for exceptions during retrieval of all endpoints.
    """
    mock_moonshot_api.api_get_all_endpoint.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        endpoint_service.get_all_endpoints()
    assert exc_info.value.error_code == error_code


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_get_all_endpoints_names_exceptions(
    mock_moonshot_api, exception, error_code, endpoint_service
):
    """
    Test case for exceptions during retrieval of all endpoint names.
    """
    mock_moonshot_api.api_get_all_endpoint_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        endpoint_service.get_all_endpoints_names()
    assert exc_info.value.error_code == error_code


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_get_all_connectors_exceptions(
    mock_moonshot_api, exception, error_code, endpoint_service
):
    """
    Test case for exceptions during retrieval of all connector types.
    """
    mock_moonshot_api.api_get_all_connector_type.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        endpoint_service.get_all_connectors()
    assert exc_info.value.error_code == error_code


@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_create_endpoint_success(mock_moonshot_api, endpoint_service):
    """
    Test case for successful creation of an endpoint.
    """
    endpoint_service.add_endpoint(MOCK_CREATE_ENDPOINT)
    mock_moonshot_api.api_create_endpoint.assert_called_once_with(
        name=MOCK_CREATE_ENDPOINT.name,
        connector_type=MOCK_CREATE_ENDPOINT.connector_type,
        uri=MOCK_CREATE_ENDPOINT.uri,
        token=MOCK_CREATE_ENDPOINT.token,
        model=MOCK_CREATE_ENDPOINT.model,
        max_calls_per_second=MOCK_CREATE_ENDPOINT.max_calls_per_second,
        max_concurrency=MOCK_CREATE_ENDPOINT.max_concurrency,
        params=MOCK_CREATE_ENDPOINT.params,
    )


@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_update_endpoint_success(mock_moonshot_api, endpoint_service):
    """
    Test case for successful update of an endpoint.
    """
    endpoint_service.update_endpoint("endpoint_id", MOCK_UPDATE_ENDPOINT)
    mock_moonshot_api.api_update_endpoint.assert_called_once_with(
        ep_id="endpoint_id", token=MOCK_UPDATE_ENDPOINT.token
    )


@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_delete_endpoint_success(mock_moonshot_api, endpoint_service):
    """
    Test case for successful deletion of an endpoint.
    """
    endpoint_service.delete_endpoint("endpoint_id")
    mock_moonshot_api.api_delete_endpoint.assert_called_once_with("endpoint_id")


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_create_endpoint_exception(
    mock_moonshot_api, endpoint_service, exception, error_code
):
    """
    Test case for exceptions during creation of an endpoint.
    """
    mock_moonshot_api.api_create_endpoint.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        endpoint_service.add_endpoint(MOCK_CREATE_ENDPOINT)
    assert exc_info.value.error_code == error_code


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_update_endpoint_exception(
    mock_moonshot_api, endpoint_service, exception, error_code
):
    """
    Test case for exceptions during update of an endpoint.
    """
    mock_moonshot_api.api_update_endpoint.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        endpoint_service.update_endpoint("endpoint_id", MOCK_UPDATE_ENDPOINT)
    assert exc_info.value.error_code == error_code


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch("moonshot.integrations.web_api.services.endpoint_service.moonshot_api")
def test_delete_endpoint_exception(
    mock_moonshot_api, endpoint_service, exception, error_code
):
    """
    Test case for exceptions during deletion of an endpoint.
    """
    mock_moonshot_api.api_delete_endpoint.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        endpoint_service.delete_endpoint("endpoint_id")
    assert exc_info.value.error_code == error_code
