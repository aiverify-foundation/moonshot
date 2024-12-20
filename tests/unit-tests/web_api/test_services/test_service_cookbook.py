import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.cookbook_service import CookbookService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.cookbook_response_model import CookbookResponseModel
from moonshot.src.recipes.recipe_arguments import RecipeArguments as Recipe
from moonshot.integrations.web_api.schemas.cookbook_create_dto import CookbookCreateDTO
from moonshot.integrations.web_api.schemas.cookbook_create_dto import CookbookUpdateDTO

MOCK_COOKBOOKS = [
    {
        "id": "test-cookbook-1",
        "name": "Test Cookbook 1",
        "description": "Test Cookbook description",
        "tags": [],
        "categories": [],
        "recipes": [
            "recipe-1",
            "recipe-2",
            "recipe-3"
        ],
        "total_prompt_in_cookbook": None,
        'total_dataset_in_cookbook': None,
        "endpoint_required": None
    },
    {
        "id": "test-cookbook-2",
        "name": "Test Cookbook 2",
        "description": "Test Cookbook description",
        "tags": [],
        "categories": [],
        "recipes": [
            "recipe-1",
            "recipe-2",
            "recipe-3"
        ],
        "total_prompt_in_cookbook": None,
        'total_dataset_in_cookbook': None,
        "endpoint_required": None
    }
]
MOCK_COOKBOOK_NAMES = ["test-cookbook-1","test-cookbook-2"]

MOCK_COOKBOOK_CREATE_DTO = CookbookCreateDTO(
    name="New Cookbook",
    description="A new cookbook description",
    recipes=["recipe-1", "recipe-2"]
)

MOCK_COOKBOOK_UPDATE_DTO = CookbookUpdateDTO(
    name="Updated Cookbook",
    description="An updated cookbook description",
    tags= [],
    categories= [],
    recipes=["recipe-1", "recipe-2", "recipe-3"]
)

# Exception scenarios to test
exception_scenarios = [
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def cookbook_service():
    return CookbookService()

@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_get_all_cookbooks_success(mock_moonshot_api, cookbook_service):
    """
    Test case for successful retrieval of all cookbooks.
    """
    mock_moonshot_api.api_get_all_cookbook.return_value = MOCK_COOKBOOKS
    cookbooks = cookbook_service.get_all_cookbooks(tags="", categories="", count=False)
    expected_cookbooks = [CookbookResponseModel(**cb) for cb in MOCK_COOKBOOKS]
    assert cookbooks == expected_cookbooks
    mock_moonshot_api.api_get_all_cookbook.assert_called_once()

@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_get_all_cookbooks_names_success(mock_moonshot_api, cookbook_service):
    """
    Test case for successful retrieval of all cookbook names.
    """
    mock_moonshot_api.api_get_all_cookbook_name.return_value = MOCK_COOKBOOK_NAMES
    cookbook_names = cookbook_service.get_all_cookbooks_names()
    assert cookbook_names == MOCK_COOKBOOK_NAMES
    mock_moonshot_api.api_get_all_cookbook_name.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_get_all_cookbooks_exceptions(mock_moonshot_api, exception, error_code, cookbook_service):
    """
    Test case for exceptions during retrieval of all cookbooks.
    """
    mock_moonshot_api.api_get_all_cookbook.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        cookbook_service.get_all_cookbooks(tags="", categories="", count=False)
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_cookbook.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_get_all_cookbooks_names_exceptions(mock_moonshot_api, exception, error_code, cookbook_service):
    """
    Test case for exceptions during retrieval of all cookbook names.
    """
    mock_moonshot_api.api_get_all_cookbook_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        cookbook_service.get_all_cookbooks_names()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_cookbook_name.assert_called_once()

@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_create_cookbook_success(mock_moonshot_api, cookbook_service):
    """
    Test case for successful creation of a cookbook.
    """
    cookbook_service.create_cookbook(MOCK_COOKBOOK_CREATE_DTO)
    mock_moonshot_api.api_create_cookbook.assert_called_once_with(
        name=MOCK_COOKBOOK_CREATE_DTO.name,
        description=MOCK_COOKBOOK_CREATE_DTO.description,
        recipes=MOCK_COOKBOOK_CREATE_DTO.recipes
    )

@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_update_cookbook_success(mock_moonshot_api, cookbook_service):
    """
    Test case for successful update of a cookbook.
    """
    cookbook_service.update_cookbook(MOCK_COOKBOOK_UPDATE_DTO, "cookbook_id")
    mock_moonshot_api.api_update_cookbook.assert_called_once_with(
        cb_id="cookbook_id",
        name=MOCK_COOKBOOK_UPDATE_DTO.name,
        description=MOCK_COOKBOOK_UPDATE_DTO.description,
        tags= MOCK_COOKBOOK_UPDATE_DTO.tags,
        categories= MOCK_COOKBOOK_UPDATE_DTO.categories,
        recipes=MOCK_COOKBOOK_UPDATE_DTO.recipes
    )

@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_delete_cookbook_success(mock_moonshot_api, cookbook_service):
    """
    Test case for successful deletion of a cookbook.
    """
    cookbook_service.delete_cookbook("cookbook_id")
    mock_moonshot_api.api_delete_cookbook.assert_called_once_with("cookbook_id")

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_create_cookbook_exceptions(mock_moonshot_api, exception, error_code, cookbook_service):
    """
    Test case for exceptions during creation of a cookbook.
    """
    mock_moonshot_api.api_create_cookbook.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        cookbook_service.create_cookbook(MOCK_COOKBOOK_CREATE_DTO)
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_update_cookbook_exceptions(mock_moonshot_api, exception, error_code, cookbook_service):
    """
    Test case for exceptions during update of a cookbook.
    """
    mock_moonshot_api.api_update_cookbook.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        cookbook_service.update_cookbook(MOCK_COOKBOOK_UPDATE_DTO, "cookbook_id")
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.cookbook_service.moonshot_api')
def test_delete_cookbook_exceptions(mock_moonshot_api, exception, error_code, cookbook_service):
    """
    Test case for exceptions during deletion of a cookbook.
    """
    mock_moonshot_api.api_delete_cookbook.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        cookbook_service.delete_cookbook("cookbook_id")
    assert exc_info.value.error_code == error_code
