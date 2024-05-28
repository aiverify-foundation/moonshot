import pytest
from unittest.mock import patch, Mock
from moonshot.integrations.web_api.services.dataset_service import DatasetService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.dataset_response_dto import DatasetResponseDTO

# Mock data for successful API calls
MOCK_DATASETS = [
    {
        "id": "squad-shifts-tnf",
        "name": "squad-shifts-tnf",
        "description": "Zero-shot reading comprehension on paragraphs and questions from squadshifts",
        "num_of_dataset_prompts": 48201,
        "created_date": "2024-05-14 21:36:21"
    },
    {
        "id": "advglue-all",
        "name": "advglue",
        "description": "Adversarial GLUE Benchmark (AdvGLUE) is a comprehensive robustness evaluation benchmark that focuses on the adversarial robustness evaluation of language models. ",
        "num_of_dataset_prompts": 721,
        "created_date": "2024-05-14 21:36:20"
    }
]
MOCK_DATASET_NAMES = ['squad-shifts-tnf', 'advglue']

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def dataset_service():
    return DatasetService()

@patch('moonshot.integrations.web_api.services.dataset_service.moonshot_api')
def test_get_all_datasets_success(mock_moonshot_api, dataset_service):
    """
    Test case for successful retrieval of all datasets.
    """
    mock_moonshot_api.api_get_all_datasets.return_value = MOCK_DATASETS
    datasets = dataset_service.get_all_datasets()
    assert datasets == [DatasetResponseDTO.model_validate(dataset) for dataset in MOCK_DATASETS]
    mock_moonshot_api.api_get_all_datasets.assert_called_once()

@patch('moonshot.integrations.web_api.services.dataset_service.moonshot_api')
def test_get_all_datasets_name_success(mock_moonshot_api, dataset_service):
    """
    Test case for successful retrieval of all dataset names.
    """
    mock_moonshot_api.api_get_all_datasets_name.return_value = MOCK_DATASET_NAMES
    dataset_names = dataset_service.get_all_datasets_name()
    assert dataset_names == MOCK_DATASET_NAMES
    mock_moonshot_api.api_get_all_datasets_name.assert_called_once()

@patch('moonshot.integrations.web_api.services.dataset_service.moonshot_api')
def test_delete_dataset_success(mock_moonshot_api, dataset_service):
    """
    Test case for successful deletion of a dataset.
    """
    dataset_service.delete_dataset('1')
    mock_moonshot_api.api_delete_dataset.assert_called_once_with('1')

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.dataset_service.moonshot_api')
def test_get_all_datasets_exceptions(mock_moonshot_api, exception, error_code, dataset_service):
    """
    Test case for exceptions during retrieval of all datasets.
    """
    mock_moonshot_api.api_get_all_datasets.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        dataset_service.get_all_datasets()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_datasets.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.dataset_service.moonshot_api')
def test_get_all_datasets_name_exceptions(mock_moonshot_api, exception, error_code, dataset_service):
    """
    Test case for exceptions during retrieval of all dataset names.
    """
    mock_moonshot_api.api_get_all_datasets_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        dataset_service.get_all_datasets_name()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_datasets_name.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.dataset_service.moonshot_api')
def test_delete_dataset_exceptions(mock_moonshot_api, exception, error_code, dataset_service):
    """
    Test case for exceptions during dataset deletion.
    """
    mock_moonshot_api.api_delete_dataset.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        dataset_service.delete_dataset('1')
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_delete_dataset.assert_called_once_with('1')