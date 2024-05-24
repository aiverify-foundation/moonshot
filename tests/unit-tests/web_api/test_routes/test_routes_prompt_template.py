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
    (None, ServiceException("No templates found", "get_prompt_templates", "FileNotFound"), 404, None),
    (None, ServiceException("Template validation error", "get_prompt_templates", "ValidationError"), 400, None),
    (None, ServiceException("Template server error", "get_prompt_templates", "ServerError"), 500, None),
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
        assert exception.msg in response.json()["detail"]

# Test for get_all_prompt_templates_names
@pytest.mark.parametrize("template_names, exception, expected_status, expected_response", [
    # Successful cases
    (["template1", "template2"], None, 200, ["template1", "template2"]),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("No template names found", "get_prompt_templates_name", "FileNotFound"), 404 ,None),
    (None, ServiceException("Template name validation error", "get_prompt_templates_name", "ValidationError"), 400, None),
    (None, ServiceException("Template name server error", "get_prompt_templates_name", "ServerError"), 500, None),
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
        assert exception.msg in response.json()["detail"]

# Test for delete_prompt_template
@pytest.mark.parametrize("pt_name, exception, expected_status, expected_response", [
    # Successful case
    ("pt_name", None, 200, {"success": True}),
    # Exception cases
    ("pt_name", ServiceException("Prompt Temeplate not found", "delete_prompt_template", "FileNotFound"), 404, None),
    ("pt_name", ServiceException("Prompt Temeplate validation error", "delete_prompt_template", "ValidationError"), 400, None),
    ("pt_name", ServiceException("Prompt Temeplate server error", "delete_prompt_template", "ServerError"), 500, None),
    ])
def test_delete_prompt_template(test_client, mock_pt_service, pt_name, exception, expected_status, expected_response):
    if exception:
        mock_pt_service.delete_prompt_template.side_effect = exception
    else:
        mock_pt_service.delete_prompt_template.return_value = {"success": True}

    response = test_client.delete(f"/api/v1/prompt-templates/{pt_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]
