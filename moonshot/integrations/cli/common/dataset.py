from ast import literal_eval

import cmd2
from rich.console import Console

from moonshot.api import api_convert_dataset, api_download_dataset

console = Console()


def convert_dataset(args) -> None:
    """
    Convert an existing dataset to a new format.

    Args:
        args: A namespace object from argparse with the following attributes:
            - name (str): Name of the new dataset.
            - description (str): Description of the new dataset.
            - reference (str): Reference of the new dataset.
            - license (str): License of the new dataset.
            - csv_file_path (str): Path to the existing dataset file.

    Returns:
        None
    """
    try:
        new_dataset_id = api_convert_dataset(
            args.name,
            args.description,
            args.reference,
            args.license,
            args.csv_file_path,
        )
        print(f"[convert_dataset]: Dataset ({new_dataset_id}) created.")
    except Exception as e:
        print(f"[convert_dataset]: {str(e)}")


def download_dataset(args) -> None:
    """
    Download a dataset from Hugging Face.

    Args:
        args: A namespace object from argparse with the following attributes:
            - name (str): Name of the new dataset.
            - description (str): Description of the new dataset.
            - reference (str): Reference of the new dataset.
            - license (str): License of the new dataset.
            - params (dict): Parameters for the dataset in dictionary format.

    Returns:
        None
    """
    try:
        new_dataset_id = api_download_dataset(
            args.name,
            args.description,
            args.reference,
            args.license,
            **args.params,
        )
        print(f"[download_dataset]: Dataset ({new_dataset_id}) created.")
    except Exception as e:
        print(f"[download_dataset]: {str(e)}")


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Convert dataset arguments
convert_dataset_args = cmd2.Cmd2ArgumentParser(
    description="Convert your dataset. The 'name' argument will be slugified to create a unique identifier.",
    epilog=(
        "Examples:\n"
        "convert_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' '/path/to/your/file.csv'"
    ),
)
convert_dataset_args.add_argument("name", type=str, help="Name of the new dataset")
convert_dataset_args.add_argument(
    "description", type=str, help="Description of the new dataset"
)
convert_dataset_args.add_argument(
    "reference", type=str, help="Reference of the new dataset"
)
convert_dataset_args.add_argument(
    "license", type=str, help="License of the new dataset"
)
convert_dataset_args.add_argument(
    "csv_file_path", type=str, help="Path to your existing dataset"
)


# Download dataset arguments
download_dataset_args = cmd2.Cmd2ArgumentParser(
    description="Download dataset from Hugging Face. The 'name' argument will be slugified to create a unique ID.",
    epilog=(
        "Examples:\n"
        "download_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' "
        "\"{'dataset_name': 'cais/mmlu', 'dataset_config': 'college_biology', 'split': 'dev', "
        "'input_col': ['question','choices'], 'target_col': 'answer'}\""
    ),
)
download_dataset_args.add_argument("name", type=str, help="Name of the new dataset")
download_dataset_args.add_argument(
    "description", type=str, help="Description of the new dataset"
)
download_dataset_args.add_argument(
    "reference", type=str, help="Reference of the new dataset"
)
download_dataset_args.add_argument(
    "license", type=str, help="License of the new dataset"
)
download_dataset_args.add_argument(
    "params",
    type=literal_eval,
    help=(
        "Params of the new dataset in dictionary format. For example: \n"
        "1. For 'csv' method: \"{'csv_file_path': '/path/to/your/file.csv'}\"\n"
        "2. For 'hf' method: \"{'dataset_name': 'cais_mmlu', 'dataset_config': 'college_biology', 'split': 'test', "
        "'input_col': ['questions','choices'], 'target_col': 'answer'}\""
    ),
)
