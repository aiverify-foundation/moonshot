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


def api_get_all_metric_config() -> dict:
    """
    Retrieves the configuration for all metrics.

    This function calls the get_all_metric_config method from the Metric class
    to retrieve the configuration details for all available metrics.

    Returns:
        dict: A dictionary containing the configuration details for all metrics.
    """
    return Metric.get_all_metric_config()


def api_update_metric_config(met_id: str, **kwargs) -> bool:
    """
    Updates the configuration of a specific metric.

    This function updates the configuration of a metric identified by its unique ID.

    Args:
        met_id (str): The unique identifier for the metric configuration to be updated.
        **kwargs: Additional keyword arguments for updating the metric configuration.

    Returns:
        bool: True if the configuration was successfully updated.
    """
    return Metric.update_metric_config(met_id, kwargs)


def api_delete_metric_config(met_id: str) -> bool:
    """
    Deletes the configuration of a specific metric.

    This function deletes the configuration of a metric identified by its unique ID.

    Args:
        met_id (str): The unique identifier for the metric configuration to be deleted.

    Returns:
        bool: True if the configuration was successfully deleted.
    """
    return Metric.delete_metric_config(met_id)
