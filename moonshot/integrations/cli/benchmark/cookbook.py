import asyncio
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table
from slugify import slugify

from moonshot.api import (
    api_create_cookbook,
    api_create_runner,
    api_delete_cookbook,
    api_get_all_cookbook,
    api_get_all_run,
    api_get_all_runner_name,
    api_load_runner,
    api_read_cookbook,
    api_read_recipes,
    api_update_cookbook,
)
from moonshot.integrations.cli.benchmark.recipe import (
    display_view_grading_scale_format,
    display_view_statistics_format,
)
from moonshot.integrations.cli.common.display_helper import display_view_list_format
from moonshot.src.utils.find_feature import find_keyword

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
        new_cookbook_id = api_create_cookbook(args.name, args.description, recipes)
        print(f"[add_cookbook]: Cookbook ({new_cookbook_id}) created.")
    except Exception as e:
        print(f"[add_cookbook]: {str(e)}")


def list_cookbooks(args) -> list | None:
    """
    List all available cookbooks.

    This function retrieves all available cookbooks by calling the api_get_all_cookbook function from the
    moonshot.api module.
    It then displays the retrieved cookbooks using the display_cookbooks function.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find cookbook(s) with a keyword.

    Returns:
        list | None: A list of Cookbook or None if there is no result.
    """
    try:
        cookbooks_list = api_get_all_cookbook()
        keyword = args.find.lower() if args.find else ""
        if keyword:
            filtered_cookbooks_list = find_keyword(keyword, cookbooks_list)
            if filtered_cookbooks_list:
                display_cookbooks(filtered_cookbooks_list)
                return filtered_cookbooks_list
            else:
                print("No cookbooks containing keyword found.")
                return None
        else:
            display_cookbooks(cookbooks_list)
            return cookbooks_list
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
            cookbook (str): The id of the cookbook to view.

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
    Run a cookbook with the specified parameters.

    This function executes a cookbook runner with the given name, cookbooks, endpoints, and other parameters.
    It checks if the runner with the specified name already exists, and if not, it creates a new one.
    The cookbooks are run against the specified endpoints, and the results are processed and displayed.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): The name of the cookbook runner.
            cookbooks (str): A string representation of a list of cookbooks to run.
            endpoints (str): A string representation of a list of endpoints to run.
            num_of_prompts (int): The number of prompts to run.
            random_seed (int): The random seed number for reproducibility.
            system_prompt (str): The system prompt to use.
            runner_proc_module (str): The runner processing module to use.
            result_proc_module (str): The result processing module to use.

    Returns:
        None
    """
    try:
        name = args.name
        cookbooks = literal_eval(args.cookbooks)
        endpoints = literal_eval(args.endpoints)
        num_of_prompts = args.num_of_prompts
        random_seed = args.random_seed
        system_prompt = args.system_prompt
        runner_proc_module = args.runner_proc_module
        result_proc_module = args.result_proc_module

        # Run the cookbooks with the defined endpoints
        slugify_id = slugify(name, lowercase=True)
        if slugify_id in api_get_all_runner_name():
            cb_runner = api_load_runner(slugify_id)
        else:
            cb_runner = api_create_runner(name, endpoints)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            cb_runner.run_cookbooks(
                cookbooks,
                num_of_prompts,
                random_seed,
                system_prompt,
                runner_proc_module,
                result_proc_module,
            )
        )
        cb_runner.close()

        # Display results
        runner_runs = api_get_all_run(cb_runner.id)
        result_info = runner_runs[-1].get("results")
        if result_info:
            show_cookbook_results(
                cookbooks, endpoints, result_info, result_info["metadata"]["duration"]
            )
        else:
            raise RuntimeError("no run result generated")

    except Exception as e:
        print(f"[run_cookbook]: {str(e)}")


def update_cookbook(args) -> None:
    """
    Update a specific cookbook.

    This function updates a specific cookbook by calling the api_update_cookbook function from the
    moonshot.api module using the cookbook name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            cookbook (str): The id of the cookbook to update.
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
    Delete a cookbook.

    This function deletes a cookbook with the specified identifier. It prompts the user for confirmation before
    proceeding with the deletion. If the user confirms, it calls the api_delete_cookbook function from the moonshot.api
    module to delete the cookbook. If the deletion is successful, it prints a confirmation message.

    If an exception occurs, it prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            cookbook (str): The identifier of the cookbook to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a cookbook
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the cookbook (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Cookbook deletion cancelled.[/]")
        return
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
    Display the list of cookbooks in a tabular format.

    This function takes a list of cookbook dictionaries and displays each cookbook's details in a table.
    The table includes the cookbook's ID, name, description, and associated recipes. If the list is empty,
    it prints a message indicating that no cookbooks are found.

    Args:
        cookbooks_list (list): A list of dictionaries, where each dictionary contains the details of a cookbook.
    """
    if cookbooks_list:
        table = Table(
            title="List of Cookbooks", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Cookbook", justify="left", width=78)
        table.add_column("Contains", justify="left", width=20, overflow="fold")
        for cookbook_id, cookbook in enumerate(cookbooks_list, 1):
            id, name, description, recipes = cookbook.values()
            cookbook_info = f"[red]ID: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"
            recipes_info = display_view_list_format("Recipes", recipes)
            table.add_section()
            table.add_row(str(cookbook_id), cookbook_info, recipes_info)
        console.print(table)
    else:
        console.print("[red]There are no cookbooks found.[/red]")


def display_view_cookbook(cookbook_info):
    """
    Display the cookbook information in a formatted table.

    This function takes a dictionary containing cookbook information and displays it in a table format using the rich
    library's Table class. It includes details such as the cookbook's ID, name, description, and associated recipes.

    Args:
        cookbook_info (dict): A dictionary containing the cookbook's information with keys such as
        'id', 'name', 'description', and 'recipes'.

    Returns:
        None
    """
    id, name, description, recipes = cookbook_info.values()
    recipes_list = api_read_recipes(recipes)
    if recipes_list:
        table = Table(
            title="View Cookbook", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Recipe", justify="left", width=78)
        table.add_column("Contains", justify="left", width=20, overflow="fold")
        for recipe_id, recipe in enumerate(recipes_list, 1):
            (
                id,
                name,
                description,
                tags,
                categories,
                datasets,
                prompt_templates,
                metrics,
                attack_strategies,
                grading_scale,
                stats,
            ) = recipe.values()

            tags_info = display_view_list_format("Tags", tags)
            categories_info = display_view_list_format("Categories", categories)
            datasets_info = display_view_list_format("Datasets", datasets)
            prompt_templates_info = display_view_list_format(
                "Prompt Templates", prompt_templates
            )
            metrics_info = display_view_list_format("Metrics", metrics)
            attack_strategies_info = display_view_list_format(
                "Attack Strategies", attack_strategies
            )
            grading_scale_info = display_view_grading_scale_format(
                "Grading Scale", grading_scale
            )
            stats_info = display_view_statistics_format("Statistics", stats)

            recipe_info = (
                f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\n"
                f"{tags_info}\n\n{categories_info}\n\n{grading_scale_info}\n\n{stats_info}"
            )
            contains_info = f"{datasets_info}\n\n{prompt_templates_info}\n\n{metrics_info}\n\n{attack_strategies_info}"

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
    run_stats = f"""{'='*50}\n[blue]Time taken to run: {duration}s[/blue]\n*Overall rating will be the lowest grade
     that the recipes have in each cookbook\n{'='*50}"""
    console.print(run_stats)


def generate_cookbook_table(cookbooks: list, endpoints: list, results: dict) -> None:
    """
    Generate and display a table with the cookbook benchmarking results.

    This function creates a table that includes the index, cookbook name, recipe name, and the results
    for each endpoint.

    The cookbook names are prefixed with "Cookbook:" and are displayed with their overall grades. Each recipe under a
    cookbook is indented and prefixed with "Recipe:" followed by its individual grades for each endpoint. If there are
    no results for a cookbook, a row with dashes across all endpoint columns is added to indicate this.

    Args:
        cookbooks (list): A list of cookbook names to display in the table.
        endpoints (list): A list of endpoints for which results are to be displayed.
        results (dict): A dictionary containing the benchmarking results for cookbooks and recipes.

    Returns:
        None: The function prints the table to the console but does not return any value.
    """
    table = Table(
        title="Cookbook Result", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("No.", width=2)
    table.add_column("Cookbook (with its recipes)", justify="left", width=78)
    for endpoint in endpoints:
        table.add_column(endpoint, justify="center")

    index = 1
    for cookbook in cookbooks:
        # Get cookbook result
        cookbook_result = next(
            (
                result
                for result in results["results"]["cookbooks"]
                if result["id"] == cookbook
            ),
            None,
        )

        if cookbook_result:
            # Add the cookbook name with the "Cookbook: " prefix as the first row for this section
            endpoint_results = []
            for endpoint in endpoints:
                # Find the evaluation summary for the endpoint
                evaluation_summary = next(
                    (
                        temp_eval
                        for temp_eval in cookbook_result["overall_evaluation_summary"]
                        if temp_eval["model_id"] == endpoint
                    ),
                    None,
                )

                # Get the grade from the evaluation_summary, or use "-" if not found
                grade = "-"
                if evaluation_summary and evaluation_summary["overall_grade"]:
                    grade = evaluation_summary["overall_grade"]
                endpoint_results.append(grade)
            table.add_row(
                str(index),
                f"Cookbook: [blue]{cookbook}[/blue]",
                *endpoint_results,
                end_section=True,
            )

            for recipe in cookbook_result["recipes"]:
                endpoint_results = []
                for endpoint in endpoints:
                    # Find the evaluation summary for the endpoint
                    evaluation_summary = next(
                        (
                            temp_eval
                            for temp_eval in recipe["evaluation_summary"]
                            if temp_eval["model_id"] == endpoint
                        ),
                        None,
                    )

                    # Get the grade from the evaluation_summary, or use "-" if not found
                    grade = "-"
                    if (
                        evaluation_summary
                        and "grade" in evaluation_summary
                        and "avg_grade_value" in evaluation_summary
                        and evaluation_summary["grade"]
                    ):
                        grade = f"{evaluation_summary['grade']} [{evaluation_summary['avg_grade_value']}]"
                    endpoint_results.append(grade)

                # Add the recipe name indented under the cookbook name
                table.add_row(
                    "",
                    f"  └──  Recipe: [blue]{recipe['id']}[/blue]",
                    *endpoint_results,
                    end_section=True,
                )

            # Increment index only after all recipes of the cookbook have been added
            index += 1
        else:
            # If no results for the cookbook, add a row indicating this with the "Cookbook: " prefix
            # and a dash for each endpoint column
            table.add_row(
                str(index),
                f"Cookbook: {cookbook}",
                *(["-"] * len(endpoints)),
                end_section=True,
            )
            index += 1

    # Display table
    console.print(table)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add cookbook arguments
add_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Add a new cookbook. The 'name' argument will be slugified to create a unique identifier.",
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
    epilog="Available keys for updating a cookbook: \n"
    "  name: The name of the cookbook. \n"
    "  description: The description of the cookbook. \n"
    "  recipes: A list of recipes included in the cookbook. \n\n"
    "Example command:\n"
    "  update_cookbook my-new-cookbook "
    "\"[('name', 'Updated Cookbook Name'), ('description', 'Updated description'), "
    "('recipes', ['analogical-similarity'])]\"",
)
update_cookbook_args.add_argument("cookbook", type=str, help="Id of the cookbook")
update_cookbook_args.add_argument(
    "update_values", type=str, help="Update cookbook key/value"
)

# View cookbook arguments
view_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="View a cookbook.",
    epilog="Example:\n view_cookbook my-new-cookbook",
)
view_cookbook_args.add_argument("cookbook", type=str, help="Id of the cookbook")

# Delete cookbook arguments
delete_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Delete a cookbook.",
    epilog="Example:\n delete_cookbook my-new-cookbook",
)
delete_cookbook_args.add_argument("cookbook", type=str, help="Id of the cookbook")

# Run cookbook arguments
run_cookbook_args = cmd2.Cmd2ArgumentParser(
    description="Run a cookbook.",
    epilog="Example:\n run_cookbook "
    '"my new cookbook runner" '
    "\"['chinese-safety-cookbook']\" "
    "\"['openai-gpt35-turbo']\" "
    '-n 1 -r 1 -s "You are an intelligent AI" ',
)
run_cookbook_args.add_argument("name", type=str, help="Name of cookbook runner")
run_cookbook_args.add_argument("cookbooks", type=str, help="List of cookbooks to run")
run_cookbook_args.add_argument("endpoints", type=str, help="List of endpoints to run")
run_cookbook_args.add_argument(
    "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
)
run_cookbook_args.add_argument(
    "-r", "--random_seed", type=int, default=0, help="Random seed number"
)
run_cookbook_args.add_argument(
    "-s", "--system_prompt", type=str, default="", help="System Prompt to use"
)
run_cookbook_args.add_argument(
    "-l",
    "--runner_proc_module",
    type=str,
    default="benchmarking",
    help="Runner processing module to use",
)
run_cookbook_args.add_argument(
    "-o",
    "--result_proc_module",
    type=str,
    default="benchmarking-result",
    help="Result processing module to use",
)

# List cookbook arguments
list_cookbooks_args = cmd2.Cmd2ArgumentParser(
    description="List all cookbooks.",
    epilog='Example:\n list_cookbooks -f "risk"',
)

list_cookbooks_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find cookbook(s) with keyword",
    nargs="?",
)
