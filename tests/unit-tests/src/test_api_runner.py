import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_create_runner,
    api_delete_runner,
    api_get_all_runner,
    api_get_all_runner_name,
    api_load_runner,
    api_read_runner,
    api_set_environment_variables,
)
from moonshot.src.runners.runner import Runner


class TestCollectionApiRunner:
    @pytest.fixture(autouse=True)
    def init(self):
        # Set environment variables for result paths
        api_set_environment_variables(
            {
                "RUNNERS": "tests/unit-tests/src/data/runners/",
                "DATABASES": "tests/unit-tests/src/data/databases/",
                "DATABASES_MODULES": "tests/unit-tests/src/data/databases-modules/",
                "CONNECTORS_ENDPOINTS": "tests/unit-tests/src/data/connectors-endpoints/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy runner data
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/runners/my-new-recipe-runner.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/openai-gpt4.json",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner.db",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner.db",
        )

        # Setup complete, proceed with tests
        yield

        # Delete the run data using os.remove
        run_data_files = [
            "tests/unit-tests/src/data/runners/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner.db",
            "tests/unit-tests/src/data/runners/my-new-runner.json",
            "tests/unit-tests/src/data/databases/my-new-runner.db",
            "tests/unit-tests/src/data/runners/my-new-run-ner-1-23.json",
            "tests/unit-tests/src/data/databases/my-new-run-ner-1-23.db",
            "tests/unit-tests/src/data/runners/my-new-runner-1.json",
            "tests/unit-tests/src/data/databases/my-new-runner-1.db",
            "tests/unit-tests/src/data/runners/none.json",
            "tests/unit-tests/src/data/databases/none.db",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        ]
        for run_data_file in run_data_files:
            if os.path.exists(run_data_file):
                os.remove(run_data_file)

    # ------------------------------------------------------------------------------
    # Test api_create_runner functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, expected_dict",
        [
            # Valid case
            (
                {
                    "name": "my-new-runner",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": True,
                    "expected_id": "my-new-runner",
                    "expected_desc": "My new Runner!",
                    "expected_endpoints": ["openai-gpt4"],
                },
            ),
            (
                {
                    "name": "my new runner 1",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": True,
                    "expected_id": "my-new-runner-1",
                    "expected_desc": "My new Runner!",
                    "expected_endpoints": ["openai-gpt4"],
                },
            ),
            (
                {
                    "name": "my_new-run ner 1@.!23",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": True,
                    "expected_id": "my-new-run-ner-1-23",
                    "expected_desc": "My new Runner!",
                    "expected_endpoints": ["openai-gpt4"],
                },
            ),
            (
                {
                    "name": "None",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": True,
                    "expected_id": "none",
                    "expected_desc": "My new Runner!",
                    "expected_endpoints": ["openai-gpt4"],
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": "",
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": True,
                    "expected_id": "my-new-runner",
                    "expected_desc": "",
                    "expected_endpoints": ["openai-gpt4"],
                },
            ),
            # Invalid cases for name
            (
                {
                    "name": "",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": False,
                    "expected_id": "",
                    "expected_error_message": "Runner name must not be empty.",
                    "expected_exception": "ValueError",
                },
            ),
            (
                {
                    "name": None,
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
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
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
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
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
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
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4"],
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
                    "name": "my-new-runner",
                    "description": None,
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": [],
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": {},
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": 123,
                    "endpoints": ["openai-gpt4"],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for endpoints
            (
                {
                    "name": "my-new-runner",
                    "description": "My new Runner!",
                    "endpoints": "",
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": "My new Runner!",
                    "endpoints": None,
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4", 123],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-runner",
                    "description": "My new Runner!",
                    "endpoints": ["openai-gpt4", ""],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-runner",
                    "expected_error_message": "Endpoints must be a non-empty list of strings.",
                    "expected_exception": "ValueError",
                },
            ),
        ],
    )
    def test_api_create_runner(self, input_args, expected_dict):
        """
        Test the api_create_runner function with various input arguments and expected outcomes.

        This test uses parametrized input arguments and expected dictionaries to validate both successful
        runner creation and proper handling of invalid inputs through exceptions.

        Args:
            input_args (dict): A dictionary containing the input parameters to the api_create_runner function.
            expected_dict (dict): A dictionary containing the expected result of the test case. This includes
                                  the expected output, expected ID, expected error message, and expected exception.

        The test cases include:
        - Valid cases with proper input arguments that should result in successful runner creation.
        - Invalid cases with improper input arguments that should raise specific exceptions with appropriate error messages.
        """
        if expected_dict["expected_output"]:
            # Test valid cases where runner creation should succeed.
            runner_instance = api_create_runner(
                input_args["name"],
                input_args["endpoints"],
                input_args["description"],
            )
            assert isinstance(runner_instance, Runner)
            assert runner_instance.id == expected_dict["expected_id"]
            assert runner_instance.description == expected_dict["expected_desc"]
            assert runner_instance.endpoints == expected_dict["expected_endpoints"]
        else:
            # Test invalid cases where runner creation should fail and raise an exception.
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_runner(
                        input_args["name"],
                        input_args["endpoints"],
                        input_args["description"],
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_runner(
                        input_args["name"],
                        input_args["endpoints"],
                        input_args["description"],
                    )
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            elif expected_dict["expected_exception"] == "ValueError":
                with pytest.raises(ValueError) as e:
                    api_create_runner(
                        input_args["name"],
                        input_args["endpoints"],
                        input_args["description"],
                    )
                assert expected_dict["expected_error_message"] in str(e.value)

            else:
                # If an unexpected exception is specified, fail the test.
                assert False

    # ------------------------------------------------------------------------------
    # Test api_load_runner functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,progress_callback_func,expected_dict",
        [
            # Valid case
            (
                "my-new-recipe-runner",
                None,
                {
                    "expected_output": True,
                    "id": "my-new-recipe-runner",
                    "name": "my new recipe runner",
                    "database_file": "data/generated-outputs/databases/my-new-recipe-runner.db",
                    "endpoints": ["openai-gpt35-turbo"],
                    "description": "",
                },
            ),
            # Invalid cases
            # Runner Id
            (
                "vanilla-cake",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Progress callback func
            (
                "my-new-recipe-runner",
                "my-vanilla-cake",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be callable",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-new-recipe-runner",
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be callable",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-new-recipe-runner",
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be callable",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-new-recipe-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be callable",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-new-recipe-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be callable",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-new-recipe-runner",
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be callable",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_load_runner(self, runner_id, progress_callback_func, expected_dict):
        if expected_dict["expected_output"]:
            runner_instance = api_load_runner(runner_id, progress_callback_func)
            assert isinstance(runner_instance, Runner)
            assert runner_instance.id == expected_dict["id"]
            assert runner_instance.name == expected_dict["name"]
            assert runner_instance.description == expected_dict["description"]
            assert runner_instance.database_file == expected_dict["database_file"]
            assert runner_instance.endpoints == expected_dict["endpoints"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_load_runner(runner_id, progress_callback_func)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_load_runner(runner_id, progress_callback_func)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_read_runner functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,expected_dict",
        [
            # Valid case
            (
                "my-new-recipe-runner",
                {
                    "expected_output": {
                        "id": "my-new-recipe-runner",
                        "name": "my new recipe runner",
                        "database_file": "data/generated-outputs/databases/my-new-recipe-runner.db",
                        "endpoints": ["openai-gpt35-turbo"],
                        "description": "",
                    }
                },
            ),
            # Invalid cases
            (
                "vanilla-cake",
                {
                    "expected_output": False,
                    "expected_error_message": "No runners found with ID: vanilla-cake",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "Runner ID is empty.",
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
                    "expected_error_message": "No runners found with ID: None",
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
    def test_api_read_runner(self, runner_id: str, expected_dict: dict):
        """
        Test the api_read_runner function with various inputs and expected outcomes.

        This test checks if the api_read_runner function returns the correct response
        or raises the expected exceptions based on the input runner_id and the
        expected outcome defined in expected_dict.

        Args:
            runner_id (str): The runner ID to be used for retrieving the runner information.
            expected_dict (dict): A dictionary containing keys 'expected_output',
                                  'expected_error_message', and 'expected_exception'
                                  which define the expected outcome of the test.

        Raises:
            AssertionError: If the api_read_runner response does not match the
                            expected output or if the expected exception is not raised
                            with the correct error message.
        """
        if expected_dict["expected_output"]:
            response = api_read_runner(runner_id)
            assert response == expected_dict["expected_output"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_read_runner(runner_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_read_runner(runner_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_delete_runner functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,expected_dict",
        [
            # Valid case
            ("my-new-recipe-runner", {"expected_output": True}),
            # Invalid cases
            (
                "apple-pie",
                {
                    "expected_output": False,
                    "expected_error_message": "No runners found with ID: apple-pie",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No runners found with ID: ",
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
                    "expected_error_message": "No runners found with ID: None",
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
    def test_api_delete_runner(self, runner_id: str, expected_dict: dict):
        """
        Test the deletion of a runner.

        This test function verifies that the api_delete_runner function behaves as expected when provided with a runner ID.
        It checks if the function returns the correct response or raises the expected exceptions with the appropriate error messages.

        Args:
            runner_id (str): The ID of the runner to be deleted.
            expected_dict (dict): A dictionary containing the expected outcomes of the test, which includes:
                - 'expected_output': The expected result from the api_delete_runner function.
                - 'expected_error_message': The expected error message if an exception is raised.
                - 'expected_exception': The type of exception expected to be raised.

        Raises:
            AssertionError: If the actual function output or raised exception does not match the expected results.
        """
        if expected_dict["expected_output"]:
            response = api_delete_runner(runner_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_runner does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_runner(runner_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_runner(runner_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_get_all_runner functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_runner(self):
        """
        Test the api_get_all_runner function.

        This test ensures that the api_get_all_runner function returns a list of runners that matches the expected runners list.
        Each runner in the returned list is checked against the expected runners to ensure that all details are correct.
        """
        expected_runners = [
            {
                "id": "my-new-recipe-runner",
                "name": "my new recipe runner",
                "database_file": "data/generated-outputs/databases/my-new-recipe-runner.db",
                "endpoints": ["openai-gpt35-turbo"],
                "description": "",
            }
        ]

        actual_runners = api_get_all_runner()
        assert len(actual_runners) == len(
            expected_runners
        ), "The number of runners returned does not match the expected count."

        for runner in actual_runners:
            assert (
                runner in expected_runners
            ), f"The runner data {runner} does not match any expected runner."

    # ------------------------------------------------------------------------------
    # Test api_get_all_runner_name functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_runner_name(self):
        """
        Test the api_get_all_runner_name function.

        This test ensures that the api_get_all_runner_name function returns a list containing the correct runner names.
        """
        expected_runner_names = ["my-new-recipe-runner"]

        runner_names_response = api_get_all_runner_name()
        assert len(runner_names_response) == len(
            expected_runner_names
        ), "The number of runner names returned does not match the expected count."
        for runner_name in runner_names_response:
            assert (
                runner_name in expected_runner_names
            ), f"Runner name '{runner_name}' is not in the list of expected runner names."
