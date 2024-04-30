import asyncio

from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.runners.runner import Runner


# ------------------------------------------------------------------------------
# Red teaming APIs
# ------------------------------------------------------------------------------
def api_run_red_teaming(runner: Runner, rt_args: dict) -> None:
    """
    Runs the red teaming process using the provided runner and arguments.

    Args:
        runner (Runner): The runner instance to be used for the red teaming process.
        rt_args (dict): The arguments for the red teaming process.

    Returns:
        None
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.run_red_teaming(rt_args))
    runner.close()


def api_get_all_attack_modules() -> list[str]:
    """
    Retrieves a list of all available attack modules.

    This function calls the `AttackModule.get_available_items` method to obtain the available attack modules
    and returns a list of attack module names.

    Returns:
        list[str]: A list of strings, each denoting the name of an attack module.
    """
    return AttackModule.get_available_items()
