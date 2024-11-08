from pydantic import conlist, validate_call

from moonshot.src.results.result import Result


# ------------------------------------------------------------------------------
# Result APIs
# ------------------------------------------------------------------------------
@validate_call
def api_read_result(res_id: str) -> dict:
    """
    Reads a result and returns its information.

    This function takes a result ID as input, reads the corresponding result from the storage manager,
    and returns a dictionary containing the result's information.

    Args:
        res_id (str): The ID of the result.

    Returns:
        dict: A dictionary containing the result's information.
    """
    return Result.read(res_id)


@validate_call
def api_read_results(res_ids: conlist(str, min_length=1)) -> list[dict]:
    """
    Reads multiple results and returns their information.

    This function takes a list of result IDs as input, reads the corresponding results from the storage manager,
    and returns a list of dictionaries, each containing a result's information.

    Args:
        res_ids (conlist(str, min_length=1)): A list of result IDs.

    Returns:
        list[dict]: A list of dictionaries, each containing a result's information.
    """
    return [Result.read(res_id) for res_id in res_ids]


@validate_call
def api_delete_result(res_id: str) -> bool:
    """
    Deletes a result by its identifier.

    This function takes a result ID as input and calls the delete method from the Result class
    to remove the specified result from storage.

    Args:
        res_id (str): The unique identifier of the result to be deleted.

    Returns:
        bool: True if the result was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return Result.delete(res_id)


def api_get_all_result() -> list[dict]:
    """
    This function retrieves all available results and returns them as a list of dictionaries.

    This function calls the get_available_items method from the Result class to retrieve all available results.
    It then returns a list of dictionaries, each containing the details of a result.

    Returns:
        list[dict]: A list of dictionaries, each representing a result's details.
    """
    _, results = Result.get_available_items()
    return [result for result in results]


def api_get_all_result_name() -> list[str]:
    """
    This function retrieves all available result names and returns them as a list.

    This function calls the get_available_items method from the Result class to retrieve all available results.
    It then extracts the names of each result and returns a list of these names.

    Returns:
        list[str]: A list of result names.
    """
    results_name, _ = Result.get_available_items()
    return results_name
