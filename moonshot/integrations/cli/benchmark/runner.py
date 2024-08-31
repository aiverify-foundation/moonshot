import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_delete_runner,
    api_get_all_run,
    api_get_all_runner,
    api_get_available_session_info,
    api_load_session,
    api_read_runner,
)
from moonshot.integrations.cli.cli_errors import (
    ERROR_BENCHMARK_DELETE_RUNNER_RUNNER_VALIDATION,
    ERROR_BENCHMARK_VIEW_RUNNER_RUNNER_VALIDATION,
)
from moonshot.integrations.cli.common.display_helper import (
    display_view_list_format,
    display_view_str_format,
)

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_runners() -> None:
    """
    List all runners.

    Retrieves and displays information about all runners, including their associated runs and session
    information. Fetches the data using the api_get_all_runner, api_get_all_run, and api_get_available_session_info
    functions, then calls the _display_runners function to present it in a user-friendly format.

    Returns:
        None
    """
    try:
        runner_info = api_get_all_runner()
        runner_run_info = api_get_all_run()
        _, runner_session_info = api_get_available_session_info()
        _display_runners(runner_info, runner_run_info, runner_session_info)
    except Exception as e:
        print(f"[list_runners]: {str(e)}")


def view_runner(args) -> None:
    """
    View a specific runner.

    Retrieves and displays information about a specific runner, including its associated runs and session
    information. Uses the runner identifier provided in the arguments to fetch the data and then calls the
    _display_runners function to present it in a user-friendly format.

    Args:
        args (argparse.Namespace): A namespace object from argparse. It should have the following attribute:
            runner (str): The identifier of the runner to view.

    Returns:
        None
    """
    try:
        if not isinstance(args.runner, str) or not args.runner or args.runner is None:
            raise TypeError(ERROR_BENCHMARK_VIEW_RUNNER_RUNNER_VALIDATION)

        runner_info = api_read_runner(args.runner)
        runner_run_info = api_get_all_run(args.runner)
        runner_session_info = api_load_session(args.runner)
        _display_runners([runner_info], runner_run_info, [runner_session_info])
    except Exception as e:
        print(f"[view_runner]: {str(e)}")


def delete_runner(args) -> None:
    """
    Delete a runner.

    Deletes a runner with the specified identifier. Prompts the user for confirmation before proceeding
    with the deletion. If the user confirms, it calls the api_delete_runner function from the moonshot.api module to
    delete the runner. If the deletion is successful, it prints a confirmation message. If an exception occurs, it
    prints an error message.

    Args:
        args (argparse.Namespace): A namespace object from argparse. It should have the following attribute:
            runner (str): The identifier of the runner to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a runner
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the runner (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Runner deletion cancelled.[/]")
        return

    try:
        if args.runner is None or not isinstance(args.runner, str) or not args.runner:
            raise ValueError(ERROR_BENCHMARK_DELETE_RUNNER_RUNNER_VALIDATION)

        api_delete_runner(args.runner)
        print("[delete_runner]: Runner deleted.")
    except Exception as e:
        print(f"[delete_runner]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_runners(
    runner_list: list, runner_run_info_list: list, runner_session_info_list: list
) -> None:
    """
    Display runners in a table format.

    Takes lists of runner information, run information, and session information, then displays them in a
    table format on the command line interface. Each runner is listed with details such as the runner's ID, name,
    description, number of runs, number of sessions, database file, and endpoints.

    Args:
        runner_list (list): A list of dictionaries, where each dictionary contains information about a runner.
        runner_run_info_list (list): A list of dictionaries, where each dictionary contains information about a run
            associated with a runner.
        runner_session_info_list (list): A list of dictionaries, where each dictionary contains information about a
            session associated with a runner.

    Returns:
        None
    """
    if runner_list:
        table = Table(
            title="List of Runners", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Runner", justify="left", width=78)
        table.add_column("Contains", justify="left", width=20, overflow="fold")
        for runner_id, runner in enumerate(runner_list, 1):
            (id, name, db_file, endpoints, description) = runner.values()

            db_info = display_view_str_format("Database", db_file)
            endpoints_info = display_view_list_format("Endpoints", endpoints)

            runs_count = sum(
                run_info["runner_id"] == id for run_info in runner_run_info_list
            )
            # Handle the case where session_info can be None
            sessions_count = sum(
                session_info is not None and session_info["session_id"] == id
                for session_info in runner_session_info_list
            )

            runner_info = (
                f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}\n"
                f"[blue]Number of Runs:[/blue] {runs_count}\n"
                f"[blue]Number of Sessions:[/blue] {sessions_count}"
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
