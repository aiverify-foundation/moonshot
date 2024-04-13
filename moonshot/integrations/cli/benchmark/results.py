import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_result, api_get_all_result_name, api_read_result
from moonshot.integrations.cli.benchmark.cookbook import show_cookbook_results
from moonshot.integrations.cli.benchmark.recipe import show_recipe_results

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_results() -> None:
    """
    List all available results.

    This function retrieves all available results by calling the api_get_all_result_name function from the
    moonshot.api module. It then creates a table with the result id and name. If there are no results, it prints a
    message indicating that no results were found.

    Returns:
        None
    """
    try:
        results_list = api_get_all_result_name()
        display_results(results_list)
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
    Delete a specific result.

    This function deletes a specific result by calling the api_delete_result function from the
    moonshot.api module using the result name provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            result (str): The name of the result to delete.

    Returns:
        None
    """
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
        table = Table("No.", "Result Id")
        for result_id, result in enumerate(results_list, 1):
            table.add_section()
            table.add_row(str(result_id), result)
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
    epilog="Example:\n view_result cookbook-my-new-cookbook-executor",
)
view_result_args.add_argument(
    "result_filename", type=str, help="Name of the result file"
)

# Delete result arguments
delete_result_args = cmd2.Cmd2ArgumentParser(
    description="Delete a result.",
    epilog="Example:\n delete_result cookbook-my-new-cookbook-executor",
)
delete_result_args.add_argument("result", type=str, help="Name of the result")
