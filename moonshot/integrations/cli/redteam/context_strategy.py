import cmd2
from rich.console import Console

from moonshot.api import api_get_all_context_strategy_name, api_update_context_strategy
from moonshot.src.configs.active_session_cfg import active_session
import argparse

console = Console()


def use_context_strategy(args: argparse.Namespace) -> None:
    """
    Use a context strategy for process the user's prompt (i.e. summarise past 3 prompts and add
    it to the current user's prompt)

    Args:
        args: A namespace with the context strategy parameters. Expected to have 'context_strategy'.
    """
    new_context_strategy_name = args.context_strategy
    # Check if current session exists
    if active_session:
        active_session["context_strategy"] = new_context_strategy_name
        api_update_context_strategy(
            active_session["session_id"], new_context_strategy_name
        )
        print(
            f"Updated session: {active_session['session_id']}. "
            f"Context Strategy: {active_session['context_strategy']}."
        )
    else:
        print(
            "There is no active session. Activate a session to send a prompt with a context strategy."
        )


def list_context_strategies() -> None:
    """
    List all context strategies available.
    """
    list_of_context_strategies = api_get_all_context_strategy_name()
    print(*list_of_context_strategies)


def clear_context_strategy() -> None:
    """
    Resets the context in a session.
    """
    # Check if current session exists
    if active_session:
        active_session["context_strategy"] = ""
        print("Cleared context strategy.")
    else:
        print(
            "There is no active session. Activate a session to send a prompt with a context strategy."
        )


# Use context strategy arguments
use_context_strategy_args = cmd2.Cmd2ArgumentParser(
    description="Use a context strategy.",
    epilog="Example:\n use_context_strategy my_strategy_one",
)
use_context_strategy_args.add_argument(
    "context_strategy",
    type=str,
    help="The name of the context strategy to use",
)
