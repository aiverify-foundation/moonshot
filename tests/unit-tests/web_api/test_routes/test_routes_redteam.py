import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("mock_response, exception, expected_status, expected_response", [
    # Success Scenario
    (
        [
            {
            "session_id": "session1",
            "description": "session1",
            "endpoints": [
                "endpoint-1",
                "endpoint-2"
            ],
            "created_epoch": "123456",
            "created_datetime": "123456",
            "prompt_template": "",
            "context_strategy": "",
            "cs_num_of_prev_prompts": 5,
            "attack_module": "",
            "metric": "",
            "system_prompt": ""
            },
            {
            "session_id": "session2",
            "description": "session2",
            "endpoints": [
                "endpoint-1",
                "endpoint-2"
            ],
            "created_epoch": "1716184723.41888",
            "created_datetime": "20240520-135843",
            "prompt_template": "",
            "context_strategy": "",
            "cs_num_of_prev_prompts": 5,
            "attack_module": "",
            "metric": "",
            "system_prompt": ""
            }
        ], None, 200,
        [
            {
            "session_id": "session1",
            "description": "session1",
            "endpoints": [
                "endpoint-1",
                "endpoint-2"
            ],
            "created_epoch": "123456",
            "created_datetime": "123456",
            "prompt_template": "",
            "context_strategy": "",
            "cs_num_of_prev_prompts": 5,
            "attack_module": "",
            "metric": "",
            "system_prompt": ""
            },
            {
            "session_id": "session2",
            "description": "session2",
            "endpoints": [
                "endpoint-1",
                "endpoint-2"
            ],
            "created_epoch": "1716184723.41888",
            "created_datetime": "20240520-135843",
            "prompt_template": "",
            "context_strategy": "",
            "cs_num_of_prev_prompts": 5,
            "attack_module": "",
            "metric": "",
            "system_prompt": ""
            }
        ]
    ),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_session", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_session", "ValidationError"), 400, None),
    (None, ServiceException("An value error occurred", "get_all_session", "ValueError"), 500, None),
])
def test_get_all_sessions(test_client, mock_session_service, mock_response, expected_status, exception, expected_response):
    if exception:
        mock_session_service.get_all_session.side_effect = exception
    else:
        mock_session_service.get_all_session.return_value = mock_response 

    response = test_client.get("/api/v1/sessions")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        assert response.json() == expected_response

@pytest.mark.parametrize("session_data, exception, expected_status, expected_response", [
    (
        {
            "name": "Test Session",
            "description": "Test Description",
            "endpoints": ["endpoint_1"]
        },
        None, 200, 
        {
            "session_name": "Test Session",
            "session_description": "Test Description",
            "session": {
                "session_id": "norman-session-11",
                "description": "",
                "endpoints": ["endpoint_1"],
                "created_epoch": "123456",
                "created_datetime": "123456",
                "prompt_template": "",
                "context_strategy": "",
                "cs_num_of_prev_prompts": 5,
                "attack_module": "",
                "metric": "",
                "system_prompt": ""
            },
            "chat_records": None
        }
    ),
    # Exception cases
    (
        {
            "name": "Test Session",
            "description": "Test Description",
            "endpoints": ["endpoint_1"]
        }
        , ServiceException("A file not found error occurred", "get_all_session", "FileNotFound"), 404, None),
    (
        {
            "name": "Test Session",
            "description": "Test Description",
            "endpoints": ["endpoint_1"]
        }
        , ServiceException("A validation error occurred", "get_all_session", "ValidationError"), 400, None),
    (
        {
            "name": "Test Session",
            "description": "Test Description",
            "endpoints": ["endpoint_1"]
        }
        , ServiceException("An value error occurred", "get_all_session", "ValueError"), 500, None),
])
def test_create_session(test_client, mock_session_service, session_data, expected_status, exception, expected_response):
    if exception:
        mock_session_service.create_new_session.side_effect = exception
    else:
        mock_session_service.create_new_session.return_value = expected_response 

    response = test_client.post("/api/v1/sessions", json=session_data)

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        if expected_status != 422:
            assert response.json() == expected_response

