import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_attack_module, api_get_all_attack_module_metadata

console = Console()


def list_attack_modules() -> None:
    """
    Retrieves and prints the metadata of all attack modules.
    """
    print("Listing attack modules may take a while...")
    attack_module_metadata_list = api_get_all_attack_module_metadata()

    if attack_module_metadata_list:
        table = Table(
            title="Attack Module List",
            show_lines=True,
            expand=True,
            header_style="bold",
        )
        table.add_column("No.", width=2)
        table.add_column("Details", justify="left", width=98)

        for attack_module_index, attack_module_data in enumerate(
            attack_module_metadata_list, 1
        ):
            attack_module_data_str = ""
            for k, v in attack_module_data.items():
                attack_module_data_str += f"[blue]{k.capitalize()}:[/blue] {v}\n\n"
            table.add_row(str(attack_module_index), attack_module_data_str)

        console.print(table)
    else:
        console.print("[red]There are no attack modules found.[/red]", style="bold")


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


# Delete attack module arguments
delete_attack_module_args = cmd2.Cmd2ArgumentParser(
    description="Delete an attack module.",
    epilog="Example:\n delete_attack_module sample_attack_module",
)

delete_attack_module_args.add_argument(
    "attack_module", type=str, help="The ID of the attack module to delete"
)
