import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_create_connector_from_endpoint,
    api_create_connectors_from_endpoints,
    api_get_all_connector_type,
    api_set_environment_variables,
)
from moonshot.src.connectors.connector import Connector


class TestCollectionApiConnector:
    @pytest.fixture(autouse=True)
    def init(self):
        # Set environment variables for the test
        api_set_environment_variables(
            {
                "CONNECTORS": "tests/unit-tests/src/data/connectors/",
                "CONNECTORS_ENDPOINTS": "tests/unit-tests/src/data/connectors-endpoints/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Prepare test data by copying sample files
        shutil.copyfile(
            "tests/unit-tests/common/samples/openai-connector.py",
            "tests/unit-tests/src/data/connectors/openai-connector.py",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/openai-gpt4.json",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        )

        # Allow tests to run with the prepared environment
        yield

        # Clean up test data by removing copied files
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
    def test_api_create_connector_from_endpoint(self, ep_id, expected_dict):
        """
        Test the api_create_connector_from_endpoint function with various inputs.

        This test checks that the function correctly creates a Connector instance or raises the appropriate exceptions.

        Parameters:
            ep_id (str): The endpoint ID to test.
            expected_dict (dict): Contains 'expected_output', 'expected_error_message', and 'expected_exception'.

        Raises:
            AssertionError: If the function's behavior doesn't match expectations.
        """
        if expected_dict["expected_output"]:
            assert isinstance(api_create_connector_from_endpoint(ep_id), Connector)
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as exc_info:
                    api_create_connector_from_endpoint(ep_id)
                assert exc_info.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as exc_info:
                    api_create_connector_from_endpoint(ep_id)
                assert len(exc_info.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in exc_info.value.errors()[0]["msg"]
                )

            else:
                assert False, "Unexpected exception type"

    # ------------------------------------------------------------------------------
    # Test api_create_connectors_from_endpoints functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "ep_ids,expected_dict",
        [
            # Valid cases
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
                    "expected_output": False,
                    "expected_error_message": "List should have at least 1 item after validation, not 0",
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
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": "ValidationError",
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
    def test_api_create_connectors_from_endpoints(self, ep_ids, expected_dict):
        """
        Test the api_create_connectors_from_endpoints function with various inputs.

        This test checks that the function correctly creates Connector instances or raises the appropriate exceptions.

        Parameters:
            ep_ids (list): The list of endpoint IDs to test.
            expected_dict (dict): Contains 'expected_output', 'expected_error_message', and 'expected_exception'.

        Raises:
            AssertionError: If the function's behavior doesn't match expectations.
        """
        if expected_dict["expected_output"]:
            instances = api_create_connectors_from_endpoints(ep_ids)
            for instance in instances:
                assert isinstance(instance, Connector)
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as exc_info:
                    api_create_connectors_from_endpoints(ep_ids)
                assert exc_info.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as exc_info:
                    api_create_connectors_from_endpoints(ep_ids)
                assert len(exc_info.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in exc_info.value.errors()[0]["msg"]
                )

            else:
                assert False, "Unexpected exception type"

    # ------------------------------------------------------------------------------
    # Test api_get_all_connector_type functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_connector_type(self):
        """
        Test that api_get_all_connector_type returns the correct connector types.

        This test verifies that the list of connector types returned by the function matches the expected list.
        """
        expected_connector_types = ["openai-connector"]
        actual_connector_types = api_get_all_connector_type()
        assert (
            actual_connector_types == expected_connector_types
        ), "Expected connector types do not match actual types"
