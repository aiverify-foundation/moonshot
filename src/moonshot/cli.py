import argparse
from ast import literal_eval

import cmd2
from cmd2 import Statement, with_argparser, with_default_category
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.src.benchmarking.cookbook import (
    add_new_cookbook,
    get_all_cookbooks,
    get_cookbook,
)
from moonshot.src.benchmarking.recipe import (
    add_new_recipe,
    get_all_recipes,
    get_recipes,
)
from moonshot.src.benchmarking.results import get_all_results, read_results
from moonshot.src.benchmarking.run import Run, RunTypes, get_all_runs
from moonshot.src.common.connection import (
    add_new_endpoint,
    get_connection_types,
    get_endpoints,
)
from moonshot.src.common.env_variables import __app_name__, __version__
from moonshot.src.common.prompt_template import get_prompt_templates
from moonshot.src.redteaming.session import Session, get_all_sessions
from moonshot.src.utils.timeit import timeit

console = Console()


class CommandLineInterface(cmd2.Cmd):
    # Add new session parser
    new_session_parser = cmd2.Cmd2ArgumentParser(
        description="Add a new red teaming session.",
        epilog="Example:\n new_session 'my_new_session' "
        "'My new session description' "
        "\"['my-openai-gpt35']\"",
    )
    new_session_parser.add_argument("name", type=str, help="Name of the new session")
    new_session_parser.add_argument(
        "description", type=str, help="Description of the new session"
    )
    new_session_parser.add_argument(
        "endpoints",
        type=str,
        help="Endpoints of the new session",
    )

    # Use session parser
    use_session_parser = cmd2.Cmd2ArgumentParser(
        description="Use an existing red teaming session.",
        epilog="Example:\n use_session 'my-session-1'",
    )
    use_session_parser.add_argument(
        "session_id",
        type=str,
        help="The ID of the session that you want to use",
    )

    # Use context strategy parser
    use_context_strategy_parser = cmd2.Cmd2ArgumentParser(
        description="Use a context strategy.",
        epilog="Example:\n use_context_strategy 5",
    )
    use_context_strategy_parser.add_argument(
        "context_strategy", type=int, help="The context strategy to use"
    )

    # Use prompt template parser
    use_prompt_template_parser = cmd2.Cmd2ArgumentParser(
        description="Use a prompt template.",
        epilog="Example:\n use_prompt_template 'analogical-similarity'",
    )
    use_prompt_template_parser.add_argument(
        "prompt_template",
        type=str,
        help="Name of the prompt template",
    )

    # Add endpoint parser
    add_endpoint_parser = cmd2.Cmd2ArgumentParser(
        description="Add a new endpoint.",
        epilog="Example:\n add_endpoint hf-gpt2 my-hf-gpt2 "
        "https://www.api.com/myapi 1234 10 1 \"{'temperature': 0}\"",
    )
    add_endpoint_parser.add_argument(
        "connector_type",
        type=str,
        help="Type of connection for the endpoint",
    )
    add_endpoint_parser.add_argument("name", type=str, help="Name of the new endpoint")
    add_endpoint_parser.add_argument("uri", type=str, help="URI of the new endpoint")
    add_endpoint_parser.add_argument(
        "token", type=str, help="Token of the new endpoint"
    )
    add_endpoint_parser.add_argument(
        "max_calls_per_second",
        type=int,
        help="Max calls per second of the new endpoint",
    )
    add_endpoint_parser.add_argument(
        "max_concurrency", type=int, help="Max concurrency of the new endpoint"
    )
    add_endpoint_parser.add_argument(
        "params", type=str, help="Params of the new endpoint"
    )

    # Add cookbook parser
    add_cookbook_parser = cmd2.Cmd2ArgumentParser(
        description="Add a new cookbook.",
        epilog="Example:\n add_cookbook 'My new cookbook' "
        "'I am cookbook description' "
        "\"['analogical-similarity','auto-categorisation']\"",
    )
    add_cookbook_parser.add_argument("name", type=str, help="Name of the new cookbook")
    add_cookbook_parser.add_argument(
        "description", type=str, help="Description of the new cookbook"
    )
    add_cookbook_parser.add_argument(
        "recipes", type=str, help="List of recipes to be included in the new cookbook"
    )

    # Add recipe parser
    add_recipe_parser = cmd2.Cmd2ArgumentParser(
        description="Add a new recipe.",
        epilog="Example:\n add_recipe 'My new recipe' "
        "'I am recipe description' "
        "\"['tag1','tag2']\" "
        "bbq-lite-age-ambiguous.json "
        "\"['analogical-similarity.json','auto-categorisation.json']\" "
        "\"['bertscore','bleuscore']\"",
    )
    add_recipe_parser.add_argument("name", type=str, help="Name of the new recipe")
    add_recipe_parser.add_argument(
        "description", type=str, help="Description of the new recipe"
    )
    add_recipe_parser.add_argument(
        "tags", type=str, help="List of tags to be included in the new recipe"
    )
    add_recipe_parser.add_argument("dataset", type=str, help="The dataset to be used")
    add_recipe_parser.add_argument(
        "prompt_templates",
        type=str,
        help="List of prompt templates to be included in the new recipe",
    )
    add_recipe_parser.add_argument(
        "metrics", type=str, help="List of metrics to be included in the new recipe"
    )

    # Resume run parser
    resume_run_parser = cmd2.Cmd2ArgumentParser(
        description="Resume an interrupted run.", epilog="Example:\n resume_run 12345"
    )
    resume_run_parser.add_argument("run_id", type=str, help="id of the run to resume")

    # Run cookbook parser
    run_cookbook_parser = cmd2.Cmd2ArgumentParser(
        description="Run a cookbook.",
        epilog="Example:\n run_cookbook "
        "-n 1 "
        "\"['bbq-lite-age-cookbook']\" "
        "\"['my-openai-gpt35']\"",
    )
    run_cookbook_parser.add_argument(
        "cookbooks", type=str, help="List of cookbooks to run"
    )
    run_cookbook_parser.add_argument(
        "endpoints", type=str, help="List of endpoints to run"
    )
    run_cookbook_parser.add_argument(
        "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
    )

    # Run recipe parser
    run_recipe_parser = cmd2.Cmd2ArgumentParser(
        description="Run a recipe.",
        epilog="Example:\n run_recipe "
        "-n 1 "
        "\"['bbq-lite-age-ambiguous','bbq-lite-age-disamb']\" "
        "\"['my-openai-gpt35']\"",
    )
    run_recipe_parser.add_argument("recipes", type=str, help="List of recipes to run")
    run_recipe_parser.add_argument(
        "endpoints", type=str, help="List of endpoints to run"
    )
    run_recipe_parser.add_argument(
        "-n", "--num_of_prompts", type=int, default=0, help="Number of prompts to run"
    )

    # View cookbook parser
    view_cookbook_parser = cmd2.Cmd2ArgumentParser(
        description="View a cookbook.",
        epilog="Example:\n view_cookbook bbq-lite-age-cookbook",
    )
    view_cookbook_parser.add_argument("cookbook", type=str, help="Name of the cookbook")

    # View results parser
    view_results_parser = cmd2.Cmd2ArgumentParser(
        description="View a results file.",
        epilog="Example:\n view_results recipe-20231125-181832",
    )
    view_results_parser.add_argument(
        "results_filename", type=str, help="Name of the results file"
    )

    def __init__(self):
        super().__init__(terminators=[])
        self.prompt = "moonshot > "

    def default(self, statement: Statement) -> None:
        if Session.current_session:
            current_session = Session.current_session
            user_prompt = statement.command + " " + statement
            user_prompt = user_prompt.strip()
            current_session.send_prompt(user_prompt)

            # Update chat display
            RedTeamingCommandSet.update_chat_display()

    def postcmd(self, stop, line):
        if Session.current_session:
            current_session = Session.current_session
            self.prompt = (
                f"moonshot ({current_session.get_session_id()}) "
                f"[PT: {current_session.get_session_prompt_template()}, "
                f"CS: {current_session.get_session_context_strategy()}] > "
            )
        else:
            self.prompt = "moonshot > "
        return stop


