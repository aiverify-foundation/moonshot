import pytest
from unittest.mock import patch, Mock
from moonshot.integrations.web_api.services.attack_module_service import AttackModuleService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Mock data for successful API calls
MOCK_ATTACK_MODULES = ['module1', 'module2', 'module3']
MOCK_ATTACK_MODULE_METADATA = [
    {'id': 'module1', 'name': 'module1', 'description': 'desc1'},
    {'id': 'module2', 'name': 'module2', 'description': 'desc2'},
    {'id': 'module3', 'name': 'module3', 'description': 'desc3'},
]

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def attack_module_service():
    return AttackModuleService()


@patch('moonshot.integrations.web_api.services.attack_module_service.moonshot_api')
def test_get_all_attack_module_success(mock_moonshot_api, attack_module_service):
    """
    Test case for successful retrieval of all attack modules.
    """
    mock_moonshot_api.api_get_all_attack_modules.return_value = MOCK_ATTACK_MODULES
    result = attack_module_service.get_all_attack_module()
    assert result == MOCK_ATTACK_MODULES
    mock_moonshot_api.api_get_all_attack_modules.assert_called_once()

@patch('moonshot.integrations.web_api.services.attack_module_service.moonshot_api')
def test_get_all_attack_module_metadata_success(mock_moonshot_api, attack_module_service):
    """
    Test case for successful retrieval of all attack module metadata.
    """
    mock_moonshot_api.api_get_all_attack_module_metadata.return_value = MOCK_ATTACK_MODULE_METADATA
    result = attack_module_service.get_all_attack_module_metadata()
    assert result == MOCK_ATTACK_MODULE_METADATA
    mock_moonshot_api.api_get_all_attack_module_metadata.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.attack_module_service.moonshot_api')
def test_get_all_attack_module_exceptions(mock_moonshot_api, exception, error_code, attack_module_service):
    """
    Test case for handling exceptions during retrieval of all attack modules.
    """
    mock_moonshot_api.api_get_all_attack_modules.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        attack_module_service.get_all_attack_module()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_attack_modules.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.attack_module_service.moonshot_api')
def test_get_all_attack_module_metadata_exceptions(mock_moonshot_api, exception, error_code, attack_module_service):
    """
    Test case for handling exceptions during retrieval of all attack module metadata.
    """
    mock_moonshot_api.api_get_all_attack_module_metadata.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        attack_module_service.get_all_attack_module_metadata()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_attack_module_metadata.assert_called_once()
