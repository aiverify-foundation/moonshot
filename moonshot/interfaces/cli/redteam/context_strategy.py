import cmd2
from rich.console import Console

from moonshot.src.redteaming.session import Session

console = Console()


def use_context_strategy(args) -> None:
    """
    Use a context strategy for processing previous prompts (i.e. summarise past 3 prompts)
    """
    new_context_strategy = args.context_strategy
    # Check if current session exists
    if Session.current_session:
        Session.current_session.set_context_strategy(new_context_strategy)
        print(
            f"Updated session: {Session.current_session.get_session_id()}. "
            f"Context Strategy: {Session.current_session.get_session_context_strategy()}."
        )


def clear_context_strategy() -> None:
    """
    Resets the context in a session.
    """
    # Check if current session exists
    if Session.current_session:
        Session.current_session.set_context_strategy("")
        print(
            f"Updated session: {Session.current_session.get_session_id()}. "
            f"Context Strategy: {Session.current_session.get_session_context_strategy()}."
        )


# Use context strategy arguments
use_context_strategy_args = cmd2.Cmd2ArgumentParser(
    description="Use a context strategy.",
    epilog="Example:\n use_context_strategy my_strategy_one",
)
use_context_strategy_args.add_argument(
    "context_strategy", type=str, help="The name of the context strategy to use"
)
