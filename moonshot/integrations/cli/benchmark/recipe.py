import asyncio
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table
from slugify import slugify

from moonshot.api import (
    api_create_recipe,
    api_create_runner,
    api_delete_recipe,
    api_get_all_recipe,
    api_get_all_run,
    api_get_all_runner_name,
    api_load_runner,
    api_read_recipe,
    api_update_recipe,
)
from moonshot.integrations.cli.cli_errors import (
    ERROR_BENCHMARK_ADD_RECIPE_CATEGORIES_LIST_STR_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_CATEGORIES_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_DATASETS_LIST_STR_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_DATASETS_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_DESC_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_GRADING_SCALE_DICT_STR_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_GRADING_SCALE_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_METRICS_LIST_STR_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_METRICS_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_NAME_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_PROMPT_TEMPLATES_LIST_STR_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_PROMPT_TEMPLATES_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_TAGS_LIST_STR_VALIDATION,
    ERROR_BENCHMARK_ADD_RECIPE_TAGS_VALIDATION,
    ERROR_BENCHMARK_DELETE_RECIPE_RECIPE_VALIDATION,
    ERROR_BENCHMARK_LIST_RECIPES_FIND_VALIDATION,
    ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION,
    ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION_1,
    ERROR_BENCHMARK_RUN_RECIPE_ENDPOINTS_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_ENDPOINTS_VALIDATION_1,
    ERROR_BENCHMARK_RUN_RECIPE_NAME_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_NO_RESULT,
    ERROR_BENCHMARK_RUN_RECIPE_PROMPT_SELECTION_PERCENTAGE_RANGE_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_PROMPT_SELECTION_PERCENTAGE_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_RANDOM_SEED_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_RECIPES_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_RECIPES_VALIDATION_1,
    ERROR_BENCHMARK_RUN_RECIPE_RESULT_PROC_MOD_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_RUNNER_PROC_MOD_VALIDATION,
    ERROR_BENCHMARK_RUN_RECIPE_SYS_PROMPT_VALIDATION,
    ERROR_BENCHMARK_UPDATE_RECIPE_RECIPE_VALIDATION,
    ERROR_BENCHMARK_UPDATE_RECIPE_UPDATE_VALUES_VALIDATION,
    ERROR_BENCHMARK_UPDATE_RECIPE_UPDATE_VALUES_VALIDATION_1,
    ERROR_BENCHMARK_VIEW_RECIPE_RECIPE_VALIDATION,
)
from moonshot.integrations.cli.common.display_helper import display_view_list_format
from moonshot.integrations.cli.utils.process_data import filter_data

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def add_recipe(args) -> None:
    """
    Add a new recipe.

    This function creates a new recipe by parsing the arguments provided and then calling the api_create_recipe
    function from the moonshot.api module.

    It expects the arguments to be strings that can be evaluated into Python data structures using literal_eval.

    Args:
        args (argparse.Namespace): The arguments provided to the command line interface.
        Expected keys are name, description, tags, categories, datasets, prompt_templates, metrics, and grading_scale.

    Returns:
        None

    Raises:
        TypeError: If any of the required arguments are not strings or are None.
        ValueError: If the evaluated arguments are not of the expected types.
    """
    try:
        if not isinstance(args.name, str) or not args.name or args.name is None:
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_NAME_VALIDATION)

        if (
            not isinstance(args.description, str)
            or not args.description
            or args.description is None
        ):
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_DESC_VALIDATION)

        if not isinstance(args.tags, str) or not args.tags or args.tags is None:
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_TAGS_VALIDATION)

        if (
            not isinstance(args.categories, str)
            or not args.categories
            or args.categories is None
        ):
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_CATEGORIES_VALIDATION)

        if (
            not isinstance(args.datasets, str)
            or not args.datasets
            or args.datasets is None
        ):
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_DATASETS_VALIDATION)

        if (
            not isinstance(args.prompt_templates, str)
            or not args.prompt_templates
            or args.prompt_templates is None
        ):
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_PROMPT_TEMPLATES_VALIDATION)

        if (
            not isinstance(args.metrics, str)
            or not args.metrics
            or args.metrics is None
        ):
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_METRICS_VALIDATION)

        if (
            not isinstance(args.grading_scale, str)
            or not args.grading_scale
            or args.grading_scale is None
        ):
            raise TypeError(ERROR_BENCHMARK_ADD_RECIPE_GRADING_SCALE_VALIDATION)

        tags = literal_eval(args.tags)
        categories = literal_eval(args.categories)
        datasets = literal_eval(args.datasets)
        prompt_templates = literal_eval(args.prompt_templates)
        metrics = literal_eval(args.metrics)
        grading_scale = literal_eval(args.grading_scale)

        if not (isinstance(tags, list) and all(isinstance(tag, str) for tag in tags)):
            raise ValueError(ERROR_BENCHMARK_ADD_RECIPE_TAGS_LIST_STR_VALIDATION)

        if not (
            isinstance(categories, list)
            and all(isinstance(category, str) for category in categories)
        ):
            raise ValueError(ERROR_BENCHMARK_ADD_RECIPE_CATEGORIES_LIST_STR_VALIDATION)

        if not (
            isinstance(datasets, list)
            and all(isinstance(dataset, str) for dataset in datasets)
        ):
            raise ValueError(ERROR_BENCHMARK_ADD_RECIPE_DATASETS_LIST_STR_VALIDATION)

        if not (
            isinstance(prompt_templates, list)
            and all(
                isinstance(prompt_template, str) for prompt_template in prompt_templates
            )
        ):
            raise ValueError(
                ERROR_BENCHMARK_ADD_RECIPE_PROMPT_TEMPLATES_LIST_STR_VALIDATION
            )

        if not (
            isinstance(metrics, list)
            and all(isinstance(metric, str) for metric in metrics)
        ):
            raise ValueError(ERROR_BENCHMARK_ADD_RECIPE_METRICS_LIST_STR_VALIDATION)

        if not (
            isinstance(grading_scale, dict)
            and all(
                isinstance(gs, list)
                and len(gs) == 2
                and all(isinstance(value, int) for value in gs)
                for gs in grading_scale.values()
            )
        ):
            raise ValueError(
                ERROR_BENCHMARK_ADD_RECIPE_GRADING_SCALE_DICT_STR_VALIDATION
            )

        new_recipe_id = api_create_recipe(
            args.name,
            args.description,
            tags,
            categories,
            datasets,
            prompt_templates,
            metrics,
            grading_scale,
        )
        print(f"[add_recipe]: Recipe ({new_recipe_id}) created.")
    except Exception as e:
        print(f"[add_recipe]: {str(e)}")


