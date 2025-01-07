import pytest

from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException


@pytest.mark.parametrize("recipe_data, exception, expected_status, expected_response", [
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
        },
        None,
        200,
        {"message": "Recipe created successfully"}
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
        None,
        422,
        None
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
        None,
        422,
        None
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
        None,
        422,
        None
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
        },
        None,
        200,
        {"message": "Recipe created successfully"}
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
        },
        None,
        200,
        {"message": "Recipe created successfully"}
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
        },
        None,
        200,
        {"message": "Recipe created successfully"}
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
        },
        None,
        200,
        {"message": "Recipe created successfully"}
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
            "name": "Test Recipe",
            "description": "A test recipe description",
            "tags": ["tag1", "tag2"],
            "categories": ["category1"],
            "datasets": ["dataset1"],
            "metrics": ["metric1"],
            "prompt_templates": ["template1"],
        },
        ServiceException("A file not found error occurred", "create_recipe", "FileNotFound"),
        404, None
    ),
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
        ServiceException("A validation error occurred", "create_recipe", "ValidationError"),
        400, None
    ),
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
        ServiceException("An unexpected error occurred", "create_recipe", "UnknownError"),
        500, None
    )
])
def test_create_recipe(test_client, mock_recipe_service, recipe_data, exception, expected_status, expected_response):
    if exception:
        mock_recipe_service.create_recipe.side_effect = exception
    else:
        mock_recipe_service.create_recipe.return_value = recipe_data 

    response = test_client.post("/api/v1/recipes", json=recipe_data)

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        if expected_status != 422:
            assert response.json() == expected_response

@pytest.mark.parametrize("query_string, mock_return_value, exception, expected_status, expected_response", [
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
            },
        ],
        None,
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset3": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
            },
        ],
        None,
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset3": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset4": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
            },
        ],
        None,
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset1": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset4": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset5": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
            },
        ],
        None,
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 2,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset2": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
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
                "grading_scale": {},
                "stats": {
                    "num_of_tags": 1,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {
                        "dataset5": 41665
                    }
                },
                "total_prompt_in_recipe": 5,
                "required_config": None
            },
        ]
    ),
    # Exception cases
    (None, None, ServiceException("A file not found error occurred", "get_all_metric", "FileNotFound"), 404, None),
    (None, None, ServiceException("A validation error occurred", "get_all_metric", "ValidationError"), 400, None),
    (None, None, ServiceException("An value error occurred", "get_all_metric", "ValueError"), 500, None),
])
def test_get_all_recipes(test_client, mock_recipe_service, query_string, mock_return_value, exception, expected_status, expected_response):
    if exception:
        mock_recipe_service.get_all_recipes.side_effect = exception
    else:
        mock_recipe_service.get_all_recipes.return_value = mock_return_value

    response = test_client.get(f"/api/v1/recipes?{query_string}")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response

@pytest.mark.parametrize("mock_return_value, exception, expected_status, expected_response", [
    (
        ["Recipe One", "Recipe Two"],
        None,
        200,
        ["Recipe One", "Recipe Two"]
    ),
    (
        None,
        ServiceException("A file not found error occurred", "get_all_recipes_names", "FileNotFound"),
        404, None
    ),
    (
        None,
        ServiceException("A validation error occurred", "get_all_recipes_names", "ValidationError"),
        400, None
    ),
    (
        None,
        ServiceException("An value error occurred", "get_all_recipes_names", "ValueError"),
        500, None
    )
])
def test_get_all_recipes_name(test_client, mock_recipe_service ,mock_return_value, exception, expected_status, expected_response):
    if exception:
        mock_recipe_service.get_all_recipes_name.side_effect = exception
    else:
        mock_recipe_service.get_all_recipes_name.return_value = mock_return_value

    response = test_client.get("/api/v1/recipes/name")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response


@pytest.mark.parametrize("recipe_id, recipe_data, expected_status, expected_response", [
    # Test successful update of recipe
    (
        "valid-recipe-id",
        {"name": "Updated Recipe", "description": "Updated description", "tags": ["tag1", "tag2"]},
        200,
        {"message": "Recipe updated successfully"}
    ),
    # Test recipe not found
    (
        "invalid-recipe-id",
        {"name": "Non-existent Recipe", "description": "This recipe does not exist", "tags": ["tag1", "tag2"]},
        404,
        ServiceException("Recipe not found", "update_recipe", "FileNotFound")
    ),
    # Test validation error
    (
        "valid-recipe-id",
        {"name": "", "description": "Invalid data", "tags": []},  # Invalid data
        400,
        ServiceException("Validation error", "update_recipe", "ValidationError")
    ),
    # Test unknown error
    (
        "valid-recipe-id",
        {"name": "Updated Recipe", "description": "Updated description", "tags": ["tag1", "tag2"]},
        500,
        ServiceException("Unknown error", "update_recipe", "UnknownError")
    ),
])
def test_update_recipe(test_client, mock_recipe_service, recipe_id, recipe_data, expected_status, expected_response):
    if isinstance(expected_response, ServiceException):
        mock_recipe_service.update_recipe.side_effect = expected_response
    else:
        mock_recipe_service.update_recipe.return_value = recipe_data

    response = test_client.put(f"/api/v1/recipes/{recipe_id}", json=recipe_data)

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    elif isinstance(expected_response, ServiceException):
        assert expected_response.msg in response.json()["detail"]

@pytest.mark.parametrize("recipe_id, service_exception, expected_status, expected_response", [
    # Test successful deletion of recipe
    ("valid-recipe-id", None, 200, {"message": "Recipe deleted successfully"}),
    # Test recipe not found
    ("invalid-recipe-id", ServiceException(msg="Recipe not found", method_name="delete_recipe", error_code="FileNotFound"), 404, None),
    # Test validation error
    ("valid-recipe-id", ServiceException(msg="Validation error", method_name="delete_recipe", error_code="ValidationError"), 400, None),
    # Test unknown error
    ("valid-recipe-id", ServiceException(msg="Internal server error", method_name="delete_recipe", error_code="UnknownError"), 500, None),
])
def test_delete_recipe(test_client, mock_recipe_service, recipe_id, service_exception, expected_status, expected_response):
    if service_exception:
        mock_recipe_service.delete_recipe.side_effect = service_exception
    else:
        mock_recipe_service.delete_recipe.return_value = None

    response = test_client.delete(f"/api/v1/recipes/{recipe_id}")

    # Assert the expected status code
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert service_exception.msg in response.json()["detail"]