@with_default_category("Initialisation")
class InitialisationCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    def do_interactive(self, _: cmd2.Statement) -> None:
        """
        Run the interactive shell.
        """
        # To prevent 'interactive is not a recognized command, alias, or macro' from triggering.
        pass

    @timeit
    def do_list_connect_types(self, _: cmd2.Statement) -> None:
        """
        Get a list of available Language Model (LLM) connection types.
        """
        connection_types = get_connection_types()
        if connection_types:
            table = Table("No.", "Connection Type")
            for connection_id, connection_type in enumerate(connection_types, 1):
                table.add_section()
                table.add_row(str(connection_id), connection_type)
            console.print(table)
        else:
            console.print("[red]There are no connection types found.[/red]")

    @timeit
    def do_list_endpoints(self, _: cmd2.Statement) -> None:
        """
        Get a list of available Language Model (LLM) endpoints.
        """
        endpoints_list = get_endpoints()
        if endpoints_list:
            table = Table(
                "No.",
                "Connection Type",
                "Name",
                "Uri",
                "Token",
                "Max calls per second",
                "Max concurrency",
                "Params",
                "Created Date",
            )
            for endpoint_id, endpoint in enumerate(endpoints_list, 1):
                (
                    connection_type,
                    name,
                    uri,
                    token,
                    max_calls_per_second,
                    max_concurrency,
                    params,
                    created_date,
                ) = endpoint.values()
                table.add_section()
                table.add_row(
                    str(endpoint_id),
                    connection_type,
                    name,
                    uri,
                    token,
                    str(max_calls_per_second),
                    str(max_concurrency),
                    str(params),
                    created_date,
                )
            console.print(table)
        else:
            console.print("[red]There are no endpoints found.[/red]")

    @timeit
    def do_version(self, _: cmd2.Statement) -> None:
        """
        Get the version of the application.
        """
        print(f"{__app_name__} v{__version__}")