def list_recipes(args) -> list | None:
    """
    List all available recipes.

    This function retrieves all available recipes by calling the api_get_all_recipe function from the
    moonshot.api module.
    It then displays the retrieved recipes using the _display_recipes function.

    Args:
        args: A namespace object from argparse. It should have optional attributes:
            find (str): Optional field to find recipe(s) with a keyword.
            pagination (str): Optional field to paginate recipes.

    Returns:
        list | None: A list of recipes or None if there is no result.

    Raises:
        TypeError: If the 'find' or 'pagination' arguments are not strings or are invalid.
        ValueError: If the 'pagination' argument cannot be evaluated into a tuple of two integers.
    """
    try:
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_BENCHMARK_LIST_RECIPES_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION_1)
        else:
            pagination = ()

        recipes_list = api_get_all_recipe()
        keyword = args.find.lower() if args.find else ""

        if recipes_list:
            filtered_recipes_list = filter_data(recipes_list, keyword, pagination)
            if filtered_recipes_list:
                _display_recipes(filtered_recipes_list)
                return filtered_recipes_list

        console.print("[red]There are no recipes found.[/red]")
        return None

    except Exception as e:
        print(f"[list_recipes]: {str(e)}")
        return None


def view_recipe(args) -> None:
    """
    View a specific recipe.

    This function retrieves a specific recipe by calling the api_read_recipe function from the
    moonshot.api module using the recipe name provided in the args.
    It then displays the retrieved recipe using the _display_recipes function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            recipe (str): The id of the recipe to view.

    Returns:
        None

    Raises:
        TypeError: If the 'recipe' argument is not a string or is None.
    """
    try:
        if not isinstance(args.recipe, str) or not args.recipe or args.recipe is None:
            raise TypeError(ERROR_BENCHMARK_VIEW_RECIPE_RECIPE_VALIDATION)

        recipe_info = api_read_recipe(args.recipe)
        _display_recipes([recipe_info])
    except Exception as e:
        print(f"[view_recipe]: {str(e)}")


