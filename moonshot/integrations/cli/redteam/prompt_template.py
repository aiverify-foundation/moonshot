import argparse

import cmd2
from rich.console import Console

from moonshot.api import api_update_prompt_template
from moonshot.integrations.cli.active_session_cfg import active_session

console = Console()


def use_prompt_template(args: argparse.Namespace) -> None:
    """
    Use a prompt template by specifying its name while user is in a session.

    Args:
        args: A namespace with the prompt template parameters. Expected to have 'prompt_template'.
    """
    new_prompt_template_name = args.prompt_template

    # Check if current session exists
    if active_session:
        try:
            api_update_prompt_template(
                active_session["session_id"], new_prompt_template_name
            )
            active_session["prompt_template"] = new_prompt_template_name
            print(
                f"Updated session: {active_session['session_id']}. "
                f"Prompt Template: {active_session['prompt_template']}."
            )
        except Exception as e:
            print(f"[use_prompt_template]: {str(e)}")
    else:
        print(
            "There is no active session. Activate a session to send a prompt with a prompt template."
        )


def clear_prompt_template() -> None:
    """
    Resets the prompt template in a session.
    """
    # Check if current session exists
    if active_session:
        try:
            api_update_prompt_template(active_session["session_id"], "")
            active_session["prompt_template"] = ""
            print("Cleared prompt template.")
        except Exception as e:
            print(f"[clear_prompt_template: {str(e)}]")
    else:
        print(
            "There is no active session. Activate a session to send a prompt with a prompt template."
        )


# Use prompt template arguments
use_prompt_template_args = cmd2.Cmd2ArgumentParser(
    description="Use a prompt template.",
    epilog="Example:\n use_prompt_template 'analogical-similarity'",
)
use_prompt_template_args.add_argument(
    "prompt_template",
    type=str,
    help="Name of the prompt template",
)
