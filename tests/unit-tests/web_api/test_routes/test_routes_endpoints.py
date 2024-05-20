from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from moonshot.integrations.web_api.container import Container
from moonshot.integrations.web_api.services.endpoint_service import EndpointService
import pytest
from moonshot.integrations.web_api.app import create_app
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.endpoint_response_model import EndpointDataModel

# Create a mock instance of EndpointService
mock_endpoint_service = Mock(spec=EndpointService)

# Create a container for testing and override the EndpointService dependency
test_container = Container()
test_container.config.from_default()  
test_container.endpoint_service.override(mock_endpoint_service)

# Wire the container
test_container.wire(modules=["moonshot.integrations.web_api.routes"])

# Create a new FastAPI app instance for testing
app = create_app(test_container.config)

# Use TestClient with the app instance
client = TestClient(app)

# Override the EndpointService dependency in the container
Container.endpoint_service.override(mock_endpoint_service)

class MockEndpointDataModel(EndpointDataModel):
    def mask_token(self):
        super().mask_token()  # Call the actual implementation if needed
        # Or you can mock the behavior directly if you don't want to rely on the actual implementation
        # self.token = "********"

@pytest.fixture
def mock_endpoint_data_model():
    return MockEndpointDataModel
pytest.mark.parametrize("endpoint_data, expected_status", [
    # Success scenario
    (
        {
            "name": "Test Endpoint",
            "connector_type": "Test Connector",
            "uri": "http://test-uri.com",
            "token": "test-token",
            "max_calls_per_second": 10,
            "max_concurrency": 5,
            "params": {"param1": "value1"}
        },
        200
    ),
    # Missing 'name'
    (
        {
            "connector_type": "Test Connector",
            "uri": "http://test-uri.com",
            "token": "test-token",
            "max_calls_per_second": 10,
            "max_concurrency": 5,
            "params": {"param1": "value1"}
        },
        422
    ),
    # All fields missing
    (
        {},
        422
    )
])
def test_add_new_endpoint(endpoint_data, expected_status):
    # Set up the return value for the mock if it's a success scenario
    if expected_status == 200:
        mock_endpoint_service.add_endpoint.return_value = {"message": "Endpoint added successfully"}

    response = client.post("/api/v1/llm-endpoints", json=endpoint_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize("mock_return_value, expected_status, expected_response", [
    # Test get all endpoints success
    (
        [
            {
                "id": "test-endpoint-1",
                "name": "Test Endpoint 1",
                "connector_type": "Test Connector 1",
                "uri": "http://test-uri-1.com",
                "token": "test-token-1",
                "max_calls_per_second": 10,
                "max_concurrency": 5,
                "params": {"param1": "value1"},
                "created_date": "2023-01-01"
            },
            {
                "id": "test-endpoint-2",
                "name": "Test Endpoint 2",
                "connector_type": "Test Connector 2",
                "uri": "http://test-uri-2.com",
                "token": "test-token-2",
                "max_calls_per_second": 15,
                "max_concurrency": 10,
                "params": {"param2": "value2"},
                "created_date": "2023-01-02"
            }
        ],
        200,
        [
            {
                "id": "test-endpoint-1",
                "name": "Test Endpoint 1",
                "connector_type": "Test Connector 1",
                "uri": "http://test-uri-1.com",
                "token": "test-token-1",
                "max_calls_per_second": 10,
                "max_concurrency": 5,
                "params": {"param1": "value1"},
                "created_date": "2023-01-01"
            },
            {
                "id": "test-endpoint-2",
                "name": "Test Endpoint 2",
                "connector_type": "Test Connector 2",
                "uri": "http://test-uri-2.com",
                "token": "test-token-2",
                "max_calls_per_second": 15,
                "max_concurrency": 10,
                "params": {"param2": "value2"},
                "created_date": "2023-01-02"
            }
        ]
    )
])
def test_get_all_endpoints(mock_return_value, expected_status, expected_response, mock_endpoint_data_model):
    # Mock the EndpointDataModel with your MockEndpointDataModel
    with patch('moonshot.integrations.web_api.routes.endpoint.EndpointDataModel', new=mock_endpoint_data_model):
        if isinstance(mock_return_value, ServiceException):
            mock_endpoint_service.get_all_endpoints.side_effect = mock_return_value
        else:
            # Here you need to ensure that the mock_return_value is a list of instances of MockEndpointDataModel
            mock_return_value = [mock_endpoint_data_model(**data) for data in mock_return_value]
            mock_endpoint_service.get_all_endpoints.return_value = mock_return_value

        response = client.get("/api/v1/llm-endpoints")

        assert response.status_code == expected_status
        # Before asserting, apply the mask_token method to each item in expected_response
        for item in expected_response:
            if 'token' in item:
                item['token'] = '*' * len(item['token'])
        assert response.json() == expected_response

@pytest.mark.parametrize("endpoint_id, expected_status, expected_response", [
    # Test successful retrieval of endpoint names
    (
        "test-endpoint-1",
        200,
        {
            "id": "test-endpoint-1",
            "name": "Test Endpoint 1",
            "connector_type": "Test Connector 1",
            "uri": "http://test-uri-1.com",
            "token": "test-token-1",
            "max_calls_per_second": 10,
            "max_concurrency": 5,
            "params": {"param1": "value1"},
            "created_date": "2023-01-01"
        }
    )
])
def test_get_endpoint(endpoint_id, expected_status, expected_response, mock_endpoint_data_model):
    # Create an instance of MockEndpointDataModel with the expected response data
    mock_endpoint_instance = mock_endpoint_data_model(**expected_response)
    # Apply the mask_token method to mask the token
    mock_endpoint_instance.mask_token()

    if expected_status == 200:
        # Return the mock instance instead of the raw data
        mock_endpoint_service.get_endpoint.return_value = mock_endpoint_instance
    else:
        mock_endpoint_service.get_endpoint.side_effect = ServiceException(
            msg="Endpoint not found", method_name="get_endpoint", error_code="FileNotFound"
        )

    response = client.get(f"/api/v1/llm-endpoints/{endpoint_id}")

    assert response.status_code == expected_status
    # Convert the mock instance to a dictionary for comparison
    assert response.json() == mock_endpoint_instance.dict()

@pytest.mark.parametrize("endpoint_id, endpoint_data, expected_status", [
    # Test successful update of endpoint
    (
        "valid-endpoint-id",
        {
            "name": "Updated Endpoint",
            "connector_type": "Updated Connector",
            "uri": "http://updated-uri.com",
            "token": "updated-token",
            "max_calls_per_second": 20,
            "max_concurrency": 10,
            "params": {"param1": "updated-value1"}
        },
        200
    )
])
def test_update_endpoint(endpoint_id, endpoint_data, expected_status):
    if expected_status == 200:
        mock_endpoint_service.update_endpoint.return_value = None
    elif expected_status == 404:
        mock_endpoint_service.update_endpoint.side_effect = ServiceException(
            msg="Endpoint not found", method_name="update_endpoint", error_code="FileNotFound"
        )
    elif expected_status == 422:
        mock_endpoint_service.update_endpoint.side_effect = ServiceException(
            msg="Validation error", method_name="update_endpoint", error_code="ValidationError"
        )

    response = client.put(f"/api/v1/llm-endpoints/{endpoint_id}", json=endpoint_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize("endpoint_id, service_exception, expected_status", [
    # Test successful deletion of endpoint
    ("valid-endpoint-id", None, 200)
])
def test_delete_endpoint(endpoint_id, service_exception, expected_status):
    # Setup the mock service method
    if service_exception:
        mock_endpoint_service.delete_endpoint.side_effect = service_exception
    else:
        mock_endpoint_service.delete_endpoint.return_value = None

    # Make the delete request
    response = client.delete(f"/api/v1/llm-endpoints/{endpoint_id}")

    # Assert the expected status code
    assert response.status_code == expected_status

    # If the status code is 200, also check the success message
    if expected_status == 200:
        assert response.json() == {"message": "Endpoint deleted successfully"}
        