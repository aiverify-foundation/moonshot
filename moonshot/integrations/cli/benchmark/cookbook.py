from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_create_cookbook,
    api_get_all_cookbook,
    api_read_cookbook,
    api_read_recipes,
)

console = Console()


def add_cookbook(args) -> None:
    """
    Add a new cookbook with the specified name, description, and a list of recipes.
    """
    recipes = literal_eval(args.recipes)
    api_create_cookbook(args.name, args.description, recipes)


def list_cookbooks() -> None:
    """
    Get a list of available cookbooks.
    """
    cookbooks_list = api_get_all_cookbook()
    if cookbooks_list:
        table = Table("No.", "Cookbook", "Recipes")
        for cookbook_id, cookbook in enumerate(cookbooks_list, 1):
            id, name, description, recipes = cookbook.values()
            cookbook_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"
            recipes_info = ""
            recipes_info = "\n".join(
                f"{i + 1}. {item}" for i, item in enumerate(recipes)
            )
            table.add_section()
            table.add_row(str(cookbook_id), cookbook_info, recipes_info)
        console.print(table)
    else:
        console.print("[red]There are no cookbooks found.[/red]")


def view_cookbook(args) -> None:
    """
    Returns a list of available recipes in the cookbook
    """
    cookbook_info = api_read_cookbook(args.cookbook)
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


# def run_cookbook(args) -> None:
#     """
#     Run cookbooks with the specified list of endpoints.
#     """
#     cookbooks = literal_eval(args.cookbooks)
#     endpoints = literal_eval(args.endpoints)
#     num_of_prompts = args.num_of_prompts

#     # Run the recipes with the defined endpoints
#     cookbook_run = api_run_cookbooks(cookbooks, endpoints, num_of_prompts)
#     cookbook_results = cookbook_run.create_run()
#     if cookbook_results:
#         # Display recipe results
#         generate_cookbook_table(endpoints, cookbook_results)
#         console.print(
#             f"[blue]Results saved in {cookbook_run.run_metadata.filepath}[/blue]"
#         )
#     else:
#         console.print("[red]There are no results.[/red]")

#     # Print run stats
#     console.print(cookbook_run.get_run_stats())


def generate_cookbook_table(endpoints: list, results: dict) -> None:
    table = Table("", "Cookbook", "Recipe", *endpoints)
    for cookbook_name, cookbook_results in results.items():
        # Get recipe name list
        recipes = []
        for recipe_endpoint, _ in cookbook_results.items():
            recipe_name, _ = recipe_endpoint.split("_")
            if recipe_name not in recipes:
                recipes.append(recipe_name)

        for recipe_index, recipe in enumerate(recipes, 1):
            endpoint_results = []
            for endpoint in endpoints:
                # Extract only the results of each prompt template
                tmp_results = {
                    prompt_template_name: prompt_template_results["results"]
                    for prompt_template_name, prompt_template_results in cookbook_results[
                        f"{recipe}_{endpoint}"
                    ].items()
                }
                endpoint_results.append(str(tmp_results))
            table.add_section()
            table.add_row(str(recipe_index), cookbook_name, recipe, *endpoint_results)
    # Display table
    console.print(table)


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

# View cookbook arguments
view_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="View a cookbook.",
    epilog="Example:\n view_cookbook bbq-lite-age-cookbook",
)
view_cookbook_args.add_argument("cookbook", type=str, help="Name of the cookbook")


# Run cookbook arguments
run_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Run a cookbook.",
    epilog="Example:\n run_cookbook "
    "-n 1 "
    "\"['bbq-lite-age-cookbook']\" "
    "\"['my-openai-gpt35']\"",
)
run_cookbook_args.add_argument("cookbooks", type=str, help="List of cookbooks to run")
run_cookbook_args.add_argument("endpoints", type=str, help="List of endpoints to run")
run_cookbook_args.add_argument(
    "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
)
