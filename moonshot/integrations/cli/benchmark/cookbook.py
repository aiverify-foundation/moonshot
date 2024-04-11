import asyncio
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_create_cookbook,
    api_create_cookbook_runner,
    api_delete_cookbook,
    api_get_all_cookbook,
    api_read_cookbook,
    api_read_recipes,
    api_update_cookbook,
)
from moonshot.src.api.api_result import api_read_result
from moonshot.src.api.api_runner import api_get_all_runner_name, api_load_runner

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def add_cookbook(args) -> None:
    """
    Add a new cookbook.

    This function creates a new cookbook with the specified parameters.
    It first converts the recipes argument from a string to a list using the literal_eval function from the ast module.
    Then, it calls the api_create_cookbook function from the moonshot.api module to create the new cookbook.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): The name of the new cookbook.
            description (str): The description of the cookbook.
            recipes (str): A string representation of a list of recipes. Each recipe is represented by its ID.

    Returns:
        None
    """
    try:
        recipes = literal_eval(args.recipes)
        api_create_cookbook(args.name, args.description, recipes)
        print("[add_cookbook]: Cookbook created.")
    except Exception as e:
        print(f"[add_cookbook]: {str(e)}")


def list_cookbooks() -> None:
    """
    List all available cookbooks.

    This function retrieves all available cookbooks by calling the api_get_all_cookbook function from the
    moonshot.api module.
    It then displays the retrieved cookbooks using the display_cookbooks function.

    Returns:
        None
    """
    try:
        cookbooks_list = api_get_all_cookbook()
        display_cookbooks(cookbooks_list)
    except Exception as e:
        print(f"[list_cookbooks]: {str(e)}")


def view_cookbook(args) -> None:
    """
    View a specific cookbook.

    This function retrieves a specific cookbook by calling the api_read_cookbook function from the
    moonshot.api module using the cookbook name provided in the args.
    It then displays the retrieved cookbook using the display_view_cookbook function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            cookbook (str): The name of the cookbook to view.

    Returns:
        None
    """
    try:
        cookbook_info = api_read_cookbook(args.cookbook)
        display_view_cookbook(cookbook_info)
    except Exception as e:
        print(f"[view_cookbook]: {str(e)}")


def run_cookbook(args) -> None:
    """
    Run a specific cookbook.

    This function initiates the execution of a specific cookbook by invoking the api_create_cookbook_executor function
    from the moonshot.api module. The function uses the cookbook and endpoints provided in the args to create
    an executor. The cookbook is then executed using the run method of the created executor. The results of the
    execution are displayed using the show_cookbook_results function.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): A unique identifier for the cookbook executor. Each execution is represented by its unique ID.
            cookbooks (str): A string representation of a list of cookbooks. Each cookbook is identified by its
                             unique ID.
            endpoints (str): A string representation of a list of endpoints. Each endpoint is identified by its
                             unique ID.
            num_of_prompts (int): The number of prompts to be used in the cookbook.

    Returns:
        None
    """
    try:
        name = args.name
        cookbooks = literal_eval(args.cookbooks)
        endpoints = literal_eval(args.endpoints)
        num_of_prompts = args.num_of_prompts

        # Run the recipes with the defined endpoints
        if name in api_get_all_runner_name():
            cb_runner = api_load_runner(name)
        else:
            cb_runner = api_create_cookbook_runner(
                name, cookbooks, endpoints, num_of_prompts
            )

        asyncio.run(cb_runner.run())
        cb_runner.close()

        # Display results
        result_info = api_read_result(name)
        show_cookbook_results(
            cookbooks, endpoints, result_info, result_info["metadata"]["duration"]
        )

    except Exception as e:
        print(f"[run_cookbook]: {str(e)}")


def update_cookbook(args) -> None:
    """
    Update a specific cookbook.

    This function updates a specific cookbook by calling the api_update_cookbook function from the
    moonshot.api module using the cookbook name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            cookbook (str): The name of the cookbook to update.
            update_values (str): A string representation of a list of tuples. Each tuple contains a key
            and a value to update in the cookbook.

    Returns:
        None
    """
    try:
        cookbook = args.cookbook
        update_values = dict(literal_eval(args.update_values))
        api_update_cookbook(cookbook, **update_values)
        print("[update_cookbook]: Cookbook updated.")
    except Exception as e:
        print(f"[update_cookbook]: {str(e)}")


