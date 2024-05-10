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
