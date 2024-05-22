import os
import shutil
from datetime import datetime

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_delete_dataset,
    api_get_all_datasets,
    api_get_all_datasets_name,
    api_set_environment_variables,
)


class TestCollectionApiDataset:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "DATASETS": "tests/unit-tests/src/data/datasets/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy dataset
        shutil.copyfile(
            "tests/unit-tests/common/samples/arc-easy.json",
            "tests/unit-tests/src/data/datasets/arc-easy.json",
        )

        # Perform tests
        yield

        # Delete the dataset using os.remove
        datasets = [
            "tests/unit-tests/src/data/datasets/arc-easy.json",
            "tests/unit-tests/src/data/datasets/cache.json",
            "tests/unit-tests/src/data/datasets/datasets_config.json",
        ]
        for dataset in datasets:
            if os.path.exists(dataset):
                os.remove(dataset)

    # ------------------------------------------------------------------------------
    # Test api_get_all_datasets functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_datasets(self):
        detected_datasets = [
            {
                "id": "arc-easy",
                "name": "ARC-Easy",
                "description": "A dataset of genuine grade-school level, multiple-choice science questions in advanced Q&A. This is the easy set.",
                "license": "CC BY-SA",
                "reference": "https://allenai.org/data/arc",
                "examples": None,
                "num_of_dataset_prompts": 1,
            }
        ]

        datasets = api_get_all_datasets()
        assert len(datasets) == len(
            detected_datasets
        ), "The number of datasets does not match the expected count."

        for dataset in datasets:
            # Check if 'created_date' is a valid date
            try:
                created_date = datetime.strptime(
                    dataset["created_date"], "%Y-%m-%d %H:%M:%S"
                )
                assert isinstance(created_date, datetime)
            except ValueError:
                assert False, "created_date is not a valid date"
            # Exclude 'created_date' from comparison for the rest of the test
            dataset.pop("created_date", None)
            assert (
                dataset in detected_datasets
            ), f"The dataset '{dataset}' was not found in the list of detected datasets."

    # ------------------------------------------------------------------------------
    # Test api_delete_dataset functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "dataset_id,expected_dict",
        [
            # Valid case
            ("arc-easy", {"expected_output": True}),
            # Invalid cases
            (
                "unknown_dataset",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: unknown_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: ",
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
                    "expected_error_message": "No datasets found with ID: None",
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
    def test_api_delete_dataset(self, dataset_id, expected_dict):
        """
        Test the deletion of a dataset via the API.

        This test function simulates the deletion of a dataset by calling the
        api_delete_dataset function with a given dataset_id. It then verifies that
        the output or exception raised matches the expected result as defined in
        expected_dict.

        Args:
            dataset_id: The ID of the dataset to delete.
            expected_dict: A dictionary containing the following keys:
                - "expected_output": The expected result from the api_delete_dataset call.
                - "expected_error_message": The expected error message for exceptions.
                - "expected_exception": The type of exception expected to be raised.

        Raises:
            AssertionError: If the actual response or exception does not match the expected.
        """
        if expected_dict["expected_output"]:
            response = api_delete_dataset(dataset_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_dataset does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_dataset(dataset_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_dataset(dataset_id)
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

    def test_api_get_all_datasets_name(self):
        """
        Test the api_get_all_datasets_name function.

        This test ensures that the api_get_all_datasets_name function returns a list containing the correct dataset names.
        """
        expected_datasets = ["arc-easy"]

        dataset_names_response = api_get_all_datasets_name()
        assert len(dataset_names_response) == len(
            expected_datasets
        ), "The number of dataset names returned does not match the expected count."
        for dataset_name in dataset_names_response:
            assert (
                dataset_name in expected_datasets
            ), f"Dataset name '{dataset_name}' is not in the list of expected dataset names."
