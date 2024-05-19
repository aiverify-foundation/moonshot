from fastapi.testclient import TestClient
from unittest.mock import Mock
from moonshot.integrations.web_api.container import Container
from moonshot.integrations.web_api.services.recipe_service import RecipeService
import pytest
from moonshot.integrations.web_api.app import create_app
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Create a mock instance of RecipeService
mock_recipe_service = Mock(spec=RecipeService)

# Create a container for testing and override the RecipeService dependency
test_container = Container()
test_container.config.from_default()  
test_container.recipe_service.override(mock_recipe_service)

# Wire the container
test_container.wire(modules=["moonshot.integrations.web_api.routes"])

# Create a new FastAPI app instance for testing
app = create_app(test_container.config)

# Use TestClient with the app instance
client = TestClient(app)

# Override the RecipeService dependency in the container
Container.recipe_service.override(mock_recipe_service)

@pytest.mark.parametrize("recipe_data, expected_status", [
    # Success scenario
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "prompt_templates": ["template1"],
            "attack_modules": ["module1"],
        },
        200
    ),
    # Missing 'name'
    (
        {
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"]
        },
        422
    ),
    # Missing 'datasets'
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "metrics": ["metric1"]
        },
        422
    ),
    # Missing 'metrics'
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"]
        },
        422
    ),
    # Missing 'description'
    (
        {
            "name": "Test Recipe",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "prompt_templates": ["template1"],
            "attack_modules": ["module1"],
        },
        422
    ),
    # Missing 'tags'
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "prompt_templates": ["template1"],
            "attack_modules": ["module1"],
        },
        200
    ),
    # Missing 'categories'
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "prompt_templates": ["template1"],
            "attack_modules": ["module1"],
        },
        200
    ),
    # Missing 'prompt_templates'
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "attack_modules": ["module1"],
        },
        200
    ),
    # Missing 'attack_modules'
    (
        {
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "prompt_templates": ["template1"],
        },
        200
    ),
    # All fields missing
    (
        {},
        422
    )
])
def test_create_recipe(recipe_data, expected_status):
    # Set up the return value for the mock if it's a success scenario
    if expected_status == 200:
        mock_recipe_service.create_recipe.return_value = {"message": "Recipe created successfully"}

    response = client.post("/api/v1/recipes", json=recipe_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize("query_string, mock_return_value, expected_status, expected_response", [
    # Test get all recipes success
    (
        "",
        [
            {
                "id": "test-recipe-1",
                "name": "Test Recipe 1",
                "description": "Description for Test Recipe 1",
                "tags": ["tag1", "tag2"],
                "categories": ["category1"],
                "datasets": ["dataset1"],
                "metrics": ["metric1"],
                "prompt_templates": ["template1"],
                "attack_modules": ["module1"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5
            },
            {
                "id": "test-recipe-2",
                "name": "Test Recipe 2",
                "description": "Description for Test Recipe 2",
                "tags": ["tag3", "tag4"],
                "categories": ["category2"],
                "datasets": ["dataset2"],
                "metrics": ["metric2"],
                "prompt_templates": ["template2"],
                "attack_modules": ["module2"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 3
            },
        ],
        200,
        [
            {
                "id": "test-recipe-1",
                "name": "Test Recipe 1",
                "description": "Description for Test Recipe 1",
                "tags": ["tag1", "tag2"],
                "categories": ["category1"],
                "datasets": ["dataset1"],
                "metrics": ["metric1"],
                "prompt_templates": ["template1"],
                "attack_modules": ["module1"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5
            },
            {
                "id": "test-recipe-2",
                "name": "Test Recipe 2",
                "description": "Description for Test Recipe 2",
                "tags": ["tag3", "tag4"],
                "categories": ["category2"],
                "datasets": ["dataset2"],
                "metrics": ["metric2"],
                "prompt_templates": ["template2"],
                "attack_modules": ["module2"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 3
            },
        ]
    ),
    # Test get recipes by IDs only
    (
        "ids=test-recipe-1,test-recipe-3",
        [
            {
                "id": "test-recipe-1",
                "name": "Filtered Recipe 1 by ID",
                "description": "Filtered Description for Test Recipe 1 by ID",
                "tags": ["tag1", "tag3"],
                "categories": ["category1"],
                "datasets": ["dataset1"],
                "metrics": ["metric1"],
                "prompt_templates": ["template1"],
                "attack_modules": ["module1"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5
            },
            {
                "id": "test-recipe-3",
                "name": "Filtered Recipe 3 by ID",
                "description": "Filtered Description for Test Recipe 3 by ID",
                "tags": ["tag2", "tag4"],
                "categories": ["category3"],
                "datasets": ["dataset3"],
                "metrics": ["metric3"],
                "prompt_templates": ["template3"],
                "attack_modules": ["module3"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset3": 41665
                    }
                },
                "total_prompt_in_recipe": 4
            },
        ],
        200,
        [
            {
                "id": "test-recipe-1",
                "name": "Filtered Recipe 1 by ID",
                "description": "Filtered Description for Test Recipe 1 by ID",
                "tags": ["tag1", "tag3"],
                "categories": ["category1"],
                "datasets": ["dataset1"],
                "metrics": ["metric1"],
                "prompt_templates": ["template1"],
                "attack_modules": ["module1"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5
            },
            {
                "id": "test-recipe-3",
                "name": "Filtered Recipe 3 by ID",
                "description": "Filtered Description for Test Recipe 3 by ID",
                "tags": ["tag2", "tag4"],
                "categories": ["category3"],
                "datasets": ["dataset3"],
                "metrics": ["metric3"],
                "prompt_templates": ["template3"],
                "attack_modules": ["module3"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset3": 41665
                    }
                },
                "total_prompt_in_recipe": 4
            },
        ]
    ),
    # Test get recipes by tags only
    (
        "tags=tag1,tag4",
        [
            {
                "id": "test-recipe-1",
                "name": "Filtered Recipe 1 by Tag",
                "description": "Filtered Description for Test Recipe 1 by Tag",
                "tags": ["tag1"],
                "categories": ["category1"],
                "datasets": ["dataset1"],
                "metrics": ["metric1"],
                "prompt_templates": ["template1"],
                "attack_modules": ["module1"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5
            },
            {
                "id": "test-recipe-4",
                "name": "Filtered Recipe 4 by Tag",
                "description": "Filtered Description for Test Recipe 4 by Tag",
                "tags": ["tag4"],
                "categories": ["category4"],
                "datasets": ["dataset4"],
                "metrics": ["metric4"],
                "prompt_templates": ["template4"],
                "attack_modules": ["module4"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset4": 41665
                    }
                },
                "total_prompt_in_recipe": 2
            },
        ],
        200,
        [
            {
                "id": "test-recipe-1",
                "name": "Filtered Recipe 1 by Tag",
                "description": "Filtered Description for Test Recipe 1 by Tag",
                "tags": ["tag1"],
                "categories": ["category1"],
                "datasets": ["dataset1"],
                "metrics": ["metric1"],
                "prompt_templates": ["template1"],
                "attack_modules": ["module1"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5
            },
            {
                "id": "test-recipe-4",
                "name": "Filtered Recipe 4 by Tag",
                "description": "Filtered Description for Test Recipe 4 by Tag",
                "tags": ["tag4"],
                "categories": ["category4"],
                "datasets": ["dataset4"],
                "metrics": ["metric4"],
                "prompt_templates": ["template4"],
                "attack_modules": ["module4"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset4": 41665
                    }
                },
                "total_prompt_in_recipe": 2
            },
        ]
    ),
    # Test get recipes by categories only
    (
        "categories=category1,category2",
        [
            {
                "id": "test-recipe-2",
                "name": "Filtered Recipe 2 by Category",
                "description": "Filtered Description for Test Recipe 2 by Category",
                "tags": ["tag2", "tag3"],
                "categories": ["category1", "category2"],
                "datasets": ["dataset2"],
                "metrics": ["metric2"],
                "prompt_templates": ["template2"],
                "attack_modules": ["module2"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 3
            },
            {
                "id": "test-recipe-5",
                "name": "Filtered Recipe 5 by Category",
                "description": "Filtered Description for Test Recipe 5 by Category",
                "tags": ["tag5"],
                "categories": ["category2"],
                "datasets": ["dataset5"],
                "metrics": ["metric5"],
                "prompt_templates": ["template5"],
                "attack_modules": ["module5"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset5": 41665
                    }
                },
                "total_prompt_in_recipe": 1
            },
        ],
        200,
        [
            {
                "id": "test-recipe-2",
                "name": "Filtered Recipe 2 by Category",
                "description": "Filtered Description for Test Recipe 2 by Category",
                "tags": ["tag2", "tag3"],
                "categories": ["category1", "category2"],
                "datasets": ["dataset2"],
                "metrics": ["metric2"],
                "prompt_templates": ["template2"],
                "attack_modules": ["module2"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 3
            },
            {
                "id": "test-recipe-5",
                "name": "Filtered Recipe 5 by Category",
                "description": "Filtered Description for Test Recipe 5 by Category",
                "tags": ["tag5"],
                "categories": ["category2"],
                "datasets": ["dataset5"],
                "metrics": ["metric5"],
                "prompt_templates": ["template5"],
                "attack_modules": ["module5"],
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_attack_modules": 1,
                    "num_of_datasets_prompts": {
                        "dataset5": 41665
                    }
                },
                "total_prompt_in_recipe": 1
            },
        ]
    ),
])
def test_get_all_recipes(query_string, mock_return_value, expected_status, expected_response):
    if isinstance(mock_return_value, ServiceException):
        mock_recipe_service.get_all_recipes.side_effect = mock_return_value
    else:
        mock_recipe_service.get_all_recipes.return_value = mock_return_value

    response = client.get(f"/api/v1/recipes?{query_string}")

    assert response.status_code == expected_status
    assert response.json() == expected_response

@pytest.mark.parametrize("service_return, expected_status, expected_response", [
    # Test successful retrieval of recipe names
    (
        ["Recipe One", "Recipe Two"],
        200,
        ["Recipe One", "Recipe Two"]
    ),
    # Test no recipe names found
    (
        ServiceException(
            msg="No recipe names found", method_name="get_all_recipes_name", error_code="FileNotFound"
        ),
        404,
        {"detail": "Failed to retrieve recipe names: [ServiceException] FileNotFound in get_all_recipes_name - No recipe names found"}
    )
])
def test_get_all_recipes_name(service_return, expected_status, expected_response):
    if isinstance(service_return, ServiceException):
        mock_recipe_service.get_all_recipes_name.side_effect = service_return
    else:
        mock_recipe_service.get_all_recipes_name.return_value = service_return

    response = client.get("/api/v1/recipes/name")

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert response.json().get("detail") == expected_response["detail"]

@pytest.mark.parametrize("recipe_id, recipe_data, expected_status", [
    # Test successful update of recipe
    (
        "valid-recipe-id",
        {"name": "Updated Recipe", "description": "Updated description", "tags": ["tag1", "tag2"]},
        200
    ),
    # Test recipe not found
    (
        "invalid-recipe-id",
        {"name": "Non-existent Recipe", "description": "This recipe does not exist", "tags": ["tag1", "tag2"]},
        404
    ),
    # Test validation error
    (
        "valid-recipe-id",
        {"name": "", "description": "Invalid data", "tags": []},  # Invalid data
        400
    ),
])
def test_update_recipe(recipe_id, recipe_data, expected_status):
    if expected_status == 200:
        mock_recipe_service.update_recipe.return_value = None
    elif expected_status == 404:
        mock_recipe_service.update_recipe.side_effect = ServiceException(
            msg="Recipe not found", method_name="update_recipe", error_code="FileNotFound"
        )
    elif expected_status == 400:
        mock_recipe_service.update_recipe.side_effect = ServiceException(
            msg="Validation error", method_name="update_recipe", error_code="ValidationError"
        )

    response = client.put(f"/api/v1/recipes/{recipe_id}", json=recipe_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize("recipe_id, service_exception, expected_status", [
    # Test successful deletion of recipe
    ("valid-recipe-id", None, 200),
    # Test recipe not found
    ("invalid-recipe-id", ServiceException(msg="Recipe not found", method_name="delete_recipe", error_code="FileNotFound"), 404),
    # Test other internal server error
    ("valid-recipe-id", ServiceException(msg="Internal server error", method_name="delete_recipe", error_code="UnknownError"), 500),
])
def test_delete_recipe(recipe_id, service_exception, expected_status):
    if service_exception:
        mock_recipe_service.delete_recipe.side_effect = service_exception
    else:
        mock_recipe_service.delete_recipe.return_value = None

    response = client.delete(f"/api/v1/recipes/{recipe_id}")

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {"message": "Recipe deleted successfully"}
