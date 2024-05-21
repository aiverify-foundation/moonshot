import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Test for get_all_prompt_templates
@pytest.mark.parametrize("template_data, exception, expected_status, expected_response", [
    # Successful cases
    ([{"name": "template1", "description": "desc1", "template": "temp1"}, { "name": "template2", "description": "desc2", "template": "temp2"}],
      None, 200, 
      [{"name": "template1", "description": "desc1", "template": "temp1"}, { "name": "template2", "description": "desc2", "template": "temp2"}]),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("No templates found", "get_prompt_templates", "FileNotFound"), 404, "No templates found"),
    (None, ServiceException("Template validation error", "get_prompt_templates", "ValidationError"), 400, "Template validation error"),
    (None, ServiceException("Template server error", "get_prompt_templates", "ServerError"), 500, "Template server error"),
])
def test_get_all_prompt_templates(test_client, mock_pt_service, template_data, exception, expected_status, expected_response):
    if exception:
        mock_pt_service.get_prompt_templates.side_effect = exception
    else:
        mock_pt_service.get_prompt_templates.return_value = template_data

    response = test_client.get("/api/v1/prompt-templates")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert expected_response in response.json()["detail"]

# Test for get_all_prompt_templates_names
@pytest.mark.parametrize("template_names, exception, expected_status, expected_response", [
    # Successful cases
    (["template1", "template2"], None, 200, ["template1", "template2"]),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("No template names found", "get_prompt_templates_name", "FileNotFound"), 404, "No template names found"),
    (None, ServiceException("Template name validation error", "get_prompt_templates_name", "ValidationError"), 400, "Template name validation error"),
    (None, ServiceException("Template name server error", "get_prompt_templates_name", "ServerError"), 500, "Template name server error"),
])
def test_get_all_prompt_templates_names(test_client, mock_pt_service, template_names, exception, expected_status, expected_response):
    if exception:
        mock_pt_service.get_prompt_templates_name.side_effect = exception
    else:
        mock_pt_service.get_prompt_templates_name.return_value = template_names

    response = test_client.get("/api/v1/prompt-templates/name")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert expected_response in response.json()["detail"]

# Test for get_all_context_strategies
@pytest.mark.parametrize("context_strategies, exception, expected_status, expected_response", [
    # Successful cases
    (["strategy1", "strategy2"], None, 200, ["strategy1", "strategy2"]),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("No context strategies found", "get_ctx_strategies", "FileNotFound"), 404, "No context strategies found"),
    (None, ServiceException("Context strategy validation error", "get_ctx_strategies", "ValidationError"), 400, "Context strategy validation error"),
    (None, ServiceException("Context strategy server error", "get_ctx_strategies", "ServerError"), 500, "Context strategy server error"),
])
def test_get_all_context_strategies(test_client, mock_pt_service, context_strategies, exception, expected_status, expected_response):
    if exception:
        mock_pt_service.get_ctx_strategies.side_effect = exception
    else:
        mock_pt_service.get_ctx_strategies.return_value = context_strategies

    response = test_client.get("/api/v1/context-strategies")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert expected_response in response.json()["detail"]

# Test for delete_context_strategy
@pytest.mark.parametrize("strategy_name, exception, expected_status, expected_response", [
    # Successful case
    ("valid_strategy", None, 200, {"success": True}),
    # Exception cases
    ("nonexistent_strategy", ServiceException("Context strategy not found", "delete_ctx_strategy", "FileNotFound"), 404, "Context strategy not found"),
    ("invalid_strategy", ServiceException("Context strategy validation error", "delete_ctx_strategy", "ValidationError"), 400, "Context strategy validation error"),
    ("error_strategy", ServiceException("Context strategy server error", "delete_ctx_strategy", "ServerError"), 500, "Context strategy server error"),
    ])
def test_delete_context_strategy(test_client, mock_pt_service, strategy_name, exception, expected_status, expected_response):
    if exception:
        mock_pt_service.delete_ctx_strategy.side_effect = exception
    else:
        mock_pt_service.delete_ctx_strategy.return_value = {"success": True}

    response = test_client.delete(f"/api/v1/context-strategies/{strategy_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert expected_response in response.json()["detail"]