@with_default_category("Moonshot Benchmarking")
class BenchmarkingCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

        # Trigger the welcome message
        self.welcome()

    def welcome(self) -> None:
        """
        Display Project Moonshot logo
        """
        logo = "  _____           _           _     __  __                       _           _   \n"
        logo += " |  __ \\         (_)         | |   |  \\/  |                     | |         | |  \n"
        logo += " | |__) | __ ___  _  ___  ___| |_  | \\  / | ___   ___  _ __  ___| |__   ___ | |_ \n"
        logo += " |  ___/ '__/ _ \\| |/ _ \\/ __| __| | |\\/| |/ _ \\ / _ \\| '_ \\/ __| '_ \\ / _ \\| __|\n"
        logo += " | |   | | | (_) | |  __/ (__| |_  | |  | | (_) | (_) | | | \\__ \\ | | | (_) | |_ \n"
        logo += " |_|   |_|  \\___/| |\\___|\\___|\\__| |_|  |_|\\___/ \\___/|_| |_|___/_| |_|\\___/ \\__|\n"
        logo += "                _/ |                                                             \n"
        logo += "               |__/                                                              \n"
        logo += "\n"
        print(logo)

    def generate_recipe_table(
        self, recipes: list, endpoints: list, results: dict
    ) -> None:
        table = Table("", "Recipe", *endpoints)
        for recipe_index, recipe in enumerate(recipes, 1):
            endpoint_results = []
            for endpoint in endpoints:
                # Extract only the results of each prompt template
                tmp_results = {
                    prompt_template_name: prompt_template_results["results"]
                    for prompt_template_name, prompt_template_results in results[
                        f"{recipe}_{endpoint}"
                    ].items()
                }
                endpoint_results.append(str(tmp_results))
            table.add_section()
            table.add_row(str(recipe_index), recipe, *endpoint_results)
        # Display table
        console.print(table)

    def generate_cookbook_table(self, endpoints: list, results: dict) -> None:
        table = Table("", "Cookbook", "Recipe", *endpoints)
        for cookbook_name, cookbook_results in results.items():
            # Get recipe name list
            recipes = []
            for recipe_endpoint, _ in cookbook_results.items():
                recipe_name, _ = recipe_endpoint.split("_")
                if recipe_name not in recipes:
                    recipes.append(recipe_name)

            for recipe_index, recipe in enumerate(recipes, 1):
                endpoint_results = []
                for endpoint in endpoints:
                    # Extract only the results of each prompt template
                    tmp_results = {
                        prompt_template_name: prompt_template_results["results"]
                        for prompt_template_name, prompt_template_results in cookbook_results[
                            f"{recipe}_{endpoint}"
                        ].items()
                    }
                    endpoint_results.append(str(tmp_results))
                table.add_section()
                table.add_row(
                    str(recipe_index), cookbook_name, recipe, *endpoint_results
                )
        # Display table
        console.print(table)

    @timeit
    def do_list_cookbooks(self, _: cmd2.Statement) -> None:
        """
        Get a list of available cookbooks.
        """
        cookbooks_list = get_all_cookbooks()
        if cookbooks_list:
            table = Table("No.", "Cookbook", "Recipes")
            for cookbook_id, cookbook in enumerate(cookbooks_list, 1):
                name, description, recipes, filename = cookbook.values()
                cookbook_info = (
                    f"[red]id: {filename}[/red]\n\n[blue]{name}[/blue]\n{description}"
                )
                recipes_info = "\n".join(
                    f"{i + 1}. {item}" for i, item in enumerate(recipes)
                )
                table.add_section()
                table.add_row(str(cookbook_id), cookbook_info, recipes_info)
            console.print(table)
        else:
            console.print("[red]There are no cookbooks found.[/red]")

    @timeit
    def do_list_recipes(self, _: cmd2.Statement) -> None:
        """
        Get a list of available recipes.
        """
        recipes_list = get_all_recipes()
        if recipes_list:
            table = Table("No.", "Recipe", "Contains")
            for recipe_id, recipe in enumerate(recipes_list, 1):
                (
                    name,
                    description,
                    tags,
                    dataset,
                    prompt_templates,
                    metrics,
                    filename,
                ) = recipe.values()
                recipe_info = f"[red]id: {filename}[/red]\n\n[blue]{name}[/blue]\n{description}\n\nTags:\n{tags}"
                dataset_info = f"[blue]Dataset[/blue]: {dataset}"
                prompt_templates_info = "[blue]Prompt Templates[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(prompt_templates)
                )
                metrics_info = "[blue]Metrics[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(metrics)
                )
                contains_info = (
                    f"{dataset_info}\n{prompt_templates_info}\n{metrics_info}"
                )
                table.add_section()
                table.add_row(str(recipe_id), recipe_info, contains_info)
            console.print(table)
        else:
            console.print("[red]There are no recipes found.[/red]")

    @timeit
    def do_list_results(self, _: cmd2.Statement) -> None:
        """
        Get a list of available results.
        """
        results_list = get_all_results()
        if results_list:
            table = Table("No.", "Result id")
            for result_id, result in enumerate(results_list, 1):
                table.add_section()
                table.add_row(str(result_id), result)
            console.print(table)
        else:
            console.print("[red]There are no results found.[/red]")

    @timeit
    def do_list_runs(self, _: cmd2.Statement) -> None:
        """
        Get a list of available runs.
        """
        runs_list = get_all_runs()
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
                contains_info += (
                    f"[blue]Number of Prompts:[/blue]\n{num_of_prompts}\n\n"
                )
                contains_info += f"[blue]Database path:[/blue]\n{db_file}"

                table.add_section()
                table.add_row(str(run_index), run_info, contains_info)
            console.print(table)
        else:
            console.print("[red]There are no runs found.[/red]")

    @timeit
    @with_argparser(CommandLineInterface.add_endpoint_parser)
    def do_add_endpoint(self, args: argparse.Namespace) -> None:
        """
        Add an endpoint for a Language Model (LLM) connector.
        """
        params_dict = literal_eval(args.params)

        add_new_endpoint(
            args.connector_type,
            args.name,
            args.uri,
            args.token,
            args.max_calls_per_second,
            args.max_concurrency,
            params_dict,
        )

    @timeit
    @with_argparser(CommandLineInterface.add_cookbook_parser)
    def do_add_cookbook(self, args: argparse.Namespace) -> None:
        """
        Add a new cookbook with the specified name, description, and a list of recipes.
        """
        recipes = literal_eval(args.recipes)

        add_new_cookbook(args.name, args.description, recipes)

    @timeit
    @with_argparser(CommandLineInterface.add_recipe_parser)
    def do_add_recipe(self, args: argparse.Namespace) -> None:
        """
        Add a new recipe with the specified name, description, tags, dataset, prompt templates, and a list of metrics.
        """
        tags = literal_eval(args.tags)
        prompt_templates = literal_eval(args.prompt_templates)
        metrics = literal_eval(args.metrics)

        add_new_recipe(
            args.name, args.description, tags, args.dataset, prompt_templates, metrics
        )

    @timeit
    @with_argparser(CommandLineInterface.resume_run_parser)
    def do_resume_run(self, args: argparse.Namespace) -> None:
        """
        Resume an interrupted run with the specified run id.
        """
        run_id = args.run_id

        resume_run_instance = Run.load_run(run_id)
        resume_run_results = resume_run_instance.create_run()
        if (
            resume_run_results
            and resume_run_instance.run_metadata.run_type == RunTypes.RECIPE
        ):
            # Display recipe results
            self.generate_recipe_table(
                resume_run_instance.run_metadata.recipes,
                resume_run_instance.run_metadata.endpoints,
                resume_run_results,
            )
            console.print(
                f"[blue]Results saved in {resume_run_instance.run_metadata.filepath}[/blue]"
            )

        elif (
            resume_run_results
            and resume_run_instance.run_metadata.run_type == RunTypes.COOKBOOK
        ):
            # Display cookbook results
            self.generate_cookbook_table(
                resume_run_instance.run_metadata.endpoints, resume_run_results
            )
            console.print(
                f"[blue]Results saved in {resume_run_instance.run_metadata.filepath}[/blue]"
            )

        else:
            console.print("[red]There are no results.[/red]")

        # Print run stats
        console.print(resume_run_instance.get_run_stats())

    @with_argparser(CommandLineInterface.run_cookbook_parser)
    def do_run_cookbook(self, args: argparse.Namespace) -> None:
        """
        Run cookbooks with the specified list of endpoints.
        """
        cookbooks = literal_eval(args.cookbooks)
        endpoints = literal_eval(args.endpoints)
        num_of_prompts = args.num_of_prompts

        # Run the recipes with the defined endpoints
        cookbook_run = Run(
            RunTypes.COOKBOOK,
            {
                "cookbooks": cookbooks,
                "endpoints": endpoints,
                "num_of_prompts": num_of_prompts,
            },
        )
        cookbook_results = cookbook_run.create_run()
        if cookbook_results:
            # Display recipe results
            self.generate_cookbook_table(endpoints, cookbook_results)
            console.print(
                f"[blue]Results saved in {cookbook_run.run_metadata.filepath}[/blue]"
            )
        else:
            console.print("[red]There are no results.[/red]")

        # Print run stats
        console.print(cookbook_run.get_run_stats())

    @with_argparser(CommandLineInterface.run_recipe_parser)
    def do_run_recipe(self, args: argparse.Namespace) -> None:
        """
        Run recipes with the specified list of endpoints.
        """
        recipes = literal_eval(args.recipes)
        endpoints = literal_eval(args.endpoints)
        num_of_prompts = args.num_of_prompts

        recipe_run = Run(
            RunTypes.RECIPE,
            {
                "recipes": recipes,
                "endpoints": endpoints,
                "num_of_prompts": num_of_prompts,
            },
        )
        recipe_results = recipe_run.create_run()
        if recipe_results:
            # Display recipe results
            self.generate_recipe_table(recipes, endpoints, recipe_results)
            console.print(
                f"[blue]Results saved in {recipe_run.run_metadata.filepath}[/blue]"
            )
        else:
            console.print("[red]There are no results.[/red]")

        # Print run stats
        console.print(recipe_run.get_run_stats())

    @timeit
    @with_argparser(CommandLineInterface.view_cookbook_parser)
    def do_view_cookbook(self, args: argparse.Namespace) -> None:
        """
        Returns a list of available recipes in the cookbook
        """
        cookbook_info = get_cookbook(args.cookbook)
        name, description, recipes = cookbook_info.values()
        recipes_list = get_recipes(recipes)
        if recipes_list:
            table = Table("No.", "Recipe", "Contains")
            for recipes_id, recipe in enumerate(recipes_list, 1):
                (
                    name,
                    description,
                    tags,
                    dataset,
                    prompt_templates,
                    metrics,
                    filename,
                ) = recipe.values()
                recipe_info = f"[red]id: {filename}[/red]\n\n[blue]{name}[/blue]\n{description}\n\nTags:\n{tags}"
                dataset_info = f"[blue]Dataset[/blue]: {dataset}"
                prompt_templates_info = "[blue]Prompt Templates[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(prompt_templates)
                )
                metrics_info = "[blue]Metrics[/blue]:" + "".join(
                    f"\n{i + 1}. {item}" for i, item in enumerate(metrics)
                )
                contains_info = (
                    f"{dataset_info}\n{prompt_templates_info}\n{metrics_info}"
                )
                table.add_section()
                table.add_row(str(recipes_id), recipe_info, contains_info)
            console.print(table)
        else:
            console.print("[red]There are no recipes found for the cookbook.[/red]")

    @timeit
    @with_argparser(CommandLineInterface.view_results_parser)
    def do_view_results(self, args: argparse.Namespace) -> None:
        """
        View recipe or cookbook results.
        """
        results = read_results(args.results_filename)
        if not results:
            console.print("[red]There are no results found.[/red]")
            return

        if args.results_filename.startswith("cookbook"):
            # find out the endpoints first
            endpoints = []
            for cookbook_name, cookbook_results in results.items():
                for recipe_endpoint, _ in cookbook_results.items():
                    _, endpoint_name = recipe_endpoint.split("_")
                    if endpoint_name not in endpoints:
                        endpoints.append(endpoint_name)

            # Display cookbook results
            self.generate_cookbook_table(endpoints, results)

        elif args.results_filename.startswith("recipe"):
            # find out the endpoints and recipes first
            endpoints = []
            recipes = []
            for recipe_endpoint, recipe_endpoint_data in results.items():
                recipe_name, endpoint_name = recipe_endpoint.split("_")
                if recipe_name not in recipes:
                    recipes.append(recipe_name)

                if endpoint_name not in endpoints:
                    endpoints.append(endpoint_name)

            # Display recipe results with reversed recipes and endpoints
            self.generate_recipe_table(recipes, endpoints, results)

        else:
            # unknown results
            console.print(
                f"[red]Unable to view results. Unknown results ({args.results_filename}).[/red]"
            )


