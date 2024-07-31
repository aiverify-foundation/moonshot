import pytest
from unittest.mock import patch
from moonshot.integrations.web_api.services.bookmark_service import BookmarkService
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException
from moonshot.integrations.web_api.schemas.bookmark_create_dto import BookmarkCreateDTO
from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments

# Mock data for bookmarks
MOCK_BOOKMARKS = [
    {
        "id": 1,
        "name": "Bookmark 1",
        "prompt": "Prompt 1",
        "prepared_prompt": "Prepared Prompt",
        "response": "Response 1",
        "context_strategy": "Strategy 1",
        "prompt_template": "Template 1",
        "attack_module": "Module 1",
        "metric": "Metric",
        "bookmark_time": "2024-0704 15:00:00"
    },
    {
        "id": 2,
        "name": "Bookmark 2",
        "prompt": "Prompt 2",
        "prepared_prompt": "Prepared Prompt",
        "response": "Response 2",
        "context_strategy": "Strategy 2",
        "prompt_template": "Template 2",
        "attack_module": "Module 2",
        "metric": "Metric",
        "bookmark_time": "2024-0704 15:00:00"
    }
]

MOCK_BOOKMARK_CREATE_DTO = BookmarkCreateDTO(
    name="New Bookmark",
    prompt="New Prompt",
    prepared_prompt="Prepared Prompt",
    response="New Response",
    context_strategy="New Strategy",
    prompt_template="New Template",
    attack_module="New Module",
    metric= "Metric"
)

# Exception scenarios to test
exception_scenarios = [
    (FileNotFoundError("File not found"), "FileNotFound"),
    (ValueError("Invalid value"), "ValueError"),
    (Exception("Unexpected error"), "UnexpectedError"),
]

@pytest.fixture
def bookmark_service():
    return BookmarkService()

@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_get_all_bookmarks_success(mock_moonshot_api, bookmark_service):
    """
    Test case for successful retrieval of all bookmarks.
    """
    mock_moonshot_api.api_get_all_bookmarks.return_value = MOCK_BOOKMARKS
    bookmarks = bookmark_service.get_all_bookmarks()
    expected_bookmarks = [BookmarkArguments(**data) for data in MOCK_BOOKMARKS]
    assert bookmarks == expected_bookmarks

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_get_all_bookmarks_exceptions(mock_moonshot_api, exception, error_code, bookmark_service):
    """
    Test case for exceptions during retrieval of all bookmarks.
    """
    mock_moonshot_api.api_get_all_bookmarks.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        bookmark_service.get_all_bookmarks()
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_insert_bookmark_success(mock_moonshot_api, bookmark_service):
    """
    Test case for successful insertion of a bookmark.
    """
    mock_moonshot_api.api_insert_bookmark.return_value = {"success": True}
    result = bookmark_service.insert_bookmark(MOCK_BOOKMARK_CREATE_DTO)
    assert result == {"success": True}

@pytest.mark.parametrize("exception, error_code", exception_scenarios)
@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_insert_bookmark_exceptions(mock_moonshot_api, exception, error_code, bookmark_service):
    """
    Test case for exceptions during insertion of a bookmark.
    """
    mock_moonshot_api.api_insert_bookmark.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        bookmark_service.insert_bookmark(MOCK_BOOKMARK_CREATE_DTO)
    assert exc_info.value.error_code == error_code

@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_delete_bookmark_success(mock_moonshot_api, bookmark_service):
    """
    Test case for successful deletion of a single bookmark by ID.
    """
    mock_moonshot_api.api_delete_bookmark.return_value = {"success": True}
    result = bookmark_service.delete_bookmarks(all=False, name="bookmark")
    assert result == {"success": True}

@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_delete_all_bookmarks_success(mock_moonshot_api, bookmark_service):
    """
    Test case for successful deletion of all bookmarks.
    """
    mock_moonshot_api.api_delete_all_bookmark.return_value = {"success": True}
    result = bookmark_service.delete_bookmarks(all=True)
    assert result == {"success": True}

@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_delete_bookmarks_no_params(mock_moonshot_api, bookmark_service):
    """
    Test case for deletion attempt without specifying 'all' or 'id'.
    """
    with pytest.raises(ServiceException):
        bookmark_service.delete_bookmarks()

@pytest.mark.parametrize("exception, error_code", [
       (ServiceException("UnexpectedError", "delete_bookmarks", "UnexpectedError"), "UnexpectedError"),
])
@patch('moonshot.integrations.web_api.services.bookmark_service.moonshot_api')
def test_delete_bookmarks_exceptions(mock_moonshot_api, exception, error_code, bookmark_service):
    """
    Test case for exceptions during deletion of bookmarks.
    """
    mock_moonshot_api.api_delete_bookmark.side_effect = exception
    with pytest.raises(ServiceException) as exc_info:
        bookmark_service.delete_bookmarks(all=False, id=1)
    assert exc_info.value.error_code == error_code
