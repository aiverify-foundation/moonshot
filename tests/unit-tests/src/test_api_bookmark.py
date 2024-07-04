import pytest
import shutil
import os

from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from moonshot.api import (
    api_get_bookmark_by_id,
    api_export_bookmarks,
    api_delete_bookmark,
    api_insert_bookmark,
    api_get_all_bookmarks,
    api_delete_all_bookmark,
    api_set_environment_variables,
)

from moonshot.src.bookmark.bookmark import Bookmark

class TestCollectionApiBookmark:
    @pytest.fixture(autouse=True)
    def init(self):
        # Initialize environment variables and copy sample files for testing
        api_set_environment_variables(
            {
                "BOOKMARK": "tests/unit-tests/src/data/bookmark/",
                "DATABASES": "tests/unit-tests/src/data/databases/",
                "DATABASES_MODULES": "tests/unit-tests/src/data/databases-modules/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        shutil.copyfile(
            "tests/unit-tests/common/samples/bookmark.db",
            "tests/unit-tests/src/data/bookmark/bookmark.db",
        )

        yield

        run_data_files = [
            "tests/unit-tests/src/data/bookmark/bookmark.db",
        ]
        for run_data_file in run_data_files:
            if os.path.exists(run_data_file):
                os.remove(run_data_file)

    # ------------------------------------------------------------------------------
    # Test bookmark instance is singleton
    # ------------------------------------------------------------------------------
    def test_bookmark_singleton(self):
        # Retrieve two instances of the Bookmark class
        bookmark_instance_1 = Bookmark()
        bookmark_instance_2 = Bookmark()

        # Assert that both instances are the same (singleton behavior)
        assert bookmark_instance_1 is bookmark_instance_2, "Bookmark instances should be the same (singleton pattern)."

    # ------------------------------------------------------------------------------
    # Test api_insert_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, expected_dict",
        [
        # Valid cases for bookmark insertions
            # All Value present
            (
                {
                    "name": "Bookmark A",
                    "prompt": "Prompt A",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A"
                },
                {"expected_output": True},
            ),
            # No Attack Module
            (
                {
                    "name": "Bookmark B",
                    "prompt": "Prompt B",
                    "response": "Response B",
                    "context_strategy": "Strategy B",
                    "prompt_template": "Template B",
                },
                {"expected_output": True},
            ),
            # No Context Strategy
            (
                {
                    "name": "Bookmark C",
                    "prompt": "Prompt C",
                    "response": "Response C",
                    "prompt_template": "Template C",
                    "attack_module": "Module C"
                },
                {"expected_output": True},
            ),
            # No Prompt Template
            (
                {
                    "name": "Bookmark D",
                    "prompt": "Prompt D",
                    "response": "Response D",
                    "context_strategy": "Strategy D",
                    "attack_module": "Module D"
                },
                {"expected_output": True},
            ),
            # Only Required Fields
            (
                {
                    "name": "Bookmark E",
                    "prompt": "Prompt E",
                    "response": "Response E",
                },
                {"expected_output": True},
            ),
            # Invalid case for 'name'
            (
                {
                    "name": None,
                    "prompt": "Prompt F",
                    "response": "Response F",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "",
                    "prompt": "Prompt G",
                    "response": "Response G",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": [],
                    "prompt": "Prompt H",
                    "response": "Response H",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": {},
                    "prompt": "Prompt I",
                    "response": "Response I",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": 123,
                    "prompt": "Prompt J",
                    "response": "Response J",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'prompt'
            (
                {
                    "name": "Bookmark K",
                    "prompt": None,
                    "response": "Response K",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark L",
                    "prompt": "",
                    "response": "Response L",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark M",
                    "prompt": [],
                    "response": "Response M",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark N",
                    "prompt": {},
                    "response": "Response N",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark O",
                    "prompt": 123,
                    "response": "Response O",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'prompt'
            (
                {
                    "name": "Bookmark P",
                    "prompt": None,
                    "response": "Response P",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark Q",
                    "prompt": "",
                    "response": "Response Q",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark R",
                    "prompt": [],
                    "response": "Response R",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark S",
                    "prompt": {},
                    "response": "Response S",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark T",
                    "prompt": 123,
                    "response": "Response T",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),

            # Invalid cases for 'response'
            (
                {
                    "name": "Bookmark U",
                    "prompt": "Prompt U",
                    "response": None,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark V",
                    "prompt": "Prompt V",
                    "response": "",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark W",
                    "prompt": "Prompt W",
                    "response": [],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark X",
                    "prompt": "Prompt X",
                    "response": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark Y",
                    "prompt": "Prompt Y",
                    "response": 123,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'attack_module'
            (
                {
                    "name": "Bookmark Z",
                    "prompt": "Prompt Z",
                    "response": "Response Z",
                    "attack_module": 123
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark AA",
                    "prompt": "Prompt AA",
                    "response": "Response AA",
                    "attack_module": []
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark AB",
                    "prompt": "Prompt AB",
                    "response": "Response AB",
                    "attack_module": {}
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'context_strategy'
            (
                {
                    "name": "Bookmark Z",
                    "prompt": "Prompt Z",
                    "response": "Response Z",
                    "context_strategy": 123
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark AA",
                    "prompt": "Prompt AA",
                    "response": "Response AA",
                    "context_strategy": []
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark AB",
                    "prompt": "Prompt AB",
                    "response": "Response AB",
                    "context_strategy": {}
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'prompt_template'
            (
                {
                    "name": "Bookmark Z",
                    "prompt": "Prompt Z",
                    "response": "Response Z",
                    "prompt_template": 123
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark AA",
                    "prompt": "Prompt AA",
                    "response": "Response AA",
                    "prompt_template": []
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark AB",
                    "prompt": "Prompt AB",
                    "response": "Response AB",
                    "prompt_template": {}
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
        ]
    )
    @patch('moonshot.src.api.api_bookmark.get_bookmark_instance')
    def test_api_insert_bookmark(self, mock_get_instance, input_args, expected_dict):
        # Mock the Bookmark instance and its methods
        mock_instance = MagicMock()
        mock_get_instance.return_value = mock_instance

        # Configure the mock to return success or failure based on expected_dict
        if expected_dict["expected_output"]:
            mock_instance.add_bookmark.return_value = {"success": True}
        else:
            # Pass the exception class itself, not an instance of the class
            mock_instance.add_bookmark.side_effect = expected_dict["expected_exception"]

        # Call the API function to insert a bookmark
        if expected_dict["expected_output"]:
            # Assert successful bookmark insertion
            result = api_insert_bookmark(**input_args)
            assert result["success"] == expected_dict["expected_output"], "Bookmark insertion should succeed."
        else:
            # Test invalid cases where bookmark insertion should fail and raise an exception
            with pytest.raises(expected_dict["expected_exception"]) as exc_info:
                api_insert_bookmark(**input_args)

    # ------------------------------------------------------------------------------
    # Test api_get_all_bookmarks functionality
    # ------------------------------------------------------------------------------
    @patch('moonshot.src.api.api_bookmark.get_bookmark_instance')
    def test_api_get_all_bookmark(self, mock_get_instance):
        # Mock the Bookmark instance and its methods
        mock_instance = MagicMock()
        mock_get_instance.return_value = mock_instance
        
        # Set up the expected return value for get_all_bookmarks
        expected_bookmarks = [
            {
                'id': 1, 'name': 'my bookmark 1',
                'prompt': 'Your prompt',
                'response': 'Your response',
                'context_strategy': 'Your context strategy',
                'prompt_template': 'Your prompt template',
                'attack_module': 'Your attack module',
                'bookmark_time': '2024-07-03 21:05:58'
            }
        ]
        mock_instance.get_all_bookmarks.return_value = expected_bookmarks

        # Call the API function
        actual_bookmarks = api_get_all_bookmarks()

        # Assert that the returned bookmarks match the expected bookmarks
        assert actual_bookmarks == expected_bookmarks, "The returned bookmarks do not match the expected bookmarks."

    # ------------------------------------------------------------------------------
    # Test api_get_bookmark_by_id functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_id, expected_dict",
        [
            # Valid case
            (
                1,
                {
                    "expected_result": {
                        'id': 1, 'name': 'my bookmark 1',
                        'prompt': 'Your prompt',
                        'response': 'Your response',
                        'context_strategy': 'Your context strategy',
                        'prompt_template': 'Your prompt template',
                        'attack_module': 'Your attack module',
                        'bookmark_time': '2024-07-03 21:05:58'
                    }
                }
            ),
            # Invalid bookmark_id (None)
            (
                None,
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] Invalid bookmark_id: None"
                }
            ),
            # Invalid bookmark_id (empty string)
            (
                "",
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] Invalid bookmark_id: "
                }
            ),
            # Invalid bookmark_id (negative number)
            (
                -1,
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] Invalid bookmark_id: -1"
                }
            ),
            # Bookmark not found
            (
                999,
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] No record found for bookmark_id 999"
                }
            ),
        ],
    )
    @patch('moonshot.src.api.api_bookmark.get_bookmark_instance')
    def test_api_get_bookmark_by_id(self, mock_get_instance, bookmark_id, expected_dict):
        # Mock the Bookmark instance and its methods
        mock_instance = MagicMock()
        mock_get_instance.return_value = mock_instance

        if "expected_exception" in expected_dict:
            # Configure the mock to raise an exception when get_bookmark_by_id is called
            mock_instance.get_bookmark_by_id.side_effect = expected_dict["expected_exception"](expected_dict["expected_message"])
            # Call the API function and assert that the expected exception is raised
            with pytest.raises(expected_dict["expected_exception"]) as exc_info:
                api_get_bookmark_by_id(bookmark_id)
            # Assert that the exception message matches the expected message
            assert str(exc_info.value) == expected_dict["expected_message"], "The expected exception message was not raised."
        else:
            # Configure the mock to return the expected bookmark
            mock_instance.get_bookmark_by_id.return_value = expected_dict["expected_result"]
            # Call the API function and get the response
            response = api_get_bookmark_by_id(bookmark_id)
            # Assert that the response matches the expected bookmark
            assert response == expected_dict["expected_result"], "The returned bookmark does not match the expected bookmark."

    # ------------------------------------------------------------------------------
    # Test api_get_delete_all_bookmark functionality
    # ------------------------------------------------------------------------------
    @patch('moonshot.src.api.api_bookmark.get_bookmark_instance')
    def test_api_delete_all_bookmark(self, mock_get_instance):
        # Mock the Bookmark instance and its methods
        mock_instance = MagicMock()
        mock_get_instance.return_value = mock_instance
        
        # Set up the expected return value for delete_all_bookmark
        expected_response = {'success': True, 'message': 'All bookmark records deleted.'}
        mock_instance.delete_all_bookmark.return_value = expected_response

        # Call the API function
        delete_response = api_delete_all_bookmark()

        # Assert that the response matches the expected response
        assert delete_response == expected_response, "The response from delete_all_bookmark does not match the expected response."

    # ------------------------------------------------------------------------------
    # Test api_delete_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_id, expected_dict",
        [
            # Valid case
            (
                1,
                {
                    "expected_result": {
                        'id': 1, 'name': 'my bookmark 1',
                        'prompt': 'Your prompt',
                        'response': 'Your response',
                        'context_strategy': 'Your context strategy',
                        'prompt_template': 'Your prompt template',
                        'attack_module': 'Your attack module',
                        'bookmark_time': '2024-07-03 21:05:58'
                    }
                }
            ),
            # Invalid bookmark_id (None)
            (
                None,
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] Invalid bookmark_id: None"
                }
            ),
            # Invalid bookmark_id (empty string)
            (
                "",
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] Invalid bookmark_id: "
                }
            ),
            # Invalid bookmark_id (negative number)
            (
                -1,
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] Invalid bookmark_id: -1"
                }
            ),
            # Bookmark not found
            (
                999,
                {
                    "expected_exception": RuntimeError,
                    "expected_message": "[Bookmark] No record found for bookmark_id 999"
                }
            ),
        ],
    )
    @patch('moonshot.src.api.api_bookmark.get_bookmark_instance')
    def test_api_delete_bookmark(self, mock_get_instance, bookmark_id, expected_dict):
        # Mock the Bookmark instance and its methods
        mock_instance = MagicMock()
        mock_get_instance.return_value = mock_instance

        # Extract variables from expected_dict
        expected_exception = expected_dict.get("expected_exception")
        expected_message = expected_dict.get("expected_message")
        expected_result = expected_dict.get("expected_result")

        if expected_exception:
            # Configure the mock to raise an exception when delete_bookmark is called
            mock_instance.delete_bookmark.side_effect = expected_exception(expected_message)
            # Call the API function and assert that the expected exception is raised
            with pytest.raises(expected_exception) as exc_info:
                api_delete_bookmark(bookmark_id)
            # Assert that the exception message matches the expected message
            assert str(exc_info.value) == expected_message, "The expected exception message was not raised."
        else:
            # Configure the mock to return the expected result
            mock_instance.delete_bookmark.return_value = expected_result
            # Call the API function and get the response
            response = api_delete_bookmark(bookmark_id)
            # Assert that the response matches the expected result
            assert response == expected_result, "The returned result does not match the expected result."

    # ------------------------------------------------------------------------------
    # Test api_export_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "write_file, export_file_name, expected_output",
        [
            # Test case no value is given
            (
                None, None,
                [
                    {'id':  1, 'name': 'my bookmark 1', 'prompt': 'Your prompt', 'response': 'Your response', 'context_strategy': 'Your context strategy', 'prompt_template': 'Your prompt template', 'attack_module': '', 'bookmark_time': '2024-07-04 15:53:23'}
                ]
            ),
            # Test case when write_file is False
            (
                False, None,
                [
                    {'id':  1, 'name': 'my bookmark 1', 'prompt': 'Your prompt', 'response': 'Your response', 'context_strategy': 'Your context strategy', 'prompt_template': 'Your prompt template', 'attack_module': '', 'bookmark_time': '2024-07-04 15:53:23'}
                ]
            ),
            # Test case when write_file is True
            (
                True, "custom_filename",
                [
                    {'id': 1, 'name': 'my bookmark 1', 'prompt': 'Your prompt', 'response': 'Your response', 'context_strategy': 'Your context strategy', 'prompt_template': 'Your prompt template', 'attack_module': '', 'bookmark_time': '2024-07-04 15:53:23'}
                ]
            )
        ]
    )
    @patch('moonshot.src.api.api_bookmark.get_bookmark_instance')
    def test_api_export_bookmarks(self, mock_get_instance, write_file, export_file_name, expected_output):
        # Mock the Bookmark instance and its methods
        mock_instance = MagicMock()
        mock_get_instance.return_value = mock_instance
        mock_instance.export_bookmarks.return_value = expected_output

        # Call the API function
        actual_output = api_export_bookmarks(write_file, export_file_name)

        # Assert that the returned output matches the expected output
        assert actual_output == expected_output, "The returned output from api_export_bookmarks does not match the expected output."
