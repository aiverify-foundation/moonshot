import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_all_runner
from moonshot.src.api.api_runner import api_delete_runner, api_read_runner

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


def view_run(args) -> None:
    """
    This function views a specific run. It takes the run id as an argument, calls the API to read the run and then
    displays the run information in a tabular format on the console. If there is an error, it catches the exception
    and displays the error message.

    Parameters:
        args (dict): A dictionary that contains the run id.

    Returns:
        None
    """
    try:
        run_info = api_read_runner(args.run)
        display_runs([run_info])
    except Exception as e:
        print(f"[view_run]: {str(e)}")


def delete_run(args) -> None:
    """
    This function deletes a specific run. It takes the run id as an argument, calls the API to delete the run and then
    displays a message saying "Run deleted." If there is an error, it catches the exception and displays the error
    message.

    Parameters:
        args (dict): A dictionary that contains the run id.

    Returns:
        None
    """
    try:
        api_delete_runner(args.run)
        print("[delete_run]: Run deleted.")
    except Exception as e:
        print(f"[delete_run]: {str(e)}")


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
                contains_info += (
                    "[blue]Recipes:[/blue]"
                    + "".join(f"\n{i + 1}. {item}" for i, item in enumerate(recipes))
                    + "\n\n"
                )
            elif cookbooks:
                contains_info += (
                    "[blue]Cookbooks:[/blue]"
                    + "".join(f"\n{i + 1}. {item}" for i, item in enumerate(cookbooks))
                    + "\n\n"
                )

            contains_info += (
                "[blue]Endpoints:[/blue]"
                + "".join(f"\n{i + 1}. {item}" for i, item in enumerate(endpoints))
                + "\n\n"
            )
            contains_info += f"[blue]Number of Prompts:[/blue]\n{num_of_prompts}\n\n"
            contains_info += f"[blue]Database path:[/blue]\n{db_file}"

            table.add_section()
            table.add_row(str(run_index), run_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no runs found.[/red]")


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# View run arguments
view_run_args = cmd2.Cmd2ArgumentParser(
    description="View a run.",
    epilog="Example:\n view_run my-new-recipe-executor",
)
view_run_args.add_argument("run", type=str, help="Name of the run")

# Delete run arguments
delete_run_args = cmd2.Cmd2ArgumentParser(
    description="Delete a run.",
    epilog="Example:\n delete_run my-new-recipe-executor",
)
delete_run_args.add_argument("run", type=str, help="Name of the run")
