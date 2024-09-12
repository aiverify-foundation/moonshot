import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_delete_all_bookmark,
    api_delete_bookmark,
    api_export_bookmarks,
    api_get_all_bookmarks,
    api_get_bookmark,
    api_insert_bookmark,
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

        # Copy the required bookmark database
        shutil.copy(
            "tests/unit-tests/common/samples/bookmark.db",
            "tests/unit-tests/src/data/bookmarks/bookmark.db",
        )

        # Create a bookmark instance
        bookmark_instance = Bookmark()

        yield

        # Terminate the bookmark_instance
        bookmark_instance.close()

        # Delete bookmark database and accompanying files
        run_data_files = [
            Path("tests/unit-tests/src/data/bookmarks/bookmark.db"),
            Path("tests/unit-tests/src/data/bookmarks/bookmark.json"),
        ]
        for run_data_file in run_data_files:
            if run_data_file.exists():
                run_data_file.unlink()

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
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {"expected_output": True},
            ),
            # No Context Strategy
            (
                {
                    "name": "Bookmark C",
                    "prompt": "Prompt C",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response C",
                    "prompt_template": "Template C",
                    "attack_module": "Module C",
                    "metric": "Metric C",
                },
                {"expected_output": True},
            ),
            # No Prompt Template
            (
                {
                    "name": "Bookmark D",
                    "prompt": "Prompt D",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response D",
                    "context_strategy": "Strategy D",
                    "attack_module": "Module D",
                    "metric": "Metric D",
                },
                {"expected_output": True},
            ),
            # No Attack Module
            (
                {
                    "name": "Bookmark B",
                    "prompt": "Prompt B",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response B",
                    "context_strategy": "Strategy B",
                    "prompt_template": "Template B",
                    "metric": "Metric B",
                },
                {"expected_output": True},
            ),
            # No Metric
            (
                {
                    "name": "Bookmark A1",
                    "prompt": "Prompt A1",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A1",
                    "context_strategy": "Strategy A1",
                    "prompt_template": "Template A1",
                },
                {"expected_output": True},
            ),
            # Only Required Fields
            (
                {
                    "name": "Bookmark E",
                    "prompt": "Prompt E",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response E",
                },
                {"expected_output": True},
            ),
            # Invalid case for 'name'
            (
                {
                    "name": None,
                    "prompt": "Prompt F",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prompt": "Prompt F",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": (),
                    "prompt": "Prompt F",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": [],
                    "prompt": "Prompt F",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prompt": "Prompt F",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prompt": "Prompt F",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark L",
                    "prompt": (),
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark M",
                    "prompt": [],
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'prepared_prompt'
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": None,
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "",
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": (),
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": [],
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": {},
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": 123,
                    "response": "Response F",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": None,
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": (),
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": [],
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": {},
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": 123,
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": None,
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": (),
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": [],
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": {},
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": 123,
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": None,
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": (),
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": [],
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": {},
                    "attack_module": "Module A",
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": 123,
                    "attack_module": "Module A",
                    "metric": "Metric A",
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
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": None,
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": (),
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": [],
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": {},
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": 123,
                    "metric": "Metric A",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            # Invalid cases for 'metric'
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": "Module A",
                    "metric": None,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": "Module A",
                    "metric": (),
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": "Module A",
                    "metric": [],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": "Module A",
                    "metric": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
            (
                {
                    "name": "Bookmark P",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Prompt Template",
                    "attack_module": "Module A",
                    "metric": 123,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": ValidationError,
                },
            ),
        ],
    )
    def test_api_insert_bookmark(self, input_args, expected_dict):
        # Call the API function to insert a bookmark
        if expected_dict["expected_output"]:
            # Assert successful bookmark insertion
            result = api_insert_bookmark(**input_args)
            assert (
                result["success"] == expected_dict["expected_output"]
            ), "Bookmark insertion should succeed."
        else:
            # Test invalid cases where bookmark insertion should fail and raise an exception
            with pytest.raises(expected_dict["expected_exception"]) as exc_info:
                api_insert_bookmark(**input_args)
            assert (
                exc_info.value.errors()[0]["msg"]
                == expected_dict["expected_error_message"]
            )

    # ------------------------------------------------------------------------------
    # Test api_get_all_bookmarks functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_bookmark(self):
        # Set up the expected return value for get_all_bookmarks
        expected_bookmarks = [
            {
                "name": "Test Bookmark",
                "prompt": "Test Prompt",
                "prepared_prompt": "Test Prepared Prompt",
                "response": "Test Response",
                "context_strategy": "",
                "prompt_template": "",
                "attack_module": "",
                "metric": "",
                "bookmark_time": "2024-07-14 22:26:51",
            }
        ]

        # Call the API function
        actual_bookmarks = api_get_all_bookmarks()
        # Assert that the returned bookmarks match the expected bookmarks
        assert (
            actual_bookmarks == expected_bookmarks
        ), "The returned bookmarks do not match the expected bookmarks."

    # ------------------------------------------------------------------------------
    # Test api_get_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_name, expected_result",
        [
            # Valid case
            (
                "Test Bookmark",
                {
                    "name": "Test Bookmark",
                    "prompt": "Test Prompt",
                    "prepared_prompt": "Test Prepared Prompt",
                    "response": "Test Response",
                    "context_strategy": "",
                    "prompt_template": "",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-07-14 22:26:51",
                },
            ),
        ],
    )
    def test_api_get_bookmark(self, bookmark_name, expected_result, mocker):
        # Mock the get_bookmark method of the Bookmark class
        mocker.patch.object(Bookmark, 'get_bookmark', return_value=expected_result)
        
        # Call the API function and get the result
        result = api_get_bookmark(bookmark_name)
        
        # Assert that the result matches the expected result
        assert result == expected_result, "The returned result does not match the expected result."

    # ------------------------------------------------------------------------------
    # Test api_delete_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_name, expected_result",
        [
            # Valid case
            (
                "Test Bookmark",
                {
                    "success": True,
                    "message": "[Bookmark] Bookmark record deleted.",
                },
            ),
            # Missing bookmark
            (
                "Invalid bookmark",
                {
                    "success": False,
                    "message": "[Bookmark] Bookmark record not found. Unable to delete."
                },
            )
        ],
    )
    def test_api_delete_bookmark(self, bookmark_name, expected_result):
        # Call the API function and get the response
        response = api_delete_bookmark(bookmark_name)
        # Assert that the response matches the expected result
        assert response == expected_result, "The returned result does not match the expected result."

    # ------------------------------------------------------------------------------
    # Test api_get_delete_all_bookmark functionality
    # ------------------------------------------------------------------------------
    def test_api_delete_all_bookmark(self):
        # Set up the expected return value for delete_all_bookmark
        expected_response = {
            "success": True,
            "message": "[Bookmark] All bookmark records deleted.",
        }

        # Call the API function
        delete_response = api_delete_all_bookmark()

        # Assert that the response matches the expected response
        assert (
            delete_response == expected_response
        ), "The response from delete_all_bookmark does not match the expected response."

    # ------------------------------------------------------------------------------
    # Test api_export_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "export_file_name, expected_output",
        [("bookmark", "tests/unit-tests/src/data/bookmarks/bookmark.json")],
    )
    def test_api_export_bookmarks(self, export_file_name, expected_output):
        # Call the API function
        actual_output = api_export_bookmarks(export_file_name)
        # Assert that the returned output matches the expected output
        assert (
            actual_output == expected_output
        ), "The returned output from api_export_bookmarks does not match the expected output."
