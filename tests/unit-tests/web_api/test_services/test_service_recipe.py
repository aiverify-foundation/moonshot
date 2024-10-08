import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.recipe_service import RecipeService
from moonshot.integrations.web_api.schemas.recipe_create_dto import RecipeCreateDTO
from moonshot.integrations.web_api.schemas.recipe_create_dto import RecipeUpdateDTO
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.recipe_response_model import RecipeResponseModel

MOCK_RECIPES = [
    {
        "id": "realtime-qa",
        "name": "RealtimeQA",
        "description": "RealTime QA is a dynamic question answering (QA) platform.",
        "tags": ["Hallucination"],
        "categories": ["Trust & Safety"],
        "datasets": ["realtimeqa-past"],
        "prompt_templates": [],
        "metrics": ["exactstrmatch"],
        "grading_scale": {},
        "stats": {
            "num_of_datasets_prompts": {"realtimeqa-past": 50}
        },
        "total_prompt_in_recipe": 50,
        "endpoint_required": None
    }
]

MOCK_RECIPE_NAMES = ["RealtimeQA"]

MOCK_RECIPE_CREATE_DTO = RecipeCreateDTO(
    name="RealtimeQA",
    description="RealTime QA is a dynamic question answering (QA) platform that inquires about the present.",
    tags=["Hallucination"],
    categories=["Trust & Safety"],
    datasets=["realtimeqa-past"],
    prompt_templates=[],
    metrics=["exactstrmatch"],
    grading_scale={}
)

MOCK_RECIPE_UPDATE_DTO = RecipeUpdateDTO(
    name="Updated RealtimeQA",
    description="Updated description.",
    tags=["Updated Hallucination"],
    categories=["Updated Trust & Safety"],
    datasets=["realtimeqa-past-updated"],
    prompt_templates=[],
    metrics=["updatedexactstrmatch"],
    grading_scale={}
)

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def recipe_service():
    return RecipeService()

@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_get_all_recipes_success(mock_moonshot_api, recipe_service):
    """
    Test case for getting all recipes successfully.
    """
    mock_moonshot_api.api_get_all_recipe.return_value = MOCK_RECIPES
    recipes = recipe_service.get_all_recipes(tags="", categories="", sort_by="id", count=True)
    expected_recipes = [RecipeResponseModel(**recipe) for recipe in MOCK_RECIPES]
    assert recipes == expected_recipes
    mock_moonshot_api.api_get_all_recipe.assert_called_once()

@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_get_all_recipes_name_success(mock_moonshot_api, recipe_service):
    """
    Test case for getting all recipe names successfully.
    """
    mock_moonshot_api.api_get_all_recipe_name.return_value = MOCK_RECIPE_NAMES
    recipe_names = recipe_service.get_all_recipes_name()
    assert recipe_names == MOCK_RECIPE_NAMES
    mock_moonshot_api.api_get_all_recipe_name.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_get_all_recipes_exceptions(mock_moonshot_api, exception, error_code, recipe_service):
    """
    Test case for handling exceptions when getting all recipes.
    """
    mock_moonshot_api.api_get_all_recipe.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        recipe_service.get_all_recipes(tags="", categories="", sort_by="id", count=True)
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_get_all_recipes_name_exceptions(mock_moonshot_api, exception, error_code, recipe_service):
    """
    Test case for handling exceptions when getting all recipe names.
    """
    mock_moonshot_api.api_get_all_recipe_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        recipe_service.get_all_recipes_name()
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_create_recipe_success(mock_moonshot_api, recipe_service):
    """
    Test case for creating a recipe successfully.
    """
    recipe_service.create_recipe(MOCK_RECIPE_CREATE_DTO)
    mock_moonshot_api.api_create_recipe.assert_called_once_with(
        name=MOCK_RECIPE_CREATE_DTO.name,
        description=MOCK_RECIPE_CREATE_DTO.description,
        tags=MOCK_RECIPE_CREATE_DTO.tags,
        categories=MOCK_RECIPE_CREATE_DTO.categories,
        datasets=MOCK_RECIPE_CREATE_DTO.datasets,
        prompt_templates=MOCK_RECIPE_CREATE_DTO.prompt_templates,
        metrics=MOCK_RECIPE_CREATE_DTO.metrics,
        grading_scale=MOCK_RECIPE_CREATE_DTO.grading_scale
    )

@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_update_recipe_success(mock_moonshot_api, recipe_service):
    """
    Test case for updating a recipe successfully.
    """
    recipe_service.update_recipe(MOCK_RECIPE_UPDATE_DTO, "realtime-qa")
    mock_moonshot_api.api_update_recipe.assert_called_once_with(
        rec_id="realtime-qa",
        **{k: v for k, v in MOCK_RECIPE_UPDATE_DTO.to_dict().items() if v is not None and k not in ["id", "stats"]}
    )

@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_delete_recipe_success(mock_moonshot_api, recipe_service):
    """
    Test case for deleting a recipe successfully.
    """
    recipe_service.delete_recipe("realtime-qa")
    mock_moonshot_api.api_delete_recipe.assert_called_once_with("realtime-qa")

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_create_recipe_exceptions(mock_moonshot_api, exception, error_code, recipe_service):
    """
    Test case for handling exceptions when creating a recipe.
    """
    mock_moonshot_api.api_create_recipe.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        recipe_service.create_recipe(MOCK_RECIPE_CREATE_DTO)
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_update_recipe_exceptions(mock_moonshot_api, exception, error_code, recipe_service):
    """
    Test case for handling exceptions when updating a recipe.
    """
    mock_moonshot_api.api_update_recipe.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        recipe_service.update_recipe(MOCK_RECIPE_UPDATE_DTO, "realtime-qa")
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.recipe_service.moonshot_api')
def test_delete_recipe_exceptions(mock_moonshot_api, exception, error_code, recipe_service):
    """
    Test case for handling exceptions when deleting a recipe.
    """
    mock_moonshot_api.api_delete_recipe.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        recipe_service.delete_recipe("realtime-qa")
    assert exc_info.value.error_code == error_code
