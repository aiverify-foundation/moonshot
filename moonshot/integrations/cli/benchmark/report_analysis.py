from ast import literal_eval
from collections import defaultdict

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.src.api.api_report_analysis import (
    api_create_report_analysis,
    api_delete_report_analysis,
    api_get_all_report_analysis,
    api_read_report_analysis,
)

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_report_analyses() -> None:
    """
    This function lists all the report analyses.
    It fetches the list of all report analyses from the API and then displays them in a tabular format on the console.
    Each row of the table contains the report analysis index, report analysis id and a string that contains information
    about the report analysis.
    """
    try:
        report_analyses_list = api_get_all_report_analysis()
        display_report_analyses(report_analyses_list)
    except Exception as e:
        print(f"[list_report_analyses]: {str(e)}")


def view_report_analysis(args) -> None:
    """
    View a specific report analysis.

    This function retrieves a specific report analysis by calling the api_read_report_analysis function from the
    moonshot.src.api.api_report_analysis module using the report analysis id provided in the args.
    It then displays the retrieved report analysis using the display_ra_info function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            ra_id (str): The id of the report analysis to view.

    Returns:
        None
    """
    try:
        ra_info = api_read_report_analysis(args.ra_id)
        display_ra_info(args.ra_id, ra_info)
    except Exception as e:
        print(f"[view_report_analysis]: {str(e)}")


def run_report_analysis(args) -> None:
    """
    Initiates and executes a report analysis.

    This function triggers the execution of a specified report analysis by invoking the api_create_report_analysis
    function from the moonshot.src.api.api_report_analysis module. It utilizes the report analysis ID ('ra_id') and a
    set of additional parameters ('kwargs') provided through the 'args' parameter. After the execution, the results of
    the report analysis are presented by calling the display_ra_output function.

    Args:
        args: An argparse namespace object containing the following attributes:
            ra_id (str): The identifier of the report analysis to be executed.
            kwargs (str): A string that represents a dictionary. This dictionary contains additional parameters
            required for the execution of the report analysis.

    Returns:
        None
    """
    try:
        ra_result = api_create_report_analysis(args.ra_id, literal_eval(args.kwargs))
        display_ra_output(ra_result)

    except Exception as e:
        print(f"[run_report_analysis]: {str(e)}")


