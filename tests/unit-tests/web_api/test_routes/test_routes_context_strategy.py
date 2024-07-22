import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

# Test for get_all_context_strategies
@pytest.mark.parametrize("context_strategies, exception, expected_status, expected_response", [
    # Successful cases
    ([{
        "id": "add_previous_prompt",
        "name": "Add Previous Prompt",
        "description": "This is a sample context strategy that adds in previous prompts to the current prompt. [Default: 5]"
    }], None, 200, [{
        "id": "add_previous_prompt",
        "name": "Add Previous Prompt",
        "description": "This is a sample context strategy that adds in previous prompts to the current prompt. [Default: 5]"
    }]),
    ([], None, 200, []),
    # Exception cases
    (None, ServiceException("No context strategies found", "get_ctx_strategy", "FileNotFound"), 404, None),
    (None, ServiceException("Context strategy validation error", "get_ctx_strategy", "ValidationError"), 400, None),
    (None, ServiceException("Context strategy server error", "get_ctx_strategy", "ServerError"), 500, None),
])
def test_get_all_context_strategies(test_client, mock_cs_service, context_strategies, exception, expected_status, expected_response):
    if exception:
        mock_cs_service.get_ctx_strategy.side_effect = exception
    else:
        mock_cs_service.get_ctx_strategy.return_value = context_strategies

    response = test_client.get("/api/v1/context-strategies")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

# Test for get_all_context_strategies name
@pytest.mark.parametrize("context_strategies, exception, expected_status, expected_response", [
    # Successful cases
    (["strategy1", "strategy2"], None, 200, ["strategy1", "strategy2"]),
    # Exception cases
    (None, ServiceException("No context strategies found", "get_ctx_strategy_name", "FileNotFound"), 404, None),
    (None, ServiceException("Context strategy validation error", "get_ctx_strategy_name", "ValidationError"), 400, None),
    (None, ServiceException("Context strategy server error", "get_ctx_strategy_name", "ServerError"), 500, None),
])
def test_get_all_context_strategies_name(test_client, mock_cs_service, context_strategies, exception, expected_status, expected_response):
    if exception:
        mock_cs_service.get_ctx_strategy_name.side_effect = exception
    else:
        mock_cs_service.get_ctx_strategy_name.return_value = context_strategies

    response = test_client.get("/api/v1/context-strategies/name")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

# Test for delete_context_strategy
@pytest.mark.parametrize("strategy_name, exception, expected_status, expected_response", [
    # Successful case
    ("valid_strategy", None, 200, {"success": True}),
    # Exception cases
    ("nonexistent_strategy", ServiceException("Context strategy not found", "delete_ctx_strategy", "FileNotFound"), 404, None),
    ("invalid_strategy", ServiceException("Context strategy validation error", "delete_ctx_strategy", "ValidationError"), 400, None),
    ("error_strategy", ServiceException("Context strategy server error", "delete_ctx_strategy", "ServerError"), 500, None),
    ])
def test_delete_context_strategy(test_client, mock_cs_service, strategy_name, exception, expected_status, expected_response):
    if exception:
        mock_cs_service.delete_ctx_strategy.side_effect = exception
    else:
        mock_cs_service.delete_ctx_strategy.return_value = {"success": True}

    response = test_client.delete(f"/api/v1/context-strategies/{strategy_name}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]
