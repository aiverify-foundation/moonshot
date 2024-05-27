import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.prompt_template_service import PromptTemplateService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Mock data for successful API calls
MOCK_PROMPT_TEMPLATES = [
    {
        "name": "legal-term-template",
        "description": "The template used for legal term dataset.",
        "template": "Explain this term that is used in the legal context: {{ prompt }}\nA: "
    },
    {
        "name": "real-toxicity-prompt-template",
        "description": "This template is used with real toxicity prompt dataset",
        "template": "Complete this prompt within a sentence: \"{{ prompt }}\""
    }
]
MOCK_PROMPT_TEMPLATE_NAMES = ["legal-term-template","real-toxicity-prompt--template"]

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def prompt_template_service():
    return PromptTemplateService()

@patch('moonshot.integrations.web_api.services.prompt_template_service.moonshot_api')
def test_get_prompt_templates_success(mock_moonshot_api, prompt_template_service):
    """
    Test successful retrieval of prompt templates.
    """
    mock_moonshot_api.api_get_all_prompt_template_detail.return_value = MOCK_PROMPT_TEMPLATES
    templates = prompt_template_service.get_prompt_templates()
    assert templates == MOCK_PROMPT_TEMPLATES
    mock_moonshot_api.api_get_all_prompt_template_detail.assert_called_once()

@patch('moonshot.integrations.web_api.services.prompt_template_service.moonshot_api')
def test_get_prompt_templates_name_success(mock_moonshot_api, prompt_template_service):
    """
    Test successful retrieval of prompt template names.
    """
    mock_moonshot_api.api_get_all_prompt_template_name.return_value = MOCK_PROMPT_TEMPLATE_NAMES
    template_names = prompt_template_service.get_prompt_templates_name()
    assert template_names == MOCK_PROMPT_TEMPLATE_NAMES
    mock_moonshot_api.api_get_all_prompt_template_name.assert_called_once()

@patch('moonshot.integrations.web_api.services.prompt_template_service.moonshot_api')
def test_delete_prompt_template_success(mock_moonshot_api, prompt_template_service):
    """
    Test successful deletion of a prompt template.
    """
    prompt_template_service.delete_prompt_template("legal-term-template")
    mock_moonshot_api.api_delete_prompt_template.assert_called_once_with("legal-term-template")

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.prompt_template_service.moonshot_api')
def test_get_prompt_templates_exceptions(mock_moonshot_api, exception, error_code, prompt_template_service):
    """
    Test exception scenarios when retrieving prompt templates.
    """
    mock_moonshot_api.api_get_all_prompt_template_detail.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        prompt_template_service.get_prompt_templates()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_prompt_template_detail.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.prompt_template_service.moonshot_api')
def test_get_prompt_templates_name_exceptions(mock_moonshot_api, exception, error_code, prompt_template_service):
    """
    Test exception scenarios when retrieving prompt template names.
    """
    mock_moonshot_api.api_get_all_prompt_template_name.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        prompt_template_service.get_prompt_templates_name()
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_get_all_prompt_template_name.assert_called_once()

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.prompt_template_service.moonshot_api')
def test_delete_prompt_template_exceptions(mock_moonshot_api, exception, error_code, prompt_template_service):
    """
    Test exception scenarios when deleting a prompt template.
    """
    mock_moonshot_api.api_delete_prompt_template.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        prompt_template_service.delete_prompt_template("legal-term-template")
    assert exc_info.value.error_code == error_code
    mock_moonshot_api.api_delete_prompt_template.assert_called_once_with("legal-term-template")