@with_default_category("Moonshot RedTeaming")
class RedTeamingCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def update_chat_display() -> None:
        """
        Display chats on console
        """
        if Session.current_session:
            num_of_previous_prompts = 10

            # Get session info for display
            session_chats = Session.current_session.get_session_chats()
            session_previous_prompts = (
                Session.current_session.get_session_previous_prompts(
                    num_of_previous_prompts
                )
            )

            # Prepare for table display
            table = Table(expand=True)
            for chat in session_chats:
                table.add_column(chat.get_id(), justify="center")

            # Check if you need to display any prior prompts
            table_list = []
            for session_previous_prompt in session_previous_prompts:
                # table
                new_table = Table(expand=True)
                new_table.add_column("Prepared Prompts", justify="left", style="cyan")
                new_table.add_column("Prompt/Response", justify="left")
                for prompts in reversed(session_previous_prompt):
                    new_table.add_row(
                        prompts["prepared_prompt"],
                        f"[magenta]{prompts['prompt']}[/magenta] \n|---> [green]{prompts['predicted_result']}[/green]",
                    )
                    new_table.add_section()
                # Add to the table list
                table_list.append(new_table)

            # Append table list to main table
            table.add_row(*table_list)

            # Display table
            panel = Panel.fit(
                Columns([table], expand=True),
                title=Session.current_session.get_session_id(),
                border_style="red",
                title_align="left",
            )
            console.print(panel)
        else:
            console.print("[red]There are no active session.[/red]")

    @timeit
    @with_argparser(CommandLineInterface.new_session_parser)
    def do_new_session(self, args: argparse.Namespace) -> None:
        """
        Add a new session to the session list.
        """
        name = args.name
        description = args.description
        endpoints = literal_eval(args.endpoints)

        # create a new session
        session_instance = Session(name, description, endpoints)

        # set the current session
        Session.current_session = session_instance
        self._cmd.poutput(
            f"Using session: {session_instance.get_session_id()}. "
            f"Session Chats: {session_instance.get_session_chats()}"
        )

        # Display chat
        self.update_chat_display()

    def do_end_session(self, _: cmd2.Statement) -> None:
        """
        End the current session.
        """
        Session.current_session = None

    def do_list_sessions(self, _: cmd2.Statement) -> None:
        """
        List all available sessions.
        """
        session_list = get_all_sessions()
        if session_list:
            table = Table("No.", "Session ID", "Contains")
            for session_index, session_data in enumerate(session_list, 1):
                (
                    session_id,
                    session_name,
                    session_description,
                    session_created_epoch,
                    session_created_datetime,
                    session_endpoints,
                    session_metadata_file,
                    session_chats,
                    session_prompt_template,
                    session_context_strategy,
                    filename,
                ) = session_data.values()
                session_info = f"[red]id: {session_id}[/red]\n\nCreated: {session_created_datetime}"

                contains_info = (
                    f"[blue]{session_name}[/blue]\n{session_description}\n\n"
                )
                contains_info += f"[blue]Endpoints:[/blue]\n{session_endpoints}\n\n"
                contains_info += (
                    f"[blue]Metadata file:[/blue]\n{session_metadata_file}\n\n"
                )
                contains_info += f"[blue]Chat IDs:[/blue]\n{session_chats}"

                table.add_section()
                table.add_row(str(session_index), session_info, contains_info)
            console.print(table)
        else:
            console.print("[red]There are no sessions found.[/red]")

    @with_argparser(CommandLineInterface.use_session_parser)
    def do_use_session(self, args: argparse.Namespace) -> None:
        """
        Use or resume a session by specifying its session ID.
        """
        session_id = args.session_id

        # load a session
        session_instance: Session = Session.load_session(session_id)

        # set the current session
        Session.current_session = session_instance
        self._cmd.poutput(
            f"Using session: {session_instance.get_session_id()}. "
            f"Session Chats: {session_instance.get_session_chats()}"
        )

        # Display chat
        self.update_chat_display()

    @with_argparser(CommandLineInterface.use_context_strategy_parser)
    def do_use_context_strategy(self, args: argparse.Namespace) -> None:
        """
        Use the past n prompts as context from the same chat
        """
        new_context_strategy = args.context_strategy

        # Check if current session exists
        if Session.current_session:
            Session.current_session.set_context_strategy(new_context_strategy)
            self._cmd.poutput(
                f"Updated session: {Session.current_session.get_session_id()}. "
                f"Context Strategy: {Session.current_session.get_session_context_strategy()}."
            )

    def do_clear_context_strategy(self, _: cmd2.Statement) -> None:
        """
        Resets the context in a session.
        """

        # Check if current session exists
        if Session.current_session:
            Session.current_session.set_context_strategy(0)
            self._cmd.poutput(
                f"Updated session: {Session.current_session.get_session_id()}. "
                f"Context Strategy: {Session.current_session.get_session_context_strategy()}."
            )

    @with_argparser(CommandLineInterface.use_prompt_template_parser)
    def do_use_prompt_template(self, args: argparse.Namespace) -> None:
        """
        Use a prompt template by specifying its name while user is in a session.
        """
        new_prompt_template_name = args.prompt_template

        # Check if current session exists
        if Session.current_session:
            Session.current_session.set_prompt_template(new_prompt_template_name)
            self._cmd.poutput(
                f"Updated session: {Session.current_session.get_session_id()}. "
                f"Prompt Template: {Session.current_session.get_session_prompt_template()}."
            )

    def do_clear_prompt_template(self, _: cmd2.Statement) -> None:
        """
        Resets the prompt template in a session.
        """

        # Check if current session exists
        if Session.current_session:
            Session.current_session.set_prompt_template()
            self._cmd.poutput(
                f"Updated session: {Session.current_session.get_session_id()}. "
                f"Prompt Template: {Session.current_session.get_session_prompt_template()}."
            )

    def do_list_prompt_templates(self, _: cmd2.Statement) -> None:
        """
        List all prompt templates available.
        """
        prompt_template_list = get_prompt_templates()
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