@pytest.mark.parametrize("session_id, exception, expected_status, expected_response", [
    # Test successful deletion of session
    ("valid-session-id", None, 200, {"success": True}),
    # Test session not found
    ("invalid-session-id", ServiceException(msg="Session not found", method_name="delete_session", error_code="FileNotFound"), 404, None),
    # Test validation error
    ("valid-session-id", ServiceException(msg="Validation error", method_name="delete_session", error_code="ValidationError"), 400, None),
    # Test unknown error
    ("valid-session-id", ServiceException(msg="Internal server error", method_name="delete_session", error_code="UnknownError"), 500, None),
])
def test_delete_session(test_client, mock_session_service, session_id, expected_status, exception, expected_response):
    if exception:
        mock_session_service.delete_session.side_effect = exception
    else:
        mock_session_service.delete_session.return_value = None

    # Make the delete request
    response = test_client.delete(f"/api/v1/sessions/{session_id}")

    # Assert the expected status code
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("session_id, prompt, exception, expected_status, expected_response", [
    # Test successful deletion of session
    ("session-1", "PROMPT", None, 200,
        {
            "current_runner_id": "session-1",
            "current_chats": {
                "endpoint-1": [
                {
                "conn_id": "endpoint-1",
                "context_strategy": "",
                "prompt_template": "",
                "attack_module": "",
                "metric": "",
                "prompt": "Test Prompt.",
                "prepared_prompt": "Test Prompt.",
                "system_prompt": "",
                "predicted_result": "This is a test prompt for the AI to respond to. Please provide a response to demonstrate your capabilities. Thank you.",
                "duration": "1.23",
                "prompt_time": "2024-05-22 21:41:05.657875"
                }
                ]
        },
        "current_batch_size": 5,
        "current_status": "COMPLETED"
        }  
     ),
    # Test session not found
    ("invalid-session-id", "PROMPT", ServiceException(msg="Session not found", method_name="send_prompt", error_code="FileNotFound"), 404, None),
    # Test validation error
    ("valid-session-id", "PROMPT", ServiceException(msg="Validation error", method_name="send_prompt", error_code="ValidationError"), 400, None),
    # Test unknown error
    ("valid-session-id", "PROMPT", ServiceException(msg="Internal server error", method_name="send_prompt", error_code="UnknownError"), 500, None),
])
def test_send_prompt(test_client, mock_session_service, session_id, prompt, expected_status, exception, expected_response):
    if exception:
        mock_session_service.send_prompt.side_effect = exception
    else:
        mock_session_service.send_prompt.return_value = expected_response

    response = test_client.post(f"/api/v1/sessions/{session_id}/prompt", json={"user_prompt": prompt})

    # Assert the expected status code
    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
        

@pytest.mark.parametrize("session_id, exception, expected_status", [
    # Test successful deletion of session
    ("valid-session-id", None, 200),
    # Test session not found
    ("invalid-session-id", ServiceException(msg="Session not found", method_name="cancel_auto_redteam", error_code="FileNotFound"), 404),
    # Test validation error
    ("valid-session-id", ServiceException(msg="Validation error", method_name="cancel_auto_redteam", error_code="ValidationError"), 400),
    # Test unknown error
    ("valid-session-id", ServiceException(msg="Internal server error", method_name="cancel_auto_redteam", error_code="UnknownError"), 500),
])
def test_cancel_redteam(test_client, mock_session_service, session_id, expected_status, exception):
    if exception:
        mock_session_service.cancel_auto_redteam.side_effect = exception
    else:
        mock_session_service.cancel_auto_redteam.return_value = None

    # Make the delete request
    response = test_client.post(f"/api/v1/sessions/{session_id}/cancel")

    # Assert the expected status code
    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
        

