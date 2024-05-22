import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("mockdata, exception, expected_status, expected_response", [
    # Successful cases
    (
        [{
        "id": "dataset-1",
        "name": "dataset-1",
        "description": "dataset-1 description",
        "num_of_dataset_prompts": 48201,
        "created_date": "2024-05-14 21:36:21"
        },
        {
        "id": "dataset-2",
        "name": "dataset-2",
        "description": "dataset-2 description.",
        "num_of_dataset_prompts": 600,
        "created_date": "2024-05-14 21:36:20"
        }],
        None,
        200,
        [{
        "id": "dataset-1",
        "name": "dataset-1",
        "description": "dataset-1 description",
        "num_of_dataset_prompts": 48201,
        "created_date": "2024-05-14 21:36:21"
        },
        {
        "id": "dataset-2",
        "name": "dataset-2",
        "description": "dataset-2 description.",
        "num_of_dataset_prompts": 600,
        "created_date": "2024-05-14 21:36:20"
        }]
    ),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_datasets", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_datasets", "ValidationError"), 400, None),
    (None, ServiceException("An server error occurred", "get_all_datasets", "ServerError"), 500, None),
])
def test_get_all_datasets(test_client, mock_dataset_service, mockdata, exception, expected_status, expected_response):
    if exception:
        mock_dataset_service.get_all_datasets.side_effect = exception
    else:
        mock_dataset_service.get_all_datasets.return_value = mockdata

    response = test_client.get("/api/v1/datasets")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("mockdata, exception, expected_status, expected_response", [
    # Successful cases
    (["dataset1", "dataset2", "dataset3"], None, 200, ["dataset1", "dataset2", "dataset3"]),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_datasets_name", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_datasets_name", "ValidationError"), 400, None),
    (None, ServiceException("An server error occurred", "get_all_datasets_name", "ServerError"), 500, None),
])
def test_get_all_dataset_names(test_client, mock_dataset_service, mockdata, exception, expected_status, expected_response):
    if exception:
        mock_dataset_service.get_all_datasets_name.side_effect = exception
    else:
        mock_dataset_service.get_all_datasets_name.return_value = mockdata

    response = test_client.get("/api/v1/datasets/name")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("dataset_id, exception, expected_status, expected_response", [
    # Success case
    ("valid-dataset-id", None, 200 , {"message": "Dataset deleted successfully"}),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_datasets_name", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_datasets_name", "ValidationError"), 400, None),
    (None, ServiceException("An server error occurred", "get_all_datasets_name", "ServerError"), 500, None),
])
def test_delete_dataset(test_client, mock_dataset_service, dataset_id, exception, expected_status, expected_response):
    if exception:
        mock_dataset_service.delete_dataset.side_effect = exception
    else:
        mock_dataset_service.delete_dataset.return_value = None

    response = test_client.delete(f"/api/v1/datasets/{dataset_id}")

    # Assert the expected status code
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]
