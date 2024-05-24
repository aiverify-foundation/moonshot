import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("metrics_data, exception, expected_status, expected_response", [
    # Successful cases
    (
        [{
        "id": "metric_1",
        "name": "Metric 1",
        "description": "Metric 1 Description."
        },{
        "id": "metric_2",
        "name": "Metric 2",
        "description": "Metric 2 Description."
        }]
    , None, 200, 
        [{
        "id": "metric_1",
        "name": "Metric 1",
        "description": "Metric 1 Description."
        },{
        "id": "metric_2",
        "name": "Metric 2",
        "description": "Metric 2 Description."
        }]
    ),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_metric", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_metric", "ValidationError"), 400,None),
    (None, ServiceException("An value error occurred", "get_all_metric", "ValueError"), 500, None),
])
def test_get_metrics(test_client, mock_metric_service, metrics_data, exception, expected_status, expected_response):
    if exception:
        mock_metric_service.get_all_metric.side_effect = exception
    else:
        mock_metric_service.get_all_metric.return_value = metrics_data

    response = test_client.get("/api/v1/metrics")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]


@pytest.mark.parametrize("metric_id, exception, expected_status, expected_response", [
    # Successful case
    ("valid_metric_id", None, 200, {"message": "Metric deleted successfully"}),
    # Exception cases
    ("nonexistent_metric_id", ServiceException("A file not found error occurred", "delete_metric", "FileNotFound"), 404, None),
    ("invalid_metric_id", ServiceException("A validation error occurred", "delete_metric", "ValidationError"), 400, None),
    ("error_metric_id", ServiceException("An value error occurred", "delete_metric", "ValueError"), 500, None),
])
def test_delete_metric(test_client, mock_metric_service, metric_id, exception, expected_status, expected_response):
    if exception:
        mock_metric_service.delete_metric.side_effect = exception
    else:
        mock_metric_service.delete_metric.return_value = {}

    response = test_client.delete(f"/api/v1/metrics/{metric_id}")

    assert response.status_code == expected_status

    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response
    