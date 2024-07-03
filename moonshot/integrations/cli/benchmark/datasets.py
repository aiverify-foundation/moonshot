import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_delete_dataset,
    api_get_all_datasets,
    api_get_all_datasets_name,
)
from moonshot.integrations.cli.common.display_helper import display_view_str_format
from moonshot.src.utils.find_feature import find_keyword

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_datasets(args) -> list | None:
    """
    List all available datasets.

    This function retrieves all available datasets by calling the api_get_all_datasets function from the
    moonshot.api module. It then displays the datasets using the display_datasets function. If an exception occurs,
    it prints an error message.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find dataset(s) with a keyword.

    Returns:
        list | None: A list of Dataset or None if there is no result.
    """
    try:
        print("Listing datasets may take a while...")
        datasets_list = api_get_all_datasets()
        keyword = args.find.lower() if args.find else ""
        if keyword:
            filtered_datasets_list = find_keyword(keyword, datasets_list)
            if filtered_datasets_list:
                display_datasets(filtered_datasets_list)
                return filtered_datasets_list
            else:
                print("No datasets containing keyword found.")
                return None
        else:
            display_datasets(datasets_list)
            return datasets_list
    except Exception as e:
        print(f"[list_datasets]: {str(e)}")


def view_dataset(args) -> None:
    """
    View a specific dataset.

    This function retrieves all available datasets and their names by calling the api_get_all_datasets and
    api_get_all_datasets_name functions. It then finds the dataset with the name specified in args.dataset_filename
    and displays it using the display_datasets function. If an exception occurs, it prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            dataset_filename (str): The name of the dataset to view.

    Returns:
        None
    """
    try:
        print("Viewing datasets may take a while...")
        datasets_list = api_get_all_datasets()
        datasets_name_list = api_get_all_datasets_name()

        # Find the index of the dataset with the name args.dataset_filename
        dataset_index = datasets_name_list.index(args.dataset_filename)
        # Pass the corresponding dataset from datasets_list to display_datasets
        display_datasets([datasets_list[dataset_index]])

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
            dataset_name (str): The name of the dataset to delete.

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
        api_delete_dataset(args.dataset)
        print("[delete_dataset]: Dataset deleted.")
    except Exception as e:
        print(f"[delete_dataset]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_datasets(datasets_list: list):
    """
    Displays a list of datasets in a table format.

    This function takes a list of datasets and displays them in a table format with each dataset's name, description,
    and other relevant details. If the list is empty, it prints a message indicating that no datasets are found.

    Args:
        datasets_list (list): A list of dictionaries, where each dictionary contains the details of a dataset.

    Returns:
        None
    """
    if datasets_list:
        table = Table(
            title="List of Datasets", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Dataset", justify="left", width=78)
        for dataset_no, dataset in enumerate(datasets_list, 1):
            (
                id,
                name,
                description,
                _,
                num_of_dataset_prompts,
                created_date,
                reference,
                license,
            ) = dataset.values()

            prompt_info = display_view_str_format("Prompts", num_of_dataset_prompts)
            created_date_info = display_view_str_format("Created Date", created_date)
            license_info = display_view_str_format("License", license)
            reference_info = display_view_str_format("Reference", reference)

            dataset_info = (
                f"[red]{id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\n"
                f"{prompt_info}\n\n{created_date_info}\n\n{license_info}\n\n{reference_info}"
            )

            table.add_section()
            table.add_row(str(dataset_no), dataset_info)
        console.print(table)
    else:
        console.print("[red]There are no datasets found.[/red]")


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
