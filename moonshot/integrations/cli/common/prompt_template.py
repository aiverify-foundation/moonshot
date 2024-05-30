import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_delete_prompt_template, api_get_all_prompt_template_detail

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def list_prompt_templates() -> None:
    """
    List all prompt templates available.
    """
    try:
        prompt_templates = api_get_all_prompt_template_detail()
        display_prompt_templates(prompt_templates)
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
        api_delete_prompt_template(args.prompt_template)
        print("[delete_prompt_template]: Prompt template deleted.")
    except Exception as e:
        print(f"[delete_prompt_template]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_prompt_templates(prompt_templates) -> None:
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
    if prompt_templates:
        for prompt_index, prompt_template in enumerate(prompt_templates, 1):
            (
                id,
                name,
                description,
                contents,
            ) = prompt_template.values()

            prompt_info = f"[red]id: {id}[/red]\n\n[blue]{name}[/blue]\n{description}"
            table.add_section()
            table.add_row(str(prompt_index), prompt_info, contents)
        console.print(table)
    else:
        console.print("[red]There are no prompt templates found.[/red]")


# Delete prompt template arguments
delete_prompt_template_args = cmd2.Cmd2ArgumentParser(
    description="Delete a prompt template.",
    epilog="Example:\n delete_prompt_template squad-shifts",
)

delete_prompt_template_args.add_argument(
    "prompt_template", type=str, help="The ID of the prompt template to delete"
)
