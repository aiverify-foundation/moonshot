import pytest
from unittest.mock import patch, Mock
from moonshot.integrations.web_api.services.benchmark_result_service import BenchmarkResultService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.types.types import BenchmarkResult

# Mock data for successful API calls
MOCK_RESULTS = [
        {
        "metadata": {
            "id": "benchmark-1",
            "start_time": "2024-05-22 17:19:28",
            "end_time": "2024-05-22 17:57:05",
            "duration": 2256,
            "status": "completed",
            "recipes": None,
            "cookbooks": [
                "common-risk-easy"
            ],
            "endpoints": [
                "openai-gpt35-turbo",
                "openai-gpt35-turbo-16k"
            ],
            "num_of_prompts": 3,
            "random_seed": 0,
            "system_prompt": "",
            "results" : {}
            }
        }
]
MOCK_RESULT_NAMES = ['result1', 'result2']
MOCK_RESULT = {'id': '1', 'name': 'result1', 'data': 'data1'}

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def benchmark_result_service():
    return BenchmarkResultService()

@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_get_all_results_success(mock_moonshot_api, benchmark_result_service):
    """
    Test for successful retrieval of all results
    """
    mock_moonshot_api.api_get_all_result.return_value = MOCK_RESULTS
    results = benchmark_result_service.get_all_results()
    assert results == [BenchmarkResult(**result) for result in MOCK_RESULTS]
    mock_moonshot_api.api_get_all_result.assert_called_once()

@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_get_all_result_name_success(mock_moonshot_api, benchmark_result_service):
    """
    Test for successful retrieval of all result names
    """
    mock_moonshot_api.api_get_all_result_name.return_value = MOCK_RESULT_NAMES
    result_names = benchmark_result_service.get_all_result_name()
    assert result_names == MOCK_RESULT_NAMES
    mock_moonshot_api.api_get_all_result_name.assert_called_once()

@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_get_result_by_id_success(mock_moonshot_api, benchmark_result_service):
    """
    Test for successful retrieval of a result by ID
    """
    mock_moonshot_api.api_read_result.return_value = MOCK_RESULT
    result = benchmark_result_service.get_result_by_id('1')
    assert result == BenchmarkResult(**MOCK_RESULT)
    mock_moonshot_api.api_read_result.assert_called_once_with('1')

@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_delete_result_success(mock_moonshot_api, benchmark_result_service):
    """
    Test for successful deletion of a result
    """
    benchmark_result_service.delete_result('1')
    mock_moonshot_api.api_delete_result.assert_called_once_with('1')

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_get_all_results_exceptions(mock_moonshot_api, exception, error_code, benchmark_result_service):
    """
    Test for exceptions when retrieving all results
    """
    mock_moonshot_api.api_get_all_result.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        benchmark_result_service.get_all_results()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_result.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_get_all_result_name_exceptions(mock_moonshot_api, exception, error_code, benchmark_result_service):
    """
    Test for exceptions when retrieving all result names
    """
    mock_moonshot_api.api_get_all_result_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        benchmark_result_service.get_all_result_name()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_result_name.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_get_result_by_id_exceptions(mock_moonshot_api, exception, error_code, benchmark_result_service):
    """
    Test for exceptions when retrieving a result by ID
    """
    mock_moonshot_api.api_read_result.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        benchmark_result_service.get_result_by_id('1')
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_read_result.assert_called_once_with('1')

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.benchmark_result_service.moonshot_api')
def test_delete_result_exceptions(mock_moonshot_api, exception, error_code, benchmark_result_service):
    """
    Test for exceptions when deleting a result
    """
    mock_moonshot_api.api_delete_result.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        benchmark_result_service.delete_result('1')
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_delete_result.assert_called_once_with('1')
