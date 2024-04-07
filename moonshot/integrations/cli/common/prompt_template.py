from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_all_prompt_template_detail

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


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_prompt_templates(prompt_templates):
    """
    Display the details of the prompt templates on the console.

    Args:
        prompt_templates (list): A list of dictionaries, each containing the details of a prompt template.
    """
    table = Table(
        "No.",
        "Prompt Name",
        "Prompt Description",
        "Prompt Template",
    )
    if prompt_templates:
        for prompt_index, prompt_template in enumerate(prompt_templates, 1):
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