def delete_cookbook(args) -> None:
    """
    Delete a specific cookbook.

    This function deletes a specific cookbook by calling the api_delete_cookbook function from the
    moonshot.api module using the cookbook name provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            cookbook (str): The name of the cookbook to delete.

    Returns:
        None
    """
    try:
        api_delete_cookbook(args.cookbook)
        print("[delete_cookbook]: Cookbook deleted.")
    except Exception as e:
        print(f"[delete_cookbook]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_cookbooks(cookbooks_list):
    """
    Display a list of cookbooks.

    This function takes a list of cookbooks and displays them in a table format. If the list is empty, it prints a
    message indicating that no cookbooks were found.

    Args:
        cookbooks_list (list): A list of cookbooks. Each cookbook is a dictionary with keys 'id', 'name',
        'description', and 'recipes'.

    Returns:
        None
    """
    if cookbooks_list:
        table = Table("No.", "Cookbook", "Recipes")
        for cookbook_id, cookbook in enumerate(cookbooks_list, 1):
            id, name, description, recipes = cookbook.values()
            cookbook_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"
            recipes_info = "\n".join(
                f"{i + 1}. {item}" for i, item in enumerate(recipes)
            )
            table.add_section()
            table.add_row(str(cookbook_id), cookbook_info, recipes_info)
        console.print(table)
    else:
        console.print("[red]There are no cookbooks found.[/red]")


def display_view_cookbook(cookbook_info):
    """
    Display a specific cookbook.

    This function takes a dictionary of cookbook information and displays it in a table format. If the cookbook has no
    recipes, it prints a message indicating that no recipes were found for the cookbook.

    Args:
        cookbook_info (dict): A dictionary with keys 'id', 'name', 'description', and 'recipes'.

    Returns:
        None
    """
    id, name, description, recipes = cookbook_info.values()
    recipes_list = api_read_recipes(recipes)
    if recipes_list:
        table = Table("No.", "Recipe", "Contains")
        for recipe_id, recipe in enumerate(recipes_list, 1):
            (
                id,
                name,
                description,
                tags,
                datasets,
                prompt_templates,
                metrics,
                rec_type,
                attack_strategies,
            ) = recipe.values()
            recipe_info = (
                f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\n"
                f"Tags:\n{tags}\n\nType:\n{rec_type}"
            )

            if datasets:
                datasets_info = "[blue]Datasets[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(datasets)
                )
            else:
                datasets_info = "[blue]Datasets[/blue]: nil"

            if prompt_templates:
                prompt_templates_info = "[blue]Prompt Templates[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(prompt_templates)
                )
            else:
                prompt_templates_info = "[blue]Prompt Templates[/blue]: nil"

            if metrics:
                metrics_info = "[blue]Metrics[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(metrics)
                )
            else:
                metrics_info = "[blue]Metrics[/blue]: nil"

            if attack_strategies:
                attack_strategies_info = "[blue]Attack Strategies[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(attack_strategies)
                )
            else:
                attack_strategies_info = "[blue]Attack Strategies[/blue]: nil"

            contains_info = f"{datasets_info}\n{prompt_templates_info}\n{metrics_info}\n{attack_strategies_info}"
            table.add_section()
            table.add_row(str(recipe_id), recipe_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no recipes found for the cookbook.[/red]")


def show_cookbook_results(cookbooks, endpoints, cookbook_results, duration):
    """
    Show the results of the cookbook benchmarking.

    This function takes the cookbooks, endpoints, cookbook results, results file, and duration as arguments.
    If there are results, it generates a table with the cookbook results and prints a message indicating
    where the results are saved. If there are no results, it prints a message indicating that no results were found.
    Finally, it prints the duration of the run.

    Args:
        cookbooks (list): A list of cookbooks.
        endpoints (list): A list of endpoints.
        cookbook_results (dict): A dictionary with the results of the cookbook benchmarking.
        duration (float): The duration of the run.

    Returns:
        None
    """
    if cookbook_results:
        # Display recipe results
        generate_cookbook_table(cookbooks, endpoints, cookbook_results)
    else:
        console.print("[red]There are no results.[/red]")

    # Print run stats
    console.print(f"{'='*50}\n[blue]Time taken to run: {duration}s[/blue]\n{'='*50}")


def generate_cookbook_table(cookbooks: list, endpoints: list, results: dict) -> None:
    """
    Generate a table with the cookbook results.

    This function takes the cookbooks, endpoints, and results as arguments. It generates a table with the cookbook
    results. The table includes the index, cookbook name, recipe name, and the results for each endpoint.

    Args:
        cookbooks (list): A list of cookbooks.
        endpoints (list): A list of endpoints.
        results (dict): A dictionary with the results of the cookbook benchmarking.

    Returns:
        None
    """
    table = Table("", "Cookbook", "Recipe", *endpoints)
    index = 1
    for cookbook in cookbooks:
        # Get cookbook result
        cookbook_result = {}
        for tmp_result in results["results"]["cookbooks"]:
            if tmp_result["id"] == cookbook:
                cookbook_result = tmp_result
                break

        if cookbook_result:
            for recipe in cookbook_result["recipes"]:
                endpoint_results = list()
                for endpoint in endpoints:
                    output_results = {}

                    # Get endpoint result
                    for tmp_result in recipe["models"]:
                        if tmp_result["id"] == endpoint:
                            for ds in tmp_result["datasets"]:
                                for pt in ds["prompt_templates"]:
                                    output_results[(ds["id"], pt["id"])] = pt["metrics"]

                    endpoint_results.append(str(output_results))
                table.add_section()
                table.add_row(str(index), cookbook, recipe["id"], *endpoint_results)
                index += 1

    # Display table
    console.print(table)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add cookbook arguments
add_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Add a new cookbook.",
    epilog="Example:\n add_cookbook 'My new cookbook' "
    "'I am cookbook description' "
    "\"['analogical-similarity','auto-categorisation']\"",
)
add_cookbook_args.add_argument("name", type=str, help="Name of the new cookbook")
add_cookbook_args.add_argument(
    "description", type=str, help="Description of the new cookbook"
)
add_cookbook_args.add_argument(
    "recipes", type=str, help="List of recipes to be included in the new cookbook"
)

