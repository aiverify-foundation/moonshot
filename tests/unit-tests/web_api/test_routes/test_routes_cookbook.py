import pytest

from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("cookbook_data, exception, expected_status, expected_response", [
    # Success scenario
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description",
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        None,
        200,
        {"message": "Cookbook created successfully"}
    ),
    # Missing 'name'
    (
        {
            "description": "A test cookbook description without name",
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        None,
        422,
        None
    ),
    # Missing 'recipes'
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description without recipes",
            "tags": [],
            "categories": []
        },
        None,
        422,
        None
    ),
    # Missing 'description'
    (
        {
            "name": "Test Cookbook",
            "recipes": ["recipe1", "recipe2"],
            "tags": [],
            "categories": [],
        },
        None,
        200,
        {"message": "Cookbook created successfully"}
    ),
    # Missing 'name' and 'description'
    (
        {
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        None,
        422,
        None
    ),
    # Missing 'recipes' and 'description'
    (
        {
            "name": "Test Cookbook",
            "tags": [],
            "categories": [],
        },
        None,
        422,
        None
    ),
    # Missing 'name' and 'recipes'
    (
        {
            "tags": [],
            "categories": [],
            "description": "A test cookbook description without name and recipes"
        },
        None,
        422,
        None
    ),
    # Empty 'name'
    (
        {
            "name": "",
            "description": "A test cookbook description with empty name",
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        None,
        422,
        None
    ),
    # Empty 'recipes'
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description with empty recipes",
            "tags": [],
            "categories": [],
            "recipes": []
        },
        None,
        422,
        None
    ),
    # 'recipes' is not a list
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description with invalid recipes type",
            "tags": [],
            "categories": [],
            "recipes": "recipe1"
        },
        None,
        422,
        None
    ),
    # All fields missing
    (
        {},
        None,
        422,
        None
    ),
    # Exception cases
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description",
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        ServiceException("A file not found error occurred", "create_cookbook", "FileNotFound"),
        404, None
    ),
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description",
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        ServiceException("A validation error occurred", "create_cookbook", "ValidationError"),
        400, None
    ),
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description",
            "tags": [],
            "categories": [],
            "recipes": ["recipe1", "recipe2"]
        },
        ServiceException("An unexpected error occurred", "create_cookbook", "UnknownError"),
        500, None
    ),
])
def test_create_cookbook(test_client, mock_cookbook_service, cookbook_data, expected_status, exception, expected_response):
    if exception:
        mock_cookbook_service.create_cookbook.side_effect = exception
    else:
        mock_cookbook_service.create_cookbook.return_value = cookbook_data 

    response = test_client.post("/api/v1/cookbooks", json=cookbook_data)

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        if expected_status != 422:
            assert response.json() == expected_response

