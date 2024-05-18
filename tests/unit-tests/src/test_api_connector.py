import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.src.api.api_connector import (
    api_create_connector_from_endpoint,
    api_create_connectors_from_endpoints,
    api_get_all_connector_type,
)
from moonshot.src.api.api_environment_variables import api_set_environment_variables
from moonshot.src.connectors.connector import Connector


class TestCollectionApiConnector:
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

        # Copy endpoint and connector
        shutil.copyfile(
            "tests/unit-tests/src/data/samples/openai-connector.py",
            "tests/unit-tests/src/data/connectors/openai-connector.py",
        )
        shutil.copyfile(
            "tests/unit-tests/src/data/samples/openai-gpt4.json",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        )

        # Perform tests
        yield

        # Delete the endpoint using os.remove
        endpoint_paths = [
            "tests/unit-tests/src/data/connectors/openai-connector.py",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        ]
        for endpoint_path in endpoint_paths:
            if os.path.exists(endpoint_path):
                os.remove(endpoint_path)

    # ------------------------------------------------------------------------------
    # Test api_create_connector_from_endpoint functionality
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
                    "expected_error_message": "No connectors_endpoints found with ID: ",
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
    def test_api_create_connector_from_endpoint(self, ep_id, expected_dict):
        """
        Validate the behavior of the api_create_connector_from_endpoint function.

        This test ensures that the api_create_connector_from_endpoint function conforms to expectations when given
        various endpoint IDs. It verifies that a Connector instance is returned when anticipated, and that the correct
        exceptions are thrown with the appropriate error messages when an error condition is encountered.

        Parameters:
            ep_id (str): The endpoint ID for testing the function.
            expected_dict (dict): A dictionary with keys 'expected_output', 'expected_error_message', and 'expected_exception'
                                  detailing the expected results of the test.

        Raises:
            AssertionError: The actual function output or raised exception does not align with the expected results.
        """
        if expected_dict["expected_output"]:
            assert isinstance(api_create_connector_from_endpoint(ep_id), Connector)
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_connector_from_endpoint(ep_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_connector_from_endpoint(ep_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_create_connectors_from_endpoints functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_id,expected_dict",
        [
            # Valid case
            (["openai-gpt4"], {"expected_output": True}),
            (["openai-gpt4", "openai-gpt4"], {"expected_output": True}),
            # Invalid cases
            (
                "openai",
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
                [],
                {
                    "expected_output": True,
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
                ["openai"],
                {
                    "expected_output": False,
                    "expected_error_message": "No connectors_endpoints found with ID: openai",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [""],
                {
                    "expected_output": False,
                    "expected_error_message": "No connectors_endpoints found with ID: ",
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
                    "expected_error_message": "No connectors_endpoints found with ID: None",
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
            (
                ["openai-gpt4", "openai"],
                {
                    "expected_output": False,
                    "expected_error_message": "No connectors_endpoints found with ID: openai",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_api_create_connectors_from_endpoints(self, ep_id, expected_dict):
        """
        Validates the behavior of api_create_connectors_from_endpoints with various inputs.

        This test ensures that the api_create_connectors_from_endpoints function performs as expected when given
        different endpoint IDs. It checks for successful connector creation and the correct handling of exceptions.

        Parameters:
            ep_id (str | list): The endpoint ID or a list of endpoint IDs for connector creation.
            expected_dict (dict): A dictionary with the expected outcomes of the test, containing:
                - expected_output (bool): The anticipated result of the function call (True if successful creation of connectors is expected).
                - expected_error_message (str): The error message expected if an exception occurs.
                - expected_exception (str): The name of the expected exception as a string.

        Raises:
            AssertionError: If the function's actual behavior does not align with the expected outcome.
        """
        if expected_dict["expected_output"]:
            instances = api_create_connectors_from_endpoints(ep_id)
            for instance in instances:
                assert isinstance(instance, Connector)
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_connectors_from_endpoints(ep_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_connectors_from_endpoints(ep_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_get_all_connector_type() functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_connector_type(self):
        """
        Verify that the api_get_all_connector_type function returns the expected connector types.

        This unit test checks that the list of connector types returned by the api_get_all_connector_type function
        matches the expected list of connector types known to be available in the system.
        """
        expected_connector_types = ["openai-connector"]
        actual_connector_types = api_get_all_connector_type()
        assert (
            actual_connector_types == expected_connector_types
        ), f"Expected connector types {expected_connector_types}, but got {actual_connector_types}"
