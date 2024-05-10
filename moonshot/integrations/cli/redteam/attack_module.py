from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.api import api_get_all_attack_module_metadata

console = Console()


def list_attack_modules() -> None:
    """
    Retrieves and prints the metadata of all attack modules.
    """
    print("Listing attack modules for the first time may take a while...")
    attack_module_metadata_list = api_get_all_attack_module_metadata()

    if attack_module_metadata_list:
        table = Table(
            title="Attack Module List",
            show_lines=True,
            expand=True,
            header_style="bold",
        )
        table.add_column("No.", style="dim", width=2)
        table.add_column("Details", justify="left", width=98)

        for attack_module_index, attack_module_data in enumerate(
            attack_module_metadata_list, 1
        ):
            attack_module_data_str = ""
            for k, v in attack_module_data.items():
                attack_module_data_str += f"[blue]{k.capitalize()}:[/blue] {v}\n\n"
            table.add_row(str(attack_module_index), attack_module_data_str)

        console.print(Panel(table))
    else:
        console.print("[red]There are no attack modules found.[/red]", style="bold")
