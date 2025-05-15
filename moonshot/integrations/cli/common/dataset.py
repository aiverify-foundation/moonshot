from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_convert_dataset,
    api_delete_dataset,
    api_download_dataset,
    api_get_all_datasets,
    api_get_all_datasets_name,
)
from moonshot.integrations.cli.cli_errors import (
    ERROR_BENCHMARK_DELETE_DATASET_DATASET_VALIDATION,
    ERROR_BENCHMARK_LIST_DATASETS_FIND_VALIDATION,
    ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION,
    ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION_1,
    ERROR_BENCHMARK_VIEW_DATASET_DATASET_FILENAME_VALIDATION,
)
from moonshot.integrations.cli.common.display_helper import display_view_str_format
from moonshot.integrations.cli.utils.process_data import filter_data

console = Console()


def list_datasets(args) -> list | None:
    """
    List all available datasets.

    This function retrieves all available datasets by calling the api_get_all_datasets function from the
    moonshot.api module. It then filters the datasets based on the provided keyword and pagination arguments.
    If there are no datasets, it prints a message indicating that no datasets were found.

    Args:
        args: A namespace object from argparse. It should have optional attributes:
            find (str): Optional keyword to filter datasets.
            pagination (str): Optional tuple to paginate datasets.

    Returns:
        list | None: A list of datasets or None if there are no datasets.
    """
    try:
        print("Listing datasets may take a while...")
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_BENCHMARK_LIST_DATASETS_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION_1)
        else:
            pagination = ()

        datasets_list = api_get_all_datasets()
        keyword = args.find.lower() if args.find else ""

        if datasets_list:
            filtered_datasets_list = filter_data(datasets_list, keyword, pagination)
            if filtered_datasets_list:
                _display_datasets(filtered_datasets_list)
                return filtered_datasets_list

        console.print("[red]There are no datasets found.[/red]")
        return None

    except Exception as e:
        print(f"[list_datasets]: {str(e)}")
        return None


def view_dataset(args) -> None:
    """
    View a specific dataset.

    This function retrieves all available datasets and their names by calling the api_get_all_datasets and
    api_get_all_datasets_name functions. It then finds the dataset with the name specified in args.dataset_filename
    and displays it using the _display_datasets function. If an exception occurs, it prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            dataset_filename (str): The name of the dataset to view.

    Returns:
        None
    """
    try:
        print("Viewing datasets may take a while...")
        if (
            not isinstance(args.dataset_filename, str)
            or not args.dataset_filename
            or args.dataset_filename is None
        ):
            raise TypeError(ERROR_BENCHMARK_VIEW_DATASET_DATASET_FILENAME_VALIDATION)

        datasets_list = api_get_all_datasets()
        datasets_name_list = api_get_all_datasets_name()

        # Find the index of the dataset with the name args.dataset_filename
        dataset_index = datasets_name_list.index(args.dataset_filename)
        # Pass the corresponding dataset from datasets_list to _display_datasets
        _display_datasets([datasets_list[dataset_index]])

    except Exception as e:
        print(f"[view_dataset]: {str(e)}")


def delete_dataset(args) -> None:
    """
    Delete a dataset.

    This function deletes a dataset with the specified name. It prompts the user for confirmation before proceeding
    with the deletion. If the user confirms, it calls the api_delete_dataset function from the moonshot.api module to
    delete the dataset. If the deletion is successful, it prints a confirmation message. If an exception occurs, it
    prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            dataset (str): The name of the dataset to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a dataset
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the dataset (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Dataset deletion cancelled.[/]")
        return

    try:
        if (
            args.dataset is None
            or not isinstance(args.dataset, str)
            or not args.dataset
        ):
            raise ValueError(ERROR_BENCHMARK_DELETE_DATASET_DATASET_VALIDATION)

        api_delete_dataset(args.dataset)
        print("[delete_dataset]: Dataset deleted.")
    except Exception as e:
        print(f"[delete_dataset]: {str(e)}")


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
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_datasets(datasets_list: list):
    """
    Displays a list of datasets in a table format.

    This function takes a list of datasets and displays them in a table format with each dataset's name, description,
    and other relevant details. If the list is empty, it prints a message indicating that no datasets are found.

    Args:
        datasets_list (list): A list of dictionaries, where each dictionary contains the details of a dataset.

    Returns:
        None
    """
    table = Table(
        title="List of Datasets", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("No.", width=2)
    table.add_column("Dataset", justify="left", width=78)
    for idx, dataset in enumerate(datasets_list, 1):
        (
            id,
            name,
            description,
            _,
            num_of_dataset_prompts,
            created_date,
            reference,
            license,
            *other_args,
        ) = dataset.values()

        idx = dataset.get("idx", idx)
        prompt_info = display_view_str_format("Prompts", num_of_dataset_prompts)
        created_date_info = display_view_str_format("Created Date", created_date)
        license_info = display_view_str_format("License", license)
        reference_info = display_view_str_format("Reference", reference)

        dataset_info = (
            f"[red]{id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\n"
            f"{prompt_info}\n\n{created_date_info}\n\n{license_info}\n\n{reference_info}"
        )

        table.add_section()
        table.add_row(str(idx), dataset_info)
    console.print(table)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# View dataset arguments
view_dataset_args = cmd2.Cmd2ArgumentParser(
    description="View a dataset file.",
    epilog="Example:\n view_dataset bbq-lite-age-ambiguous",
)
view_dataset_args.add_argument(
    "dataset_filename", type=str, help="Name of the dataset file"
)

# Delete dataset arguments
delete_dataset_args = cmd2.Cmd2ArgumentParser(
    description="Delete a dataset.",
    epilog="Example:\n delete_dataset bbq-lite-age-ambiguous",
)
delete_dataset_args.add_argument("dataset", type=str, help="Name of the dataset")

# List dataset arguments
list_datasets_args = cmd2.Cmd2ArgumentParser(
    description="List all datasets.",
    epilog='Example:\n list_datasets -f "bbq"',
)

list_datasets_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find dataset(s) with keyword",
    nargs="?",
)

list_datasets_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate dataset(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)

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
        "{'dataset_name': 'cais_mmlu', 'dataset_config': 'college_biology', 'split': 'test', "
        "'input_col': ['questions','choices'], 'target_col': 'answer'}\""
    ),
)
