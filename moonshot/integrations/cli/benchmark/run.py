import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_all_executor

# from moonshot.api import api_get_all_runs, api_load_run
# from moonshot.integrations.cli.benchmark.cookbook import generate_cookbook_table
# from moonshot.integrations.cli.benchmark.recipe import generate_recipe_table
# from moonshot.src.benchmarking.run import RunTypes

console = Console()


def list_runs() -> None:
    """
    Get a list of available runs.
    """
    runs_list = api_get_all_executor()
    if runs_list:
        table = Table("No.", "Run id", "Contains")
        for run_index, run_data in enumerate(runs_list, 1):
            (
                run_id,
                run_type,
                arguments,
                start_time,
                end_time,
                duration,
                db_file,
                filepath,
                recipes,
                cookbooks,
                endpoints,
                num_of_prompts,
                results,
            ) = run_data.values()
            run_info = f"[red]id: {run_id}[/red]\n"

            contains_info = ""
            if recipes:
                contains_info += f"[blue]Recipes:[/blue]\n{recipes}\n\n"
            elif cookbooks:
                contains_info += f"[blue]Cookbooks:[/blue]\n{cookbooks}\n\n"
            contains_info += f"[blue]Endpoints:[/blue]\n{endpoints}\n\n"
            contains_info += f"[blue]Number of Prompts:[/blue]\n{num_of_prompts}\n\n"
            contains_info += f"[blue]Database path:[/blue]\n{db_file}"

            table.add_section()
            table.add_row(str(run_index), run_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no runs found.[/red]")


# def resume_run(args) -> None:
#     """
#     Resume an interrupted run with the specified run id.
#     """
#     run_id = args.run_id

#     resume_run_instance = api_load_run(run_id)
#     resume_run_results = resume_run_instance.create_run()
#     if (
#         resume_run_results
#         and resume_run_instance.run_metadata.run_type == RunTypes.RECIPE
#     ):
#         # Display recipe results
#         generate_recipe_table(
#             resume_run_instance.run_metadata.recipes,
#             resume_run_instance.run_metadata.endpoints,
#             resume_run_results,
#         )
#         console.print(
#             f"[blue]Results saved in {resume_run_instance.run_metadata.filepath}[/blue]"
#         )

#     elif (
#         resume_run_results
#         and resume_run_instance.run_metadata.run_type == RunTypes.COOKBOOK
#     ):
#         # Display cookbook results
#         generate_cookbook_table(
#             resume_run_instance.run_metadata.endpoints, resume_run_results
#         )
#         console.print(
#             f"[blue]Results saved in {resume_run_instance.run_metadata.filepath}[/blue]"
#         )

#     else:
#         console.print("[red]There are no results.[/red]")

#     # Print run stats
#     console.print(resume_run_instance.get_run_stats())


# Resume run arguments
resume_run_args = cmd2.Cmd2ArgumentParser(
    description="Resume an interrupted run.", epilog="Example:\n resume_run 12345"
)
resume_run_args.add_argument("run_id", type=str, help="id of the run to resume")
