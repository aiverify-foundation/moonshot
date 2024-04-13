from moonshot.src.report_analysis.report_analysis import ReportAnalysis


# ------------------------------------------------------------------------------
# Report Analysis APIs
# ------------------------------------------------------------------------------
def api_create_report_analysis(ra_id: str, ra_args: dict) -> dict:
    """
    Creates a report analysis.

    This method accepts a report analysis ID and a dictionary of arguments.
    It loads the report analysis by its ID and generates an analysis using the provided arguments.
    It returns the generated analysis.

    Args:
        ra_id (str): The report analysis ID for which to generate an analysis.
        ra_args (dict): The arguments to be used in the generation of the analysis.

    Returns:
        dict: The generated analysis represented as a dictionary.

    Raises:
        Exception: If there is an error during the loading of the ID or the generation of the analysis.
    """
    ra_instance = ReportAnalysis.load(ra_id)
    return ra_instance.generate_analysis(ra_args)  # type: ignore ; ducktyping


def api_read_report_analysis(ra_id: str) -> dict:
    """
    Reads a report analysis.

    This method takes a report analysis ID as input, loads the corresponding report analysis module,
    and retrieves its metadata.
    It returns a dictionary containing the metadata of the report analysis module.

    Args:
        ra_id (str): The ID of the report analysis for which to retrieve metadata.

    Returns:
        dict: A dictionary containing the metadata of the report analysis module.

    Raises:
        Exception: If there is an error during the loading of the module or the retrieval of the metadata.
    """
    ra_instance = ReportAnalysis.load(ra_id)
    return ra_instance.get_metadata()  # type: ignore ; ducktyping


def api_delete_report_analysis(ra_id: str) -> None:
    """
    Deletes a report analysis.

    This method takes a report analysis ID as input, deletes the corresponding Python file from the directory specified
    by `EnvironmentVars.REPORTS_ANALYSIS_MODULES`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        ra_id (str): The ID of the report analysis to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    ReportAnalysis.delete(ra_id)


def api_get_all_report_analysis() -> list[str]:
    """
    Retrieves all available report analysis modules.

    This function calls the get_available_items method from the ReportAnalysis class to retrieve all available report
    analysis modules. It then returns a list of these modules.

    Returns:
        list[str]: A list of strings, each representing a report analysis module.
    """
    return ReportAnalysis.get_available_items()
