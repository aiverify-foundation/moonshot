from pydantic import validate_call

from moonshot.src.redteaming.attack.context_strategy import ContextStrategy


# ------------------------------------------------------------------------------
# Context Strategy APIs
# ------------------------------------------------------------------------------
def api_get_all_context_strategies() -> list[str]:
    """
    Retrieves and returns the names of all context strategies currently available.

    This API endpoint interfaces with the `ContextStrategy.get_all_context_strategies` method to fetch a list
    of all context strategy names. It's designed for clients that need to know what context strategies are available for
    use in sessions or other components of the system.

    Returns:
        list[str]: A list of strings, each representing the name of a context strategy.
    """
    return ContextStrategy.get_all_context_strategies()


@validate_call
def api_delete_context_strategy(cs_id: str) -> bool:
    """
    Deletes a context strategy identified by its ID.

    This API endpoint interfaces with the `ContextStrategy.delete` method to remove a context strategy from the system.
    It is used to manage the available context strategies by allowing for their removal when they are no longer needed.

    Args:
        cs_id (str): The unique identifier of the context strategy to be deleted.

    Returns:
        bool: True if the context strategy was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return ContextStrategy.delete(cs_id)


def api_get_all_context_strategy_metadata() -> list[dict]:
    """
    Retrieves metadata for all context strategy modules.

    This function retrieves the metadata for all available context strategies and
    returns a list of metadata dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing the details of a context strategy's metadata.
    """

    return [
        ContextStrategy.load(context_strategy_name).get_metadata()  # type: ignore ; ducktyping
        for context_strategy_name in ContextStrategy.get_all_context_strategies()
    ]
