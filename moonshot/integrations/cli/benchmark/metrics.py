import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_metric, api_get_all_metric, api_get_all_metric_name
from moonshot.src.utils.find_feature import find_keyword

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_metrics(args) -> list | None:
    """
    List all available metrics.

    This function retrieves all available metrics by calling the api_get_all_metric function from the
    moonshot.api module. It then displays the metrics using the display_metrics function. If an exception occurs,
    it prints an error message.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find metric(s) with a keyword.

    Returns:
        list | None: A list of Metric or None if there is no result.
    """
    try:
        print("Listing metrics may take a while...")
        metrics_list = api_get_all_metric()
        keyword = args.find.lower() if args.find else ""
        if keyword:
            filtered_metrics_list = find_keyword(keyword, metrics_list)
            if filtered_metrics_list:
                display_metrics(filtered_metrics_list)
                return filtered_metrics_list
            else:
                print("No metrics containing keyword found.")
                return None
        else:
            display_metrics(metrics_list)
            return metrics_list
    except Exception as e:
        print(f"[list_metrics]: {str(e)}")


def view_metric(args) -> None:
    """
    View a specific metric.

    This function retrieves all available metrics and their names by calling the api_get_all_metric and
    api_get_all_metric_name functions. It then finds the metric with the name specified in args.metric_filename
    and displays it using the display_metrics function. If an exception occurs, it prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            metric_filename (str): The name of the metric to view.

    Returns:
        None
    """
    try:
        print("Viewing metrics may take a while...")
        metrics_list = api_get_all_metric()
        metrics_name_list = api_get_all_metric_name()

        # Find the index of the metric with the name args.metric_filename
        metric_index = metrics_name_list.index(args.metric_filename)
        # Pass the corresponding metric from metrics_list to display_metrics
        display_metrics([metrics_list[metric_index]])

    except Exception as e:
        print(f"[view_metric]: {str(e)}")


def delete_metric(args) -> None:
    """
    Delete a metric.

    This function deletes a metric with the specified identifier. It prompts the user for confirmation before proceeding
    with the deletion. If the user confirms, it calls the api_delete_metric function from the moonshot.api module to
    delete the metric. If the deletion is successful, it prints a confirmation message. If an exception occurs, it
    prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            metric (str): The identifier of the metric to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a metric
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the metric (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Metric deletion cancelled.[/]")
        return
    try:
        api_delete_metric(args.metric)
        print("[delete_metric]: Metric deleted.")
    except Exception as e:
        print(f"[delete_metric]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_metrics(metrics_list: list):
    """
    Displays a list of metrics in a table format.

    This function takes a list of metrics and displays them in a table format with each metric's ID, name, and
    description. If the list is empty, it prints a message indicating that no metrics are found.

    Args:
        metrics_list (list): A list of dictionaries, where each dictionary contains the details of a metric.

    Returns:
        None
    """
    if metrics_list:
        table = Table(
            title="List of Metrics", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", width=2)
        table.add_column("Metric", justify="left", width=78)
        for metric_no, metric in enumerate(metrics_list, 1):
            id, name, description = metric.values()
            result_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"

            table.add_section()
            table.add_row(str(metric_no), result_info)
        console.print(table)
    else:
        console.print("[red]There are no metrics found.[/red]")


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# View metric arguments
view_metric_args = cmd2.Cmd2ArgumentParser(
    description="View a metric file.",
    epilog="Example:\n view_metric my-new-metric",
)
view_metric_args.add_argument(
    "metric_filename", type=str, help="Name of the metric file"
)

# Delete metric arguments
delete_metric_args = cmd2.Cmd2ArgumentParser(
    description="Delete a metric.",
    epilog="Example:\n delete_metric my-new-metric",
)
delete_metric_args.add_argument("metric", type=str, help="Name of the metric")

# List metric arguments
list_metrics_args = cmd2.Cmd2ArgumentParser(
    description="List all metrics.",
    epilog='Example:\n list_metrics -f "exact"',
)

list_metrics_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find metric(s) with keyword",
    nargs="?",
)
