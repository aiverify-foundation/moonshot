import asyncio
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_create_recipe,
    api_create_recipe_executor,
    api_delete_recipe,
    api_get_all_recipe,
    api_read_recipe,
    api_update_recipe,
)

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def add_recipe(args) -> None:
    """
    Add a new recipe.

    This function creates a new recipe with the specified parameters.
    It first converts the tags, dataset, prompt_templates, and metrics arguments from a string to a list using the
    literal_eval function from the ast module. Then, it calls the api_create_recipe function from the moonshot.api
    module to create the new recipe.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): The name of the new recipe.
            description (str): The description of the recipe.
            tags (str): A string representation of a list of tags.
            dataset (str): A string representation of a list of datasets.
            prompt_templates (str): A string representation of a list of prompt templates.
            metrics (str): A string representation of a list of metrics.

    Returns:
        None
    """
    tags = literal_eval(args.tags)
    datasets = literal_eval(args.dataset)
    prompt_templates = literal_eval(args.prompt_templates)
    metrics = literal_eval(args.metrics)

    api_create_recipe(
        args.name, args.description, tags, datasets, prompt_templates, metrics
    )


def list_recipes() -> None:
    """
    List all available recipes.

    This function retrieves all available recipes by calling the api_get_all_recipe function from the
    moonshot.api module.
    It then displays the retrieved recipes using the display_recipes function.

    Returns:
        None
    """
    recipes_list = api_get_all_recipe()
    display_recipes(recipes_list)


def view_recipe(args) -> None:
    """
    View a specific recipe.

    This function retrieves a specific recipe by calling the api_read_recipe function from the
    moonshot.api module using the recipe name provided in the args.
    It then displays the retrieved recipe using the display_view_recipe function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            recipe (str): The name of the recipe to view.

    Returns:
        None
    """
    recipe_info = api_read_recipe(args.recipe)
    # Add into list for display
    display_recipes([recipe_info])


def run_recipe(args) -> None:
    """
    Run a specific recipe.

    This function runs a specific recipe by calling the api_create_recipe_executor function from the
    moonshot.api module using the recipe, endpoints, and number of prompts provided in the args.
    It then executes the recipe using the execute method of the returned executor object.
    Finally, it displays the results using the show_recipe_results function and closes the executor.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): A string representation of the recipe executor. Each run is represented by its ID.
            recipes (str): A string representation of a list of recipes to run.
            endpoints (str): A string representation of a list of endpoints to run.
            num_of_prompts (int): The number of prompts to generate for each recipe.

    Returns:
        None
    """
    name = args.name
    recipes = literal_eval(args.recipes)
    endpoints = literal_eval(args.endpoints)
    num_of_prompts = args.num_of_prompts

    bm_executor = api_create_recipe_executor(
        name, recipes, endpoints, num_of_prompts
    )

    asyncio.run(bm_executor.execute())
    show_recipe_results(
        recipes,
        endpoints,
        bm_executor.results,
        bm_executor.results_file,
        bm_executor.duration,
    )
    bm_executor.close_executor()


def update_recipe(args) -> None:
    """
    Update a specific recipe.

    This function updates a specific recipe by calling the api_update_recipe function from the
    moonshot.api module using the recipe name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            recipe (str): The name of the recipe to update.
            update_kwargs (str): A string representation of a list of tuples. Each tuple contains a key
            and a value to update in the recipe.

    Returns:
        None
    """
    recipe = args.recipe
    update_values = dict(literal_eval(args.update_kwargs))
    api_update_recipe(recipe, **update_values)


