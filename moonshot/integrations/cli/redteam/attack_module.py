from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_attack_module, api_get_all_attack_module_metadata
from moonshot.integrations.cli.cli_errors import (
    ERROR_RED_TEAMING_LIST_ATTACK_MODULES_FIND_VALIDATION,
    ERROR_RED_TEAMING_LIST_ATTACK_MODULES_PAGINATION_VALIDATION,
    ERROR_RED_TEAMING_LIST_ATTACK_MODULES_PAGINATION_VALIDATION_1,
)
from moonshot.integrations.cli.utils.process_data import filter_data

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_attack_modules(args) -> list | None:
    """
    Retrieves and prints the metadata of all attack modules.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find attack module(s) with a keyword.
        pagination (str): Optional field to paginate attack modules.

    Returns:
         list | None: A list of AttackModule or None if there is no result.
    """
    try:
        print("Listing attack modules may take a while...")
        attack_module_metadata_list = api_get_all_attack_module_metadata()

        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_RED_TEAMING_LIST_ATTACK_MODULES_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(
                    ERROR_RED_TEAMING_LIST_ATTACK_MODULES_PAGINATION_VALIDATION
                )
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_RED_TEAMING_LIST_ATTACK_MODULES_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(
                    ERROR_RED_TEAMING_LIST_ATTACK_MODULES_PAGINATION_VALIDATION_1
                )

        keyword = args.find.lower() if args.find else ""
        pagination = literal_eval(args.pagination) if args.pagination else ()

        if attack_module_metadata_list:
            filtered_attack_modules_list = filter_data(
                attack_module_metadata_list, keyword, pagination
            )
            if filtered_attack_modules_list:
                _display_attack_modules(filtered_attack_modules_list)
                return filtered_attack_modules_list

        console.print("[red]There are no attack modules found.[/red]")
        return None
    except Exception as e:
        print(f"[list_attack_modules]: {str(e)}")


def delete_attack_module(args) -> None:
    """
    Deletes an attack module after confirming with the user.

    Args:
        args (object): The arguments object. It should have a 'attack_modulee' attribute
                       which is the ID of the attack module to delete.
    """
    # Confirm with the user before deleting an attack module
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the attack module (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Attack module deletion cancelled.[/]")
        return
    try:
        api_delete_attack_module(args.attack_module)
        print("[delete_attack_module]: Attack module deleted.")
    except Exception as e:
        print(f"[delete_attack_module]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_attack_modules(attack_modules: list) -> None:
    """
    Display a list of attack modules.

    This function takes a list of attack modules and displays them in a table format. If the list is empty, it prints a
    message indicating that no attack modules were found.

    Args:
        attack_modules (list): A list of attack modules.

    Returns:
        None
    """
    table = Table(
        title="Attack Module List",
        show_lines=True,
        expand=True,
        header_style="bold",
    )
    table.add_column("No.", width=2)
    table.add_column("Details", justify="left", width=98)

    for idx, attack_module_data in enumerate(attack_modules, 1):
        attack_module_data_str = ""
        for k, v in attack_module_data.items():
            if k != "idx":
                attack_module_data_str += f"[blue]{k.capitalize()}:[/blue] {v}\n\n"
        idx = attack_module_data.get("idx", idx)
        table.add_row(str(idx), attack_module_data_str)
    console.print(table)


# Delete attack module arguments
delete_attack_module_args = cmd2.Cmd2ArgumentParser(
    description="Delete an attack module.",
    epilog="Example:\n delete_attack_module sample_attack_module",
)

delete_attack_module_args.add_argument(
    "attack_module", type=str, help="The ID of the attack module to delete"
)

# List attack modules arguments
list_attack_modules_args = cmd2.Cmd2ArgumentParser(
    description="List all attack modules.",
    epilog='Example:\n list_attack_modules -f "text"',
)

list_attack_modules_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find attack module(s) with keyword",
    nargs="?",
)

list_attack_modules_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate attack module(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
