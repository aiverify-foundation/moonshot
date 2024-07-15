import pytest
import shutil
import os

from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from moonshot.api import (
    api_get_bookmark,
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
                "BOOKMARKS": "tests/unit-tests/src/data/bookmarks/",
                "DATABASES": "tests/unit-tests/src/data/databases/",
                "DATABASES_MODULES": "tests/unit-tests/src/data/databases-modules/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )
    
        shutil.copyfile(
            "tests/unit-tests/common/samples/bookmark.db",
            "tests/unit-tests/src/data/bookmarks/bookmark.db",
        )

        yield

        run_data_files = [
            # "tests/unit-tests/src/data/bookmarks/bookmark.db",
            "tests/unit-tests/src/data/bookmarks/bookmark.json",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
                },
                {"expected_output": True},
            ),
            # Invalid case for 'name'
            (
                {
                    "name": None,
                    "prompt": "Prompt F",
                    "response": "Response F",
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
                    "prepared_prompt": "Prepared Prompt",
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
    def test_api_insert_bookmark(self, input_args, expected_dict):
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
    def test_api_get_all_bookmark(self):
        # Set up the expected return value for get_all_bookmarks
        expected_bookmarks = [
            {
                'name': 'Test Bookmark',
                'prompt': 'Test Prompt',
                "prepared_prompt": "Test Prepared Prompt",
                'response': 'Test Response',
                'context_strategy': '',
                'prompt_template': '',
                'attack_module': '',
                'metric': '',
                'bookmark_time': '2024-07-14 22:26:51'
            }
        ]

        # Call the API function
        actual_bookmarks = api_get_all_bookmarks()
        # Assert that the returned bookmarks match the expected bookmarks
        assert actual_bookmarks == expected_bookmarks, "The returned bookmarks do not match the expected bookmarks."

    @pytest.mark.parametrize(
        "bookmark_name, expected_dict",
    [
        # Valid case
        (
            "Test Bookmark",
            {
                "expected_result": {
                    'name': 'Test Bookmark',
                    'prompt': 'Test Prompt',
                    "prepared_prompt": "Test Prepared Prompt",
                    'response': 'Test Response',
                    'context_strategy': '',
                    'prompt_template': '',
                    'attack_module': '',
                    'metric': '',
                    'bookmark_time': '2024-07-14 22:26:51'
                }
            }
        ),
    ],
)
    def test_api_get_bookmark(self, bookmark_name, expected_dict):
        if "expected_exception" in expected_dict:
            # Call the API function and assert that the expected exception is raised
            with pytest.raises(expected_dict["expected_exception"]) as exc_info:
                api_get_bookmark(bookmark_name)
            # Assert that the exception message matches the expected message
            assert str(exc_info.value) == expected_dict["expected_message"], "The expected exception message was not raised."
        else:
            # Call the API function and get the response
            response = api_get_bookmark(bookmark_name)
            # Assert that the response matches the expected bookmark
            assert response == expected_dict["expected_result"], "The returned bookmark does not match the expected bookmark."
    

    # ------------------------------------------------------------------------------
    # Test api_get_delete_all_bookmark functionality
    # ------------------------------------------------------------------------------
    def test_api_delete_all_bookmark(self):
        # Set up the expected return value for delete_all_bookmark
        expected_response = {'success': True, 'message': 'All bookmark records deleted.'}

        # Call the API function
        delete_response = api_delete_all_bookmark()

        # Assert that the response matches the expected response
        assert delete_response == expected_response, "The response from delete_all_bookmark does not match the expected response."


    # ------------------------------------------------------------------------------
    # Test api_delete_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_name, expected_dict",
        [
            # Valid case
            (
                "Test Bookmark",
                {
                    "expected_result": {
                        'success': True, 'message': 'Bookmark record deleted.'
                    }
                }
            )
        ],
    )
    def test_api_delete_bookmark(self, bookmark_name, expected_dict):
        # Extract variables from expected_dict
        expected_exception = expected_dict.get("expected_exception")
        expected_message = expected_dict.get("expected_message")
        expected_result = expected_dict.get("expected_result")

        if expected_exception:
            # Call the API function and assert that the expected exception is raised
            with pytest.raises(expected_exception) as exc_info:
                api_delete_bookmark(bookmark_name)
            # Assert that the exception message matches the expected message
            assert str(exc_info.value) == expected_message, "The expected exception message was not raised."
        else:
            # Call the API function and get the response
            response = api_delete_bookmark(bookmark_name)
            # Assert that the response matches the expected result
            assert response == expected_result, "The returned result does not match the expected result."

    # ------------------------------------------------------------------------------
    # Test api_export_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "export_file_name, expected_output",
        [
            ("bookmark", "../moonshot-data/generated-outputs/bookmarks/bookmark.json")
        ]
    )
    def test_api_export_bookmarks(self, export_file_name, expected_output):
        # Call the API function
        actual_output = api_export_bookmarks(export_file_name)
        print(actual_output)
        # Assert that the returned output matches the expected output
        assert actual_output == expected_output, "The returned output from api_export_bookmarks does not match the expected output."
