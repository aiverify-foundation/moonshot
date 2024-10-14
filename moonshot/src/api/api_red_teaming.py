from pydantic import validate_call

from moonshot.src.redteaming.attack.attack_module import AttackModule


# ------------------------------------------------------------------------------
# Red teaming APIs
# ------------------------------------------------------------------------------
def api_get_all_attack_modules() -> list[str]:
    """
    Retrieves all available attack module IDs.

    This function calls the `get_available_items` method from the `AttackModule` class to retrieve all available
    attack modules. It then extracts the IDs of each attack module and returns a list of these IDs.

    Returns:
        list[str]: A list of strings, each representing an attack module ID.
    """
    attack_modules_ids, _ = AttackModule.get_available_items()
    return attack_modules_ids


def api_get_all_attack_module_metadata() -> list[dict]:
    """
    Retrieves metadata for all available attack modules.

    This function calls the `get_available_items` method from the `AttackModule` class to retrieve all available
    attack modules. It then extracts the metadata for each attack module and returns a list of dictionaries,
    each containing the metadata of an attack module.

    Returns:
        list[dict]: A list of dictionaries, each representing the metadata of an attack module.
    """
    _, attack_modules_metadata = AttackModule.get_available_items()
    return attack_modules_metadata


@validate_call
def api_delete_attack_module(am_id: str) -> bool:
    """
    Deletes an attack module by its identifier.

    This function takes an attack module ID as input and calls the `delete` method from the `AttackModule` class
    to remove the specified attack module from storage.

    Args:
        am_id (str): The unique identifier of the attack module to be deleted.

    Returns:
        bool: True if the attack module was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return AttackModule.delete(am_id)
