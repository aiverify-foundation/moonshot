import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.augmentor_service import AugmentorService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Mock data for augmentor
MOCK_RECIPE_ID = "mock-recipe-id"
MOCK_DATASET_ID = "mock-dataset-id"
MOCK_ATTACK_MODULE_ID = "mock-attack-module-id"
MOCK_NEW_RECIPE_ID = "mock-new-recipe-id"
MOCK_NEW_DATASET_ID = "mock-new-dataset-id"

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def augmentor_service():
    return AugmentorService()

@patch('moonshot.integrations.web_api.services.augmentor_service.moonshot_api')
def test_augment_recipe_success(mock_moonshot_api, augmentor_service):
    """
    Test case for successful augmentation of a recipe.
    """
    mock_moonshot_api.api_augment_recipe.return_value = MOCK_NEW_RECIPE_ID
    new_recipe_id = augmentor_service.augment_recipe(MOCK_RECIPE_ID, MOCK_ATTACK_MODULE_ID)
    assert new_recipe_id == MOCK_NEW_RECIPE_ID

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.augmentor_service.moonshot_api')
def test_augment_recipe_exceptions(mock_moonshot_api, exception, error_code, augmentor_service):
    """
    Test case for exceptions during augmentation of a recipe.
    """
    mock_moonshot_api.api_augment_recipe.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        augmentor_service.augment_recipe(MOCK_RECIPE_ID, MOCK_ATTACK_MODULE_ID)
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.augmentor_service.moonshot_api')
def test_augment_dataset_success(mock_moonshot_api, augmentor_service):
    """
    Test case for successful augmentation of a dataset.
    """
    mock_moonshot_api.api_augment_dataset.return_value = MOCK_NEW_DATASET_ID
    new_dataset_id = augmentor_service.augment_dataset(MOCK_DATASET_ID, MOCK_ATTACK_MODULE_ID)
    assert new_dataset_id == MOCK_NEW_DATASET_ID

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.augmentor_service.moonshot_api')
def test_augment_dataset_exceptions(mock_moonshot_api, exception, error_code, augmentor_service):
    """
    Test case for exceptions during augmentation of a dataset.
    """
    mock_moonshot_api.api_augment_dataset.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        augmentor_service.augment_dataset(MOCK_DATASET_ID, MOCK_ATTACK_MODULE_ID)
    assert exc_info.value.error_code == error_code