import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from moonshot.src.storage.storage import Storage
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.api import api_set_environment_variables

@pytest.fixture(autouse=True)
def init():
    api_set_environment_variables(
        {
            "DATASETS": "tests/unit-tests/src/data/datasets/",
            "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
        }
    )

    yield 

    # Delete files after testing
    run_data_files = [
            Path("tests/unit-tests/src/data/datasets/sample-dataset.json"),
        ]

    for run_data_file in run_data_files:
        if run_data_file.exists():
            run_data_file.unlink()

@pytest.fixture
def mock_get_instance():
    with patch('moonshot.src.storage.storage.get_instance') as mock:
        yield mock

def test_create_object_with_iterator(mock_get_instance):
        # Example data and iterator
        obj_type = EnvVariables.DATASETS.name
        obj_id = "sample-dataset"
        obj_info = {
            "id": "sample-dataset",
            "name": "sample dataset",
            "description": "test description",
            "reference": "reference",
            "license": "license"
        }
        obj_extension = "json"
        obj_mod_type = "jsonio"
        iterator_keys = ["examples"]
        iterator_data = iter([
            {"input": "The cat sat on the mat.", "target": "A"},
            {"input": "The dog sat on the log.", "target": "B"},
            {"input": "The bird flew in the sky.", "target": "C"},
            {"input": "The fish swam in the sea.", "target": "D"},
            {"input": "The horse galloped across the field.", "target": "E"},
            {"input": "The cow grazed in the meadow.", "target": "F"},
            {"input": "The mouse ran into the hole.", "target": "G"},
            {"input": "The rabbit hopped in the garden.", "target": "H"},
            {"input": "The snake slithered in the grass.", "target": "I"},
            {"input": "The frog jumped into the pond.", "target": "J"}
        ])

        # Expected JSON content
        expected_json = {
            "id": "sample-dataset",
            "name": "sample dataset",
            "description": "test description",
            "reference": "reference",
            "license": "license",
            "examples": [
                {"input": "The cat sat on the mat.", "target": "A"},
                {"input": "The dog sat on the log.", "target": "B"},
                {"input": "The bird flew in the sky.", "target": "C"},
                {"input": "The fish swam in the sea.", "target": "D"},
                {"input": "The horse galloped across the field.", "target": "E"},
                {"input": "The cow grazed in the meadow.", "target": "F"},
                {"input": "The mouse ran into the hole.", "target": "G"},
                {"input": "The rabbit hopped in the garden.", "target": "H"},
                {"input": "The snake slithered in the grass.", "target": "I"},
                {"input": "The frog jumped into the pond.", "target": "J"}
            ]
        }

        # Mock the get_instance function to return a mock object with the create_file_with_iterator method
        mock_instance = MagicMock()
        mock_instance.create_file_with_iterator = MagicMock()
        mock_get_instance.return_value = lambda _: mock_instance
        # Mock the create_file_with_iterator method to write to a temporary file
        def mock_create_file_with_iterator(obj_info, iterator_keys, iterator_data):
            file_path = os.path.join("tests/unit-tests/src/data/datasets", f"{obj_id}.{obj_extension}")
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(expected_json, json_file)
            print(file_path)
            return file_path

        mock_instance.create_file_with_iterator.side_effect = mock_create_file_with_iterator

        # Call the function
        written_path = Storage.create_object_with_iterator(
            obj_type, obj_id, obj_info, obj_extension, obj_mod_type, iterator_keys, iterator_data
        )
        print(written_path)
        # Verify that the create_file_with_iterator method was called with the correct arguments
        mock_instance.create_file_with_iterator.assert_called_once_with(
            obj_info, iterator_keys, iterator_data
        )

        # Verify the file path
        assert os.path.exists(written_path), f"File was not created at {written_path}"

        # Read the newly created JSON file
        with open(written_path, "r", encoding="utf-8") as json_file:
            result_json = json.load(json_file)
        
        # Compare the result with the expected JSON
        assert result_json == expected_json, "The JSON content does not match the expected content."