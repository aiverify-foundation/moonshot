import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_all_runner, api_delete_runner, api_read_runner
from moonshot.integrations.cli.common.display_helper import display_view_list_format, display_view_str_format

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_runners() -> None:
    """
    List all available runners.

    This function retrieves all available runners by calling the api_get_all_runner function from the
    moonshot.api module. It then displays the runners' information using the display_runners function.
    If an exception occurs, it prints an error message.

    Returns:
        None
    """
    try:
        runner_info = api_get_all_runner()
        display_runners(runner_info)
    except Exception as e:
        print(f"[list_runners]: {str(e)}")

def view_runner(args) -> None:
    """
    View a specific runner.

    This function retrieves a specific runner by calling the api_read_runner function from the
    moonshot.api module using the runner identifier provided in the args.
    It then displays the runner's information using the display_runners function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            runner (str): The identifier of the runner to view.

    Returns:
        None
    """
    try:
        runner_info = api_read_runner(args.runner)
        display_runners([runner_info])
    except Exception as e:
        print(f"[view_runner]: {str(e)}")

def delete_runner(args) -> None:
    """
    Delete a runner.

    This function deletes a runner with the specified identifier. It prompts the user for confirmation before proceeding
    with the deletion. If the user confirms, it calls the api_delete_runner function from the moonshot.api module to
    delete the runner. If the deletion is successful, it prints a confirmation message. If an exception occurs, it
    prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            runner (str): The identifier of the runner to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a runner
    confirmation = console.input("[bold red]Are you sure you want to delete the runner (y/N)? [/]")
    if confirmation.lower() != 'y':
        console.print("[bold yellow]Runner deletion cancelled.[/]")
        return
    try:
        api_delete_runner(args.runner)
        print("[delete_runner]: Runner deleted.")
    except Exception as e:
        print(f"[delete_runner]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_runners(runner_list: list) -> None:
    """
    Display the list of runners in a tabular format.

    This function takes a list of runner dictionaries and displays each runner's details in a table.
    The table includes the runner's ID, name, database file, endpoints, and description. If the list is empty,
    it prints a message indicating that no runners are found.

    Args:
        runner_list (list): A list of dictionaries, where each dictionary contains the details of a runner.
    """
    if runner_list:
        table = Table(
            title="List of Runners", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Runner", justify="left", width=78)
        table.add_column("Contains", justify="left", width=20, overflow="fold")
        for runner_id, runner in enumerate(runner_list, 1):
            (
                id,
                name,
                db_file,
                endpoints,
                description
            ) = runner.values()

            db_info = display_view_str_format("Database", db_file)
            endpoints_info = display_view_list_format("Endpoints", endpoints)

            runner_info = (
                f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"
            )
            contains_info = f"{db_info}\n\n{endpoints_info}"

            table.add_section()
            table.add_row(str(runner_id), runner_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no runners found.[/red]")


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# View runner arguments
view_runner_args = cmd2.Cmd2ArgumentParser(
    description="View a runner.",
    epilog="Example:\n view_runner my-new-cookbook-runner",
)
view_runner_args.add_argument("runner", type=str, help="Name of the runner")

# Delete runner arguments
delete_runner_args = cmd2.Cmd2ArgumentParser(
    description="Delete a runner.",
    epilog="Example:\n delete_runner my-new-cookbook-runner",
)
delete_runner_args.add_argument("runner", type=str, help="Name of the runner")
