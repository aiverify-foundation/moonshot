import asyncio
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_create_cookbook,
    api_create_cookbook_executor,
    api_delete_cookbook,
    api_get_all_cookbook,
    api_read_cookbook,
    api_read_recipes,
    api_update_cookbook,
)

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
    recipes = literal_eval(args.recipes)
    api_create_cookbook(args.name, args.description, recipes)


def list_cookbooks() -> None:
    """
    List all available cookbooks.

    This function retrieves all available cookbooks by calling the api_get_all_cookbook function from the
    moonshot.api module.
    It then displays the retrieved cookbooks using the display_cookbooks function.

    Returns:
        None
    """
    cookbooks_list = api_get_all_cookbook()
    display_cookbooks(cookbooks_list)


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
    cookbook_info = api_read_cookbook(args.cookbook)
    display_view_cookbook(cookbook_info)


def run_cookbook(args) -> None:
    """
    Run a specific cookbook.

    This function runs a specific cookbook by calling the api_create_cookbook_executor function from the
    moonshot.api module using the cookbook and endpoints provided in the args.
    It then executes the cookbook using the execute method of the created executor and displays the results using the
    show_cookbook_results function.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): A string representation of the cookbook executor. Each run is represented by its ID.
            cookbooks (str): A string representation of a list of cookbooks. Each cookbook is represented by its ID.
            endpoints (str): A string representation of a list of endpoints. Each endpoint is represented by its ID.
            num_of_prompts (int): The number of prompts to be used in the cookbook.

    Returns:
        None
    """
    name = args.name
    cookbooks = literal_eval(args.cookbooks)
    endpoints = literal_eval(args.endpoints)
    num_of_prompts = args.num_of_prompts

    # Run the recipes with the defined endpoints
    bm_executor = api_create_cookbook_executor(
        name, cookbooks, endpoints, num_of_prompts
    )

    asyncio.run(bm_executor.execute())
    show_cookbook_results(
        cookbooks,
        endpoints,
        bm_executor.results,
        bm_executor.results_file,
        bm_executor.duration,
    )
    bm_executor.close_executor()


def update_cookbook(args) -> None:
    """
    Update a specific cookbook.

    This function updates a specific cookbook by calling the api_update_cookbook function from the
    moonshot.api module using the cookbook name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            cookbook (str): The name of the cookbook to update.
            update_kwargs (str): A string representation of a list of tuples. Each tuple contains a key
            and a value to update in the cookbook.

    Returns:
        None
    """
    cookbook = args.cookbook
    update_values = dict(literal_eval(args.update_kwargs))
    api_update_cookbook(cookbook, **update_values)


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
    api_delete_cookbook(args.cookbook)


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
        for recipes_id, recipe in enumerate(recipes_list, 1):
            (
                id,
                name,
                description,
                tags,
                dataset,
                prompt_templates,
                metrics,
            ) = recipe.values()
            recipe_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\nTags:\n{tags}"
            dataset_info = f"[blue]Dataset[/blue]: {dataset}"
            prompt_templates_info = "[blue]Prompt Templates[/blue]:" + "".join(
                f"\n{i + 1}. {item}" for i, item in enumerate(prompt_templates)
            )
            metrics_info = "[blue]Metrics[/blue]:" + "".join(
                f"\n{i + 1}. {item}" for i, item in enumerate(metrics)
            )
            contains_info = f"{dataset_info}\n{prompt_templates_info}\n{metrics_info}"
            table.add_section()
            table.add_row(str(recipes_id), recipe_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no recipes found for the cookbook.[/red]")


def show_cookbook_results(
    cookbooks, endpoints, cookbook_results, results_file, duration
):
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
        results_file (str): The file where the results are saved.
        duration (float): The duration of the run.

    Returns:
        None
    """
    if cookbook_results:
        # Display recipe results
        generate_cookbook_table(cookbooks, endpoints, cookbook_results)
        console.print(f"[blue]Results saved in {results_file}[/blue]")
    else:
        console.print("[red]There are no results.[/red]")

    # Print run stats
    console.print(f"{'='*50}\n[blue]Time taken to run: {duration}s[/blue]\n{'='*50}")


def generate_cookbook_table(cookbooks, endpoints: list, results: dict) -> None:
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
        cookbook_results = results[cookbook]
        for recipe_name, recipe_results in cookbook_results.items():
            endpoint_results = list()
            for endpoint in endpoints:
                tmp_results = {}
                for result_key, result_value in results[cookbook][recipe_name].items():
                    if set((endpoint, recipe_name)).issubset(result_key):
                        result_ep, result_recipe, result_ds, result_pt = result_key
                        tmp_results[(result_ds, result_pt)] = result_value["results"]
                endpoint_results.append(str(tmp_results))
            table.add_section()
            table.add_row(str(index), cookbook, recipe_name, *endpoint_results)
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
    epilog="Example:\n update_cookbook my-new-cookbook "
    "\"[('name', 'my-special-bbq-cookbook'), ('recipes', ['my-recipe2', 'my-recipe3'])]\" ",
)
update_cookbook_args.add_argument("cookbook", type=str, help="Name of the cookbook")
update_cookbook_args.add_argument(
    "update_kwargs", type=str, help="Update cookbook key/value"
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
