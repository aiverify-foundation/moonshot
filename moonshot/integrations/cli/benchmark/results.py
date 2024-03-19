import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_get_all_result,
    api_get_all_result_name,
    api_read_result,
    api_read_results,
)
from moonshot.integrations.cli.benchmark.cookbook import generate_cookbook_table
from moonshot.integrations.cli.benchmark.recipe import generate_recipe_table

console = Console()


def list_results() -> None:
    """
    Get a list of available results.
    """
    results_list = api_get_all_result_name()
    if results_list:
        table = Table("No.", "Result Id")
        for result_id, result in enumerate(results_list, 1):
            table.add_section()
            table.add_row(str(result_id), result)
        console.print(table)
    else:
        console.print("[red]There are no results found.[/red]")


def view_results(args) -> None:
    """
    View recipe or cookbook results.
    """
    results = api_read_result(args.results_filename)
    if not results:
        console.print("[red]There are no results found.[/red]")
        return

    if args.results_filename.startswith("cookbook"):
        # find out the endpoints first
        endpoints = []
    #         for cookbook_name, cookbook_results in results.items():
    #             for recipe_endpoint, _ in cookbook_results.items():
    #                 _, endpoint_name = recipe_endpoint.split("_")
    #                 if endpoint_name not in endpoints:
    #                     endpoints.append(endpoint_name)

    #         # Display cookbook results
    #         generate_cookbook_table(endpoints, results)

    elif args.results_filename.startswith("recipe"):
        # find out the endpoints and recipes first
        endpoints = []
        recipes = []
        print(results)
        #         for recipe_endpoint, recipe_endpoint_data in results.items():
        #             recipe_name, endpoint_name = recipe_endpoint.split("_")
        #             if recipe_name not in recipes:
        #                 recipes.append(recipe_name)

        #             if endpoint_name not in endpoints:
        #                 endpoints.append(endpoint_name)

        #         # Display recipe results with reversed recipes and endpoints
        #         generate_recipe_table(recipes, endpoints, results)
        data_transformation_stages = current_pipeline[:-1]
    else:
        # unknown results
        console.print(
            f"[red]Unable to view results. Unknown results ({args.results_filename}).[/red]"
        )


# View results arguments
view_results_args = cmd2.Cmd2ArgumentParser(
    description="View a results file.",
    epilog="Example:\n view_results recipe-20231125-181832",
)
view_results_args.add_argument(
    "results_filename", type=str, help="Name of the results file"
)
