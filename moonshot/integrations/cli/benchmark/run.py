from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_all_runner

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_runs() -> None:
    """
    This function lists all the runs. It fetches the list of all runs from the API and then displays them in a tabular
    format on the console.
    Each row of the table contains the run index, run id and a string that contains information about the run such as
    recipes, cookbooks, endpoints, number of prompts and the database path.
    If there are no runs, it displays a message saying "There are no runs found."
    """
    try:
        runs_list = api_get_all_runner()
        display_runs(runs_list)
    except Exception as e:
        print(f"[list_runs]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_runs(runs_list) -> None:
    """
    This function displays the runs on the console in a tabular format. It takes a list of runs as input.
    Each row of the table contains the run index, run id and a string that contains information about the run such as
    recipes, cookbooks, endpoints, number of prompts and the database path.
    If there are no runs, it displays a message saying "There are no runs found."

    Parameters:
        runs_list (list): A list of runs. Each run is a dictionary that contains information about the run.

    Returns:
        None
    """
    if runs_list:
        table = Table("No.", "Run id", "Contains")
        for run_index, run_data in enumerate(runs_list, 1):
            (
                run_id,
                run_name,
                run_type,
                db_file,
                recipes,
                cookbooks,
                endpoints,
                num_of_prompts,
            ) = run_data.values()
            run_info = f"[red]id: {run_id}[/red]\n"

            contains_info = ""
            if recipes:
                contains_info += f"[blue]Recipes:[/blue]\n{recipes}\n\n"
            elif cookbooks:
                contains_info += f"[blue]Cookbooks:[/blue]\n{cookbooks}\n\n"
            contains_info += f"[blue]Endpoints:[/blue]\n{endpoints}\n\n"
            contains_info += f"[blue]Number of Prompts:[/blue]\n{num_of_prompts}\n\n"
            contains_info += f"[blue]Database path:[/blue]\n{db_file}"

            table.add_section()
            table.add_row(str(run_index), run_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no runs found.[/red]")
