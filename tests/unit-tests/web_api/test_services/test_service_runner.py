import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.runner_service import RunnerService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Mock data for successful API calls
MOCK_RUNNERS = [
    {
        "id": "test_runner_1",
        "name": "test runner 1",
        "database_file": "../moonshot-data/generated-outputs/databases/test_runner_1.db",
        "endpoints": [
            "endpoint-1",
            "endpoint-2",
        ],
        "description": "hello"
    },
    {
        "id": "test_runner_2",
        "name": "test runner 2",
        "database_file": "../moonshot-data/generated-outputs/databases/test_runner_2.db",
        "endpoints": [
            "endpoint-1",
            "endpoint-2",
        ],
        "description": ""
    }
]
MOCK_RUNNER_NAMES = ["test_runner_1","test_runner_2"]
MOCK_RUNNER_DETAILS = {
    "run_id": 1,
    "runner_id": "test_runner_1",
    "runner_args": {
        "cookbooks": [
            "leaderboard-cookbook"
        ],
        "num_of_prompts": 5,
        "random_seed": 0,
        "system_prompt": "",
        "runner_processing_module": "benchmarking",
        "result_processing_module": "benchmarking-result"
    },
        "endpoints": [
            "endpoint-1",
            "endpoint-2",
        ],
    "start_time": 1716106071.3418639
}

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def runner_service():
    return RunnerService()

@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_get_all_runner_success(mock_moonshot_api, runner_service):
    """
    Test for successful retrieval of all runners.
    """
    mock_moonshot_api.api_get_all_runner.return_value = MOCK_RUNNERS
    runners = runner_service.get_all_runner()
    assert runners == MOCK_RUNNERS
    mock_moonshot_api.api_get_all_runner.assert_called_once()

@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_get_all_runner_name_success(mock_moonshot_api, runner_service):
    """
    Test for successful retrieval of all runner names.
    """
    mock_moonshot_api.api_get_all_runner_name.return_value = MOCK_RUNNER_NAMES
    runner_names = runner_service.get_all_runner_name()
    assert runner_names == MOCK_RUNNER_NAMES
    mock_moonshot_api.api_get_all_runner_name.assert_called_once()

@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_get_runner_by_id_success(mock_moonshot_api, runner_service):
    """
    Test for successful retrieval of a runner by ID.
    """
    mock_moonshot_api.api_read_runner.return_value = MOCK_RUNNER_DETAILS
    runner = runner_service.get_runner_by_id("testing")
    assert runner == MOCK_RUNNER_DETAILS
    mock_moonshot_api.api_read_runner.assert_called_once_with("testing")

@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_delete_run_success(mock_moonshot_api, runner_service):
    """
    Test for successful deletion of a run.
    """
    runner_service.delete_run("testing")
    mock_moonshot_api.api_delete_runner.assert_called_once_with("testing")

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_get_all_runner_exceptions(mock_moonshot_api, exception, error_code, runner_service):
    """
    Test for exceptions when retrieving all runners.
    """
    mock_moonshot_api.api_get_all_runner.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        runner_service.get_all_runner()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_runner.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_get_all_runner_name_exceptions(mock_moonshot_api, exception, error_code, runner_service):
    """
    Test for exceptions when retrieving all runner names.
    """
    mock_moonshot_api.api_get_all_runner_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        runner_service.get_all_runner_name()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_runner_name.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_get_runner_by_id_exceptions(mock_moonshot_api, exception, error_code, runner_service):
    """
    Test for exceptions when retrieving a runner by ID.
    """
    mock_moonshot_api.api_read_runner.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        runner_service.get_runner_by_id("testing")
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_read_runner.assert_called_once_with("testing")

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.runner_service.moonshot_api')
def test_delete_run_exceptions(mock_moonshot_api, exception, error_code, runner_service):
    """
    Test for exceptions when deleting a run.
    """
    mock_moonshot_api.api_delete_runner.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        runner_service.delete_run("testing")
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_delete_runner.assert_called_once_with("testing")
