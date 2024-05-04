from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.api import api_get_all_attack_module_metadata

console = Console()


def list_attack_modules() -> None:
    """
    Retrieves and prints the metadata of all attack modules.
    """
    attack_module_metadata_list = api_get_all_attack_module_metadata()

    if attack_module_metadata_list:
        table = Table(title="Attack Module List", show_lines=True)
        table.add_column("No.", style="dim", width=6)
        table.add_column("Attack Module ID", justify="left")
        table.add_column("Details", justify="left")

        for attack_module_index, attack_module_data in enumerate(
            attack_module_metadata_list, 1
        ):
            attack_module_id = attack_module_data.get("id", "")
            name = attack_module_data.get("name", "")
            description = attack_module_data.get("description", "")

            attack_module_id_info = f"[red]id: {attack_module_id}[/red]\n"
            attack_module_details = (
                f"[blue]Name:[/blue] {name}\n\n[blue]Description:[/blue] {description}"
            )
            table.add_row(
                str(attack_module_index), attack_module_id_info, attack_module_details
            )
        console.print(Panel(table))
    else:
        console.print("[red]There are no attack modules found.[/red]", style="bold")
