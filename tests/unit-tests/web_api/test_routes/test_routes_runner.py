import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize(
    "runner_data, exception, expected_status, expected_response",
    [
        # Successful cases
        (
            [
                {
                    "id": "test1",
                    "name": "test1",
                    "database_file": "../moonshot-data/generated-outputs/databases/test1.db",
                    "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                    "description": "test1",
                },
                {
                    "id": "test2",
                    "name": "test2",
                    "database_file": "../moonshot-data/generated-outputs/databases/test2.db",
                    "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                    "description": "test2",
                },
            ],
            None,
            200,
            [
                {
                    "id": "test1",
                    "name": "test1",
                    "database_file": "../moonshot-data/generated-outputs/databases/test1.db",
                    "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                    "description": "test1",
                },
                {
                    "id": "test2",
                    "name": "test2",
                    "database_file": "../moonshot-data/generated-outputs/databases/test2.db",
                    "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                    "description": "test2",
                },
            ],
        ),
        ([], None, 200, []),
        # Exception cases
        (
            None,
            ServiceException("A file not found error occurred", "get_all_runner", "FileNotFound"),
            404,
            None
        ),
        (
            None,
            ServiceException("A validation error occurred", "get_all_runner", "ValidationError"),
            400,
            None        
        ),
        (
            None,
            ServiceException("An server error occurred", "get_all_runner", "ServerError"),
            500,
            None        
        ),
    ],
)
def test_get_all_runners(test_client, mock_runner_service, runner_data, exception, expected_status, expected_response):
    if exception:
        mock_runner_service.get_all_runner.side_effect = exception
    else:
        mock_runner_service.get_all_runner.return_value = runner_data

    response = test_client.get("/api/v1/runners")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_data, exception, expected_status, expected_response", [
    # Successful cases
    (["runner1", "runner2", "runner3"], None, 200, ["runner1", "runner2", "runner3"]),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_runner_name", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_runner_name", "ValidationError"), 400, None),
    (None, ServiceException("An server error occurred", "get_all_runner_name", "ServerError"), 500, None),
])
def test_get_all_runner_name(test_client, mock_runner_service, runner_data, exception, expected_status, expected_response):
    if exception:
        mock_runner_service.get_all_runner_name.side_effect = exception
    else:
        mock_runner_service.get_all_runner_name.return_value = runner_data

    response = test_client.get("/api/v1/runners/name")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize(
    "runner_id, runner_data, exception, expected_status, expected_response",
    [
        # Successful cases
        (   
            "test1",
            {
                "id": "test1",
                "name": "test1",
                "database_file": "../moonshot-data/generated-outputs/databases/test1.db",
                "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                "description": "test1",
            },
            None,
            200,
            {
                "id": "test1",
                "name": "test1",
                "database_file": "../moonshot-data/generated-outputs/databases/test1.db",
                "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                "description": "test1",
            }
        ),
        # Exception cases
        (
            None,
            None,
            ServiceException("A file not found error occurred", "get_runner_by_id", "FileNotFound"),
            404,
            None
        ),
        (
            None,
            None,
            ServiceException("A validation error occurred", "get_runner_by_id", "ValidationError"),
            400,None        
        ),
        (
            None,
            None,
            ServiceException("An server error occurred", "get_runner_by_id", "ServerError"),
            500,
            None
        ),
    ],
)
def test_get_runner_by_id(test_client, mock_runner_service, runner_id, runner_data, exception, expected_status, expected_response):
    if exception:
        mock_runner_service.get_runner_by_id.side_effect = exception
    else:
        mock_runner_service.get_runner_by_id.return_value = runner_data

    response = test_client.get(f"/api/v1/runners/{runner_id}")

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, exception, expected_status, expected_response", [
    # Test successful deletion of runner
    ("valid-runner-id", None, 200, {"message": "Runner deleted successfully"}),
    # Exception cases
    ("runner-id", ServiceException(msg="Runner not found", method_name="delete_run", error_code="FileNotFound"), 404, None),
    ("runner-id", ServiceException(msg="Validation error", method_name="delete_run", error_code="ValidationError"), 400, None),
    ("runner-id", ServiceException(msg="Internal server error", method_name="delete_run", error_code="UnknownError"), 500, None),
])
def test_delete_runner(test_client, mock_runner_service, runner_id, exception, expected_status, expected_response):
    if exception:
        mock_runner_service.delete_run.side_effect = exception
    else:
        mock_runner_service.delete_run.return_value = None

    response = test_client.delete(f"/api/v1/runners/{runner_id}")

    # Assert the expected status code
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, run_id, mock_response, exception, expected_status, expected_response", [
    # Test successful deletion of runner
    ("valid-runner-id", "run_id",
     {
        "run_id": 1,
        "runner_id": "benchmark-test",
        "runner_args": {
            "cookbooks": ["test-cookbook"],
            "num_of_prompts": 5,
            "random_seed": 0,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "result_processing_module": "benchmarking-result"
        },
        "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
        "start_time": 1716106071.3418639
    },
    None, 200,
    {
        "run_id": 1,
        "runner_id": "benchmark-test",
        "runner_args": {
            "cookbooks": ["test-cookbook"],
            "num_of_prompts": 5,
            "random_seed": 0,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "result_processing_module": "benchmarking-result"
        },
        "endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
        "start_time": 1716106071.3418639
    }
    ),
    # Exception cases
    ("runner-id", "run_id", None, ServiceException(msg="Runner not found", method_name="get_run_details_by_runner", error_code="FileNotFound"), 404, None),
    ("runner-id", "run_id", None, ServiceException(msg="Validation error", method_name="get_run_details_by_runner", error_code="ValidationError"), 400, None),
    ("runner-id", "run_id", None, ServiceException(msg="Internal server error", method_name="get_run_details_by_runner", error_code="UnknownError"), 500, None),
])
def test_get_run_details_by_runner(test_client, mock_runner_service, runner_id, run_id, mock_response, exception, expected_status, expected_response):
    if exception:
        mock_runner_service.get_run_details_by_runner.side_effect = exception
    else:
        mock_runner_service.get_run_details_by_runner.return_value = mock_response
    
    response = test_client.get(f"/api/v1/runners/{runner_id}/runs/{run_id}")
    
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, mock_response, exception, expected_status, expected_response", [
    # Test successful deletion of runner
    ("valid-runner-id",
    [1,2,3],
    None, 200,
    [1,2,3],
    ),
    # Exception cases
    ("runner-id", None, ServiceException(msg="Runner not found", method_name="get_run_details_by_runner", error_code="FileNotFound"), 404, None),
    ("runner-id", None, ServiceException(msg="Validation error", method_name="get_run_details_by_runner", error_code="ValidationError"), 400, None),
    ("runner-id", None, ServiceException(msg="Internal server error", method_name="get_run_details_by_runner", error_code="UnknownError"), 500, None),
])
def test_get_run_ids_in_runner(test_client, mock_runner_service ,runner_id ,mock_response ,exception ,expected_status ,expected_response):
    if exception:
        mock_runner_service.get_runs_id_in_runner.side_effect = exception
    else:
        mock_runner_service.get_runs_id_in_runner.return_value = mock_response

    response = test_client.get(f"/api/v1/runners/{runner_id}/runs")
    
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]
