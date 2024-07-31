from ast import literal_eval

import cmd2
from rich.console import Console

from moonshot.api import (
    api_create_datasets,
)

console = Console()
def add_dataset(args) -> None:
    """
    Create a new dataset using the provided arguments and log the result.

    This function attempts to create a new dataset by calling the `api_create_datasets`
    function with the necessary parameters extracted from `args`. If successful, it logs
    the creation of the dataset with its ID. If an exception occurs, it logs the error.

    Args:
        args: An argparse.Namespace object containing the following attributes:
            - name (str): Name of the new dataset.
            - description (str): Description of the new dataset.
            - reference (str): Reference URL for the new dataset.
            - license (str): License type for the new dataset.
            - method (str): Method to convert the new dataset ('hf' or 'csv').
            - params (dict): Additional parameters for dataset creation.
    """
    try:
        new_dataset_id = api_create_datasets(
            args.name,
            args.description,
            args.reference,
            args.license,
            args.method,
            **args.params,
        )
        print(f"[add_dataset]: Dataset ({new_dataset_id}) created.")
    except Exception as e:
        print(f"[add_dataset]: {str(e)}")

        # ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add dataset arguments
add_dataset_args = cmd2.Cmd2ArgumentParser(
    description="Add a new dataset. The 'name' argument will be slugified to create a unique identifier.",
    epilog=(
        "Examples:\n"
        "1. add_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' 'csv' \"{'csv_file_path': '/path/to/your/file.csv'}\"\n"
        "2. add_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' 'hf' \"{'dataset_name': 'cais/mmlu', 'dataset_config': 'college_biology', 'split': 'test', 'input_col': ['question','choices'], 'target_col': 'answer'}\""
    ),
)
add_dataset_args.add_argument("name", type=str, help="Name of the new dataset")
add_dataset_args.add_argument("description", type=str, help="Description of the new dataset")
add_dataset_args.add_argument("reference", type=str, help="Reference of the new dataset")
add_dataset_args.add_argument("license", type=str, help="License of the new dataset")
add_dataset_args.add_argument("method", type=str, choices=['hf', 'csv'], help="Method to convert the new dataset. Choose either 'hf' or 'csv'.")
add_dataset_args.add_argument(
    "params", 
    type=literal_eval, 
    help=(
        "Params of the new dataset in dictionary format. For example: \n"
        "1. For 'csv' method: \"{'csv_file_path': '/path/to/your/file.csv'}\"\n"
        "2. For 'hf' method: \"{'dataset_name': 'cais_mmlu', 'dataset_config': 'college_biology', 'split': 'test', 'input_col': ['questions','choices'], 'target_col': 'answer'}\""
    )
)