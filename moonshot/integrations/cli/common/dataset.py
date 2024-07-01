from ast import literal_eval

import cmd2
from rich.console import Console

from moonshot.api import (
    api_create_datasets,
)

console = Console()

def add_dataset(args) -> None:
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
        "2. add_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' 'hf' \"{'dataset_name': 'cais_mmlu', 'dataset_config': 'college_biology', 'split': 'test', 'input_col': ['questions','choices'], 'target_col': 'answer'}\""
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