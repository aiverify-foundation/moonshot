from pydantic import validate_call

from moonshot.src.metrics.metric import Metric


# ------------------------------------------------------------------------------
# Metrics APIs
# ------------------------------------------------------------------------------
@validate_call
def api_delete_metric(met_id: str) -> bool:
    """
    Deletes a metric identified by its unique metric ID.

    Args:
        met_id (str): The unique identifier for the metric to be deleted.

    Returns:
        bool: True if the metric was successfully deleted, False otherwise.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return Metric.delete(met_id)


def api_get_all_metric() -> list[dict]:
    """
    Retrieves all available metrics.

    This function calls the get_available_items method from the Metric class to retrieve all available metrics.
    It then returns a list of dictionaries, each containing the details of a metric.

    Returns:
        list[dict]: A list of dictionaries, each representing a metric's details.
    """
    _, metrics_info = Metric.get_available_items()
    return metrics_info


def api_get_all_metric_name() -> list[str]:
    """
    Retrieves all available metric names.

    This function calls the get_available_items method from the Metric class to retrieve all available metrics.
    It then extracts the names of each metric and returns a list of these names.

    Returns:
        list[str]: A list of strings, each representing a metric name.
    """
    metrics_names, _ = Metric.get_available_items()
    return metrics_names