def run_recipe(args) -> None:
    """
    Execute a recipe with the specified parameters.

    This function runs a recipe runner with the given name, recipes, endpoints, and other parameters.
    It checks if the runner with the specified name already exists, and if not, it creates a new one.
    The recipes are run against the specified endpoints, and the results are processed and displayed.

    Args:
        args (argparse.Namespace): The arguments provided to the command line interface.
        Expected keys are:
            name (str): The name of the recipe runner.
            recipes (str): A string representation of a list of recipes to run.
            endpoints (str): A string representation of a list of endpoints to run.
            prompt_selection_percentage (int): The percentage of prompts to run.
            random_seed (int): The random seed number for reproducibility.
            system_prompt (str): The system prompt to use.
            runner_proc_module (str): The runner processing module to use.
            result_proc_module (str): The result processing module to use.

    Returns:
        None

    Raises:
        TypeError: If any of the required arguments are not of the expected types or are None.
        ValueError: If the 'recipes' or 'endpoints' arguments cannot be evaluated into lists of strings.
        RuntimeError: If no results are found after running the recipes.
    """
    try:
        if not isinstance(args.name, str) or not args.name or args.name is None:
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_NAME_VALIDATION)

        if (
            not isinstance(args.recipes, str)
            or not args.recipes
            or args.recipes is None
        ):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_RECIPES_VALIDATION)

        if (
            not isinstance(args.endpoints, str)
            or not args.endpoints
            or args.endpoints is None
        ):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_ENDPOINTS_VALIDATION)

        if isinstance(args.prompt_selection_percentage, bool) or not isinstance(
            args.prompt_selection_percentage, int
        ):
            raise TypeError(
                ERROR_BENCHMARK_RUN_RECIPE_PROMPT_SELECTION_PERCENTAGE_VALIDATION
            )
        elif (
            args.prompt_selection_percentage < 1
            or args.prompt_selection_percentage > 100
        ):
            raise ValueError(
                ERROR_BENCHMARK_RUN_RECIPE_PROMPT_SELECTION_PERCENTAGE_RANGE_VALIDATION
            )

        if isinstance(args.random_seed, bool) or not isinstance(args.random_seed, int):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_RANDOM_SEED_VALIDATION)

        if not isinstance(args.system_prompt, str) or args.system_prompt is None:
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_SYS_PROMPT_VALIDATION)

        if (
            not isinstance(args.runner_proc_module, str)
            or not args.runner_proc_module
            or args.runner_proc_module is None
        ):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_RUNNER_PROC_MOD_VALIDATION)

        if (
            not isinstance(args.result_proc_module, str)
            or not args.result_proc_module
            or args.result_proc_module is None
        ):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_RESULT_PROC_MOD_VALIDATION)

        recipes = literal_eval(args.recipes)
        if not (
            isinstance(recipes, list) and all(isinstance(item, str) for item in recipes)
        ):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_RECIPES_VALIDATION_1)

        endpoints = literal_eval(args.endpoints)
        if not (
            isinstance(endpoints, list)
            and all(isinstance(item, str) for item in endpoints)
        ):
            raise TypeError(ERROR_BENCHMARK_RUN_RECIPE_ENDPOINTS_VALIDATION_1)

        # Run the recipes with the defined endpoints
        slugify_id = slugify(args.name, lowercase=True)
        if slugify_id in api_get_all_runner_name():
            rec_runner = api_load_runner(slugify_id)
        else:
            rec_runner = api_create_runner(args.name, endpoints)

        async def run():
            await rec_runner.run_recipes(
                recipes,
                args.prompt_selection_percentage,
                args.random_seed,
                args.system_prompt,
                args.runner_proc_module,
                args.result_proc_module,
            )
            await rec_runner.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

        # Display results
        runner_runs = api_get_all_run(rec_runner.id)
        result_info = runner_runs[-1].get("results")
        if result_info:
            _show_recipe_results(
                recipes, endpoints, result_info, result_info["metadata"]["duration"]
            )
        else:
            raise RuntimeError(ERROR_BENCHMARK_RUN_RECIPE_NO_RESULT)

    except Exception as e:
        print(f"[run_recipe]: {str(e)}")