@pytest.mark.parametrize("runner_id, prompt_template_name, exception, expected_status, expected_response", [
    # Successful cases
    ("runner-id", "prompt_template_name",None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "prompt_template_name", ServiceException("A file not found error occurred", "select_prompt_template", "FileNotFound"), 404, None),
    ("runner-id", "prompt_template_name", ServiceException("A validation error occurred", "select_prompt_template", "ValidationError"), 400, None),
    ("runner-id", "prompt_template_name", ServiceException("An server error occurred", "select_prompt_template", "ServerError"), 500, None),
])
def test_set_prompt_template(test_client, mock_session_service, runner_id, prompt_template_name, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_prompt_template.side_effect = exception
    else:
        mock_session_service.select_prompt_template.return_value = prompt_template_name

    response = test_client.put(f"/api/v1/sessions/{runner_id}/prompt-template/{prompt_template_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, prompt_template_name, exception, expected_status, expected_response", [
    # Successful cases
    # ("runner-id", "prompt_template_name",None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "prompt_template_name", ServiceException("A file not found error occurred", "select_prompt_template", "FileNotFound"), 404, None),
    ("runner-id", "prompt_template_name", ServiceException("A validation error occurred", "select_prompt_template", "ValidationError"), 400, None),
    ("runner-id", "prompt_template_name", ServiceException("An server error occurred", "select_prompt_template", "ServerError"), 500, None),
])
def test_unset_prompt_template(test_client, mock_session_service, runner_id, prompt_template_name, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_prompt_template.side_effect = exception
    else:
        mock_session_service.select_prompt_template.return_value = None

    response = test_client.delete(f"/api/v1/sessions/{runner_id}/prompt-template/{prompt_template_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]


@pytest.mark.parametrize("runner_id, ctx_strategy_name, num_of_prompts, exception, expected_status, expected_response", [
    # Successful cases
    ("runner-id", "ctx_strategy_name",10,  None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "ctx_strategy_name",5, ServiceException("A file not found error occurred", "select_ctx_strategy", "FileNotFound"), 404, None),
    ("runner-id", "ctx_strategy_name",5, ServiceException("A validation error occurred", "select_ctx_strategy", "ValidationError"), 400, None),
    ("runner-id", "ctx_strategy_name",5, ServiceException("An server error occurred", "select_ctx_strategy", "ServerError"), 500, None),
])
def test_set_context_strategy(test_client, mock_session_service, runner_id, ctx_strategy_name, num_of_prompts, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_ctx_strategy.side_effect = exception
    else:
        mock_session_service.select_ctx_strategy.return_value = ctx_strategy_name

    response = test_client.put(f"/api/v1/sessions/{runner_id}/context-strategy/{ctx_strategy_name}/{num_of_prompts}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, ctx_strategy_name, num_of_prompts , exception, expected_status, expected_response", [
    # Successful cases
    # ("runner-id", "ctx_strategy_name",0,None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "ctx_strategy_name",0, ServiceException("A file not found error occurred", "select_ctx_strategy", "FileNotFound"), 404, None),
    ("runner-id", "ctx_strategy_name",0, ServiceException("A validation error occurred", "select_ctx_strategy", "ValidationError"), 400, None),
    ("runner-id", "ctx_strategy_name",0, ServiceException("An server error occurred", "select_ctx_strategy", "ServerError"), 500, None),
])
def test_unset_context_strategy(test_client, mock_session_service, runner_id, ctx_strategy_name, num_of_prompts, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_ctx_strategy.side_effect = exception
    else:
        mock_session_service.select_ctx_strategy.return_value = None

    response = test_client.delete(f"/api/v1/sessions/{runner_id}/context-strategy/{ctx_strategy_name}/{num_of_prompts}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, atk_module_name, exception, expected_status, expected_response", [
    # Successful cases
    ("runner-id", "atk_module_name",None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "atk_module_name", ServiceException("A file not found error occurred", "select_attack_module", "FileNotFound"), 404, None),
    ("runner-id", "atk_module_name", ServiceException("A validation error occurred", "select_attack_module", "ValidationError"), 400, None),
    ("runner-id", "atk_module_name", ServiceException("An server error occurred", "select_attack_module", "ServerError"), 500, None),
])
def test_set_attack_module(test_client, mock_session_service, runner_id, atk_module_name, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_attack_module.side_effect = exception
    else:
        mock_session_service.select_attack_module.return_value = atk_module_name

    response = test_client.put(f"/api/v1/sessions/{runner_id}/attack-module/{atk_module_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, atk_module_name, exception, expected_status, expected_response", [
    # Successful cases
    # ("runner-id", "atk_module_name",None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "atk_module_name", ServiceException("A file not found error occurred", "select_attack_module", "FileNotFound"), 404, None),
    ("runner-id", "atk_module_name", ServiceException("A validation error occurred", "select_attack_module", "ValidationError"), 400, None),
    ("runner-id", "atk_module_name", ServiceException("An server error occurred", "select_attack_module", "ServerError"), 500, None),
])
def test_unset_attack_module(test_client, mock_session_service, runner_id, atk_module_name, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_attack_module.side_effect = exception
    else:
        mock_session_service.select_attack_module.return_value = None

    response = test_client.delete(f"/api/v1/sessions/{runner_id}/attack-module/{atk_module_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, metric_name, exception, expected_status, expected_response", [
    # Successful cases
    ("runner-id", "metric-name",None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "metric-name", ServiceException("A file not found error occurred", "select_metric", "FileNotFound"), 404, None),
    ("runner-id", "metric-name", ServiceException("A validation error occurred", "select_metric", "ValidationError"), 400, None),
    ("runner-id", "metric-name", ServiceException("An server error occurred", "select_metric", "ServerError"), 500, None),
])
def test_set_metric(test_client, mock_session_service, runner_id, metric_name, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_metric.side_effect = exception
    else:
        mock_session_service.select_metric.return_value = metric_name

    response = test_client.put(f"/api/v1/sessions/{runner_id}/metric/{metric_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, metric_name, exception, expected_status, expected_response", [
    # Successful cases
    # ("runner-id", "metric-name",None, 200, {"success": True}),
    # Exception cases
    ("runner-id", "metric-name", ServiceException("A file not found error occurred", "select_metric", "FileNotFound"), 404, None),
    ("runner-id", "metric-name", ServiceException("A validation error occurred", "select_metric", "ValidationError"), 400, None),
    ("runner-id", "metric-name", ServiceException("An server error occurred", "select_metric", "ServerError"), 500, None),
])
def test_unset_metric(test_client, mock_session_service, runner_id, metric_name, exception, expected_status, expected_response):
    if exception:
        mock_session_service.select_metric.side_effect = exception
    else:
        mock_session_service.select_metric.return_value = None

    response = test_client.delete(f"/api/v1/sessions/{runner_id}/metric/{metric_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]


@pytest.mark.parametrize("runner_id, body_data, exception, expected_status, expected_response", [
    # Successful cases
    ("runner-id", 
    {
        "system_prompt" : "You shall act as Jedi Master Yoda."
    },
    None, 200, {"success": True}
    ),
    # Invalid Parameter 
    ("runner-id", {}, None, 422, {"success": True}
    ),
    # Exception cases
    ("runner-id", 
    {
        "system_prompt" : "You shall act as Jedi Master Yoda."
    },
    ServiceException("A file not found error occurred", "update_system_prompt", "FileNotFound"), 404, None),
    ("runner-id", 
    {
        "system_prompt" : "You shall act as Jedi Master Yoda."
    },
    ServiceException("A validation error occurred", "update_system_prompt", "ValidationError"), 400, None),
    ("runner-id", 
    {
        "system_prompt" : "You shall act as Jedi Master Yoda."
    },
    ServiceException("An server error occurred", "update_system_prompt", "ServerError"), 500, None),
])
def test_set_system_prompt(test_client, mock_session_service, runner_id, body_data, exception, expected_status, expected_response):
    if exception:
        mock_session_service.update_system_prompt.side_effect = exception
    else:
        mock_session_service.update_system_prompt.return_value = body_data

    response = test_client.put(f"/api/v1/sessions/{runner_id}/system-prompt",json = body_data)
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, exception, expected_status, expected_response", [
    # Successful cases
    # ("runner-id", None, 200, {"success": True}),
    # Exception cases
    ("runner-id", ServiceException("A file not found error occurred", "update_system_prompt", "FileNotFound"), 404, None),
    ("runner-id", ServiceException("A validation error occurred", "update_system_prompt", "ValidationError"), 400, None),
    ("runner-id", ServiceException("An server error occurred", "update_system_prompt", "ServerError"), 500, None),
])
def test_unset_system_prompt(test_client, mock_session_service, runner_id, exception, expected_status, expected_response):
    if exception:
        mock_session_service.update_system_prompt.side_effect = exception
    else:
        mock_session_service.update_system_prompt.return_value = {"success": True}

    response = test_client.delete(f"/api/v1/sessions/{runner_id}/system-prompt")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, exception, expected_status, expected_response", [
    # Successful cases
    ("runner-id", None, 200, {"success": True}),
    # Exception cases
    ("runner-id", ServiceException("A file not found error occurred", "end_session", "FileNotFound"), 404, None),
    ("runner-id", ServiceException("A validation error occurred", "end_session", "ValidationError"), 400, None),
    ("runner-id", ServiceException("An server error occurred", "end_session", "ServerError"), 500, None),
])
def test_close_session(test_client, mock_session_service, runner_id, exception, expected_status, expected_response):
    if exception:
        mock_session_service.end_session.side_effect = exception

    response = test_client.get(f"/api/v1/sessions/{runner_id}/close")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]
