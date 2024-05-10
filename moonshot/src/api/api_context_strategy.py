from moonshot.src.redteaming.attack.context_strategy import ContextStrategy


# ------------------------------------------------------------------------------
# Context Strategy APIs
# ------------------------------------------------------------------------------
def api_get_all_context_strategies() -> list[str]:
    """
    Retrieves and returns the names of all context strategies currently available.

    This API endpoint interfaces with the `ContextStrategy.get_all_context_strategy_names` method to fetch a list
    of all context strategy names. It's designed for clients that need to know what context strategies are available for
    use in sessions or other components of the system.

    Returns:
        list[str]: A list of strings, each representing the name of a context strategy.
    """
    return ContextStrategy.get_all_context_strategies()


def api_delete_context_strategy(cs_id: str) -> None:
    """
    Deletes a context strategy based on the provided ID.

    This API endpoint interfaces with the `ContextStrategy.delete` method, facilitating the
    removal of a specified context strategy from the system. It is particularly useful for managing the lifecycle of
    context strategies, allowing for the deletion of strategies that are no longer needed or relevant.

    Args:
        cs_id (str): The ID of the context strategy to be deleted

    Returns:
        None: This method does not return a value, but it will remove the specified context strategy from the system.
    """
    ContextStrategy.delete(cs_id)


def api_get_all_context_strategy_metadata() -> list:
    """
    Retrieves metadata for all context strategy modules.

    This function retrieves the metadata for all available context strategies and
    returns a list of metadata dictionaries.

    Returns:
        list: A list of attack module metadata.
    """

    return [
        ContextStrategy.load(context_strategy_name).get_metadata()
        for context_strategy_name in ContextStrategy.get_all_context_strategies()
    ]
