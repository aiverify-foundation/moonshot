from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_result, api_get_all_result, api_read_result
from moonshot.integrations.cli.benchmark.cookbook import _show_cookbook_results
from moonshot.integrations.cli.benchmark.recipe import _show_recipe_results
from moonshot.integrations.cli.cli_errors import (
    ERROR_BENCHMARK_DELETE_RESULT_RESULT_VALIDATION,
    ERROR_BENCHMARK_LIST_RESULTS_FIND_VALIDATION,
    ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION,
    ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION_1,
    ERROR_BENCHMARK_VIEW_RESULT_METADATA_INVALID_VALIDATION,
    ERROR_BENCHMARK_VIEW_RESULT_METADATA_VALIDATION,
    ERROR_BENCHMARK_VIEW_RESULT_RESULT_FILENAME_VALIDATION,
)
from moonshot.integrations.cli.common.display_helper import (
    display_view_list_format,
    display_view_str_format,
)
from moonshot.integrations.cli.utils.process_data import filter_data

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_results(args) -> list | None:
    """
    List all available results.

    This function retrieves all available results by calling the api_get_all_result function from the
    moonshot.api module. It then filters the results based on the provided keyword and pagination arguments.
    If there are no results, it prints a message indicating that no results were found.

    Args:
        args (argparse.Namespace): The arguments provided to the command line interface.
            find (str): Optional field to find result(s) with a keyword.
            pagination (str): Optional field to paginate results.

    Returns:
        list | None: A list of results or None if there are no results.
    """

    try:
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_BENCHMARK_LIST_RESULTS_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION_1)
        else:
            pagination = ()

        results_list = api_get_all_result()
        keyword = args.find.lower() if args.find else ""

        if results_list:
            filtered_results_list = filter_data(results_list, keyword, pagination)
            if filtered_results_list:
                _display_results(filtered_results_list)
                return filtered_results_list

        console.print("[red]There are no results found.[/red]")
        return None

    except Exception as e:
        print(f"[list_results]: {str(e)}")
        return None


def view_result(args) -> None:
    """
    View a specific result.

    This function retrieves a specific result by calling the api_read_result function from the
    moonshot.api module using the result filename provided in the args.
    It then checks the metadata of the result to determine whether to display it as a cookbook or recipe result.

    Args:
        args (argparse.Namespace): The arguments provided to the command line interface.
            result_filename (str): The filename of the result to view.

    Returns:
        None
    """
    try:
        if (
            not isinstance(args.result_filename, str)
            or not args.result_filename
            or args.result_filename is None
        ):
            raise TypeError(ERROR_BENCHMARK_VIEW_RESULT_RESULT_FILENAME_VALIDATION)

        result_info = api_read_result(args.result_filename)
        if isinstance(result_info, dict) and "metadata" in result_info:
            if result_info["metadata"].get("cookbooks"):
                _display_view_cookbook_result(result_info)
            elif result_info["metadata"].get("recipes"):
                _display_view_recipe_result(result_info)
            else:
                raise TypeError(ERROR_BENCHMARK_VIEW_RESULT_METADATA_INVALID_VALIDATION)
        else:
            raise TypeError(ERROR_BENCHMARK_VIEW_RESULT_METADATA_VALIDATION)

    except Exception as e:
        print(f"[view_result]: {str(e)}")


