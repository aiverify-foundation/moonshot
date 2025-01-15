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


@pytest.mark.parametrize("dataset_data, exception, expected_status, expected_response", [
    # Successful case for "hf" method
    (
        {
            "name": "New De Dataset 2",
            "description": "This dataset is created from postman in hf",
            "license": "",
            "reference": "",
            "params": {
                "dataset_name": "cais/mmlu",
                "dataset_config": "college_biology",
                "split": "test",
                "input_col": ["question", "choices"],
                "target_col": "answer"
            }
        },
        None,
        200,
        "Dataset created successfully"
    ),
    # Exception cases
    (
        {
            "name": "New De Dataset 2",
            "description": "This dataset is created from postman in hf",
            "license": "",
            "reference": "",
            "params": {
                "dataset_name": "cais/mmlu",
                "dataset_config": "college_biology",
                "split": "dev",
                "input_col": ["question", "choices"],
                "target_col": "answer"
            }
        },
        ServiceException("A file not found error occurred", "create_dataset", "FileNotFound"),
        404,
        {'detail': 'Failed to download dataset: [ServiceException] FileNotFound in create_dataset - A file not found error occurred'}
    ),
    (
        {
            "name": "New De Dataset 2",
            "description": "This dataset is created from postman in hf",
            "license": "",
            "reference": "",
            "params": {
                "dataset_name": "cais/mmlu",
                "dataset_config": "college_biology",
                "split": "dev",
                "input_col": ["question", "choices"],
                "target_col": "answer"
            }
        },
        ServiceException("An server error occurred", "create_dataset", "ServerError"),
        500,
        {'detail': 'Failed to download dataset: [ServiceException] ServerError in create_dataset - An server error occurred'}
    ),
])
def test_download_dataset(test_client, mock_dataset_service, dataset_data, exception, expected_status, expected_response, mocker):
    mocker.patch("moonshot.integrations.web_api.routes.dataset.Provide", return_value=mock_dataset_service)
    
    if exception:
        mock_dataset_service.download_dataset.side_effect = exception
    else:
        mock_dataset_service.download_dataset.return_value = expected_response

    response = test_client.post("/api/v1/datasets/hf", json=dataset_data)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize("file_name, form_data, exception, expected_status, expected_response", [
    # Successful case
    (
        "test.csv",
        {
            "name": "New Dataset",
            "description": "This dataset is created from postman",
            "license": "norman license",
            "reference": "reference.com",
        },
        None,
        200,
        "Dataset created successfully"
    ),
    # Exception cases
    (
        "test.csv",
        {
            "name": "New Dataset",
            "description": "This dataset is created from postman",
            "license": "norman license",
            "reference": "reference.com",
        },
        ServiceException("A validation error occurred", "create_dataset", "ValidationError"),
        400,
        {'detail': 'Failed to convert dataset: [ServiceException] ValidationError in create_dataset - A validation error occurred'}
    ),
    (
        "test.csv",
        {
            "name": "New Dataset",
            "description": "This dataset is created from postman",
            "license": "norman license",
            "reference": "reference.com",
        },
        ServiceException("A file not found error occurred", "create_dataset", "FileNotFound"),
        404,
        {'detail': 'Failed to convert dataset: [ServiceException] FileNotFound in create_dataset - A file not found error occurred'}
    ),
    (
        "test.csv",
        {
            "name": "New Dataset",
            "description": "This dataset is created from postman",
            "license": "norman license",
            "reference": "reference.com",
        },
        ServiceException("An server error occurred", "create_dataset", "ServerError"),
        500,
        {'detail': 'Failed to convert dataset: [ServiceException] ServerError in create_dataset - An server error occurred'}
    ),
])
def test_convert_dataset(test_client, mock_dataset_service, file_name, form_data, exception, expected_status, expected_response, mocker):
    mocker.patch("moonshot.integrations.web_api.routes.dataset.Provide", return_value=mock_dataset_service)
    
    # Create a mock file content
    file_content = b"mock,csv,content\n1,2,3"
    files = {
        "file": (file_name, file_content, "text/csv")
    }
    
    if exception:
        mock_dataset_service.convert_dataset.side_effect = exception
    else:
        mock_dataset_service.convert_dataset.return_value = expected_response

    # Use test client with form data and files
    response = test_client.post(
        "/api/v1/datasets/file",
        data=form_data,
        files=files
    )
    
    assert response.status_code == expected_status
    assert response.json() == expected_response