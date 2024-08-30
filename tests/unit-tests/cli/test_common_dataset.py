from ast import literal_eval
import pytest
from unittest.mock import patch
from argparse import Namespace
from moonshot.integrations.cli.common.dataset import add_dataset
from _pytest.assertion import truncate
truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999

class TestCollectionCliDataset:
    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Add Dataset
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "name, description, reference, license_name, method, params, expected_output",
    [
        # Valid cases
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "csv",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: Dataset (test-dataset) created."
        ),
        (
            "test-dataset2",
            "my sample description2",
            "http://sample-reference.net",
            "BSD",
            "hf",
            "{'dataset_name': 'cais/mmlu', 'dataset_config': 'college_biology', 'split': 'test', 'input_col': ['question','choices'], 'target_col': 'answer'}",
            "[add_dataset]: Dataset (test-dataset) created."
        ),   
        (
            "test-dataset2",
            "my sample description2",
            "http://sample-reference.net",
            "BSD",
            "HF",
            "{'dataset_name': 'cais/mmlu', 'dataset_config': 'college_biology', 'split': 'test', 'input_col': ['question','choices'], 'target_col': 'answer'}",
            "[add_dataset]: Dataset (test-dataset) created."
        ),           
        # Invalid name
        (
            None,
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'name' argument must be a non-empty string and not None."
        ),
        (
            ["test-dataset"],
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'name' argument must be a non-empty string and not None."
        ),
        (
            {"test-dataset"},
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'name' argument must be a non-empty string and not None."
        ),        
        (
            123,
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'name' argument must be a non-empty string and not None."
        ),      
        (
            True,
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'name' argument must be a non-empty string and not None."
        ),         
        # invalid description
        (
            "test-dataset",
            None,
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'description' argument must be a non-empty string and not None."
        ),
        (
            "test-dataset",
            ["my sample description"],
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'description' argument must be a non-empty string and not None."
        ),
        (
            "test-dataset",
            {"my sample description"},
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'description' argument must be a non-empty string and not None."
        ),        
        (
            "test-dataset",
            123,
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'description' argument must be a non-empty string and not None."
        ),      
        (
            "test-dataset",
            True,
            "http://sample-reference.com",
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'description' argument must be a non-empty string and not None."
        ),                         
        # Invalid reference
        (
            "test-dataset",
            "my sample description",
            None,
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'reference' argument must be a non-empty string and not None."
        ),      
        (
            "test-dataset",
            "my sample description",
            ["http://sample-reference.com"],
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'reference' argument must be a non-empty string and not None."
        ),           
        (
            "test-dataset",
            "my sample description",
            {"http://sample-reference.com"},
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'reference' argument must be a non-empty string and not None."
        ),            
        (
            "test-dataset",
            "my sample description",
            123,
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'reference' argument must be a non-empty string and not None."
        ),     
        (
            "test-dataset",
            "my sample description",
            True,
            "MIT",
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'reference' argument must be a non-empty string and not None."
        ),                            
        # Invalid license
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            None,
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'license' argument must be a non-empty string and not None."
        ),        
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            ["MIT"],
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'license' argument must be a non-empty string and not None."
        ),                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            {"MIT"},
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'license' argument must be a non-empty string and not None."
        ),   
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            123,
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'license' argument must be a non-empty string and not None."
        ),     
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            True,
            "hf",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'license' argument must be a non-empty string and not None."
        ),                                     
        # Invalid method
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            None,
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            ["hf"],
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            {"hf"},
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            123,
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            True,
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                                                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            None,
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                    
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "neither hf nor csv",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                     
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "",
            "{'csv_file_path': '/path/to/your/file.csv'}",
            "[add_dataset]: The 'method' argument must be a non-empty string and not None. It must be either 'hf' or 'csv'."
        ),                                 
        # Invalid params
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "csv",
            None,
            "[add_dataset]: The 'params' argument must be a non-empty dictionary and not None."
        ),      
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "csv",
            "['csv_file_path', '/path/to/your/file.csv']",
            "[add_dataset]: The 'params' argument must be a non-empty dictionary and not None."
        ),                
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "csv",
            "['csv_file_path', '/path/to/your/file.csv']",
            "[add_dataset]: The 'params' argument must be a non-empty dictionary and not None."
        ),                        
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "csv",
            "123",
            "[add_dataset]: The 'params' argument must be a non-empty dictionary and not None."
        ),                          
        (
            "test-dataset",
            "my sample description",
            "http://sample-reference.com",
            "MIT",
            "csv",
            "True",
            "[add_dataset]: The 'params' argument must be a non-empty dictionary and not None."
        ),             
    ],
)
    @patch("moonshot.integrations.cli.common.dataset.api_create_datasets")
    def test_add_dataset(
        self,
        mock_api_create_datasets,
        name,
        description,
        reference,
        license_name,
        method,
        params,
        expected_output,
        capsys
    ):
        if "error" in expected_output:
            mock_api_create_datasets.side_effect = Exception(
                "An error has occurred while creating dataset."
            )
        else:
            mock_api_create_datasets.return_value = "test-dataset"

        args = Namespace(
            name = name, 
            description = description,
            reference = reference,
            license = license_name,
            method = method,
            params=literal_eval(params) if params is not None else None,
        )

        add_dataset(args)

        captured = capsys.readouterr()
        assert expected_output == captured.out.strip()

        if (
            name and
            isinstance(name, str)
            and description
            and isinstance(description, str)
            and reference
            and isinstance(reference, str)
            and license_name
            and isinstance(license_name, str)
            and method
            and isinstance(method, str)                        
            and (method.lower() in ["hf","csv"])
            and args.params
            and isinstance(args.params, dict)
        ):
            mock_api_create_datasets.assert_called_once_with(
                name, description, reference, license_name, method, **args.params
            )
        else:
            mock_api_create_datasets.assert_not_called()