def delete_report_analysis(args) -> None:
    """
    Delete a specific report analysis.

    This function deletes a specific report analysis by calling the api_delete_report_analysis function from the
    moonshot.src.api.api_report_analysis module using the report analysis id provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            report_analysis (str): The id of the report analysis to delete.

    Returns:
        None
    """
    try:
        api_delete_report_analysis(args.ra_id)
        print("[delete_report_analysis]: Report Analysis module deleted.")
    except Exception as e:
        print(f"[delete_report_analysis]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_ra_output(ra_result: dict) -> None:
    """
    Presents the outcomes of a report analysis execution.

    This function processes and displays the outcomes of a report analysis. It specifically checks if the report
    analysis ID is 'results-comparator' and, in such cases, invokes the `display_ra_results_comparator` function to
    present the findings in detail. For report analysis modules that are not supported, it outputs a message indicating
    the absence of support for those modules.

    Args:
        ra_result (dict): A dictionary representing the outcome of a report analysis. It must include an 'id' key to
        identify the report analysis type, and a 'results' key with the analysis outcomes.

    Returns:
        None
    """
    if ra_result["id"] == "results-comparator":
        display_ra_results_comparator(ra_result["results"])
    else:
        console.print("[red]Display for report analysis module not supported.[/red]")


def display_ra_results_comparator(ra_result: list):
    """
    Display detailed results for the 'results-comparator' report analysis.

    This function takes a list of dictionaries, each representing a result from the 'results-comparator'
    report analysis, and displays them in a detailed, aggregated table format. The table includes columns for Cookbook,
    Recipe, Dataset, Prompt Template, and a dynamic set of columns for each unique combination of result_id and
    endpoint_id found in the input data. Each row represents a unique combination of cookbook_id, recipe_id, dataset_id,
    and prompt_template, with the corresponding metrics aggregated across different result_id and endpoint_id
    combinations.

    Args:
        ra_result (list): A list of dictionaries, where each dictionary contains the keys 'cookbook_id', 'recipe_id',
            'dataset_id', 'prompt_template', 'result_id', 'endpoint_id', and 'metrics'. Each dictionary represents a
            single result from the 'results-comparator' report analysis.

    Returns:
        None
    """
    if ra_result:
        # Gather the unique number of result_id and endpoint_id
        unique_result_ids = {item["result_id"] for item in ra_result}
        unique_endpoint_ids = {item["endpoint_id"] for item in ra_result}

        # Initialize a dictionary to hold aggregated data
        aggregated_data = defaultdict(
            lambda: defaultdict(lambda: "-")
        )  # Default value for metrics is "-"

        # Aggregate data
        for row in ra_result:
            key = (
                row["cookbook_id"],
                row["recipe_id"],
                row["dataset_id"],
                row["prompt_template"],
            )
            result_key = (row["result_id"], row["endpoint_id"])
            # Assuming you want to display some metric or value from the row, here it's set to row["metrics"]
            aggregated_data[key][result_key] = row["metrics"]

        # table columns
        table_columns = ["Cookbook", "Recipe", "Dataset", "Prompt Template"]
        column_index_map = {}
        index = 4  # Starting index for result_id | endpoint_id columns

        for res_id in unique_result_ids:
            for ep_id in unique_endpoint_ids:
                table_columns.append(f"{res_id} | {ep_id}")
                column_index_map[(res_id, ep_id)] = index
                index += 1

        table = Table(*table_columns)
        table.add_section()

        # Add aggregated data to the table
        for key, results in aggregated_data.items():
            row_entries = ["-"] * len(table_columns)
            row_entries[0:4] = key  # Set the first four columns from the key

            for result_key, metric in results.items():
                result_position = column_index_map.get(result_key)
                if result_position is not None:
                    row_entries[result_position] = metric

            table.add_row(*row_entries)
        console.print(table)
    else:
        console.print("[red]No results found for results-comparator.[/red]")


def display_ra_info(ra_id: str, ra_info: dict):
    """
    Display a specific report analysis.

    This function takes a report analysis id and a dictionary of report analysis information and displays them in a
    table format. If the id or info is not provided, it prints a message indicating that the report analysis was
    not found.

    Args:
        ra_id (str): The id of the report analysis.
        ra_info (dict): A dictionary of report analysis information.

    Returns:
        None
    """
    if ra_id and ra_info:
        table = Table("Report Analysis Id", "Metadata")
        table.add_section()

        # format ra_info into str
        ra_info_str = ""
        for ra_info_key, ra_info_value in ra_info.items():
            ra_info_str += f"[blue]{ra_info_key}:[/blue]\n{ra_info_value}\n\n"
        table.add_row(str(ra_id), ra_info_str)
        console.print(table)
    else:
        console.print("[red]Report analysis module not found.[/red]")


def display_report_analyses(report_analyses_list):
    """
    Display a list of report analyses.

    This function takes a list of report analyses and displays them in a table format. If the list is empty, it prints a
    message indicating that no report analyses were found.

    Args:
        report_analyses_list (list): A list of report analyses. Each report analysis is a dictionary with keys 'id',
        'name', 'description', 'tags', 'datasets', 'prompt_templates', and 'metrics'.

    Returns:
        None
    """
    if report_analyses_list:
        table = Table("No.", "Report Analysis Id")
        for ra_id, ra in enumerate(report_analyses_list, 1):
            table.add_section()
            table.add_row(str(ra_id), ra)
        console.print(table)
    else:
        console.print("[red]There are no report analysis modules found.[/red]")


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# View report analysis arguments
view_report_analysis_args = cmd2.Cmd2ArgumentParser(
    description="View a report analysis.",
    epilog="Example:\n view_report_analysis my-new-report-analysis",
)
view_report_analysis_args.add_argument(
    "ra_id", type=str, help="Id of the report analysis module"
)

# Delete report analysis arguments
delete_report_analysis_args = cmd2.Cmd2ArgumentParser(
    description="Delete a report analysis.",
    epilog="Example:\n delete_report_analysis my-new-report-analysis",
)
delete_report_analysis_args.add_argument(
    "ra_id", type=str, help="Id of the report analysis module"
)

# Run report analysis arguments
run_report_analysis_args = cmd2.Cmd2ArgumentParser(
    description="Run report analyses.",
    epilog="Example:\n run_report_analyses "
    "'my-new-report-analysis' "
    "\"{'runs_id':['runs1','runs2'],'endpoints_id':['test-openai-endpoint']}\" ",
)
run_report_analysis_args.add_argument(
    "ra_id", type=str, help="Id of report analysis module"
)
run_report_analysis_args.add_argument(
    "kwargs",
    type=str,
    help="Additional arguments in dictionary format",
)
