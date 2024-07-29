import argparse
from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_delete_context_strategy,
    api_get_all_context_strategy_metadata,
    api_update_context_strategy,
)
from moonshot.integrations.cli.active_session_cfg import active_session
from moonshot.integrations.cli.utils.process_data import filter_data
from moonshot.src.redteaming.session.session import Session

console = Console()


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
        else Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
    )

    # Check if current session exists. If it does, update context strategy and number of previous prompts
    if active_session:
        try:
            api_update_context_strategy(
                active_session["session_id"], new_context_strategy_name
            )
            active_session["context_strategy"] = new_context_strategy_name
            active_session["cs_num_of_prev_prompts"] = num_of_prev_prompts
            print(
                f"Updated session: {active_session['session_id']}. "
                f"Context Strategy: {active_session['context_strategy']}."
                f"No. of previous prompts for Context Strategy: {active_session['cs_num_of_prev_prompts']}."
            )
        except Exception as e:
            print(f"[use_context_strategy]: {str(e)}")

    else:
        print(
            "There is no active session. Activate a session to send a prompt with a context strategy."
        )


def list_context_strategies(args) -> list | None:
    """
    List all context strategies available.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find context strategies with a keyword.
        pagination (str): Optional field to paginate context strategies.

    Returns:
        list | None: A list of ContextStrategy or None if there is no result.
    """
    try:
        context_strategy_metadata_list = api_get_all_context_strategy_metadata()
        keyword = args.find.lower() if args.find else ""
        pagination = literal_eval(args.pagination) if args.pagination else ()

        if context_strategy_metadata_list:
            filtered_context_strategies_list = filter_data(
                context_strategy_metadata_list, keyword, pagination
            )
            if filtered_context_strategies_list:
                _display_context_strategies(filtered_context_strategies_list)
                return filtered_context_strategies_list

        console.print("[red]There are no context strategies found.[/red]")
        return None

    except Exception as e:
        print(f"[list_context_strategies]: {str(e)}")


def clear_context_strategy() -> None:
    """
    Resets the context in a session.
    """
    # Check if current session exists
    if active_session:
        try:
            api_update_context_strategy(active_session["session_id"], "")
            active_session["context_strategy"] = ""
            print("Cleared context strategy.")
        except Exception as e:
            print(f"[clear_context_strategy: {str(e)}]")
    else:
        print(
            "There is no active session. Activate a session to send a prompt with a context strategy."
        )


def delete_context_strategy(args) -> None:
    """
    Deletes a context strategy after confirming with the user.

    Args:
        args (object): The arguments object. It should have a 'context_strategy' attribute
                       which is the ID of the context strategy to delete.
    """
    # Confirm with the user before deleting a context strategy
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the context strategy (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Context strategy deletion cancelled.[/]")
        return
    try:
        api_delete_context_strategy(args.context_strategy)
        print("[delete_context_strategy]: Context strategy deleted.")
    except Exception as e:
        print(f"[delete_context_strategy]: {str(e)}")


def _display_context_strategies(context_strategies: list) -> None:
    """
    Display a list of context strategies.

    This function takes a list of context strategies and displays them in a table format. If the list is empty,
    it prints a message indicating that no attack modules were found.

    Args:
        context_strategies (list): A list of context strategies.

    Returns:
        None
    """
    table = Table(
        title="Context Strategy List",
        show_lines=True,
        expand=True,
        header_style="bold",
    )
    table.add_column("No.", justify="left", width=2)
    table.add_column("Context Strategy Information", justify="left", width=98)
    for idx, context_strategy_data in enumerate(context_strategies, 1):
        context_strategy_data_str = ""
        for k, v in context_strategy_data.items():
            if k != "idx":
                context_strategy_data_str += f"[blue]{k.capitalize()}:[/blue] {v}\n\n"
        table.add_row(str(idx), context_strategy_data_str)
    console.print(table)


# Use context strategy arguments
use_context_strategy_args = cmd2.Cmd2ArgumentParser(
    description="Use a context strategy.",
    epilog="Example:\n use_context_strategy my_strategy_one",
)
use_context_strategy_args.add_argument(
    "context_strategy",
    type=str,
    help="The ID of the context strategy to use",
)
use_context_strategy_args.add_argument(
    "-n",
    "--num_of_prev_prompts",
    type=int,
    help="The number of previous prompts to use with the context strategy",
    nargs="?",
)

# Delete context strategy arguments
delete_context_strategy_args = cmd2.Cmd2ArgumentParser(
    description="Delete a context strategy.",
    epilog="Example:\n delete_context_strategy add_previous_prompt",
)

delete_context_strategy_args.add_argument(
    "context_strategy", type=str, help="The ID of the context strategy to delete"
)

# List context strategies arguments
list_context_strategies_args = cmd2.Cmd2ArgumentParser(
    description="List all context strategies.",
    epilog='Example:\n list_context_strategies -f "previous_prompt"',
)

list_context_strategies_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find context strategies with keyword",
    nargs="?",
)

list_context_strategies_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate context strategies(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
