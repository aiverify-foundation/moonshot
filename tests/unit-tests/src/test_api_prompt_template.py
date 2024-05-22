import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_delete_prompt_template,
    api_get_all_prompt_template_detail,
    api_get_all_prompt_template_name,
    api_set_environment_variables,
)


class TestCollectionApiPromptTemplate:
    @pytest.fixture(autouse=True)
    def init(self):
        # Set environment variables for prompt templates and IO modules
        api_set_environment_variables(
            {
                "PROMPT_TEMPLATES": "tests/unit-tests/src/data/prompt-templates/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy sample prompt template for testing
        shutil.copyfile(
            "tests/unit-tests/common/samples/answer-template.json",
            "tests/unit-tests/src/data/prompt-templates/answer-template.json",
        )

        # Setup complete, proceed with tests
        yield

        # Cleanup: Remove test prompt template file
        prompt_template_path = (
            "tests/unit-tests/src/data/prompt-templates/answer-template.json"
        )
        if os.path.exists(prompt_template_path):
            os.remove(prompt_template_path)

    # ------------------------------------------------------------------------------
    # Test api_get_all_prompt_template_name functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_prompt_template_name(self):
        """
        Test the retrieval of all prompt template names.

        This test ensures that the api_get_all_prompt_template_name function returns a list of prompt template names
        that matches the expected list of available prompt templates.
        """
        expected_prompt_template_names = ["answer-template"]

        prompt_template_names = api_get_all_prompt_template_name()
        assert len(prompt_template_names) == len(
            expected_prompt_template_names
        ), "The number of prompt templates does not match the expected count."

        for template_name in prompt_template_names:
            assert (
                template_name in expected_prompt_template_names
            ), f"The template name '{template_name}' was not found in the list of expected prompt template names."

    # ------------------------------------------------------------------------------
    # Test api_delete_prompt_template functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "template_id,expected_result",
        [
            # Valid case
            ("answer-template", {"success": True}),
            # Invalid cases
            (
                "invalid_template",
                {
                    "success": False,
                    "error_message": "No prompt_templates found with ID: invalid_template",
                    "exception": RuntimeError,
                },
            ),
            (
                "",
                {
                    "success": False,
                    "error_message": "No prompt_templates found with ID: ",
                    "exception": RuntimeError,
                },
            ),
            (
                None,
                {
                    "success": False,
                    "error_message": "Input should be a valid string",
                    "exception": ValidationError,
                },
            ),
            (
                "None",
                {
                    "success": False,
                    "error_message": "No prompt_templates found with ID: None",
                    "exception": RuntimeError,
                },
            ),
            (
                {},
                {
                    "success": False,
                    "error_message": "Input should be a valid string",
                    "exception": ValidationError,
                },
            ),
            (
                [],
                {
                    "success": False,
                    "error_message": "Input should be a valid string",
                    "exception": ValidationError,
                },
            ),
            (
                123,
                {
                    "success": False,
                    "error_message": "Input should be a valid string",
                    "exception": ValidationError,
                },
            ),
        ],
    )
    def test_api_delete_prompt_template(self, template_id, expected_result):
        """
        Test the deletion of a prompt template.

        This test checks if the api_delete_prompt_template function successfully deletes the specified prompt template
        or raises the expected exception with the correct error message.

        Args:
            template_id: The ID of the prompt template to delete.
            expected_result: A dictionary containing the expected 'success', 'error_message', and 'exception' keys.
        """
        if expected_result["success"]:
            result = api_delete_prompt_template(template_id)
            assert (
                result == expected_result["success"]
            ), "The api_delete_prompt_template function did not return the expected success state."
        else:
            if expected_result["exception"] is RuntimeError:
                with pytest.raises(RuntimeError) as e:
                    api_delete_prompt_template(template_id)
                assert (
                    e.value.args[0] == expected_result["error_message"]
                ), "The error message from the exception does not match the expected error message."

            elif expected_result["exception"] is ValidationError:
                with pytest.raises(ValidationError) as e:
                    api_delete_prompt_template(template_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_result["error_message"] in e.value.errors()[0]["msg"]
                ), "The error message from the exception does not match the expected error message."

    # ------------------------------------------------------------------------------
    # Test api_get_all_prompt_template_detail functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_prompt_template_detail(self):
        """
        Test the retrieval of all prompt template details.

        This test verifies that the api_get_all_prompt_template_detail function returns the correct list of prompt templates with their details.
        """
        expected_prompt_templates = [
            {
                "id": "answer-template",
                "name": "answer-template",
                "description": "A template for typical question answering benchmark.",
                "template": "{{ prompt }}\nAnswer:",
            }
        ]

        prompt_template_details = api_get_all_prompt_template_detail()
        assert len(prompt_template_details) == len(
            expected_prompt_templates
        ), "The number of prompt templates detected does not match the expected count."

        for template_detail in prompt_template_details:
            assert (
                template_detail in expected_prompt_templates
            ), f"Prompt template detail {template_detail} not found in expected prompt templates."
