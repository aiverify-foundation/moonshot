from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_prompt_template, api_get_all_prompt_template_detail
from moonshot.integrations.cli.cli_errors import (
    ERROR_COMMON_DELETE_PROMPT_TEMPLATE_PROMPT_TEMPLATE_VALIDATION,
    ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION,
    ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION_1,
    ERROR_COMMON_LIST_PROMPT_TEMPLATES_FIND_VALIDATION,
)
from moonshot.integrations.cli.utils.process_data import filter_data

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_prompt_templates(args) -> list | None:
    """
    List all prompt templates available.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find prompt template(s) with a keyword.
        pagination (str): Optional field to paginate prompt templates.

    Returns:
        list | None: A list of PromptTemplate or None if there is no result.
    """
    try:
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_COMMON_LIST_PROMPT_TEMPLATES_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(
                    ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION_1
                )
        else:
            pagination = ()

        prompt_templates_list = api_get_all_prompt_template_detail()
        keyword = args.find.lower() if args.find else ""

        if prompt_templates_list:
            filtered_prompt_templates_list = filter_data(
                prompt_templates_list, keyword, pagination
            )
            if filtered_prompt_templates_list:
                _display_prompt_templates(filtered_prompt_templates_list)
                return filtered_prompt_templates_list

        console.print("[red]There are no prompt templates found.[/red]")
        return None
    except Exception as e:
        print(f"[list_prompt_templates]: {str(e)}")


def delete_prompt_template(args) -> None:
    """
    Deletes a prompt_template after confirming with the user.

    Args:
        args (object): The arguments object. It should have a 'prompt_template' attribute
                       which is the ID of the prompt template to delete.
    """
    # Confirm with the user before deleting a prompt template
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the prompt template (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Prompt template deletion cancelled.[/]")
        return
    try:
        if (
            args.prompt_template is None
            or not isinstance(args.prompt_template, str)
            or not args.prompt_template
        ):
            raise ValueError(
                ERROR_COMMON_DELETE_PROMPT_TEMPLATE_PROMPT_TEMPLATE_VALIDATION
            )
        api_delete_prompt_template(args.prompt_template)
        print("[delete_prompt_template]: Prompt template deleted.")
    except Exception as e:
        print(f"[delete_prompt_template]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_prompt_templates(prompt_templates) -> None:
    """
    Display the list of prompt templates in a formatted table.

    This function takes a list of prompt templates and displays them in a formatted table.
    Each row in the table represents a prompt template with its ID, name, description, and contents.
    If the list of prompt templates is empty, it prints a message indicating that no prompt templates were found.

    Args:
        prompt_templates (list): A list of dictionaries, each representing a prompt template.
    """
    table = Table(
        title="List of Prompt Templates",
        show_lines=True,
        expand=True,
        header_style="bold",
    )
    table.add_column("No.", width=2)
    table.add_column("Prompt Template", justify="left", width=50)
    table.add_column("Contains", justify="left", width=48, overflow="fold")
    for idx, prompt_template in enumerate(prompt_templates, 1):
        (id, name, description, contents, *other_args) = prompt_template.values()
        idx = prompt_template.get("idx", idx)
        prompt_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"
        table.add_section()
        table.add_row(str(idx), prompt_info, contents)
    console.print(table)


# Delete prompt template arguments
delete_prompt_template_args = cmd2.Cmd2ArgumentParser(
    description="Delete a prompt template.",
    epilog="Example:\n delete_prompt_template squad-shifts",
)

delete_prompt_template_args.add_argument(
    "prompt_template", type=str, help="The ID of the prompt template to delete"
)

# List prompt template arguments
list_prompt_templates_args = cmd2.Cmd2ArgumentParser(
    description="List all prompt templates.",
    epilog='Example:\n list_prompt_templates -f "toxicity"',
)

list_prompt_templates_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find prompt template(s) with keyword",
    nargs="?",
)

list_prompt_templates_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate prompt template(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
