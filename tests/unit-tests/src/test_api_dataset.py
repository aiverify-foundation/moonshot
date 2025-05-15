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
    api_download_dataset,
    api_convert_dataset,
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
            "tests/unit-tests/src/data/datasets/test-hf-dataset.json",
            "tests/unit-tests/src/data/datasets/test-csv-dataset.json",
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

    # ------------------------------------------------------------------------------
    # Test test_api_convert_dataset functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "dataset_details, expected_result",
        [
            # Valid cases for api_convert_dataset
            (
                {
                    "name": "Test CSV Dataset",
                    "description": "Dataset convert from csv",
                    "reference": "www.reference.com",
                    "license": "LICENSE",
                    "method": "csv",
                    "file_path": "tests/unit-tests/common/samples/sample-dataset.csv"
                },
                "tests/unit-tests/src/data/datasets/test-csv-dataset.json"
            )
        ],
    )
    def test_api_convert_dataset(self, dataset_details, expected_result):
        """
        Test the creation of datasets via the API.

        This test function simulates the creation of datasets by calling the
        api_convert_datasets function with various dataset details. It then verifies that
        the output matches the expected result.

        Args:
            dataset_details: A dictionary containing the details of the dataset to create.
            expected_result: The expected result from the api_convert_datasets call.
        """
        # Extract the common arguments
        name = dataset_details.pop('name')
        description = dataset_details.pop('description')
        reference = dataset_details.pop('reference')
        license = dataset_details.pop('license')
        file_path= dataset_details.pop('file_path')

        # Call the api_convert_dataset function with unpacked arguments
        result = api_convert_dataset(name, description, reference, license, file_path)
        # Assert that the result matches the expected result
        assert result == expected_result, f"The result '{result}' does not match the expected result '{expected_result}'."

    @pytest.mark.parametrize(
        "dataset_details, expected_result",
        [
            # Valid cases for api_download_dataset
            (
                {
                    'name': 'Test HF Dataset',
                    'description': 'Dataset convert from hf',
                    'reference': 'www.reference.com',
                    'license': 'NORMAN LICENSE',
                    'dataset_name': 'cais/mmlu',
                    'dataset_config': 'college_biology',
                    'split': 'dev',
                    'input_col': ['question', 'choices'],
                    'target_col': 'answer'
                },
                "tests/unit-tests/src/data/datasets/test-hf-dataset.json"
            )
        ],
    )
    def test_api_download_dataset(self, dataset_details, expected_result):
        """
        Test the downloading of datasets via the API.

        This test function simulates the downloading of datasets by calling the
        api_download_dataset function with various dataset details. It then verifies that
        the output matches the expected result.

        Args:
            dataset_details: A dictionary containing the details of the dataset to download.
            expected_result: The expected result from the api_download_dataset call.
        """
        # Extract the common arguments
        name = dataset_details.pop('name')
        description = dataset_details.pop('description')
        reference = dataset_details.pop('reference')
        license = dataset_details.pop('license')

        # Call the api_download_dataset function with unpacked arguments
        result = api_download_dataset(name, description, reference, license, **dataset_details)
        # Assert that the result matches the expected result
        assert result == expected_result, f"The result '{result}' does not match the expected result '{expected_result}'."