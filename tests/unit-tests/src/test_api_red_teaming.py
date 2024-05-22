import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_delete_attack_module,
    api_get_all_attack_module_metadata,
    api_get_all_attack_modules,
    api_set_environment_variables,
)


class TestCollectionApiAttackModule:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "ATTACK_MODULES": "tests/unit-tests/src/data/attack-modules/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy attack module
        shutil.copyfile(
            "tests/unit-tests/common/samples/sample_attack_module.py",
            "tests/unit-tests/src/data/attack-modules/sample_attack_module.py",
        )

        # Perform tests
        yield

        # Delete the attack module using os.remove
        attack_modules = [
            "tests/unit-tests/src/data/attack-modules/sample_attack_module.py",
            "tests/unit-tests/src/data/attack-modules/cache.json",
        ]
        for attack_module in attack_modules:
            if os.path.exists(attack_module):
                os.remove(attack_module)

    # ------------------------------------------------------------------------------
    # Test api_get_all_attack_modules functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_attack_modules(self):
        """
        Test the api_get_all_attack_modules function.

        This test ensures that the api_get_all_attack_modules function returns a list of attack modules
        that matches the expected list of detected attack modules.
        """
        detected_attack_modules = ["sample_attack_module"]

        attack_modules = api_get_all_attack_modules()
        assert len(attack_modules) == len(
            detected_attack_modules
        ), "The number of attack modules does not match the expected count."

        for module in attack_modules:
            assert (
                module in detected_attack_modules
            ), f"The module '{module}' was not found in the list of detected attack modules."

    # ------------------------------------------------------------------------------
    # Test api_delete_attack_module functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "am_id,expected_dict",
        [
            # Valid case
            ("sample_attack_module", {"expected_output": True}),
            # Invalid cases
            (
                "nonexistent_module",
                {
                    "expected_output": False,
                    "expected_error_message": "No attack_modules found with ID: nonexistent_module",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No attack_modules found with ID: ",
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
                    "expected_error_message": "No attack_modules found with ID: None",
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
    def test_api_delete_attack_module(self, am_id, expected_dict):
        """
        Test the api_delete_attack_module function.

        This test checks if the function either returns the expected output or raises the expected exception with the correct error message.

        Args:
            am_id: The attack module ID to delete.
            expected_dict: A dictionary containing the 'expected_output', 'expected_error_message', and 'expected_exception' keys.
        """
        if expected_dict["expected_output"]:
            response = api_delete_attack_module(am_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_attack_module does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_attack_module(am_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_attack_module(am_id)
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
    # Test api_get_all_attack_module_metadata functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_attack_module_metadata(self):
        """
        Test the api_get_all_attack_module_metadata function.

        This test verifies that the api_get_all_attack_module_metadata function returns the correct list of attack modules with their metadata.
        """
        detected_attack_modules = [
            {
                "id": "sample_attack_module",
                "name": "Sample Attack Module",
                "description": "This is a sample attack module.",
            }
        ]

        attack_modules = api_get_all_attack_module_metadata()
        assert len(attack_modules) == len(
            detected_attack_modules
        ), "Mismatch in the number of attack modules detected."

        for module_metadata in attack_modules:
            assert (
                module_metadata in detected_attack_modules
            ), f"Module metadata {module_metadata} not found in detected attack modules."
