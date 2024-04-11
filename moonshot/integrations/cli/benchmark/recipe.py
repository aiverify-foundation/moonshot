import asyncio
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_create_recipe,
    api_create_recipe_runner,
    api_delete_recipe,
    api_get_all_recipe,
    api_read_recipe,
    api_update_recipe,
)
from moonshot.src.api.api_result import api_read_result
from moonshot.src.api.api_runner import api_get_all_runner_name, api_load_runner

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def add_recipe(args) -> None:
    """
    Add a new recipe.

    This function creates a new recipe with the specified parameters.
    It first converts the tags, dataset, prompt_templates, metrics, and attack_strategies arguments from a string
    to a list using the literal_eval function from the ast module. Then, it calls the api_create_recipe function
    from the moonshot.api module to create the new recipe.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): The name of the new recipe.
            description (str): The description of the recipe.
            tags (str): A string representation of a list of tags.
            dataset (str): A string representation of a list of datasets.
            prompt_templates (str): A string representation of a list of prompt templates.
            metrics (str): A string representation of a list of metrics.
            type (str): The type of the recipe.
            attack_strategies (str): A string representation of a list of attack strategies.

    Returns:
        None
    """
    try:
        tags = literal_eval(args.tags)
        datasets = literal_eval(args.dataset)
        prompt_templates = literal_eval(args.prompt_templates)
        metrics = literal_eval(args.metrics)
        attack_strategies = literal_eval(args.attack_strategies)

        api_create_recipe(
            args.name,
            args.description,
            tags,
            datasets,
            prompt_templates,
            metrics,
            args.type,
            attack_strategies,
        )
        print("[add_recipe]: Recipe created.")
    except Exception as e:
        print(f"[add_recipe]: {str(e)}")


def list_recipes() -> None:
    """
    List all available recipes.

    This function retrieves all available recipes by calling the api_get_all_recipe function from the
    moonshot.api module.
    It then displays the retrieved recipes using the display_recipes function.

    Returns:
        None
    """
    try:
        recipes_list = api_get_all_recipe()
        display_recipes(recipes_list)
    except Exception as e:
        print(f"[list_recipes]: {str(e)}")


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
    try:
        recipe_info = api_read_recipe(args.recipe)
        display_recipes([recipe_info])
    except Exception as e:
        print(f"[view_recipe]: {str(e)}")


def run_recipe(args) -> None:
    """
    Run a specific recipe.

    This function runs a specific recipe by first checking if a runner with the provided name already exists.
    If it does, it loads the runner using the api_load_runner function from the moonshot.api module.
    If it doesn't, it creates a new runner using the api_create_recipe_runner function from the moonshot.api module.
    The runner is created or loaded using the recipe, endpoints, and number of prompts provided in the args.

    The function then executes the run using the run method of the runner object.
    After the run is complete, it retrieves the run arguments of the latest run using the get_latest_run_arguments
    method of the runner object.

    Finally, it displays the results using the show_recipe_results function and closes the runner.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): A string representation of the recipe runner. Each run is represented by its ID.
            recipes (str): A string representation of a list of recipes to run.
            endpoints (str): A string representation of a list of endpoints to run.
            num_of_prompts (int): The number of prompts to generate for each recipe.

    Returns:
        None
    """
    try:
        name = args.name
        recipes = literal_eval(args.recipes)
        endpoints = literal_eval(args.endpoints)
        num_of_prompts = args.num_of_prompts

        # Run the recipes with the defined endpoints
        if name in api_get_all_runner_name():
            rec_runner = api_load_runner(name)
        else:
            rec_runner = api_create_recipe_runner(
                name, recipes, endpoints, num_of_prompts
            )

        asyncio.run(rec_runner.run())
        rec_runner.close()

        # Display results
        result_info = api_read_result(name)
        show_recipe_results(
            recipes, endpoints, result_info, result_info["metadata"]["duration"]
        )

    except Exception as e:
        print(f"[run_recipe]: {str(e)}")


def update_recipe(args) -> None:
    """
    Update a specific recipe.

    This function updates a specific recipe by calling the api_update_recipe function from the
    moonshot.api module using the recipe name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            recipe (str): The name of the recipe to update.
            update_values (str): A string representation of a list of tuples. Each tuple contains a key
            and a value to update in the recipe.

    Returns:
        None
    """
    try:
        recipe = args.recipe
        update_values = dict(literal_eval(args.update_values))
        api_update_recipe(recipe, **update_values)
        print("[update_recipe]: Recipe updated.")
    except Exception as e:
        print(f"[update_recipe]: {str(e)}")


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
    try:
        api_delete_recipe(args.recipe)
        print("[delete_recipe]: Recipe deleted.")
    except Exception as e:
        print(f"[delete_recipe]: {str(e)}")


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
        console.print("[red]There are no recipes found.[/red]")


def show_recipe_results(recipes, endpoints, recipe_results, duration):
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
        duration (float): The time taken to run the benchmarking in seconds.

    Returns:
        None
    """
    if recipe_results:
        # Display recipe results
        generate_recipe_table(recipes, endpoints, recipe_results)
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
        # Get recipe result
        recipe_result = {}
        for tmp_result in results["results"]["recipes"]:
            if tmp_result["id"] == recipe:
                recipe_result = tmp_result
                break

        if recipe_result:
            endpoint_results = list()
            for endpoint in endpoints:
                output_results = {}

                # Get endpoint result
                for tmp_result in recipe_result["models"]:
                    if tmp_result["id"] == endpoint:
                        for ds in tmp_result["datasets"]:
                            for pt in ds["prompt_templates"]:
                                output_results[(ds["id"], pt["id"])] = pt["metrics"]

                endpoint_results.append(str(output_results))
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
    "\"['bertscore','bleuscore']\" "
    "benchmark "
    '"[]"',
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
add_recipe_args.add_argument(
    "type", type=str, help="The type of recipe, benchmark or redteam"
)
add_recipe_args.add_argument(
    "attack_strategies",
    type=str,
    help="List of attack strategies to be included in the new recipe",
)

# Update recipe arguments
update_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Update a recipe.",
    epilog="available keys: \n  name: Name of recipe \n  description: Description of recipe \n"
    "  tags: List of tags \n  datasets: List of datasets \n  prompt_templates: List of prompt templates \n"
    "  metrics: List of metrics \n  type: Recipe type eg. benchmark or redteam \n"
    "  attack_strategies: List of attack strategies\n\nExample:\n update_recipe my-new-recipe "
    "\"[('name', 'my-special-bbq-recipe'), ('tags', ['fairness', 'bbq'])]\" ",
)
update_recipe_args.add_argument("recipe", type=str, help="Name of the recipe")
update_recipe_args.add_argument(
    "update_values", type=str, help="Update recipe key/value"
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
