import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_delete_metric,
    api_get_all_metric,
    api_get_all_metric_name,
    api_set_environment_variables,
)


class TestCollectionApiMetric:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "METRICS": "tests/unit-tests/src/data/metrics/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy metric
        shutil.copyfile(
            "tests/unit-tests/common/samples/advglue.py",
            "tests/unit-tests/src/data/metrics/advglue.py",
        )

        # Perform tests
        yield

        # Delete the metric using os.remove
        metrics = [
            "tests/unit-tests/src/data/metrics/advglue.py",
            "tests/unit-tests/src/data/metrics/cache.json",
            "tests/unit-tests/src/data/metrics/metrics_config.json",
        ]
        for metric in metrics:
            if os.path.exists(metric):
                os.remove(metric)

    # ------------------------------------------------------------------------------
    # Test api_get_all_metrics functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_metric(self):
        detected_metrics = [
            {
                "id": "advglue",
                "name": "Attack Success Rate",
                "description": "Attack success rate measures how successful a changed prompt performs. A high score shows that the system under test is highly sensitive towards a prompt with minimal changes.",
            }
        ]

        metrics = api_get_all_metric()
        assert len(metrics) == len(
            detected_metrics
        ), "The number of metrics does not match the expected count."

        for metric in metrics:
            assert (
                metric in detected_metrics
            ), f"The metric '{metric}' was not found in the list of detected metrics."

    # ------------------------------------------------------------------------------
    # Test api_delete_metric functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "metric_id,expected_dict",
        [
            # Valid case
            ("advglue", {"expected_output": True}),
            # Invalid cases
            (
                "unknown_metric",
                {
                    "expected_output": False,
                    "expected_error_message": "No metrics found with ID: unknown_metric",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No metrics found with ID: ",
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
                    "expected_error_message": "No metrics found with ID: None",
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
    def test_api_delete_metric(self, metric_id, expected_dict):
        """
        Test the deletion of a metric via the API.

        This test function simulates the deletion of a metric by calling the
        api_delete_metric function with a given metric_id. It then verifies that
        the output or exception raised matches the expected result as defined in
        expected_dict.

        Args:
            metric_id: The ID of the metric to delete.
            expected_dict: A dictionary containing the following keys:
                - "expected_output": The expected result from the api_delete_metric call.
                - "expected_error_message": The expected error message for exceptions.
                - "expected_exception": The type of exception expected to be raised.

        Raises:
            AssertionError: If the actual response or exception does not match the expected.
        """
        if expected_dict["expected_output"]:
            response = api_delete_metric(metric_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_metric does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_metric(metric_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_metric(metric_id)
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

    def test_api_get_all_metric_name(self):
        """
        Test the api_get_all_metric_name function.

        This test ensures that the api_get_all_metric_name function returns a list containing the correct metric names.
        """
        expected_metrics = ["advglue"]

        metric_names_response = api_get_all_metric_name()
        assert len(metric_names_response) == len(
            expected_metrics
        ), "The number of metric names returned does not match the expected count."
        for metric_name in metric_names_response:
            assert (
                metric_name in expected_metrics
            ), f"Metric name '{metric_name}' is not in the list of expected metric names."
