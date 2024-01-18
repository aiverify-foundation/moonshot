import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_prompt_template_names, api_get_prompt_templates
from moonshot.src.redteaming.session import Session

console = Console()


def use_prompt_template(args) -> None:
    """
    Use a prompt template by specifying its name while user is in a session.
    """
    new_prompt_template_name = args.prompt_template
    # Check if current session exists
    if Session.current_session:
        Session.current_session.set_prompt_template(new_prompt_template_name)
        print(
            f"Updated session: {Session.current_session.get_session_id()}. "
            f"Prompt Template: {Session.current_session.get_session_prompt_template()}."
        )


def list_prompt_templates() -> None:
    """
    List all prompt templates available.
    """
    prompt_template_list = api_get_prompt_templates()
    table = Table(
        "No.",
        "Prompt Name",
        "Prompt Description",
        "Prompt Template",
    )
    if prompt_template_list:
        for prompt_index, prompt_template in enumerate(prompt_template_list, 1):
            (
                prompt_name,
                prompt_description,
                prompt_template_contents,
            ) = prompt_template.values()

            table.add_section()
            table.add_row(
                str(prompt_index),
                prompt_name,
                prompt_description,
                prompt_template_contents,
            )
        console.print(table)
    else:
        console.print("[red]There are no prompt templates found.[/red]")


def clear_prompt_template() -> None:
    """
    Resets the prompt template in a session.
    """
    # Check if current session exists
    if Session.current_session:
        Session.current_session.set_prompt_template()
        print(
            f"Updated session: {Session.current_session.get_session_id()}. "
            f"Prompt Template: {Session.current_session.get_session_prompt_template()}."
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
    choices=api_get_prompt_template_names(),
)
