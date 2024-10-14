import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_create_cookbook,
    api_delete_cookbook,
    api_get_all_cookbook,
    api_get_all_cookbook_name,
    api_read_cookbook,
    api_read_cookbooks,
    api_set_environment_variables,
    api_update_cookbook,
)


class TestCollectionApiCookbook:
    @pytest.fixture(autouse=True)
    def init(self):
        # Initialize environment variables and copy sample files for testing
        api_set_environment_variables(
            {
                "COOKBOOKS": "tests/unit-tests/src/data/cookbooks/",
                "RECIPES": "tests/unit-tests/src/data/recipes/",
                "DATASETS": "tests/unit-tests/src/data/datasets/",
                "TEMPLATES": "tests/unit-tests/src/data/templates/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/"
            }
        )

        # Copy sample cookbook and dataset files for testing
        shutil.copyfile(
            "tests/unit-tests/common/samples/sample-cookbook.json",
            "tests/unit-tests/src/data/cookbooks/sample-cookbook.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/arc.json",
            "tests/unit-tests/src/data/recipes/arc.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/arc-easy.json",
            "tests/unit-tests/src/data/datasets/arc-easy.json",
        )

        # Yield to test execution
        yield

        # Cleanup test environment by removing test cookbook files
        cookbook_paths = [
            "tests/unit-tests/src/data/cookbooks/sample-cookbook.json",
            "tests/unit-tests/src/data/recipes/arc.json",
            "tests/unit-tests/src/data/datasets/arc-easy.json",
            "tests/unit-tests/src/data/cookbooks/my-new-coo-kbook-1-23.json",
            "tests/unit-tests/src/data/cookbooks/my-new-cookbook-1.json",
            "tests/unit-tests/src/data/cookbooks/my-new-cookbook.json",
            "tests/unit-tests/src/data/cookbooks/none.json",
        ]
        for cookbook_path in cookbook_paths:
            if os.path.exists(cookbook_path):
                os.remove(cookbook_path)

    # ------------------------------------------------------------------------------
    # Test api_create_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, expected_dict",
        [
            # Test cases for valid cookbook creation
            (
                {
                    "name": "my-new-cookbook",
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {"expected_output": True, "expected_id": "my-new-cookbook"},
            ),
            (
                {
                    "name": "my new cookbook 1",
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {"expected_output": True, "expected_id": "my-new-cookbook-1"},
            ),
            (
                {
                    "name": "my_new-coo kbook 1@.!23",
                    "description": "My new Recipe!",
                    "recipes": ["arc"],
                },
                {"expected_output": True, "expected_id": "my-new-coo-kbook-1-23"},
            ),
            (
                {
                    "name": "None",
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {
                    "expected_output": True,
                    "expected_id": "none",
                },
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": "",
                    "recipes": ["arc"],
                },
                {"expected_output": True, "expected_id": "my-new-cookbook"},
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {"expected_output": True, "expected_id": "my-new-cookbook"},
            ),
            # Invalid cases for name
            (
                {
                    "name": "",
                    "description": "My new Cookbook!",
                    "tags": [],
                    "categories": [],
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_id": "",
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": None,
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": [],
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": {},
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": 123,
                    "description": "My new Cookbook!",
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for description
            (
                {
                    "name": "my-new-cookbook",
                    "description": None,
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": [],
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": {},
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": 123,
                    "recipes": ["arc"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for recipes
            (
                {
                    "name": "my-new-cookbook",
                    "description": "A collection of recipes!",
                    "recipes": "",
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": "A collection of recipes!",
                    "recipes": None,
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-cookbook",
                    "description": "A collection of recipes!",
                    "recipes": ["arc", 123],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-cookbook",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_create_cookbook(self, input_args, expected_dict):
        """
        Validate the creation of cookbooks with various inputs.

        This test checks the api_create_cookbook function with different input arguments and expected outcomes,
        ensuring that valid inputs result in successful creation and invalid inputs raise the appropriate exceptions.

        Args:
            input_args (dict): Parameters for cookbook creation.
            expected_dict (dict): Expected results, including output, ID, error message, and exception type.

        """
        if expected_dict["expected_output"]:
            # Assert successful cookbook creation
            assert (
                api_create_cookbook(
                    input_args["name"],
                    input_args["description"],
                    input_args["recipes"],
                )
                == expected_dict["expected_id"]
            )
        else:
            # Test invalid cases where cookbook creation should fail and raise an exception.
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_cookbook(
                        input_args["name"],
                        input_args["description"],
                        input_args["recipes"],
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_cookbook(
                        input_args["name"],
                        input_args["description"],
                        input_args["recipes"],
                    )
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                # If an unexpected exception is specified, fail the test.
                assert False

    # ------------------------------------------------------------------------------
    # Test api_read_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook_id,expected_dict",
        [
            # Valid case
            (
                "sample-cookbook",
                {
                    "expected_output": {
                        "id": "sample-cookbook",
                        "name": "Sample Cookbook",
                        "description": "This is a sample cookbook",
                        "tags": [],
                        "categories": [],
                        "recipes": ["arc"],
                    }
                },
            ),
            # Invalid cases
            (
                "vanilla-cake",
                {
                    "expected_output": False,
                    "expected_error_message": "No cookbooks found with ID: vanilla-cake",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "Cookbook ID is empty.",
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
                    "expected_error_message": "No cookbooks found with ID: None",
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
    def test_api_read_cookbook(self, cookbook_id: str, expected_dict: dict):
        """
        Test the api_read_cookbook function.

        This test function is parameterized to handle multiple test cases for the api_read_cookbook function.
        It tests both valid and invalid inputs, checking for the correct output or exception as expected.

        Args:
            cookbook_id (str): The cookbook ID to read.
            expected_dict (dict): A dictionary containing the expected output or the expected error message and exception.

        Raises:
            AssertionError: If the actual output or exception does not match the expected value.
        """
        if expected_dict["expected_output"]:
            response = api_read_cookbook(cookbook_id)
            assert response == expected_dict["expected_output"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_read_cookbook(cookbook_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_read_cookbook(cookbook_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_read_cookbooks functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook_ids,expected_dict",
        [
            # Valid case
            (
                ["sample-cookbook"],
                {
                    "expected_output": [
                        {
                            "id": "sample-cookbook",
                            "name": "Sample Cookbook",
                            "description": "This is a sample cookbook",
                            "tags": [],
                            "categories": [],
                            "recipes": ["arc"],
                        }
                    ]
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "List should have at least 1 item after validation, not 0",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases
            (
                "evaluation-catalogue-cookbook",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                ["nonexistent-cookbook"],
                {
                    "expected_output": False,
                    "expected_error_message": "No cookbooks found with ID: nonexistent-cookbook",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [""],
                {
                    "expected_output": False,
                    "expected_error_message": "Cookbook ID is empty.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [None],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                ["None"],
                {
                    "expected_output": False,
                    "expected_error_message": "No cookbooks found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [{}],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [[]],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [123],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_read_cookbooks(self, cookbook_ids: list[str], expected_dict: dict):
        if expected_dict["expected_output"]:
            response = api_read_cookbooks(cookbook_ids)
            assert response == expected_dict["expected_output"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_read_cookbooks(cookbook_ids)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_read_cookbooks(cookbook_ids)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_update_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook_id,cookbook_dict,expected_dict",
        [
            # Valid case
            (
                "sample-cookbook",
                {
                    "name": "Updated Sample Cookbook",
                    "description": "This is an updated sample cookbook",
                },
                {"expected_output": True},
            ),
            # Case: Update with valid key that exists in the cookbook
            (
                "sample-cookbook",
                {
                    "name": "Another Updated Sample Cookbook",
                },
                {"expected_output": True},
            ),
            # Case: Update with multiple valid keys
            (
                "sample-cookbook",
                {
                    "name": "Another Updated Sample Cookbook",
                    "description": "A comprehensive guide to baking",
                    "recipes": ["arc"],
                },
                {"expected_output": True},
            ),
            (
                "sample-cookbook",
                {
                    "Non-existant": "12345",
                },
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-cookbook",
                {
                    "name": "Nonexistent Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Cookbook with ID 'nonexistent-cookbook' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "name": "No ID Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Cookbook with ID '' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "name": "Null ID Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "name": "String None ID Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Cookbook with ID 'None' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "name": "Dict ID Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "name": "List ID Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "name": "Numeric ID Cookbook",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid keys to update
            (
                "sample-cookbook",
                {
                    "name": None,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "sample-cookbook",
                {
                    "name": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "sample-cookbook",
                {
                    "name": [],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_cookbook(
        self, cookbook_id: str, cookbook_dict: dict, expected_dict: dict
    ):
        """
        Test the API update cookbook functionality.

        This test checks if the API update cookbook behaves as expected when provided with
        different inputs and expected outcomes. It tests for both successful updates and
        various error scenarios.

        Args:
            cookbook_id (str): The cookbook ID to update.
            cookbook_dict (dict): A dictionary containing the update data.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_cookbook(cookbook_id, **cookbook_dict)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_cookbook(cookbook_id, **cookbook_dict)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_cookbook(cookbook_id, **cookbook_dict)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_delete_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook_id,expected_dict",
        [
            # Valid case
            ("sample-cookbook", {"expected_output": True}),
            # Invalid cases
            (
                "apple-pie-cookbook",
                {
                    "expected_output": False,
                    "expected_error_message": "No cookbooks found with ID: apple-pie-cookbook",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No cookbooks found with ID: ",
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
                    "expected_error_message": "No cookbooks found with ID: None",
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
    def test_api_delete_cookbook(self, cookbook_id: str, expected_dict: dict):
        """
        Test the deletion of a cookbook.

        This test function verifies that the api_delete_cookbook function behaves as expected when provided with a cookbook ID.
        It checks if the function returns the correct response or raises the expected exceptions with the appropriate error messages.

        Args:
            cookbook_id (str): The ID of the cookbook to be deleted.
            expected_dict (dict): A dictionary containing the expected outcomes of the test, which includes:
                - 'expected_output': The expected result from the api_delete_cookbook function.
                - 'expected_error_message': The expected error message if an exception is raised.
                - 'expected_exception': The type of exception expected to be raised.

        Raises:
            AssertionError: If the actual function output or raised exception does not match the expected results.
        """
        if expected_dict["expected_output"]:
            response = api_delete_cookbook(cookbook_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_cookbook does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_cookbook(cookbook_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_cookbook(cookbook_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Unexpected exception type provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_get_all_cookbook functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_cookbook(self):
        """
        Test the api_get_all_cookbook function.

        This test ensures that api_get_all_cookbook returns a correct list of cookbooks,
        with each cookbook containing a valid 'created_date' field, which is not compared here.
        """
        expected_cookbooks = [
            {
                "description": "This is a sample cookbook",
                "id": "sample-cookbook",
                "name": "Sample Cookbook",
                "recipes": ["arc"],
                "tags": [],
                "categories": [],
            }
        ]

        actual_cookbooks = api_get_all_cookbook()
        assert len(actual_cookbooks) == len(
            expected_cookbooks
        ), "Mismatch in cookbook count."
        for cookbook in actual_cookbooks:
            assert (
                cookbook in expected_cookbooks
            ), f"Unexpected cookbook data: {cookbook}"

    # ------------------------------------------------------------------------------
    # Test api_get_all_cookbook_name functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_cookbook_name(self):
        """
        Confirm correct cookbook names are returned.

        This test checks that api_get_all_cookbook_name returns a list of the correct cookbook names.
        """
        expected_cookbook_names = ["sample-cookbook"]

        cookbook_names_response = api_get_all_cookbook_name()
        assert len(cookbook_names_response) == len(
            expected_cookbook_names
        ), "Mismatch in cookbook names count."
        for cookbook_name in cookbook_names_response:
            assert (
                cookbook_name in expected_cookbook_names
            ), f"Unexpected cookbook name: '{cookbook_name}'."
