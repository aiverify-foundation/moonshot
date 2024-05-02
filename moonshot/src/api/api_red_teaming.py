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
