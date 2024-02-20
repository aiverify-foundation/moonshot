import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from ..app import init_api
from ..schemas.endpoint_response_model import EndpointDataModel
import inspect

app = init_api()

@patch('web_api.services.benchmarking_service.get_all_endpoints')
def test_get_all_endpoints(mock_get_all_endpoints):
    # Define the mock return value
    mock_get_all_endpoints.return_value = [
        EndpointDataModel(
            type="Type1",
            name="Mock Endpoint 1",
            uri="http://mockendpoint1.com",
            token="token1",
            max_calls_per_second=100,
            max_concurrency=10
        ),
        EndpointDataModel(
            type="Type2",
            name="Mock Endpoint 2",
            uri="http://mockendpoint2.com",
            token="token2",
            max_calls_per_second=200,
            max_concurrency=20
        )
    ]

    with TestClient(app) as client:
        response = client.get("/v1/llm_endpoints")
    
    # Assertions to verify the behavior
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Mock Endpoint 1"
    assert response.json()[1]["name"] == "Mock Endpoint 2"
    assert response.json()[0]["uri"] == "http://mockendpoint1.com"
    assert response.json()[1]["uri"] == "http://mockendpoint2.com"
    assert response.json()[0]["type"] == "Type1"
    assert response.json()[1]["type"] == "Type2"
    assert response.json()[0]["token"] == "token1"
    assert response.json()[1]["token"] == "token2"
    assert response.json()[0]["max_calls_per_second"] == 100
    assert response.json()[1]["max_calls_per_second"] == 200
    assert response.json()[0]["max_concurrency"] == 10
    assert response.json()[1]["max_concurrency"] == 20

