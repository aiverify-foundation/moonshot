import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_result, api_get_all_result, api_read_result
from moonshot.integrations.cli.benchmark.cookbook import show_cookbook_results
from moonshot.integrations.cli.benchmark.recipe import show_recipe_results
from moonshot.integrations.cli.common.display_helper import (
    display_view_list_format,
    display_view_str_format,
)
from moonshot.src.utils.find_feature import find_keyword

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_results(args) -> list | None:
    """
    List all available results.

    This function retrieves all available results by calling the api_get_all_result_name function from the
    moonshot.api module. It then creates a table with the result id and name. If there are no results, it prints a
    message indicating that no results were found.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find result(s) with a keyword.

    Returns:
        list | None: A list of Result or None if there is no result.
    """
    try:
        results_list = api_get_all_result()
        keyword = args.find.lower() if args.find else ""
        if keyword:
            filtered_results_list = find_keyword(keyword, results_list)
            if filtered_results_list:
                display_results(filtered_results_list)
                return filtered_results_list
            else:
                print("No results containing keyword found.")
                return None
        else:
            display_results(results_list)
            return results_list
    except Exception as e:
        print(f"[list_results]: {str(e)}")


def view_result(args) -> None:
    """
    View a specific result.

    This function retrieves a specific result by calling the api_read_result function from the
    moonshot.api module using the result filename provided in the args.
    It then checks if the result filename starts with "cookbook". If it does, it displays the result using the
    display_view_cookbook_result function. Otherwise, it uses the display_view_recipe_result function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            result_filename (str): The filename of the result to view.

    Returns:
        None
    """
    try:
        result_info = api_read_result(args.result_filename)
        if result_info["metadata"].get("cookbooks"):
            display_view_cookbook_result(result_info)
        elif result_info["metadata"].get("recipes"):
            display_view_recipe_result(result_info)
        else:
            print("[view_result]: Unable to determine cookbook or recipe")
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
        args: A namespace object from argparse. It should have the following attribute:
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
        api_delete_result(args.result)
        print("[delete_result]: Result deleted.")
    except Exception as e:
        print(f"[delete_result]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_results(results_list):
    """
    Display a list of results.

    This function takes a list of results and displays them in a table format. If the list is empty, it prints a
    message indicating that no results were found.

    Args:
        results_list (list): A list of results. Each result is a dictionary with keys 'id' and 'name'.

    Returns:
        None
    """
    if results_list:
        table = Table(
            title="List of Results", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Result", justify="left", width=78)
        table.add_column("Contains", justify="left", width=20, overflow="fold")
        for result_id, result in enumerate(results_list, 1):
            metadata, results = result.values()

            id = metadata["id"]
            start_time = metadata["start_time"]
            end_time = metadata["end_time"]
            duration = metadata["duration"]
            status = metadata["status"]
            recipes = metadata["recipes"]
            cookbooks = metadata["cookbooks"]
            endpoints = metadata["endpoints"]
            num_of_prompts = metadata["num_of_prompts"]
            random_seed = metadata["random_seed"]
            system_prompt = metadata["system_prompt"]

            duration_info = (
                f"[blue]Period:[/blue] {start_time} - {end_time} ({duration}s)"
            )
            status_info = display_view_str_format("Status", status)
            recipes_info = display_view_list_format("Recipes", recipes)
            cookbooks_info = display_view_list_format("Cookbooks", cookbooks)
            endpoints_info = display_view_list_format("Endpoints", endpoints)
            prompts_info = display_view_str_format("Number of Prompts", num_of_prompts)
            seed_info = display_view_str_format("Seed", random_seed)
            system_prompt_info = display_view_str_format("System Prompt", system_prompt)

            result_info = f"[red]id: {id}[/red]\n\n{duration_info}\n\n{status_info}"
            contains_info = (
                f"{recipes_info}\n\n{cookbooks_info}\n\n{endpoints_info}\n\n{prompts_info}"
                f"\n\n{seed_info}\n\n{system_prompt_info}"
            )

            table.add_section()
            table.add_row(str(result_id), result_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no results found.[/red]")


def display_view_recipe_result(result_info):
    """
    Display the recipe result.

    This function takes the result file and result info as arguments. It converts the result info into a dictionary
    using the convert_string_tuples_in_dict function. It then retrieves the recipes, endpoints, and duration from the
    converted result info. Finally, it calls the show_recipe_results function from the
    moonshot.integrations.cli.benchmark.recipe module to display the recipe results.

    Args:
        result_info (dict): The result info.

    Returns:
        None
    """
    recipes = result_info["metadata"]["recipes"]
    endpoints = result_info["metadata"]["endpoints"]
    duration = result_info["metadata"]["duration"]
    show_recipe_results(recipes, endpoints, result_info, duration)


def display_view_cookbook_result(result_info):
    """
    Display the cookbook result.

    This function takes the result file and result info as arguments. It converts the result info into a dictionary
    using the convert_string_tuples_in_dict function. It then retrieves the cookbooks, endpoints, and duration from the
    converted result info. Finally, it calls the show_cookbook_results function from the
    moonshot.integrations.cli.benchmark.cookbook module to display the cookbook results.

    Args:
        result_info (dict): The result info.

    Returns:
        None
    """
    cookbooks = result_info["metadata"]["cookbooks"]
    endpoints = result_info["metadata"]["endpoints"]
    duration = result_info["metadata"]["duration"]
    show_cookbook_results(cookbooks, endpoints, result_info, duration)


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
