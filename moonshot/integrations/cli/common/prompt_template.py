from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_all_prompt_template_detail

console = Console()


def list_prompt_templates() -> None:
    """
    List all prompt templates available.
    """
    prompt_template_list = api_get_all_prompt_template_detail()
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
