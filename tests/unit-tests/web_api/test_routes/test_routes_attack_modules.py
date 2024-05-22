import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("attack_module_data, exception, expected_status, expected_response", [
    # Successful cases
    (["module1", "module2", "module3"], None, 200, ["module1", "module2", "module3"]),
    # Exception cases
    (None, ServiceException("A file not found error occurred", "get_all_attack_module", "FileNotFound"), 404, None),
    (None, ServiceException("A validation error occurred", "get_all_attack_module", "ValidationError"), 400, None),
    (None, ServiceException("An server error occurred", "get_all_attack_module", "ServerError"), 500, None),
])
def test_get_all_attack_module(test_client, mock_am_service, attack_module_data, exception, expected_status, expected_response):
    if exception:
        mock_am_service.get_all_attack_module.side_effect = exception
    else:
        mock_am_service.get_all_attack_module.return_value = attack_module_data

    response = test_client.get("/api/v1/attack-modules")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("exception, expected_status, expected_response", [
    # Successful case
    (None, 200, [{"name": "module1", "version": "1.0"}, {"name": "module2", "version": "2.0"}]),
    # Exception cases
    (ServiceException("A file not found error occurred", "get_all_attack_module_metadata", "FileNotFound"), 404, None),
    (ServiceException("A validation error occurred", "get_all_attack_module_metadata", "ValidationError"), 400, None),
    (ServiceException("An server error occurred", "get_all_attack_module_metadata", "ServerError"), 500, None),
])
def test_get_all_attack_module_metadata(test_client, mock_am_service, exception, expected_status, expected_response):
    if exception:
        mock_am_service.get_all_attack_module_metadata.side_effect = exception
    else:
        mock_am_service.get_all_attack_module_metadata.return_value = expected_response

    response = test_client.get("/api/v1/attack-modules/metadata")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == expected_response
    else:
        assert exception.msg in response.json()["detail"]