@pytest.mark.parametrize("query_string, mock_return_value, exception, expected_status, expected_response", [
   # Test get all cookbooks success
    (
        "",
        [
            {
                "id": "test-cookbook-1",
                "name": "Test Cookbook 1",
                "description": "Description for Test Cookbook 1",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
                'total_dataset_in_cookbook': None,
                "required_config": None
            },
            {
                "id": "test-cookbook-2",
                "name": "Test Cookbook 2",
                "description": "Description for Test Cookbook 2",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": None
            },
        ],
        None,
        200,
        [
            {
                "id": "test-cookbook-1",
                "name": "Test Cookbook 1",
                "description": "Description for Test Cookbook 1",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,                
                "required_config": None
            },
            {
                "id": "test-cookbook-2",
                "name": "Test Cookbook 2",
                "description": "Description for Test Cookbook 2",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": None
            },
        ]
    ),
    # Test get cookbooks by IDs
    (
        "ids=test-cookbook-1",
        [
            {
                "id": "test-cookbook-1",
                "name": "Filtered Cookbook 1",
                "description": "Filtered Description 1",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-3"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": None
            }
        ],
        None,
        200,
        [
            {
                "id": "test-cookbook-1",
                "name": "Filtered Cookbook 1",
                "description": "Filtered Description 1",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-3"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": None
            }
        ]
    ),
    # Test get cookbooks by tags
    (
        "tags=bias",
        [
            {
                "id": "test-cookbook-tagged",
                "name": "Tagged Cookbook",
                "description": "A cookbook with a specific tag",
                "tags": [],
                "categories": [],
                "recipes": ["one-recipe-contains-this-tag"],
                "total_prompt_in_cookbook": None,
                'total_dataset_in_cookbook': None,
                "required_config": None
            }
        ],
        None,
        200,
        [
            {
                "id": "test-cookbook-tagged",
                "name": "Tagged Cookbook",
                "description": "A cookbook with a specific tag",
                "tags": [],
                "categories": [],
                "recipes": ["one-recipe-contains-this-tag"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": None
            }
        ]
    ),
    # Test get cookbooks by categories
    (
        "categories=trust",
        [
            {
                "id": "test-cookbook-category",
                "name": "Category Cookbook",
                "description": "A cookbook with a specific category",
                "tags": [],
                "categories": [],
                "recipes": ["one-recipe-contains-this-category"],
                "total_prompt_in_cookbook": None,
                'total_dataset_in_cookbook': None,
                "required_config": None
            }
        ],
        None,
        200,
        [
            {
                "id": "test-cookbook-category",
                "name": "Category Cookbook",
                "description": "A cookbook with a specific category",
                "tags": [],
                "categories": [],
                "recipes": ["one-recipe-contains-this-category"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": None
            }
        ]
    ),
    # Test get cookbooks with count
    (
        "count=true",
        [
            {
                "id": "test-cookbook-count",
                "name": "Cookbook with Count",
                "description": "A cookbook with a count of recipes",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": 2,
                'total_dataset_in_cookbook': None,
                "required_config": None
            }
        ],
        None,
        200,
        [
            {
                "id": "test-cookbook-count",
                "name": "Cookbook with Count",
                "description": "A cookbook with a count of recipes",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": 2,
                "total_dataset_in_cookbook": None,
                "required_config": None
            }
        ],
    ),
    # Test get cookbooks with endpoints
    (
        "count=true",
        [
            {
                "id": "test-cookbook-count",
                "name": "Cookbook with Count",
                "description": "A cookbook with a count of recipes",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
                'total_dataset_in_cookbook': None,
                "required_config": {"endpoints": ["openai-gpt35-turbo-16k"]}
            }
        ],
        None,
        200,
        [
            {
                "id": "test-cookbook-count",
                "name": "Cookbook with Count",
                "description": "A cookbook with a count of recipes",
                "tags": [],
                "categories": [],
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
                "total_dataset_in_cookbook": None,
                "required_config": {"endpoints": ["openai-gpt35-turbo-16k"]}
            }
        ]
    ),
    # Exception cases
    (None, None, ServiceException("A file not found error occurred", "get_all_cookbooks", "FileNotFound"), 404, None),
    (None, None, ServiceException("A validation error occurred", "get_all_cookbooks", "ValidationError"), 400, None),
    (None, None, ServiceException("An value error occurred", "get_all_cookbooks", "ValueError"), 500, None),
])
def test_get_cookbooks(test_client, mock_cookbook_service, query_string, mock_return_value, exception, expected_status, expected_response):
    if exception:
        mock_cookbook_service.get_all_cookbooks.side_effect = exception
    else:
        mock_cookbook_service.get_all_cookbooks.return_value = mock_return_value

    response = test_client.get(f"/api/v1/cookbooks?{query_string}")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response

@pytest.mark.parametrize("mock_return_value, exception, expected_status, expected_response", [
    # Test successful retrieval of cookbook names
    (
        ["Cookbook One", "Cookbook Two"],
        None,
        200,
        ["Cookbook One", "Cookbook Two"]
    ),
    # Test exception when retrieving cookbook names
    (
        None,
        ServiceException("A file not found error occurred", "get_all_cookbooks_names", "FileNotFound"),
        404, None
    ),
    (
        None,
        ServiceException("A validation error occurred", "get_all_cookbooks_names", "ValidationError"),
        400, None
    ),
    (
        None,
        ServiceException("An value error occurred", "get_all_cookbooks_names", "ValueError"),
        500, None
    )
])
def test_get_all_cookbooks_name(test_client, mock_cookbook_service, mock_return_value, exception, expected_status, expected_response):
    if exception:
        mock_cookbook_service.get_all_cookbooks_names.side_effect = exception
    else:
        mock_cookbook_service.get_all_cookbooks_names.return_value = mock_return_value

    response = test_client.get("/api/v1/cookbooks/name")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response


@pytest.mark.parametrize("cookbook_id, cookbook_data, expected_status, expected_response", [
    # Test successful update of cookbook
    (
        "valid-cookbook-id",
        {"name": "Updated Cookbook", "description": "Updated description", "recipes": ["recipe-1"]},
        200,
        {"message": "Cookbook updated successfully"}
    ),
    # Test cookbook not found
    (
        "invalid-cookbook-id",
        {"name": "Non-existent Cookbook", "description": "This cookbook does not exist", "recipes": ["recipe-1"]},
        404,
        ServiceException("Recipe not found", "update_cookbook", "FileNotFound")
    ),
    # Test validation error
    (
        "valid-cookbook-id",
        {"name": "Updated Cookbook", "description": "Updated description", "recipes": ["recipe-1"]},
        400,
        ServiceException("Validation error", "update_cookbook", "ValidationError")
    ),
    # Test unknown error
    (
        "valid-cookbook-id",
        {"name": "Another Cookbook", "description": "Another description", "recipes": ["recipe-2"]},
        500,
        ServiceException("Unknown error", "update_cookbook", "UnknownError")
    ),
])
def test_update_cookbook(test_client, mock_cookbook_service, cookbook_id, cookbook_data, expected_status, expected_response):
    if isinstance(expected_response, ServiceException):
        mock_cookbook_service.update_cookbook.side_effect = expected_response
    else:
        mock_cookbook_service.update_cookbook.return_value = cookbook_data

    response = test_client.put(f"/api/v1/cookbooks/{cookbook_id}", json=cookbook_data)

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    elif isinstance(expected_response, ServiceException):
        assert expected_response.msg in response.json()["detail"]

@pytest.mark.parametrize("cb_id, service_exception, expected_status, expected_response", [
    # Test successful deletion of cookbook
    ("valid-cookbook-id", None, 200, {"message": "Cookbook deleted successfully"}),
    # Test cookbook not found
    ("invalid-cookbook-id", ServiceException(msg="Cookbook not found", method_name="delete_cookbook", error_code="FileNotFound"), 404, None),
    # Test validation error
    ("valid-cookbook-id", ServiceException(msg="Validation error", method_name="delete_cookbook", error_code="ValidationError"), 400, None),
    # Test unknown error
    ("valid-cookbook-id", ServiceException(msg="Internal server error", method_name="delete_cookbook", error_code="UnknownError"), 500, None),
])
def test_delete_cookbook(test_client, mock_cookbook_service, cb_id, service_exception, expected_status, expected_response):
    if service_exception:
        mock_cookbook_service.delete_cookbook.side_effect = service_exception
    else:
        mock_cookbook_service.delete_cookbook.return_value = None

    # Make the delete request
    response = test_client.delete(f"/api/v1/cookbooks/{cb_id}")

    # Assert the expected status code
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert service_exception.msg in response.json()["detail"]
