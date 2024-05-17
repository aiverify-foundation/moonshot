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
                "CONNECTORS": "./tests/unit-tests/src/data/connectors/",
                "CONNECTORS_ENDPOINTS": "./tests/unit-tests/src/data/connectors-endpoints/",
                "IO_MODULES": "./tests/unit-tests/src/data/io-modules/",
            }
        )

        # Perform tests
        yield

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
                    "expected_error_message": "[Storage]: No connectors_endpoints found with ID: openai",
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
                    "expected_error_message": "[Storage]: No connectors_endpoints found with ID: None",
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
        Test the api_create_connector_from_endpoint function with various endpoint IDs.

        This test checks if the api_create_connector_from_endpoint function behaves as expected when provided with
        different endpoint IDs and expected outcomes. It asserts that the function returns a Connector instance when
        expected, and raises the appropriate exceptions with the correct error messages when an error is expected.

        Args:
            self: Instance of the test class.
            ep_id (str): The endpoint ID to test the function with.
            expected_dict (dict): A dictionary containing the expected output, error message, and exception.

        Raises:
            AssertionError: If the function's output does not match the expected output or if the expected exception
                            is not raised with the correct error message.
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
                assert False, "Unexpected exception type provided in test case."

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
                    "expected_error_message": "[Storage]: No connectors_endpoints found with ID: openai",
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
                    "expected_error_message": "[Storage]: No connectors_endpoints found with ID: None",
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
                    "expected_error_message": "[Storage]: No connectors_endpoints found with ID: openai",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_api_create_connectors_from_endpoints(self, ep_id, expected_dict):
        """
        Test the api_create_connectors_from_endpoints function.

        This test checks if the api_create_connectors_from_endpoints function behaves as expected when provided with
        different endpoint IDs and expected outcomes. It tests for both successful connector creation and expected
        exceptions.

        Args:
            ep_id (str | list): The endpoint ID or list of endpoint IDs to create connectors from.
            expected_dict (dict): A dictionary containing the expected test outcomes, which includes:
                - expected_output (bool): The expected result of the function call (True if connectors are expected to be created successfully).
                - expected_error_message (str): The expected error message if an exception is raised.
                - expected_exception (str): The type of exception expected to be raised as a string.

        Raises:
            AssertionError: If the actual behavior of the function does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            insts = api_create_connectors_from_endpoints(ep_id)
            for inst in insts:
                assert isinstance(inst, Connector)
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
        Test the api_get_all_connector_type function.

        This test verifies that the api_get_all_connector_type function returns the correct list of connector types.
        """
        assert api_get_all_connector_type() == [
            "openai-connector",
            "test_connectors_file",
        ]