# Update cookbook arguments
update_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Update a cookbook.",
    epilog="available keys: \n  name: Name of cookbook \n  description: Description of cookbook "
    "\n  recipes: recipes in cookbook \n\nExample:\n update_cookbook my-new-cookbook "
    "\"[('name', 'my-special-bbq-cookbook'), ('recipes', ['my-recipe2', 'my-recipe3'])]\" ",
)
update_cookbook_args.add_argument("cookbook", type=str, help="Name of the cookbook")
update_cookbook_args.add_argument(
    "update_values", type=str, help="Update cookbook key/value"
)

# View cookbook arguments
view_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="View a cookbook.",
    epilog="Example:\n view_cookbook my-new-cookbook",
)
view_cookbook_args.add_argument("cookbook", type=str, help="Name of the cookbook")

# Delete cookbook arguments
delete_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Delete a cookbook.",
    epilog="Example:\n delete_cookbook my-new-cookbook",
)
delete_cookbook_args.add_argument("cookbook", type=str, help="Name of the cookbook")

# Run cookbook arguments
run_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Run a cookbook.",
    epilog="Example:\n run_cookbook "
    "-n 1 "
    "my-new-cookbook-executor "
    "\"['bbq-lite-age-cookbook']\" "
    "\"['test-openai-endpoint']\"",
)
run_cookbook_args.add_argument("name", type=str, help="Name of cookbook executor")
run_cookbook_args.add_argument("cookbooks", type=str, help="List of cookbooks to run")
run_cookbook_args.add_argument("endpoints", type=str, help="List of endpoints to run")
run_cookbook_args.add_argument(
    "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
)
