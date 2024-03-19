from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_create_recipe, api_get_all_recipe

console = Console()


def add_recipe(args) -> None:
    """
    Add a new recipe with the specified name, description, tags, dataset, prompt templates, and a list of metrics.
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
    Get a list of available recipes.
    """
    recipes_list = api_get_all_recipe()
    if recipes_list:
        table = Table("No.", "Recipe", "Contains")
        for recipe_id, recipe in enumerate(recipes_list, 1):
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
            table.add_row(str(recipe_id), recipe_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no recipes found.[/red]")


# def run_recipe(args) -> None:
#     """
#     Run recipes with the specified list of endpoints.
#     """
#     recipes = literal_eval(args.recipes)
#     endpoints = literal_eval(args.endpoints)
#     num_of_prompts = args.num_of_prompts

#     recipe_run = api_run_recipe(recipes, endpoints, num_of_prompts)
#     recipe_results = recipe_run.create_run()
#     if recipe_results:
#         # Display recipe results
#         generate_recipe_table(recipes, endpoints, recipe_results)
#         console.print(
#             f"[blue]Results saved in {recipe_run.run_metadata.filepath}[/blue]"
#         )
#     else:
#         console.print("[red]There are no results.[/red]")

#     # Print run stats
#     console.print(recipe_run.get_run_stats())


def generate_recipe_table(recipes: list, endpoints: list, results: dict) -> None:
    table = Table("", "Recipe", *endpoints)
    for recipe_index, recipe in enumerate(recipes, 1):
        endpoint_results = []
        for endpoint in endpoints:
            # Extract only the results of each prompt template
            tmp_results = {
                prompt_template_name: prompt_template_results["results"]
                for prompt_template_name, prompt_template_results in results[
                    f"{recipe}_{endpoint}"
                ].items()
            }
            endpoint_results.append(str(tmp_results))
        table.add_section()
        table.add_row(str(recipe_index), recipe, *endpoint_results)
    # Display table
    console.print(table)


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

# Run recipe arguuments
run_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Run a recipe.",
    epilog="Example:\n run_recipe "
    "-n 1 "
    "\"['bbq-lite-age-ambiguous','bbq-lite-age-disamb']\" "
    "\"['my-openai-gpt35']\"",
)
run_recipe_args.add_argument("recipes", type=str, help="List of recipes to run")
run_recipe_args.add_argument("endpoints", type=str, help="List of endpoints to run")
run_recipe_args.add_argument(
    "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
)