def update_recipe(args) -> None:
    """
    Update a specific recipe.

    This function updates a specific recipe by calling the api_update_recipe function from the
    moonshot.api module using the recipe name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            recipe (str): The id of the recipe to update.
            update_values (str): A string representation of a list of tuples. Each tuple contains a key
            and a value to update in the recipe.

    Returns:
        None

    Raises:
        ValueError: If the 'recipe' or 'update_values' arguments are not strings or are None.
        ValueError: If the 'update_values' argument cannot be evaluated into a list of tuples.
    """
    try:
        if args.recipe is None or not isinstance(args.recipe, str) or not args.recipe:
            raise ValueError(ERROR_BENCHMARK_UPDATE_RECIPE_RECIPE_VALIDATION)

        if (
            args.update_values is None
            or not isinstance(args.update_values, str)
            or not args.update_values
        ):
            raise ValueError(ERROR_BENCHMARK_UPDATE_RECIPE_UPDATE_VALUES_VALIDATION)

        recipe = args.recipe
        if literal_eval(args.update_values) and all(
            isinstance(i, tuple) for i in literal_eval(args.update_values)
        ):
            update_values = dict(literal_eval(args.update_values))
        else:
            raise ValueError(ERROR_BENCHMARK_UPDATE_RECIPE_UPDATE_VALUES_VALIDATION_1)
        api_update_recipe(recipe, **update_values)

        print("[update_recipe]: Recipe updated.")
    except Exception as e:
        print(f"[update_recipe]: {str(e)}")


