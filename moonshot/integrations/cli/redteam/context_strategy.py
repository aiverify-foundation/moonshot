import argparse

import cmd2
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.api import (
    api_get_all_context_strategy_metadata,
    api_update_context_strategy,
)
from moonshot.integrations.cli.active_session_cfg import active_session

console = Console()

DEFAULT_CONTEXT_STRATEGY_PROMPT = 5


def use_context_strategy(args: argparse.Namespace) -> None:
    """
    Use a context strategy for process the user's prompt (i.e. summarise past 3 prompts and add
    it to the current user's prompt)

    Args:
        args: A namespace with the context strategy parameters. Expected to have 'context_strategy'.
    """
    new_context_strategy_name = args.context_strategy
    num_of_prev_prompts = (
        args.num_of_prev_prompts
        if args.num_of_prev_prompts
        else DEFAULT_CONTEXT_STRATEGY_PROMPT
    )

    # Check if current session exists. If it does, update context strategy and number of previous prompts
    if active_session:
        active_session["context_strategy"] = new_context_strategy_name
        active_session["cs_num_of_prev_prompts"] = num_of_prev_prompts

        api_update_context_strategy(
            active_session["session_id"], new_context_strategy_name
        )
        print(
            f"Updated session: {active_session['session_id']}. "
            f"Context Strategy: {active_session['context_strategy']}."
            f"No. of previous prompts for Context Strategy: {active_session['cs_num_of_prev_prompts']}."
        )
    else:
        print(
            "There is no active session. Activate a session to send a prompt with a context strategy."
        )


def list_context_strategies() -> None:
    """
    List all context strategies available.
    """
    context_strategy_metadata_list = api_get_all_context_strategy_metadata()
    if context_strategy_metadata_list:
        table = Table(title="Context Strategy List", show_lines=True)
        table.add_column("No.", style="dim", width=6)
        table.add_column("Context Strategy Information", justify="left")
        for context_strategy_index, context_strategy_data in enumerate(
            context_strategy_metadata_list, 1
        ):
            context_strategy_data_str = ""
            for k, v in context_strategy_data.items():
                context_strategy_data_str += f"[blue]{k.capitalize()}:[/blue] {v}\n\n"
            table.add_row(str(context_strategy_index), context_strategy_data_str)
        console.print(Panel(table))
    else:
        console.print("[red]There are no context strategies found.[/red]", style="bold")


def clear_context_strategy() -> None:
    """
    Resets the context in a session.
    """
    # Check if current session exists
    if active_session:
        api_update_context_strategy(active_session["session_id"], "")
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
use_context_strategy_args.add_argument(
    "-n",
    "--num_of_prev_prompts",
    type=int,
    help="The number of previous prompts to use with the context strategy",
    nargs="?",
)
