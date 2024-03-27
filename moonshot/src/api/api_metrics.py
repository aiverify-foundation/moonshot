from moonshot.src.metrics.metric import Metric


# ------------------------------------------------------------------------------
# Metrics APIs
# ------------------------------------------------------------------------------
def api_delete_metric(met_id: str) -> None:
    """
    Deletes a metric.

    This method takes a metric ID as input, deletes the corresponding JSON file from the directory specified by
    `EnvironmentVars.METRICS`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        met_id (str): The ID of the metric to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    Metric.delete(met_id)


def api_get_all_metric() -> list[str]:
    """
    Retrieves all available metrics.

    This function calls the get_available_metrics method to retrieve all available metrics.
    It then returns a list of these metrics.

    Returns:
        list[str]: A list of strings, each representing a metric.
    """
    return Metric.get_available_items()