def delete_recipe(args) -> None:
    """
    Delete a recipe.

    This function deletes a recipe with the specified identifier. It prompts the user for confirmation before proceeding
    with the deletion. If the user confirms, it calls the api_delete_recipe function from the moonshot.api module to
    delete the recipe. If the deletion is successful, it prints a confirmation message. If an exception occurs, it
    prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            recipe (str): The identifier of the recipe to delete.

    Returns:
        None

    Raises:
        ValueError: If the 'recipe' argument is not a string or is None.
    """
    # Confirm with the user before deleting a recipe
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the recipe (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Recipe deletion cancelled.[/]")
        return

    try:
        if args.recipe is None or not isinstance(args.recipe, str) or not args.recipe:
            raise ValueError(ERROR_BENCHMARK_DELETE_RECIPE_RECIPE_VALIDATION)

        api_delete_recipe(args.recipe)
        print("[delete_recipe]: Recipe deleted.")
    except Exception as e:
        print(f"[delete_recipe]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_view_grading_scale_format(title: str, grading_scale: dict) -> str:
    """
    Format the grading scale for display.

    This function takes a title and a grading scale dictionary and formats them into a string suitable for display.
    The grading scale dictionary is expected to have grade levels as keys and tuples representing the range as values.
    If the grading scale is empty, it returns the title with 'nil'.

    Args:
        title (str): The title to display above the grading scale.
        grading_scale (dict): A dictionary with grade levels as keys and range tuples as values.

    Returns:
        str: The formatted grading scale as a string.
    """
    if grading_scale:
        formatted_grades = "\n".join(
            f"{i + 1}. {grade} [{range_[0]} - {range_[1]}]"
            for i, (grade, range_) in enumerate(grading_scale.items())
        )
        return f"[blue]{title}[/blue]:\n{formatted_grades}"
    else:
        return f"[blue]{title}[/blue]: nil"


def _display_view_statistics_format(title: str, stats: dict) -> str:
    """
    Format the statistics for display.

    This function takes a title and a statistics dictionary and formats them into a string suitable for display.
    The statistics dictionary is expected to have various statistics as keys and their counts or sub-statistics
    as values.

    If the statistics dictionary is empty, it returns the title with 'nil'.

    Args:
        title (str): The title to display above the statistics.
        stats (dict): A dictionary with various statistics as keys and their counts or sub-statistics as values.

    Returns:
        str: The formatted statistics as a string.
    """
    if stats:
        formatted_stats = []
        for i, (stat, value) in enumerate(stats.items(), start=1):
            if isinstance(value, dict):
                sub_stats = "\n".join(
                    f"    {sub_key}: {sub_value}"
                    for sub_key, sub_value in value.items()
                )
                formatted_stats.append(f"{i}. {stat}:\n{sub_stats}")
            else:
                formatted_stats.append(f"{i}. {stat}: {value}")
        return f"[blue]{title}[/blue]:\n" + "\n".join(formatted_stats)
    else:
        return f"[blue]{title}[/blue]: nil"


def _display_recipes(recipes_list: list) -> None:
    """
    Display the list of recipes in a tabular format.

    This function takes a list of recipe dictionaries and displays each recipe's details in a table.
    The table includes the recipe's ID, name, description, and associated details such as tags, categories,
    datasets, prompt templates, metrics, attack strategies, grading scale, and statistics. If the list is empty,
    it prints a message indicating that no recipes are found.

    Args:
        recipes_list (list): A list of dictionaries, where each dictionary contains the details of a recipe.
    """
    table = Table(
        title="List of Recipes", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("No.", width=2)
    table.add_column("Recipe", justify="left", width=78)
    table.add_column("Contains", justify="left", width=20, overflow="fold")
    for idx, recipe in enumerate(recipes_list, 1):
        (
            id,
            name,
            description,
            tags,
            categories,
            datasets,
            prompt_templates,
            metrics,
            grading_scale,
            stats,
            *other_args,
        ) = recipe.values()
        idx = recipe.get("idx", idx)
        tags_info = display_view_list_format("Tags", tags)
        categories_info = display_view_list_format("Categories", categories)
        datasets_info = display_view_list_format("Datasets", datasets)
        prompt_templates_info = display_view_list_format(
            "Prompt Templates", prompt_templates
        )
        metrics_info = display_view_list_format("Metrics", metrics)
        grading_scale_info = _display_view_grading_scale_format(
            "Grading Scale", grading_scale
        )
        stats_info = _display_view_statistics_format("Statistics", stats)

        recipe_info = (
            f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}\n\n"
            f"{tags_info}\n\n{categories_info}\n\n{grading_scale_info}\n\n{stats_info}"
        )
        contains_info = f"{datasets_info}\n\n{prompt_templates_info}\n\n{metrics_info}"

        table.add_section()
        table.add_row(str(idx), recipe_info, contains_info)
    console.print(table)


def _show_recipe_results(recipes, endpoints, recipe_results, duration):
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
        _generate_recipe_table(recipes, endpoints, recipe_results)
    else:
        console.print("[red]There are no results.[/red]")

    # Print run stats
    run_stats = f"""{'='*50}\n[blue]Time taken to run: {duration}s[/blue]\n*Overall rating will be the lowest grade
    that the recipes have in each cookbook\n{'='*50}"""
    console.print(run_stats)


def _generate_recipe_table(recipes: list, endpoints: list, results: dict) -> None:
    """
    Generate and display a table of recipe results.

    This function creates a table that lists the results of running recipes against various endpoints.
    Each row in the table corresponds to a recipe, and each column corresponds to an endpoint.
    The results include the grade and average grade value for each recipe-endpoint pair.

    Args:
        recipes (list): A list of recipe IDs that were benchmarked.
        endpoints (list): A list of endpoint IDs against which the recipes were run.
        results (dict): A dictionary containing the results of the benchmarking.

    Returns:
        None: This function does not return anything. It prints the table to the console.
    """
    # Create a table with a title and headers
    table = Table(
        title="Recipes Result", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("No.", width=2)
    table.add_column("Recipe", justify="left", width=78)
    # Add a column for each endpoint
    for endpoint in endpoints:
        table.add_column(endpoint, justify="center")

    # Iterate over each recipe and populate the table with results
    for index, recipe_id in enumerate(recipes, start=1):
        # Attempt to find the result for the current recipe
        recipe_result = next(
            (
                result
                for result in results["results"]["recipes"]
                if result["id"] == recipe_id
            ),
            None,
        )

        # If the result exists, extract and format the results for each endpoint
        if recipe_result:
            endpoint_results = []
            for endpoint in endpoints:
                # Find the evaluation summary for the endpoint
                evaluation_summary = next(
                    (
                        eval_summary
                        for eval_summary in recipe_result["evaluation_summary"]
                        if eval_summary["model_id"] == endpoint
                    ),
                    None,
                )

                # Format the grade and average grade value, or use "-" if not found
                grade = "-"
                if (
                    evaluation_summary
                    and "grade" in evaluation_summary
                    and "avg_grade_value" in evaluation_summary
                    and evaluation_summary["grade"]
                ):
                    grade = f"{evaluation_summary['grade']} [{evaluation_summary['avg_grade_value']}]"
                endpoint_results.append(grade)

            # Add a row for the recipe with its results
            table.add_row(
                str(index),
                f"Recipe: [blue]{recipe_result['id']}[/blue]",
                *endpoint_results,
                end_section=True,
            )
        else:
            # If no result is found, add a row with placeholders
            table.add_row(
                str(index),
                f"Recipe: [blue]{recipe_id}[/blue]",
                *(["-"] * len(endpoints)),
                end_section=True,
            )

    # Print the table to the console
    console.print(table)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add recipe arguments
add_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Add a new recipe. The 'name' argument will be slugified to create a unique identifier.",
    epilog="Example:\n add_recipe 'My new recipe' "
    "'I am recipe description' "
    "\"['category1','category2']\" "
    "\"['bbq-lite-age-ambiguous']\" "
    "\"['bertscore','bleuscore']\" "
    "-p \"['analogical-similarity','mmlu']\" "
    "-t \"['tag1','tag2']\" "
    "-g \"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}\" ",
)
add_recipe_args.add_argument("name", type=str, help="Name of the new recipe")
add_recipe_args.add_argument(
    "description", type=str, help="Description of the new recipe"
)
add_recipe_args.add_argument(
    "-t",
    "--tags",
    type=str,
    help="List of tags to be included in the new recipe",
    nargs="?",
)
add_recipe_args.add_argument(
    "categories", type=str, help="List of tags to be included in the new recipe"
)
add_recipe_args.add_argument("datasets", type=str, help="The dataset to be used")
add_recipe_args.add_argument(
    "-p",
    "--prompt_templates",
    type=str,
    help="List of prompt templates to be included in the new recipe",
    nargs="?",
)
add_recipe_args.add_argument(
    "metrics", type=str, help="List of metrics to be included in the new recipe"
)
add_recipe_args.add_argument(
    "-g",
    "--grading_scale",
    type=str,
    help="Dict of grading scale for the metric to be included in the new recipe",
    nargs="?",
)

# Update recipe arguments
update_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Update a recipe.",
    epilog="Available keys for updating a recipe: \n"
    "  name: The name of the recipe. \n"
    "  description: The description of the recipe. \n"
    "  tags: A list of tags associated with the recipe. \n"
    "  categories: A list of categories used in the recipe. \n"
    "  datasets: A list of datasets used in the recipe. \n"
    "  prompt_templates: A list of prompt templates for the recipe. \n"
    "  metrics: A list of metrics to evaluate the recipe. \n"
    "  grading_scale: A list of grading scale used in the recipe. \n\n"
    "Example command:\n"
    "  update_recipe my-new-recipe \"[('name', 'My Updated Recipe'), ('tags', ['fairness', 'bbq'])]\" ",
)
update_recipe_args.add_argument("recipe", type=str, help="Id of the recipe")
update_recipe_args.add_argument(
    "update_values", type=str, help="Update recipe key/value"
)

# View recipe arguments
view_recipe_args = cmd2.Cmd2ArgumentParser(
    description="View a recipe.",
    epilog="Example:\n view_recipe my-new-recipe",
)
view_recipe_args.add_argument("recipe", type=str, help="Id of the recipe")

# Delete recipe arguments
delete_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Delete a recipe.",
    epilog="Example:\n delete_recipe my-new-recipe",
)
delete_recipe_args.add_argument("recipe", type=str, help="Id of the recipe")

