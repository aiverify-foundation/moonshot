from moonshot.src.reports.report_module import ReportModule


# ------------------------------------------------------------------------------
# Report Module APIs
# ------------------------------------------------------------------------------
def api_delete_report_module(report_module_id: str) -> None:
    """
    Deletes a report module by its ID.

    This function calls the delete method of the ReportModule class to remove a report module
    using the provided report_module_id.

    Args:
        report_module_id (str): The unique identifier of the report module to be deleted.
    """
    ReportModule.delete(report_module_id)


def api_get_all_report_module() -> list[str]:
    """
    Retrieves all available report modules.

    This function calls the get_available_items method of the ReportModule class to retrieve a list
    of all available report modules.

    Returns:
        list[str]: A list of report module identifiers.
    """
    return ReportModule.get_available_items()
