from fastapi.testclient import TestClient
from unittest.mock import Mock
from moonshot.integrations.web_api.container import Container
from moonshot.integrations.web_api.services.cookbook_service import CookbookService
import pytest
from moonshot.integrations.web_api.app import create_app
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Create a mock instance of CookbookService
mock_cookbook_service = Mock(spec=CookbookService)

# Create a container for testing and override the CookbookService dependency
test_container = Container()
test_container.config.from_default()  
test_container.cookbook_service.override(mock_cookbook_service)

# Wire the container
test_container.wire(modules=["moonshot.integrations.web_api.routes"])

# Create a new FastAPI app instance for testing
app = create_app(test_container.config)

# Use TestClient with the app instance
client = TestClient(app)

# Override the CookbookService dependency in the container
Container.cookbook_service.override(mock_cookbook_service)

@pytest.mark.parametrize("cookbook_data, expected_status", [
    # Success scenario
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description",
            "recipes": ["recipe1", "recipe2"]
        },
        200
    ),
    # Missing 'name'
    (
        {
            "description": "A test cookbook description without name",
            "recipes": ["recipe1", "recipe2"]
        },
        422
    ),
    # Missing 'recipes'
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description without recipes"
        },
        422
    ),
    # Missing 'description'
    (
        {
            "name": "Test Cookbook",
            "recipes": ["recipe1", "recipe2"]
        },
        422
    ),
    # Missing 'name' and 'description'
    (
        {
            "recipes": ["recipe1", "recipe2"]
        },
        422
    ),
    # Missing 'recipes' and 'description'
    (
        {
            "name": "Test Cookbook"
        },
        422,
    ),
    # Missing 'name' and 'recipes'
    (
        {
            "description": "A test cookbook description without name and recipes"
        },
        422,
    ),
    # Empty 'name'
    (
        {
            "name": "",
            "description": "A test cookbook description with empty name",
            "recipes": ["recipe1", "recipe2"]
        },
        422
    ),
    # Empty 'recipes'
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description with empty recipes",
            "recipes": []
        },
        422
    ),
    # 'recipes' is not a list
    (
        {
            "name": "Test Cookbook",
            "description": "A test cookbook description with invalid recipes type",
            "recipes": "recipe1"
        },
        422
    ),
    # All fields missing
    (
        {},
        422
    )
])
def test_create_cookbook(cookbook_data, expected_status):
    response = client.post("/api/v1/cookbooks", json=cookbook_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize("query_string, mock_return_value, expected_status, expected_response", [
    # Test get all cookbooks success
    (
        "",
        [
            {
                "id": "test-cookbook-1",
                "name": "Test Cookbook 1",
                "description": "Description for Test Cookbook 1",
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
            },
            {
                "id": "test-cookbook-2",
                "name": "Test Cookbook 2",
                "description": "Description for Test Cookbook 2",
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None
            },
        ],
        200,
        [
            {
                "id": "test-cookbook-1",
                "name": "Test Cookbook 1",
                "description": "Description for Test Cookbook 1",
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None,
            },
            {
                "id": "test-cookbook-2",
                "name": "Test Cookbook 2",
                "description": "Description for Test Cookbook 2",
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": None
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
                "recipes": ["recipe-3"],
                "total_prompt_in_cookbook": None,
            }
        ],
        200,
        [
            {
                "id": "test-cookbook-1",
                "name": "Filtered Cookbook 1",
                "description": "Filtered Description 1",
                "recipes": ["recipe-3"],
                "total_prompt_in_cookbook": None,
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
                "recipes": ["one-recipe-contains-this-tag"],
                "total_prompt_in_cookbook": None,
            }
        ],
        200,
        [
            {
                "id": "test-cookbook-tagged",
                "name": "Tagged Cookbook",
                "description": "A cookbook with a specific tag",
                "recipes": ["one-recipe-contains-this-tag"],
                "total_prompt_in_cookbook": None,
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
                "recipes": ["one-recipe-contains-this-category"],
                "total_prompt_in_cookbook": None,
            }
        ],
        200,
        [
            {
                "id": "test-cookbook-category",
                "name": "Category Cookbook",
                "description": "A cookbook with a specific category",
                "recipes": ["one-recipe-contains-this-category"],
                "total_prompt_in_cookbook": None,
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
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": 2,
            }
        ],
        200,
        [
            {
                "id": "test-cookbook-count",
                "name": "Cookbook with Count",
                "description": "A cookbook with a count of recipes",
                "recipes": ["recipe-1", "recipe-2"],
                "total_prompt_in_cookbook": 2,
            }
        ]
    ),
])
def test_get_cookbooks(query_string, mock_return_value, expected_status, expected_response):
    if isinstance(mock_return_value, ServiceException):
        mock_cookbook_service.get_all_cookbooks.side_effect = mock_return_value
    else:
        mock_cookbook_service.get_all_cookbooks.return_value = mock_return_value

    response = client.get(f"/api/v1/cookbooks?{query_string}")

    assert response.status_code == expected_status
    assert response.json() == expected_response

@pytest.mark.parametrize("service_return, expected_status, expected_response", [
    # Test successful retrieval of cookbook names
    (
        ["Cookbook One", "Cookbook Two"],
        200,
        ["Cookbook One", "Cookbook Two"]
    )
])
def test_get_all_cookbooks_name(service_return, expected_status, expected_response):
    mock_cookbook_service.get_all_cookbooks_names.return_value = service_return
    response = client.get("/api/v1/cookbooks/name")

    assert response.status_code == expected_status
    assert response.json() == expected_response

@pytest.mark.parametrize("cookbook_id, cookbook_data, expected_status", [
    # Test successful update of cookbook
    (
        "valid-cookbook-id",
        {"name": "Updated Cookbook", "description": "Updated description", "recipes": ["recipe-1"]},
        200
    ),
    # Test cookbook not found
    (
        "invalid-cookbook-id",
        {"name": "Non-existent Cookbook", "description": "This cookbook does not exist", "recipes": ["recipe-1"]},
        404
    ),
    # Test validation error
    (
        "valid-cookbook-id",
        {"name": "", "description": "Invalid data", "recipes": []},  # Invalid data
        422
    ),
])
def test_update_cookbook(cookbook_id, cookbook_data, expected_status):
    # Mock the service method based on the expected status
    if expected_status == 200:
        mock_cookbook_service.update_cookbook.return_value = None
    elif expected_status == 404:
        mock_cookbook_service.update_cookbook.side_effect = ServiceException(
            msg="Cookbook not found", method_name="update_cookbook", error_code="FileNotFound"
        )
    elif expected_status == 400:
        mock_cookbook_service.update_cookbook.side_effect = ServiceException(
            msg="Validation error", method_name="update_cookbook", error_code="ValidationError"
        )

    response = client.put(f"/api/v1/cookbooks/{cookbook_id}", json=cookbook_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize("cb_id, service_exception, expected_status", [
    # Test successful deletion of cookbook
    ("valid-cookbook-id", None, 200),
    # Test cookbook not found
    ("invalid-cookbook-id", ServiceException(msg="Cookbook not found", method_name="delete_cookbook", error_code="FileNotFound"), 404),
    # Test other internal server error
    ("valid-cookbook-id", ServiceException(msg="Internal server error", method_name="delete_cookbook", error_code="UnknownError"), 500),
])
def test_delete_cookbook(cb_id, service_exception, expected_status):
    # Setup the mock service method
    if service_exception:
        mock_cookbook_service.delete_cookbook.side_effect = service_exception
    else:
        mock_cookbook_service.delete_cookbook.return_value = None

    # Make the delete request
    response = client.delete(f"/api/v1/cookbooks/{cb_id}")

    # Assert the expected status code
    assert response.status_code == expected_status

    # If the status code is 200, also check the success message
    if expected_status == 200:
        assert response.json() == {"message": "Cookbook deleted successfully"}
    