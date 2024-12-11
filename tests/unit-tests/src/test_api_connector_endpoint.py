import os
import shutil
from datetime import datetime

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_create_endpoint,
    api_delete_endpoint,
    api_get_all_endpoint,
    api_get_all_endpoint_name,
    api_read_endpoint,
    api_set_environment_variables,
    api_update_endpoint,
)


class TestCollectionApiConnectorEndpoint:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "CONNECTORS": "tests/unit-tests/src/data/connectors/",
                "CONNECTORS_ENDPOINTS": "tests/unit-tests/src/data/connectors-endpoints/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy endpoint
        shutil.copyfile(
            "tests/unit-tests/common/samples/openai-gpt4.json",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        )

        # Perform tests
        yield

        # Delete the endpoint using os.remove
        endpoint_paths = [
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
            "tests/unit-tests/src/data/connectors-endpoints/my-new-end-point-1-23.json",
            "tests/unit-tests/src/data/connectors-endpoints/my-new-endpoint-1.json",
            "tests/unit-tests/src/data/connectors-endpoints/my-new-endpoint.json",
        ]
        for endpoint_path in endpoint_paths:
            if os.path.exists(endpoint_path):
                os.remove(endpoint_path)

    # ------------------------------------------------------------------------------
    # Test api_create_endpoint functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, expected_dict",
        [
            # Valid case
            (
                {
                    "name": "my-new-endpoint",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {"expected_output": True, "expected_id": "my-new-endpoint"},
            ),
            (
                {
                    "name": "my new endpoint 1",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {"expected_output": True, "expected_id": "my-new-endpoint-1"},
            ),
            (
                {
                    "name": "my_new-end point 1@.!23",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {"expected_output": True, "expected_id": "my-new-end-point-1-23"},
            ),
            # Invalid cases
            (
                {
                    "name": "",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "Name",
                    "connector_type": "OpenAIConnector",
                    "uri": None,
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "Name",
                    "connector_type": "OpenAIConnector",
                    "uri": {},
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "Name",
                    "connector_type": "OpenAIConnector",
                    "uri": [],
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "Name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": None,
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "Name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": {},
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "Name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": [],
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 0,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be greater than 0",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": -1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be greater than 0",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": 123,
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": None,
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
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
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
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
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": [],
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": None,
                    "params": {"temperature": "0.5"},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": [],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": "",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "valid-name",
                    "connector_type": "OpenAIConnector",
                    "uri": "",
                    "token": "",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-4-turbo",
                    "params": None,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_create_endpoint(self, input_args, expected_dict):
        """
        Test the api_create_endpoint function with various input arguments and expected outcomes.

        This test uses parametrized input arguments and expected dictionaries to validate both successful
        endpoint creation and proper handling of invalid inputs through exceptions.

        Args:
            input_args (dict): A dictionary containing the input parameters to the api_create_endpoint function.
            expected_dict (dict): A dictionary containing the expected result of the test case. This includes
                                  the expected output, expected ID, expected error message, and expected exception.

        The test cases include:
        - Valid cases with proper input arguments that should result in successful endpoint creation.
        - Invalid cases with improper input arguments that should raise specific exceptions with
          appropriate error messages.
        """
        if expected_dict["expected_output"]:
            # Test valid cases where endpoint creation should succeed.
            assert (
                api_create_endpoint(
                    input_args["name"],
                    input_args["connector_type"],
                    input_args["uri"],
                    input_args["token"],
                    input_args["max_calls_per_second"],
                    input_args["max_concurrency"],
                    input_args["model"],
                    input_args["params"],
                )
                == expected_dict["expected_id"]
            )
        else:
            # Test invalid cases where endpoint creation should fail and raise an exception.
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_endpoint(
                        input_args["name"],
                        input_args["connector_type"],
                        input_args["uri"],
                        input_args["token"],
                        input_args["max_calls_per_second"],
                        input_args["max_concurrency"],
                        input_args["model"],
                        input_args["params"],
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_endpoint(
                        input_args["name"],
                        input_args["connector_type"],
                        input_args["uri"],
                        input_args["token"],
                        input_args["max_calls_per_second"],
                        input_args["max_concurrency"],
                        input_args["model"],
                        input_args["params"],
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
    # Test api_read_endpoint functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_id,expected_dict",
        [
            # Valid case
            (
                "openai-gpt4",
                {
                    "expected_output": {
                        "id": "openai-gpt4",
                        "name": "OpenAI GPT4",
                        "connector_type": "openai-connector",
                        "uri": "",
                        "token": "",
                        "max_calls_per_second": 100,
                        "max_concurrency": 100,
                        "model": "gpt-4",
                        "params": {
                            "timeout": 300,
                            "max_attempts": 3,
                            "temperature": 0.5,
                        },
                    }
                },
            ),
            # Invalid cases
            (
                "openai",
                {
                    "expected_output": False,
                    "expected_error_message": "No connectors_endpoints found with ID: openai",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": "ValidationError",
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
                    "expected_error_message": "No connectors_endpoints found with ID: None",
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
    def test_api_read_endpoint(self, ep_id: str, expected_dict: dict):
        """
        Test the api_read_endpoint function.

        This test function is parameterized to handle multiple test cases for the api_read_endpoint function.
        It tests both valid and invalid inputs, checking for the correct output or exception as expected.

        Args:
            ep_id (str): The endpoint ID to read.
            expected_dict (dict): A dictionary containing the expected output or the expected error message
                                  and exception.

        Raises:
            AssertionError: If the actual output or exception does not match the expected value.
        """
        if expected_dict["expected_output"]:
            response = api_read_endpoint(ep_id)
            # Check if 'created_date' is a valid date
            try:
                created_date = datetime.strptime(
                    response["created_date"], "%Y-%m-%d %H:%M:%S"
                )
                assert isinstance(created_date, datetime)
            except ValueError:
                assert False, "created_date is not a valid date"
            # Exclude 'created_date' from comparison for the rest of the test
            response.pop("created_date", None)
            assert response == expected_dict["expected_output"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_read_endpoint(ep_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_read_endpoint(ep_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_update_endpoint functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_id,ep_dict,expected_dict",
        [
            # Valid case
            (
                "openai-gpt4",
                {
                    "name": "helloworld",
                },
                {"expected_output": True},
            ),
            # Case: Update with valid key that exists on the endpoint
            (
                "openai-gpt4",
                {
                    "name": "Updated OpenAI GPT4",
                },
                {"expected_output": True},
            ),
            # Case: Update with multiple valid keys
            (
                "openai-gpt4",
                {
                    "name": "Updated OpenAI GPT4",
                    "max_calls_per_second": 200,
                    "max_concurrency": 200,
                },
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "openai",
                {
                    "name": "helloworld",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "[api_update_endpoint]: Endpoint with ID 'openai' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "name": "helloworld",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "[api_update_endpoint]: Endpoint with ID '' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "name": "helloworld",
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
                    "name": "helloworld",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "[api_update_endpoint]: Endpoint with ID 'None' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "name": "helloworld",
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
                    "name": "helloworld",
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
                    "name": "helloworld",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid keys to update
            (
                "openai-gpt4",
                {
                    "name1234": "OpenAI GPT4",
                },
                {"expected_output": True},
            ),
            # Case: Update with a key that does not exist on the endpoint
            (
                "openai-gpt4",
                {
                    "nonexistent_key": "value",
                },
                {"expected_output": True},
            ),
            (
                "openai-gpt4",
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
                "openai-gpt4",
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
                "openai-gpt4",
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
    def test_api_update_endpoint(self, ep_id: str, ep_dict: dict, expected_dict: dict):
        """
        Test the API update endpoint functionality.

        This test checks if the API update endpoint behaves as expected when provided with
        different inputs and expected outcomes. It tests for both successful updates and
        various error scenarios.

        Args:
            ep_id (str): The endpoint ID to update.
            ep_dict (dict): A dictionary containing the update data.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_endpoint(ep_id, **ep_dict)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_endpoint(ep_id, **ep_dict)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_endpoint(ep_id, **ep_dict)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_delete_endpoint functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_id,expected_dict",
        [
            # Valid case
            ("openai-gpt4", {"expected_output": True}),
            # Invalid cases
            (
                "openai",
                {
                    "expected_output": False,
                    "expected_error_message": "No connectors_endpoints found with ID: openai",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": "ValidationError",
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
                    "expected_error_message": "No connectors_endpoints found with ID: None",
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
    def test_api_delete_endpoint(self, ep_id: str, expected_dict: dict):
        """
        Test the deletion of an API endpoint.

        This test function verifies that the api_delete_endpoint function behaves as expected when provided
        with an endpoint ID.

        It checks if the function returns the correct response or raises the expected exceptions with the
        appropriate error messages.

        Args:
            ep_id (str): The ID of the endpoint to be deleted.
            expected_dict (dict): A dictionary containing the expected outcomes of the test, which includes:
                - 'expected_output': The expected result from the api_delete_endpoint function.
                - 'expected_error_message': The expected error message if an exception is raised.
                - 'expected_exception': The type of exception expected to be raised.

        Raises:
            AssertionError: If the actual function output or raised exception does not match the expected results.
        """
        if expected_dict["expected_output"]:
            response = api_delete_endpoint(ep_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_endpoint does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_endpoint(ep_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_endpoint(ep_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            elif expected_dict["expected_exception"] == "ValueError":
                with pytest.raises(ValueError) as e:
                    api_delete_endpoint(ep_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_get_all_endpoint functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_endpoint(self):
        """
        Test the api_get_all_endpoint function.

        This test verifies that the api_get_all_endpoint function returns the correct list of endpoints,
        and that each endpoint has a valid 'created_date' field. The 'created_date' field is not compared
        in the endpoint data comparison.
        """
        expected_endpoints = [
            {
                "id": "openai-gpt4",
                "name": "OpenAI GPT4",
                "connector_type": "openai-connector",
                "uri": "",
                "token": "",
                "max_calls_per_second": 100,
                "max_concurrency": 100,
                "model": "gpt-4",
                "params": {"timeout": 300, "max_attempts": 3, "temperature": 0.5},
            }
        ]

        actual_endpoints = api_get_all_endpoint()
        assert len(actual_endpoints) == len(
            expected_endpoints
        ), "The number of endpoints returned does not match the expected count."

        for endpoint in actual_endpoints:
            # Check if 'created_date' is a valid date
            assert (
                "created_date" in endpoint
            ), "The 'created_date' field is missing from the endpoint data."
            try:
                created_date = datetime.strptime(
                    endpoint["created_date"], "%Y-%m-%d %H:%M:%S"
                )
                assert isinstance(
                    created_date, datetime
                ), "The 'created_date' field is not a valid datetime."
            except ValueError:
                assert (
                    False
                ), "The 'created_date' field does not match the expected format '%Y-%m-%d %H:%M:%S'."

            # Exclude 'created_date' from comparison for the rest of the test
            endpoint_without_date = {
                key: value for key, value in endpoint.items() if key != "created_date"
            }

            assert (
                endpoint_without_date in expected_endpoints
            ), f"The endpoint data {endpoint_without_date} does not match any expected endpoint."

    # ------------------------------------------------------------------------------
    # Test api_get_all_endpoint_name functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_endpoint_name(self):
        """
        Test the api_get_all_endpoint_name function.

        This test ensures that the api_get_all_endpoint_name function returns a list containing
        the correct endpoint names.
        """
        detected_endpoints = ["openai-gpt4"]

        endpoint_response = api_get_all_endpoint_name()
        assert len(endpoint_response) == len(
            detected_endpoints
        ), "The number of endpoints returned does not match the expected count."
        for endpoint in endpoint_response:
            assert (
                endpoint in detected_endpoints
            ), f"Endpoint '{endpoint}' is not in the list of detected endpoints."
