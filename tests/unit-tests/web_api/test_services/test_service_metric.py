import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.metric_service import MetricService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Mock data for individual metric details
MOCK_METRIC_DETAILS = [
    {
        "id": "bertscore",
        "name": "BertScore",
        "description": "BertScore uses Bert to check for the similarity in embedding between two sentences."
    },
    {
        "id": "spelling",
        "name": "SpellingScore",
        "description": "SpellingScore uses Levenshetein Distance to find permutations within an edit distance of 2 from the original."
    }
]

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def metric_service():
    return MetricService()

@patch('moonshot.integrations.web_api.services.metric_service.moonshot_api')
def test_get_all_metric_success(mock_moonshot_api, metric_service):
    """
    Test case for successful retrieval of all metrics.
    """
    mock_moonshot_api.api_get_all_metric.return_value = MOCK_METRIC_DETAILS
    metrics = metric_service.get_all_metric()
    assert metrics == MOCK_METRIC_DETAILS
    mock_moonshot_api.api_get_all_metric.assert_called_once()

@patch('moonshot.integrations.web_api.services.metric_service.moonshot_api')
def test_delete_metric_success(mock_moonshot_api, metric_service):
    """
    Test case for successful deletion of a metric.
    """
    metric_service.delete_metric('bertscore')
    mock_moonshot_api.api_delete_metric.assert_called_once_with('bertscore')

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.metric_service.moonshot_api')
def test_get_all_metric_exceptions(mock_moonshot_api, exception, error_code, metric_service):
    """
    Test case for exceptions during retrieval of all metrics.
    """
    mock_moonshot_api.api_get_all_metric.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        metric_service.get_all_metric()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_metric.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.metric_service.moonshot_api')
def test_delete_metric_exceptions(mock_moonshot_api, exception, error_code, metric_service):
    """
    Test case for exceptions during deletion of a metric.
    """
    mock_moonshot_api.api_delete_metric.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        metric_service.delete_metric('bertscore')
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_delete_metric.assert_called_once_with('bertscore')
