from moonshot.src.redteaming.attack.attack_module import AttackModule


# ------------------------------------------------------------------------------
# Red teaming APIs
# ------------------------------------------------------------------------------
def api_get_all_attack_modules() -> list[str]:
    """
    Retrieves a list of all available attack modules.

    This function calls the `AttackModule.get_available_items` method to obtain the available attack modules
    and returns a list of attack module names.

    Returns:
        list[str]: A list of strings, each denoting the name of an attack module.
    """
    return AttackModule.get_available_items()


def api_get_all_attack_module_metadata() -> list:
    """
    Retrieves metadata for all available attack modules.

    This function retrieves the metadata for all available attack modules by calling the
    `AttackModule.load_without_am_arguments` method for each attack module and returns a list of metadata dictionaries.

    Returns:
        list: A list of attack module metadata.
    """
    attack_module_ids = AttackModule.get_available_items()
    return [
        AttackModule.load(am_id=attack_module_id).get_metadata()
        for attack_module_id in attack_module_ids
    ]


def api_delete_attack_module(am_id: str) -> None:
    """
    Deletes a specified attack module.

    This function deletes the attack module with the given ID by calling the `AttackModule.delete` method.

    Args:
        am_id (str): The ID of the attack module to delete.

    Returns:
        None
    """
    AttackModule.delete(am_id)