def delete_result(args) -> None:
    """
    Delete a result.

    This function deletes a result with the specified identifier. It prompts the user for confirmation before proceeding
    with the deletion. If the user confirms, it calls the api_delete_result function from the moonshot.api module to
    delete the result. If the deletion is successful, it prints a confirmation message. If an exception occurs, it
    prints an error message.

    Args:
        args (argparse.Namespace): The arguments provided to the command line interface.
            result (str): The identifier of the result to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a result
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the result (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Result deletion cancelled.[/]")
        return

    try:
        if args.result is None or not isinstance(args.result, str) or not args.result:
            raise ValueError(ERROR_BENCHMARK_DELETE_RESULT_RESULT_VALIDATION)

        api_delete_result(args.result)
        print("[delete_result]: Result deleted.")
    except Exception as e:
        print(f"[delete_result]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_results(results_list):
    """
    Display a list of results.

    This function takes a list of results and displays them in a table format. If the list is empty, it prints a
    message indicating that no results were found.

    Args:
        results_list (list): A list of results. Each result is a dictionary with keys 'id' and 'metadata'.

    Returns:
        None
    """
    table = Table(
        title="List of Results", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("No.", width=2)
    table.add_column("Result", justify="left", width=78)
    table.add_column("Contains", justify="left", width=20, overflow="fold")
    for idx, result in enumerate(results_list, 1):
        metadata, results, *other_args = result.values()

        id = metadata["id"]
        start_time = metadata["start_time"]
        end_time = metadata["end_time"]
        duration = metadata["duration"]
        status = metadata["status"]
        recipes = metadata["recipes"]
        cookbooks = metadata["cookbooks"]
        endpoints = metadata["endpoints"]
        prompt_selection_percentage = metadata["prompt_selection_percentage"]
        random_seed = metadata["random_seed"]
        system_prompt = metadata["system_prompt"]
        idx = result.get("idx", idx)

        duration_info = f"[blue]Period:[/blue] {start_time} - {end_time} ({duration}s)"
        status_info = display_view_str_format("Status", status)
        recipes_info = display_view_list_format("Recipes", recipes)
        cookbooks_info = display_view_list_format("Cookbooks", cookbooks)
        endpoints_info = display_view_list_format("Endpoints", endpoints)
        prompts_info = display_view_str_format(
            "Prompt Selection Percentage", prompt_selection_percentage
        )
        seed_info = display_view_str_format("Seed", random_seed)
        system_prompt_info = display_view_str_format("System Prompt", system_prompt)

        result_info = f"[red]id: {id}[/red]\n\n{duration_info}\n\n{status_info}"
        contains_info = (
            f"{recipes_info}\n\n{cookbooks_info}\n\n{endpoints_info}\n\n{prompts_info}"
            f"\n\n{seed_info}\n\n{system_prompt_info}"
        )

        table.add_section()
        table.add_row(str(idx), result_info, contains_info)
    console.print(table)


def _display_view_recipe_result(result_info):
    """
    Display the recipe result.

    This function takes the result info as an argument. It retrieves the recipes, endpoints, and duration from the
    result info. Finally, it calls the show_recipe_results function from the
    moonshot.integrations.cli.benchmark.recipe module to display the recipe results.

    Args:
        result_info (dict): The result info.

    Returns:
        None
    """
    recipes = result_info["metadata"]["recipes"]
    endpoints = result_info["metadata"]["endpoints"]
    duration = result_info["metadata"]["duration"]
    _show_recipe_results(recipes, endpoints, result_info, duration)


def _display_view_cookbook_result(result_info):
    """
    Display the cookbook result.

    This function takes the result info as an argument. It retrieves the cookbooks, endpoints, and duration from the
    result info. Finally, it calls the show_cookbook_results function from the
    moonshot.integrations.cli.benchmark.cookbook module to display the cookbook results.

    Args:
        result_info (dict): The result info.

    Returns:
        None
    """
    cookbooks = result_info["metadata"]["cookbooks"]
    endpoints = result_info["metadata"]["endpoints"]
    duration = result_info["metadata"]["duration"]
    _show_cookbook_results(cookbooks, endpoints, result_info, duration)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# View result arguments
view_result_args = cmd2.Cmd2ArgumentParser(
    description="View a result file.",
    epilog="Example:\n view_result my-new-cookbook-runner",
)
view_result_args.add_argument(
    "result_filename", type=str, help="Name of the result file"
)

# Delete result arguments
delete_result_args = cmd2.Cmd2ArgumentParser(
    description="Delete a result.",
    epilog="Example:\n delete_result my-new-cookbook-runner",
)
delete_result_args.add_argument("result", type=str, help="Name of the result")

# List result arguments
list_results_args = cmd2.Cmd2ArgumentParser(
    description="List all results.",
    epilog='Example:\n list_results -f "my-runner"',
)

list_results_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find result(s) with keyword",
    nargs="?",
)

list_results_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate result(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
