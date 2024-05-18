import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.src.api.api_environment_variables import api_set_environment_variables
from moonshot.src.api.api_prompt_template import (
    api_delete_prompt_template,
    api_get_all_prompt_template_detail,
    api_get_all_prompt_template_name,
)


class TestCollectionApiPromptTemplate:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "PROMPT_TEMPLATES": "tests/unit-tests/src/data/prompt-templates/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy endpoint
        shutil.copyfile(
            "tests/unit-tests/src/data/samples/answer-template.json",
            "tests/unit-tests/src/data/prompt-templates/answer-template.json",
        )

        # Perform tests
        yield

        # Delete the endpoint using os.remove
        prompt_templates = [
            "tests/unit-tests/src/data/prompt-templates/answer-template.json"
        ]
        for prompt_template in prompt_templates:
            if os.path.exists(prompt_template):
                os.remove(prompt_template)

    # ------------------------------------------------------------------------------
    # Test api_get_all_prompt_template_name functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_prompt_template_name(self):
        """
        Test the api_get_all_prompt_template_name function.

        This test ensures that the api_get_all_prompt_template_name function returns a list of prompt template names
        that matches the expected list of detected prompt templates.
        """
        detected_prompt_templates = ["answer-template"]

        prompt_templates = api_get_all_prompt_template_name()
        print(prompt_templates)
        assert len(prompt_templates) == len(
            detected_prompt_templates
        ), "The number of prompt templates does not match the expected count."

        for template in prompt_templates:
            assert (
                template in detected_prompt_templates
            ), f"The template '{template}' was not found in the list of detected prompt templates."

    # ------------------------------------------------------------------------------
    # Test api_delete_prompt_template functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "pt_id,expected_dict",
        [
            # Valid case
            ("answer-template", {"expected_output": True}),
            # Invalid cases
            (
                "invalid_template",
                {
                    "expected_output": False,
                    "expected_error_message": "No prompt_templates found with ID: invalid_template",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No prompt_templates found with ID: ",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "No prompt_templates found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_delete_prompt_template(self, pt_id, expected_dict):
        """
        Test the api_delete_prompt_template function.

        This test checks if the function either returns the expected output or raises the expected exception with the correct error message.

        Args:
            pt_id: The prompt template ID to delete.
            expected_dict: A dictionary containing the 'expected_output', 'expected_error_message', and 'expected_exception' keys.
        """
        if expected_dict["expected_output"]:
            response = api_delete_prompt_template(pt_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_prompt_template does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_prompt_template(pt_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_prompt_template(pt_id)
                assert (
                    len(e.value.errors()) == 1
                ), "The number of validation errors does not match the expected count."
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                ), "The validation error message does not contain the expected text."

            else:
                assert (
                    False
                ), "An unexpected exception type was specified in the test parameters."

    # ------------------------------------------------------------------------------
    # Test api_get_all_prompt_template_detail functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_prompt_template_detail(self):
        """
        Test the api_get_all_prompt_template_detail function.

        This test verifies that the api_get_all_prompt_template_detail function returns the correct list of prompt templates with their details.
        """
        detected_prompt_templates = [
            {
                "id": "answer-template",
                "name": "answer-template",
                "description": "A template for typical question answering benchmark.",
                "template": "{{ prompt }}\nAnswer:",
            }
        ]

        prompt_templates = api_get_all_prompt_template_detail()
        assert len(prompt_templates) == len(
            detected_prompt_templates
        ), "Mismatch in the number of prompt templates detected."

        for template_detail in prompt_templates:
            assert (
                template_detail in detected_prompt_templates
            ), f"Template detail {template_detail} not found in detected prompt templates."
