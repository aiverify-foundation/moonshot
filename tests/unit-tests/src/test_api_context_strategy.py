import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_delete_context_strategy,
    api_get_all_context_strategies,
    api_get_all_context_strategy_metadata,
    api_set_environment_variables,
)


class TestCollectionApiContextStrategy:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "CONTEXT_STRATEGY": "tests/unit-tests/src/data/context-strategy/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy endpoint
        shutil.copyfile(
            "tests/unit-tests/common/samples/add_previous_prompt.py",
            "tests/unit-tests/src/data/context-strategy/add_previous_prompt.py",
        )

        # Perform tests
        yield

        # Delete the endpoint using os.remove
        context_strategies = [
            "tests/unit-tests/src/data/context-strategy/add_previous_prompt.py"
        ]
        for context_strategy in context_strategies:
            if os.path.exists(context_strategy):
                os.remove(context_strategy)

    # ------------------------------------------------------------------------------
    # Test api_get_all_context_strategies functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_context_strategies(self):
        """
        Test the api_get_all_context_strategies function.

        This test ensures that the api_get_all_context_strategies function returns a list of context strategies
        that matches the expected list of detected context strategies.
        """
        detected_context_strategies = ["add_previous_prompt"]

        context_strategies = api_get_all_context_strategies()
        assert len(context_strategies) == len(
            detected_context_strategies
        ), "The number of context strategies does not match the expected count."

        for strategy in context_strategies:
            assert (
                strategy in detected_context_strategies
            ), f"The strategy '{strategy}' was not found in the list of detected context strategies."

    # ------------------------------------------------------------------------------
    # Test api_delete_context_strategy functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cs_id,expected_dict",
        [
            # Valid case
            ("add_previous_prompt", {"expected_output": True}),
            # Invalid cases
            (
                "previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "No context_strategy found with ID: previous_prompt",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No context_strategy found with ID: ",
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
                    "expected_error_message": "No context_strategy found with ID: None",
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
    def test_api_delete_context_strategy(self, cs_id, expected_dict):
        """
        Test the api_delete_context_strategy function.

        This test checks if the function either returns the expected output or raises the expected exception with the correct error message.

        Args:
            cs_id: The context strategy ID to delete.
            expected_dict: A dictionary containing the 'expected_output', 'expected_error_message', and 'expected_exception' keys.
        """
        if expected_dict["expected_output"]:
            response = api_delete_context_strategy(cs_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_context_strategy does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_context_strategy(cs_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_context_strategy(cs_id)
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
    # Test api_get_all_context_strategy_metadata functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_context_strategy_metadata(self):
        """
        Test the api_get_all_context_strategy_metadata function.

        This test verifies that the api_get_all_context_strategy_metadata function returns the correct list of context strategies with their metadata.
        """
        detected_context_strategies = [
            {
                "id": "add_previous_prompt",
                "name": "Add Previous Prompt",
                "description": "This is a sample context strategy that adds in previous prompts to the current prompt. [Default: 5]",
            }
        ]

        context_strategies = api_get_all_context_strategy_metadata()
        assert len(context_strategies) == len(
            detected_context_strategies
        ), "Mismatch in the number of context strategies detected."

        for strategy_metadata in context_strategies:
            assert (
                strategy_metadata in detected_context_strategies
            ), f"Strategy metadata {strategy_metadata} not found in detected context strategies."