# Run recipe arguments
run_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Run a recipe.",
    epilog="Example:\n run_recipe "
    '"my new recipe runner" '
    "\"['bbq','mmlu']\" "
    "\"['openai-gpt35-turbo']\" "
    '-n 1 -r 1 -s "You are an intelligent AI" ',
)
run_recipe_args.add_argument("name", type=str, help="Name of recipe runner")
run_recipe_args.add_argument("recipes", type=str, help="List of recipes to run")
run_recipe_args.add_argument("endpoints", type=str, help="List of endpoints to run")
run_recipe_args.add_argument(
    "-n",
    "--prompt_selection_percentage",
    type=int,
    default=100,
    help="Percentage of prompts to run",
)
run_recipe_args.add_argument(
    "-r", "--random_seed", type=int, default=0, help="Random seed number"
)
run_recipe_args.add_argument(
    "-s", "--system_prompt", type=str, default="", help="System Prompt to use"
)
run_recipe_args.add_argument(
    "-l",
    "--runner_proc_module",
    type=str,
    default="benchmarking",
    help="Runner processing module to use",
)
run_recipe_args.add_argument(
    "-o",
    "--result_proc_module",
    type=str,
    default="benchmarking-result",
    help="Result processing module to use",
)

# List recipe arguments
list_recipes_args = cmd2.Cmd2ArgumentParser(
    description="List all recipes.",
    epilog='Example:\n list_recipes -f "mmlu"',
)

list_recipes_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find recipe(s) with keyword",
    nargs="?",
)

list_recipes_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate recipes(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
