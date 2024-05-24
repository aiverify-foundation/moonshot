import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# not mocking response cause response too long
@pytest.mark.parametrize("exception, expected_status", [
    # Successful cases
    (None, 200),
    # Exception cases
    (ServiceException("A file not found error occurred", "get_all_results", "FileNotFound"), 404),
    (ServiceException("A validation error occurred", "get_all_results", "ValidationError"), 400),
    (ServiceException("An unexpected error occurred", "get_all_results", "ServerError"), 500),
])
def test_get_all_benchmark_results(test_client, mock_bm_result_service, exception, expected_status):
    if exception:
        mock_bm_result_service.get_all_results.side_effect = exception
    if expected_status == 200:
        mock_bm_result_service.get_all_results.return_value = []
    response = test_client.get("/api/v1/benchmarks/results")
    assert response.status_code == expected_status
    if expected_status != 200:
        assert exception.msg in response.json()["detail"]

# not mocking response cause response too long
@pytest.mark.parametrize("mock_response, exception, expected_status, expected_response", [
    # Successful cases
    (["result1", "result2", "result3"], None, 200, ["result1", "result2", "result3"]),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_result_name", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_result_name", "ValidationError"), 400, None),
    (None, ServiceException("An unexpected error occurred", "get_all_result_name", "ServerError"), 500, None),
])
def test_get_all_results_name(test_client, mock_bm_result_service, mock_response, exception, expected_status, expected_response):
    if exception:
        mock_bm_result_service.get_all_result_name.side_effect = exception
    if expected_status == 200:
        mock_bm_result_service.get_all_result_name.return_value = mock_response

    response = test_client.get("/api/v1/benchmarks/results/name")
    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]


# not mocking response cause response too long
@pytest.mark.parametrize("result_id, exception, expected_status", [
    # Successful cases
    ("valid_id", None, 200),
    # Exception cases
    ("valid_id", ServiceException("A file not found error occurred", "get_result_by_id", "FileNotFound"), 404),
    ("valid_id", ServiceException("A validation error occurred", "get_result_by_id", "ValidationError"), 400),
    ("valid_id", ServiceException("An unexpected error occurred", "get_result_by_id", "ServerError"), 500),
])
def test_get_one_benchmark_results(test_client, mock_bm_result_service, result_id, exception, expected_status):
    if exception:
        mock_bm_result_service.get_result_by_id.side_effect = exception
    if expected_status == 200:
        mock_bm_result_service.get_result_by_id.return_value = {}
    response = test_client.get(f"/api/v1/benchmarks/results/{result_id}")
    assert response.status_code == expected_status
    if expected_status != 200:
        assert exception.msg in response.json()["detail"]


@pytest.mark.parametrize("result_id, exception, expected_status, expected_response", [
    # Successful cases
    ("valid_id", None, 200, {"message": "Result deleted successfully"}),
    # Exception cases
    ("valid_id", ServiceException("A file not found error occurred", "get_result_by_id", "FileNotFound"), 404, None),
    ("valid_id", ServiceException("A validation error occurred", "get_result_by_id", "ValidationError"), 400, None),
    ("valid_id", ServiceException("An unexpected error occurred", "get_result_by_id", "ServerError"), 500, None),
])
def test_delete_result(test_client, mock_bm_result_service, result_id, exception, expected_status,expected_response):
    if exception:
        mock_bm_result_service.delete_result.side_effect = exception
    else:
        mock_bm_result_service.delete_result.return_value = {}

    response = test_client.delete(f"/api/v1/benchmarks/results/{result_id}")

    assert response.status_code == expected_status

    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response
    