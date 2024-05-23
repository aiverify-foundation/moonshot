import pytest
from unittest.mock import patch, AsyncMock, Mock
from moonshot.integrations.web_api.services.session_service import SessionService
from moonshot.integrations.web_api.schemas.session_create_dto import SessionCreateDTO
from moonshot.integrations.web_api.schemas.session_response_model import SessionResponseModel
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.session_prompt_dto import SessionPromptDTO
from moonshot.integrations.web_api.schemas.prompt_response_model import PromptResponseModel
from moonshot.src.runners.runner import Runner


# Mock data for successful API calls
MOCK_SESSION_CREATE_DTO = SessionCreateDTO(
    name="Test Session",
    endpoints=["endpoint1", "endpoint2"],
    description="A test session",
    context_strategy="strategy1",
    prompt_template="template1",
    cs_num_of_prev_prompts=5,
    attack_module="module1",
    metric="metric1",
    system_prompt="prompt1"
)

MOCK_SESSION_METADATA = {
    "session_id": "test-session-1",
    "description": "Test Session",
    "endpoints": ["endpoint-1"],
    "created_epoch": "1716384285.944733",
    "created_datetime": "20240522-212445",
    "prompt_template": "",
    "context_strategy": "",
    "cs_num_of_prev_prompts": 5,
    "attack_module": "",
    "metric": "",
    "system_prompt": ""
}

MOCK_SESSION_NAMES = ["test-session-1"]

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def session_service():
    return SessionService(auto_red_team_test_manager=AsyncMock(), progress_status_updater=AsyncMock(), runner_service=AsyncMock())
    
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_session_success(mock_moonshot_api, session_service):
    mock_moonshot_api.api_get_all_session_metadata.return_value = [MOCK_SESSION_METADATA]
    sessions = session_service.get_all_session()
    assert len(sessions) == 1
    mock_moonshot_api.api_get_all_session_metadata.assert_called_once()

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_sessions_names_success(mock_moonshot_api, session_service):
    mock_moonshot_api.api_get_all_session_names.return_value = MOCK_SESSION_NAMES
    session_names = session_service.get_all_sessions_names()
    assert session_names == MOCK_SESSION_NAMES
    mock_moonshot_api.api_get_all_session_names.assert_called_once()


@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_session_exception(mock_moonshot_api, session_service, exception, error_code):
    mock_moonshot_api.api_get_all_session_metadata.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        session_service.get_all_session()
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_sessions_names_exception(mock_moonshot_api, session_service, exception, error_code):
    mock_moonshot_api.api_get_all_session_names.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        session_service.get_all_sessions_names()
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_delete_session_success(mock_moonshot_api, session_service):
    runner_id = "test-runner-id"
    # No return value needed for delete operation, since it should return None
    session_service.delete_session(runner_id)
    # Assert that the api_delete_session was called once with the correct runner_id
    mock_moonshot_api.api_delete_session.assert_called_once_with(runner_id)

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_delete_session_exception(mock_moonshot_api, session_service, exception, error_code):
    runner_id = "test-runner-id"
    # Set the side effect of the API call to raise the exception
    mock_moonshot_api.api_delete_session.side_effect = exception
    # Use pytest.raises to check for ServiceException
    with pytest.raises(ServiceException) as exc_info:
        session_service.delete_session(runner_id)
    # Check if the error code matches the expected error code
    assert exc_info.value.error_code == error_code


@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_prompt_template_success(mock_moonshot_api, session_service):
# Create a mock Runner object with a specific id
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Set the prompt template name to be selected
    prompt_template_name = "template-name"

    # Call the method under test
    session_service.select_prompt_template(mock_runner.id, prompt_template_name)

    # Assert that the api_update_prompt_template was called once with the correct parameters
    mock_moonshot_api.api_update_prompt_template.assert_called_once_with(mock_runner.id, prompt_template_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_context_strategy_success(mock_moonshot_api, session_service):
# Create a mock Runner object with a specific id
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Set the context strategy name to be selected
    context_strategy_name = "cs-name"

    # Call the method under test
    session_service.select_ctx_strategy(mock_runner.id, context_strategy_name)

    # Assert that the api_update_context_strategy was called once with the correct parameters
    mock_moonshot_api.api_update_context_strategy.assert_called_once_with(mock_runner.id, context_strategy_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_attack_module_success(mock_moonshot_api, session_service):
# Create a mock Runner object with a specific id
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Set the attack_module name to be selected
    attack_module_name = "am-name"

    # Call the method under test
    session_service.select_attack_module(mock_runner.id, attack_module_name)

    # Assert that the api_update_attack_module was called once with the correct parameters
    mock_moonshot_api.api_update_attack_module.assert_called_once_with(mock_runner.id, attack_module_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_metric_success(mock_moonshot_api, session_service):
# Create a mock Runner object with a specific id
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Set the metric name to be selected
    metric_name = "metric-name"

    # Call the method under test
    session_service.select_metric(mock_runner.id, metric_name)

    # Assert that the api_update_metric was called once with the correct parameters
    mock_moonshot_api.api_update_metric.assert_called_once_with(mock_runner.id, metric_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_update_system_prompt_success(mock_moonshot_api, session_service):
# Create a mock Runner object with a specific id
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Set the context strategy name to be selected
    system_prompt = "prompt"

    # Call the method under test
    session_service.update_system_prompt(mock_runner.id, system_prompt)

    # Assert that the api_update_system_prompt was called once with the correct parameters
    mock_moonshot_api.api_update_system_prompt.assert_called_once_with(mock_runner.id, system_prompt)

@pytest.mark.asyncio
async def test_cancel_auto_redteam_success(session_service):
    # Create a mock Runner object with a specific id
    mock_runner = AsyncMock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Mock the cancel_task method of the auto_red_team_test_manager
    session_service.auto_red_team_test_manager.cancel_task = AsyncMock()

    # Call the method under test
    await session_service.cancel_auto_redteam(mock_runner.id)

    # Assert that the cancel_task was called once with the correct runner_id
    session_service.auto_red_team_test_manager.cancel_task.assert_called_once_with(mock_runner.id)

@pytest.mark.asyncio
async def test_end_session_success(session_service):
    # Create a mock Runner object with a specific id
    mock_runner = AsyncMock(spec=Runner)
    mock_runner.id = "test-runner-id"

    # Assign the mock Runner to active_runner
    session_service.active_runner = mock_runner

    # Mock the close method of the active_runner
    session_service.active_runner.close = AsyncMock()

    # Call the method under test
    await session_service.end_session(mock_runner.id)

    # Assert that the close method was called once
    session_service.active_runner.close.assert_called_once()
