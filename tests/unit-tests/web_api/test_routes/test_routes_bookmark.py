import pytest

from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize(
    "bookmark_id, mock_return_value, exception, expected_status, expected_response",
    [
        # Success scenario - all bookmarks
        (
            None,
            [
                {
                    'id': 1, 'name': 'my bookmark 1',
                    'prompt': 'Your prompt',
                    'response': 'Your response',
                    "prepared_prompt": "Your Prepared prompt",
                    'context_strategy': 'Your context strategy',
                    'prompt_template': 'Your prompt template',
                    'attack_module': 'Your attack module',
                    'metric': '',
                    'bookmark_time': '2024-07-03 21:05:58'
                }
            ],
            None,
            200,
            [
                {
                    'name': 'my bookmark 1',
                    'prompt': 'Your prompt',
                    'prepared_prompt': 'Your Prepared prompt',
                    'response': 'Your response',
                    'context_strategy': 'Your context strategy',
                    'prompt_template': 'Your prompt template',
                    'attack_module': 'Your attack module',
                    'metric': '',
                    'bookmark_time': '2024-07-03 21:05:58'
                }
            ]
        ),
        # FileNotFound exception
        (
            None,
            None,
            ServiceException("Bookmark not found", "get_all_bookmarks", "FileNotFound"),
            404,
            {"detail": "Failed to retrieve bookmarks: [ServiceException] FileNotFound in get_all_bookmarks - Bookmark not found"}
        ),
        # ValidationError exception
        (
            None,
            None,
            ServiceException("Invalid bookmark data", "get_all_bookmarks", "ValidationError"),
            400,
            {"detail": "Failed to retrieve bookmarks: [ServiceException] ValidationError in get_all_bookmarks - Invalid bookmark data"}
        ),
        # Generic exception (any other error)
        (
            None,
            None,
            ServiceException("Unknown error", "get_all_bookmarks", "UnknownError"),
            500,
            {"detail": "Failed to retrieve bookmarks: [ServiceException] UnknownError in get_all_bookmarks - Unknown error"}
        ),
    ]
)
def test_get_all_bookmarks(test_client, mock_bookmark_service, bookmark_id, mock_return_value, exception, expected_status, expected_response):
    # Setup the mock service based on the exception parameter
    if exception:
        mock_bookmark_service.get_all_bookmarks.side_effect = exception
    else:
        mock_bookmark_service.get_all_bookmarks.return_value = mock_return_value

    # Make the GET request to the API
    response = test_client.get(f"/api/v1/bookmarks?id={bookmark_id}" if bookmark_id else "/api/v1/bookmarks")
    # Assert the status code and response match the expected values
    assert response.status_code == expected_status
    assert response.json() == expected_response

@pytest.mark.parametrize("bookmark_data, exception, expected_status, expected_response", [
    # Success scenario
    (
        {
            "name": "Bookmark 1",
            "prompt": "How to test?",
            "prepared_prompt": "Your Prepared prompt",
            "response": "Using pytest",
            "context_strategy": "Strategy A",
            "prompt_template": "Template A",
            "attack_module": "Module A"
        },
        None,
        200,
        {
            "name": "Bookmark 1",
            "prompt": "How to test?",
            "prepared_prompt": "Your Prepared prompt",
            "response": "Using pytest",
            "context_strategy": "Strategy A",
            "prompt_template": "Template A",
            "attack_module": "Module A"
        }
    ),
    # Validation error scenario
    (
        {
            "name": "",
            "prompt": "How to test?",
            "prepared_prompt": "Your Prepared prompt",
            "response": "Using pytest"
        },
        ServiceException("Validation error occurred", "insert_bookmark", "ValidationError"),
        422,
        None
    ),
    # File not found error scenario
    (
        {
            "name": "Bookmark 2",
            "prompt": "How to test?",
            "prepared_prompt": "Your Prepared prompt",
            "response": "Using pytest"
        },
        ServiceException("File not found error occurred", "insert_bookmark", "FileNotFound"),
        404,
        {"detail": "Failed to insert bookmark: File not found error occurred"}
    ),
    # Unknown error scenario
    (
        {
            "name": "Bookmark 3",
            "prompt": "How to test?",
            "prepared_prompt": "Your Prepared prompt",
            "response": "Using pytest"
        },
        ServiceException("Unknown error occurred", "insert_bookmark", "UnknownError"),
        500,
        {"detail": "Failed to insert bookmark: Unknown error occurred"}
    ),
])
def test_insert_bookmark(test_client, mock_bookmark_service, bookmark_data, exception, expected_status, expected_response):
    # Setup the mock service based on the exception parameter
    if exception:
        mock_bookmark_service.insert_bookmark.side_effect = exception
    else:
        mock_bookmark_service.insert_bookmark.return_value = bookmark_data

    # Make the POST request to the API
    response = test_client.post("/api/v1/bookmarks", json=bookmark_data)

    # Assert the status code and response match the expected values
    assert response.status_code == expected_status
    if expected_status != 422:
        if exception:
            # Check if the exception message is in the response detail
            assert exception.msg in response.json()["detail"]
        else:
            # For non-exception cases, check if the response matches the expected response
            assert response.json() == expected_response

@pytest.mark.parametrize(
    "delete_all, bookmark_name, exception, expected_status, expected_response",
    [
        # Delete a single bookmark by ID
        (
            False,
            "Bookmark 1",
            None,
            200,
            {"message": "Bookmark deleted successfully"}
        ),
        # Delete all bookmarks
        (
            True,
            None,
            None,
            200,
            {"message": "All bookmarks deleted successfully"}
        ),
        # Missing 'all' or 'id' parameter
        (
            False,
            None,
            None,
            400,
            {"detail": "Must specify 'all' or 'name' parameter"}
        ),
        # FileNotFound exception
        (
            False,
            999,
            ServiceException("Bookmark not found", "delete_bookmark", "FileNotFound"),
            404,
            {"detail": "Failed to delete bookmark: [ServiceException] FileNotFound in delete_bookmark - Bookmark not found"}
        ),
        # ValidationError exception
        (
            False,
            None,
            ServiceException("Invalid bookmark ID", "delete_bookmark", "ValidationError"),
            400,
            {"detail": "Must specify 'all' or 'name' parameter"}
        ),
        # Generic exception
        (
            False,
            1,
            ServiceException("Unknown error", "delete_bookmark", "UnknownError"),
            500,
            {"detail": "Failed to delete bookmark: [ServiceException] UnknownError in delete_bookmark - Unknown error"}
        ),
    ]
)
def test_delete_bookmark(test_client, mock_bookmark_service, delete_all, bookmark_name, exception, expected_status, expected_response):
    # Setup the mock service based on the exception parameter
    if exception:
        mock_bookmark_service.delete_bookmarks.side_effect = exception
    else:
        mock_bookmark_service.delete_bookmarks.return_value = expected_response

    # Build the query string based on the parameters
    query_string = f"?all={delete_all}"
    if bookmark_name is not None:
        query_string += f"&name={bookmark_name}"

    # Make the DELETE request to the API
    response = test_client.delete(f"/api/v1/bookmarks{query_string}")
    # Assert the status code and response match the expected values
    assert response.status_code == expected_status
    assert response.json() == expected_response    