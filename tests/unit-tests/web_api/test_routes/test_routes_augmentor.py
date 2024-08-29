import pytest

from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("augment_data, mock_return_value, exception, expected_status, expected_response", [
    ({"dataset_id": "my_dataset", "attack_module_id": "my_attack_module"}, "new_dataset_id", None, 200, "new_dataset_id"),
    ({"dataset_id": "", "attack_module_id": "my_attack_module"}, None, 
     ServiceException("Dataset not found", "augment_dataset", "FileNotFound"), 404, {"detail": "Failed to augment dataset: [ServiceException] FileNotFound in augment_dataset - Dataset not found"}),
    ({"dataset_id": "123", "attack_module_id": "abc"}, None, 
     ServiceException("Invalid data", "augment_dataset", "ValidationError"), 400, {"detail": "Failed to augment dataset: [ServiceException] ValidationError in augment_dataset - Invalid data"}),
    ({"dataset_id": "123", "attack_module_id": "abc"}, None, 
     ServiceException("Unknown error", "augment_dataset", "UnknownError"), 500, {"detail": "Failed to augment dataset: [ServiceException] UnknownError in augment_dataset - Unknown error"}),
])
def test_augment_dataset(test_client, mock_augmentor_service, augment_data, mock_return_value, exception, expected_status, expected_response):
    if exception:
        mock_augmentor_service.augment_dataset.side_effect = exception
    else:
        mock_augmentor_service.augment_dataset.return_value = mock_return_value

    # Make the POST request to the API
    response = test_client.post("/api/v1/augment/dataset", json=augment_data)
    
    # Assert the status code and response match the expected values
    assert response.status_code == expected_status
    assert response.json() == expected_response

@pytest.mark.parametrize("augment_data, mock_return_value, exception, expected_status, expected_response", [
    ({"recipe_id": "my_recipe", "attack_module_id": "my_attack_module"}, "new_recipe_id", None, 200, "new_recipe_id"),
    ({"recipe_id": "", "attack_module_id": "my_attack_module"}, None, 
     ServiceException("Recipe not found", "augment_recipe", "FileNotFound"), 404, {"detail": "Failed to augment recipe: [ServiceException] FileNotFound in augment_recipe - Recipe not found"}),
    ({"recipe_id": "123", "attack_module_id": "abc"}, None, 
     ServiceException("Invalid data", "augment_recipe", "ValidationError"), 400, {"detail": "Failed to augment recipe: [ServiceException] ValidationError in augment_recipe - Invalid data"}),
    ({"recipe_id": "123", "attack_module_id": "abc"}, None, 
     ServiceException("Unknown error", "augment_recipe", "UnknownError"), 500, {"detail": "Failed to augment recipe: [ServiceException] UnknownError in augment_recipe - Unknown error"}),
])
def test_augment_recipe(test_client, mock_augmentor_service, augment_data, mock_return_value, exception, expected_status, expected_response):
    if exception:
        mock_augmentor_service.augment_recipe.side_effect = exception
    else:
        mock_augmentor_service.augment_recipe.return_value = mock_return_value

    # Make the POST request to the API
    response = test_client.post("/api/v1/augment/recipe", json=augment_data)
    
    # Assert the status code and response match the expected values
    print(response.json())
    assert response.status_code == expected_status
    assert response.json() == expected_response