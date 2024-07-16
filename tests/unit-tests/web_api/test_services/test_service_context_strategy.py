import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.context_strategy_service import ContextStrategyService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Mock data for successful API calls
MOCK_STRATEGY_METADATA = [
    {
        "id": "add_previous_prompt",
        "name": "Add Previous Prompt",
        "description": "This is a sample context strategy that adds in previous prompts to the current prompt. [Default: 5]"
    },
    {
        "id": "summarize_previous_prompt",
        "name": "Summarize Previous Prompt",
        "description": "This is a sample context strategy that summarize previous prompts to the current prompt."
    }
]
MOCK_STRATEGY_NAMES = ["Add Previous Prompt", "Summarize Previous Prompt"]

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def context_strategy_service():
    return ContextStrategyService()

@patch('moonshot.integrations.web_api.services.context_strategy_service.moonshot_api')
def test_get_ctx_strategy_success(mock_moonshot_api, context_strategy_service):
    """
    Test successful retrieval of context strategies.
    """
    mock_moonshot_api.api_get_all_context_strategy_metadata.return_value = MOCK_STRATEGY_METADATA
    strategies = context_strategy_service.get_ctx_strategy()
    assert strategies == MOCK_STRATEGY_METADATA
    mock_moonshot_api.api_get_all_context_strategy_metadata.assert_called_once()

@patch('moonshot.integrations.web_api.services.context_strategy_service.moonshot_api')
def test_get_ctx_strategy_name_success(mock_moonshot_api, context_strategy_service):
    """
    Test successful retrieval of context strategy names.
    """
    mock_moonshot_api.api_get_all_context_strategies.return_value = MOCK_STRATEGY_NAMES
    strategy_names = context_strategy_service.get_ctx_strategy_name()
    assert strategy_names == MOCK_STRATEGY_NAMES
    mock_moonshot_api.api_get_all_context_strategies.assert_called_once()

@patch('moonshot.integrations.web_api.services.context_strategy_service.moonshot_api')
def test_delete_ctx_strategy_success(mock_moonshot_api, context_strategy_service):
    """
    Test successful deletion of a context strategy.
    """
    context_strategy_service.delete_ctx_strategy("Add Previous Prompt")
    mock_moonshot_api.api_delete_context_strategy.assert_called_once_with("Add Previous Prompt")

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.context_strategy_service.moonshot_api')
def test_get_ctx_strategy_exceptions(mock_moonshot_api, exception, error_code, context_strategy_service):
    """
    Test exception handling for retrieving context strategies.
    """
    mock_moonshot_api.api_get_all_context_strategy_metadata.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        context_strategy_service.get_ctx_strategy()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_context_strategy_metadata.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.context_strategy_service.moonshot_api')
def test_get_ctx_strategy_name_exceptions(mock_moonshot_api, exception, error_code, context_strategy_service):
    """
    Test exception handling for retrieving context strategy names.
    """
    mock_moonshot_api.api_get_all_context_strategies.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        context_strategy_service.get_ctx_strategy_name()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_context_strategies.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.context_strategy_service.moonshot_api')
def test_delete_ctx_strategy_exceptions(mock_moonshot_api, exception, error_code, context_strategy_service):
    """
    Test exception handling for deleting a context strategy.
    """
    mock_moonshot_api.api_delete_context_strategy.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        context_strategy_service.delete_ctx_strategy("Add Previous Prompt")
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_delete_context_strategy.assert_called_once_with("Add Previous Prompt")