def delete_recipe(args) -> None:
    """
    Delete a specific recipe.

    This function deletes a specific recipe by calling the api_delete_recipe function from the
    moonshot.api module using the recipe name provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            recipe (str): The name of the recipe to delete.

    Returns:
        None
    """
    api_delete_recipe(args.recipe)


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_recipes(recipes_list):
    """
    Display a list of recipes.

    This function takes a list of recipes and displays them in a table format. If the list is empty, it prints a
    message indicating that no recipes were found.

    Args:
        recipes_list (list): A list of recipes. Each recipe is a dictionary with keys 'id', 'name',
        'description', 'tags', 'datasets', 'prompt_templates', and 'metrics'.

    Returns:
        None
    """
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
            ) = recipe.values()
            recipe_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\nTags:\n{tags}"
            dataset_info = "[blue]Datasets[/blue]:" + "".join(
                f"\n{i + 1}. {item}" for i, item in enumerate(datasets)
            )
            prompt_templates_info = "[blue]Prompt Templates[/blue]:" + "".join(
                f"\n{i + 1}. {item}" for i, item in enumerate(prompt_templates)
            )
            metrics_info = "[blue]Metrics[/blue]:" + "".join(
                f"\n{i + 1}. {item}" for i, item in enumerate(metrics)
            )
            contains_info = f"{dataset_info}\n{prompt_templates_info}\n{metrics_info}"
            table.add_section()
            table.add_row(str(recipe_id), recipe_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no recipes found.[/red]")


def show_recipe_results(recipes, endpoints, recipe_results, results_file, duration):
    """
    Show the results of the recipe benchmarking.

    This function takes the recipes, endpoints, recipe results, results file, and duration as arguments.
    If there are any recipe results, it generates a table to display them using the generate_recipe_table function.
    It also prints the location of the results file and the time taken to run the benchmarking.
    If there are no recipe results, it prints a message indicating that there are no results.

    Args:
        recipes (list): A list of recipes that were benchmarked.
        endpoints (list): A list of endpoints that were used in the benchmarking.
        recipe_results (dict): A dictionary with the results of the recipe benchmarking.
        results_file (str): The location of the results file.
        duration (float): The time taken to run the benchmarking in seconds.

    Returns:
        None
    """
    if recipe_results:
        # Display recipe results
        generate_recipe_table(recipes, endpoints, recipe_results)
        console.print(f"[blue]Results saved in {results_file}[/blue]")
    else:
        console.print("[red]There are no results.[/red]")

    # Print run stats
    console.print(f"{'='*50}\n[blue]Time taken to run: {duration}s[/blue]\n{'='*50}")


def generate_recipe_table(recipes: list, endpoints: list, results: dict) -> None:
    """
    Generate a table to display the results of the recipe benchmarking.

    This function takes the recipes, endpoints, and results as arguments. It creates a table with the recipe names and
    their corresponding results for each endpoint. The results are displayed in a dictionary format with the dataset
    and prompt template as the key and the result as the value. If there are no results for a particular recipe and
    endpoint, it displays an empty dictionary.

    Args:
        recipes (list): A list of recipes that were benchmarked.
        endpoints (list): A list of endpoints that were used in the benchmarking.
        results (dict): A dictionary with the results of the recipe benchmarking. The keys are tuples containing the
        endpoint, recipe, dataset, and prompt template. The values are dictionaries with the 'results' key and the
        result as the value.

    Returns:
        None
    """
    table = Table("", "Recipe", *endpoints)
    for recipe_index, recipe in enumerate(recipes, 1):
        endpoint_results = list()
        for endpoint in endpoints:
            tmp_results = {}
            for result_key, result_value in results[recipe].items():
                if set((endpoint, recipe)).issubset(result_key):
                    result_ep, result_recipe, result_ds, result_pt = result_key
                    tmp_results[(result_ds, result_pt)] = result_value["results"]
            endpoint_results.append(str(tmp_results))
        table.add_section()
        table.add_row(str(recipe_index), recipe, *endpoint_results)
    # Display table
    console.print(table)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add recipe arguments
add_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Add a new recipe.",
    epilog="Example:\n add_recipe 'My new recipe' "
    "'I am recipe description' "
    "\"['tag1','tag2']\" "
    "\"['bbq-lite-age-ambiguous']\" "
    "\"['analogical-similarity','auto-categorisation']\" "
    "\"['bertscore','bleuscore']\"",
)
add_recipe_args.add_argument("name", type=str, help="Name of the new recipe")
add_recipe_args.add_argument(
    "description", type=str, help="Description of the new recipe"
)
add_recipe_args.add_argument(
    "tags", type=str, help="List of tags to be included in the new recipe"
)
add_recipe_args.add_argument("dataset", type=str, help="The dataset to be used")
add_recipe_args.add_argument(
    "prompt_templates",
    type=str,
    help="List of prompt templates to be included in the new recipe",
)
add_recipe_args.add_argument(
    "metrics", type=str, help="List of metrics to be included in the new recipe"
)

# Update recipe arguments
update_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Update a recipe.",
    epilog="Example:\n update_recipe my-new-recipe "
    "\"[('name', 'my-special-bbq-recipe'), ('tags', ['fairness', 'bbq'])]\" ",
)
update_recipe_args.add_argument("recipe", type=str, help="Name of the recipe")
update_recipe_args.add_argument(
    "update_kwargs", type=str, help="Update recipe key/value"
)

# View recipe arguments
view_recipe_args = cmd2.Cmd2ArgumentParser(
    description="View a recipe.",
    epilog="Example:\n view_recipe my-new-recipe",
)
view_recipe_args.add_argument("recipe", type=str, help="Name of the recipe")

# Delete recipe arguments
delete_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Delete a recipe.",
    epilog="Example:\n delete_recipe my-new-recipe",
)
delete_recipe_args.add_argument("recipe", type=str, help="Name of the recipe")

# Run recipe arguments
run_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Run a recipe.",
    epilog="Example:\n run_recipe "
    "-n 1 "
    "my-new-recipe-executor "
    "\"['bbq','auto-categorisation']\" "
    "\"['test-openai-endpoint']\"",
)
run_recipe_args.add_argument("name", type=str, help="Name of recipe executor")
run_recipe_args.add_argument("recipes", type=str, help="List of recipes to run")
run_recipe_args.add_argument("endpoints", type=str, help="List of endpoints to run")
run_recipe_args.add_argument(
    "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
)
