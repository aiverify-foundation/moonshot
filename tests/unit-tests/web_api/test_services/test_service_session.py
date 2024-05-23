import pytest
from unittest.mock import patch, AsyncMock, Mock
from moonshot.integrations.web_api.services.session_service import SessionService
from moonshot.integrations.web_api.schemas.session_create_dto import SessionCreateDTO
from moonshot.integrations.web_api.schemas.session_response_model import SessionResponseModel
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.session_prompt_dto import SessionPromptDTO
from moonshot.integrations.web_api.schemas.prompt_response_model import PromptResponseModel
from moonshot.src.runners.runner import Runner
from moonshot.src.storage.db_interface import DBInterface


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
    """
    Test retrieval of all session metadata is successful.
    """
    mock_moonshot_api.api_get_all_session_metadata.return_value = [MOCK_SESSION_METADATA]
    sessions = session_service.get_all_session()
    assert len(sessions) == 1
    mock_moonshot_api.api_get_all_session_metadata.assert_called_once()

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_sessions_names_success(mock_moonshot_api, session_service):
    """
    Test retrieval of all session names is successful.
    """
    mock_moonshot_api.api_get_all_session_names.return_value = MOCK_SESSION_NAMES
    session_names = session_service.get_all_sessions_names()
    assert session_names == MOCK_SESSION_NAMES
    mock_moonshot_api.api_get_all_session_names.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_session_exception(mock_moonshot_api, session_service, exception, error_code):
    """
    Test retrieval of all session metadata raises an exception.
    """
    mock_moonshot_api.api_get_all_session_metadata.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        session_service.get_all_session()
    assert exc_info.value.error_code == error_code

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_get_all_sessions_names_exception(mock_moonshot_api, session_service, exception, error_code):
    """
    Test retrieval of all session names raises an exception.
    """
    mock_moonshot_api.api_get_all_session_names.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        session_service.get_all_sessions_names()
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_delete_session_success(mock_moonshot_api, session_service):
    """
    Test successful deletion of a session.
    """
    runner_id = "test-runner-id"
    session_service.delete_session(runner_id)
    mock_moonshot_api.api_delete_session.assert_called_once_with(runner_id)

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_delete_session_exception(mock_moonshot_api, session_service, exception, error_code):
    """
    Test deletion of a session raises an exception.
    """
    runner_id = "test-runner-id"
    mock_moonshot_api.api_delete_session.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        session_service.delete_session(runner_id)
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_prompt_template_success(mock_moonshot_api, session_service):
    """
    Test successful selection of a prompt template.
    """
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    prompt_template_name = "template-name"
    session_service.select_prompt_template(mock_runner.id, prompt_template_name)
    mock_moonshot_api.api_update_prompt_template.assert_called_once_with(mock_runner.id, prompt_template_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_context_strategy_success(mock_moonshot_api, session_service):
    """
    Test successful selection of a context strategy.
    """
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    context_strategy_name = "cs-name"
    session_service.select_ctx_strategy(mock_runner.id, context_strategy_name)
    mock_moonshot_api.api_update_context_strategy.assert_called_once_with(mock_runner.id, context_strategy_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_attack_module_success(mock_moonshot_api, session_service):
    """
    Test successful selection of an attack module.
    """
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    attack_module_name = "am-name"
    session_service.select_attack_module(mock_runner.id, attack_module_name)
    mock_moonshot_api.api_update_attack_module.assert_called_once_with(mock_runner.id, attack_module_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_select_metric_success(mock_moonshot_api, session_service):
    """
    Test successful selection of a metric.
    """
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    metric_name = "metric-name"
    session_service.select_metric(mock_runner.id, metric_name)
    mock_moonshot_api.api_update_metric.assert_called_once_with(mock_runner.id, metric_name)

@patch('moonshot.integrations.web_api.services.session_service.moonshot_api')
def test_update_system_prompt_success(mock_moonshot_api, session_service):
    """
    Test successful update of the system prompt.
    """
    mock_runner = Mock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    system_prompt = "prompt"
    session_service.update_system_prompt(mock_runner.id, system_prompt)
    mock_moonshot_api.api_update_system_prompt.assert_called_once_with(mock_runner.id, system_prompt)

@pytest.mark.asyncio
async def test_cancel_auto_redteam_success(session_service):
    """Test successful cancellation of an auto red team task."""
    mock_runner = AsyncMock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    session_service.auto_red_team_test_manager.cancel_task = AsyncMock()
    await session_service.cancel_auto_redteam(mock_runner.id)
    session_service.auto_red_team_test_manager.cancel_task.assert_called_once_with(mock_runner.id)

@pytest.mark.asyncio
async def test_end_session_success(session_service):
    """Test successful end of a session."""
    mock_runner = AsyncMock(spec=Runner)
    mock_runner.id = "test-runner-id"
    session_service.active_runner = mock_runner
    session_service.active_runner.close = AsyncMock()
    await session_service.end_session(mock_runner.id)
    session_service.active_runner.close.assert_called_once()
