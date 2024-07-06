import asyncio
from ast import literal_eval

import cmd2
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.api import (
    api_create_runner,
    api_create_session,
    api_delete_bookmark,
    api_delete_session,
    api_export_bookmarks,
    api_get_all_bookmarks,
    api_get_all_chats_from_session,
    api_get_all_session_metadata,
    api_insert_bookmark,
    api_load_runner,
    api_load_session,
)
from moonshot.integrations.cli.active_session_cfg import active_session
from moonshot.src.api.api_bookmark import api_get_bookmark_by_id
from moonshot.src.redteaming.session.session import Session

console = Console()


def new_session(args) -> None:
    """
    Creates a new session based on the provided arguments.

    Args:
        args (Namespace): The arguments passed to the function.
    """
    global active_session

    runner_id = args.runner_id
    context_strategy = args.context_strategy if args.context_strategy else ""
    prompt_template = args.prompt_template if args.prompt_template else ""
    endpoints = literal_eval(args.endpoints) if args.endpoints else []

    # create new runner and session
    if endpoints:
        runner = api_create_runner(runner_id, endpoints)
    # load existing runner
    else:
        runner = api_load_runner(runner_id)

    runner_args = {}
    runner_args["context_strategy"] = context_strategy
    runner_args["prompt_template"] = prompt_template

    # create new session in runner
    if runner.database_instance:
        api_create_session(
            runner.id, runner.database_instance, runner.endpoints, runner_args
        )
        session_metadata = api_load_session(runner_id)
        if session_metadata:
            active_session.update(session_metadata)
            if active_session["context_strategy"]:
                active_session[
                    "cs_num_of_prev_prompts"
                ] = Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
            print(f"Using session: {active_session['session_id']}")
            update_chat_display()
        else:
            raise RuntimeError("Unable to use session")


def use_session(args) -> None:
    """
    Resumes a session by specifying its runner ID and updates the active session.

    Args:
        args (Namespace): The arguments passed to the function.
    """
    global active_session
    runner_id = args.runner_id

    # Load session metadata
    try:
        session_metadata = api_load_session(runner_id)
        if not session_metadata:
            print(
                "[Session] Cannot find a session with the existing Runner ID. Please try again."
            )
            return

        # Set the current session
        active_session.update(session_metadata)
        if active_session["context_strategy"]:
            active_session[
                "cs_num_of_prev_prompts"
            ] = Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
        print(f"Using session: {active_session['session_id']}. ")
        update_chat_display()
    except Exception as e:
        print(f"[use_session]: {str(e)}")


def end_session() -> None:
    """
    Ends the current session by clearing active_session variable.
    """
    global active_session
    active_session.clear()


def list_sessions() -> None:
    """
    Retrieves and displays the list of sessions.

    This function retrieves the metadata in dict for all sessions and displays them in a tabular format.
    If no sessions are found, a message is printed to the console.
    """
    session_metadata_list = api_get_all_session_metadata()
    if session_metadata_list:
        table = Table(
            title="Session List", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("No.", justify="left", width=2)
        table.add_column("Session ID", justify="left", width=20)
        table.add_column("Contains", justify="left", width=78)

        for session_index, session_data in enumerate(session_metadata_list, 1):
            session_id = session_data.get("session_id", "")
            endpoints = ", ".join(session_data.get("endpoints", []))
            created_datetime = session_data.get("created_datetime", "")

            session_info = f"[red]id: {session_id}[/red]\n\nCreated: {created_datetime}"
            contains_info = f"[blue]Endpoints:[/blue] {endpoints}\n\n"
            table.add_row(str(session_index), session_info, contains_info)
        console.print(table)
    else:
        console.print("[red]There are no sessions found.[/red]", style="bold")


def update_chat_display() -> None:
    """
    Updates the chat display for the active session.

    This function retrieves the chat details for the active session and prepares a table display for the chat history.
    The table includes columns for the chat ID, prepared prompts, and the prompt/response pairs.
    If there is no active session, a message is printed to the console.
    """
    global active_session

    if active_session:
        list_of_endpoint_chats = api_get_all_chats_from_session(
            active_session["session_id"]
        )

        # Prepare for table display
        table = Table(expand=True, show_lines=True, header_style="bold")
        table_list = []
        active_session["list_of_endpoint_chats"] = list_of_endpoint_chats

        for endpoint, endpoint_chats in list_of_endpoint_chats.items():
            table.add_column(endpoint, justify="center")
            new_table = Table(expand=True)
            new_table.add_column("ID", justify="left", ratio=1, min_width=5)
            new_table.add_column(
                "Prepared Prompts", justify="left", style="cyan", ratio=7
            )
            new_table.add_column("Prompt/Response", justify="left", ratio=7)

            for chat_with_details in endpoint_chats:
                new_table.add_row(
                    str(chat_with_details["chat_record_id"]),
                    chat_with_details["prepared_prompt"],
                    (
                        f"[magenta]{chat_with_details['prompt']}[/magenta] \n"
                        f"|---> [green]{chat_with_details['predicted_result']}[/green]"
                    ),
                )
                new_table.add_section()
            table_list.append(new_table)
            table.add_row(*table_list)

        # Display table
        panel = Panel.fit(
            Columns([table], expand=True),
            title=active_session["session_id"],
            border_style="red",
            title_align="left",
        )
        console.print(panel)

    else:
        console.print("[red]There are no active session.[/red]")


def bookmark_prompt(args) -> None:
    global active_session

    if active_session:
        endpoint = args.endpoint
        prompt_id = args.prompt_id
        bookmark_name = args.bookmark_name
        try:
            list_of_target_endpoint_chat = active_session.get(
                "list_of_endpoint_chats", None
            )
            target_endpoint_chats = list_of_target_endpoint_chat.get(endpoint, None)
            target_endpoint_chat_record = {}
            if not target_endpoint_chats:
                print(
                    "Incorrect endpoint. Please select a valid endpoint in this session."
                )
                return
            for endpoint_chat in target_endpoint_chats:
                if endpoint_chat["chat_record_id"] == prompt_id:
                    # found the prompt to bookmark
                    target_endpoint_chat_record = endpoint_chat
                    break
            if target_endpoint_chat_record:
                bookmark_message = api_insert_bookmark(
                    bookmark_name,
                    target_endpoint_chat_record["prompt"],
                    target_endpoint_chat_record["predicted_result"],
                    target_endpoint_chat_record["context_strategy"],
                    target_endpoint_chat_record["prompt_template"],
                    target_endpoint_chat_record["attack_module"],
                )
                print("[bookmark_prompt]:", bookmark_message["error_message"])
            else:
                print(
                    f"Unable to find prompt ID in the of prompts for endpoint {endpoint}. Please select a valid ID."
                )
        except Exception as e:
            print(f"[bookmark_prompt]: str({e})")
    else:
        print("There is no active session. Activate a session to bookmark a prompt.")
        return


def delete_bookmark(args) -> None:
    """
    Delete a bookmark.

    This function deletes a cookbook with the specified identifier. It prompts the user for confirmation before
    proceeding with the deletion. If the user confirms, it calls the api_delete_bookmark function from the moonshot.api
    module to delete the bookmark. If the deletion is successful, it prints a confirmation message.

    If an exception occurs, it prints an error message.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            bookmark_id (int): The identifier of the bookmark to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a bookmark
    # TODO: to decide if we wanna use name to identify bookmark instead as names as unique
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the bookmark (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Bookmark deletion cancelled.[/]")
        return
    try:
        bookmark_message = api_delete_bookmark(args.bookmark_id)
        print("[delete_bookmark]:", bookmark_message["error_message"])
    except Exception as e:
        print(f"[delete_bookmark]: {str(e)}")


def list_bookmarks() -> None:
    """
    List all available bookmarks.

    This function retrieves all available bookmarks by calling the api_get_all_bookmarks function from the
    moonshot.api module.
    It then displays the retrieved bookmarks using the display_bookmarks function.

    Returns:
        None
    """
    try:
        bookmarks_list = api_get_all_bookmarks()
        display_bookmarks(bookmarks_list)
    except Exception as e:
        print(f"[list_bookmarks]: {str(e)}")


def display_bookmarks(bookmarks_list) -> None:
    """
    Display the list of bookmarks in a tabular format.

    This function takes a list of bookmarks dictionaries and displays each bookmark's details in a table.
    The table includes the bookmark ID, name, prompt, responses, context strategy, prompt template, attack module and
    bookmark time. If the list is empty, it prints a message indicating that no bookmarks are found.

    Args:
        bookmarks_list (list): A list of dictionaries, where each dictionary contains the details of a bookmark.
    """
    if bookmarks_list:
        table = Table(
            title="Bookmark List", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("ID.", justify="left", ratio=1)
        table.add_column("Name", justify="left", ratio=2)
        table.add_column("Prompt", justify="left", ratio=5)
        table.add_column("Response", justify="left", ratio=5)
        table.add_column("Context Strategy", justify="left", ratio=2)
        table.add_column("Prompt Template", justify="left", ratio=2)
        table.add_column("Attack Module", justify="left", ratio=2)
        table.add_column("Bookmark Time", justify="left", ratio=2)
        if bookmarks_list:
            for index, bookmark in enumerate(bookmarks_list, 1):
                (
                    id,
                    name,
                    prompt,
                    response,
                    context_strategy,
                    prompt_template,
                    attack_module,
                    bookmark_time,
                ) = bookmark.values()
                table.add_section()
                table.add_row(
                    str(id),
                    name,
                    prompt,
                    response,
                    context_strategy,
                    prompt_template,
                    attack_module,
                    bookmark_time,
                )
            console.print(table)
        else:
            console.print("[red]There are no bookmarks found.[/red]")


def view_bookmark(args) -> None:
    """
    Displays the details of a specific bookmark by its ID.

    Args:
        args (Namespace): The arguments passed to the function, containing the bookmark ID.
    """

    try:
        bookmark_info = api_get_bookmark_by_id(args.bookmark_id)
        display_bookmarks([bookmark_info])
    except Exception as e:
        print(f"[view_bookmark]: {str(e)}")


def export_bookmarks(args) -> None:
    """
    Exports all bookmarks to a JSON file.

    Args:
        args (Namespace): The arguments passed to the function, containing the name of the export file.
    """
    try:
        api_export_bookmarks(write_file=True, export_file_name=args.bookmark_list_name)
        print("Bookmarks exported successfully.")
    except Exception as e:
        print(f"[export_bookmarks]: {str(e)}")


def manual_red_teaming(user_prompt: str) -> None:
    """
    Initiates manual red teaming with the provided user prompt.

    Args:
        user_prompt (str): The user prompt to be used for manual red teaming.

    If there is no active session, a message is printed to the console and the function returns.

    The function then prepares the manual red teaming arguments and runs the red teaming process using the provided
    user prompt, context strategy, and prompt template. After running the red teaming process, the session is reloaded.
    """
    if not active_session:
        print("There is no active session. Activate a session to start red teaming.")
        return
    prompt_template = (
        [active_session["prompt_template"]] if active_session["prompt_template"] else []
    )
    context_strategy = (
        active_session["context_strategy"] if active_session["context_strategy"] else []
    )
    num_of_prev_prompts = (
        active_session["cs_num_of_prev_prompts"]
        if active_session["context_strategy"]
        else Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
    )

    if context_strategy:
        context_strategy_info = [
            {
                "context_strategy_id": context_strategy,
                "num_of_prev_prompts": num_of_prev_prompts,
            }
        ]
    else:
        context_strategy_info = []

    mrt_arguments = {
        "manual_rt_args": {
            "prompt": user_prompt,
            "context_strategy_info": context_strategy_info,
            "prompt_template_ids": prompt_template,
        }
    }

    # load runner, perform red teaming and close the runner
    try:
        runner = api_load_runner(active_session["session_id"])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(runner.run_red_teaming(mrt_arguments))
        runner.close()
        _reload_session(active_session["session_id"])
    except Exception as e:
        print(f"[manual_red_teaming]: str({e})")


def run_attack_module(args):
    """
    Initiates automated red teaming with the provided arguments.

    Args:
        args: The arguments for automated red teaming.

    If there is no active session, a message is printed to the console and the function returns.

    The function prepares the runner arguments for automated red teaming using the provided arguments such as
    attack module ID, prompt, system prompt, context strategy, prompt template, and metric. It then loads the runner,
    performs red teaming, closes the runner, and reloads the session metadata.
    """
    if not active_session:
        print("There is no active session. Activate a session to start red teaming.")
        return
    try:
        attack_module_id = args.attack_module_id
        prompt = args.prompt
        system_prompt = args.system_prompt if args.system_prompt else ""
        context_strategy = args.context_strategy or []
        prompt_template = [args.prompt_template] if args.prompt_template else []
        metric = [args.metric] if args.metric else []
        num_of_prev_prompts = (
            args.num_of_prev_prompts
            if args.num_of_prev_prompts
            else Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
        )

        if context_strategy:
            context_strategy_info = [
                {
                    "context_strategy_id": context_strategy,
                    "num_of_prev_prompts": num_of_prev_prompts,
                }
            ]
        else:
            context_strategy_info = []

        # form runner arguments
        attack_strategy = [
            {
                "attack_module_id": attack_module_id,
                "prompt": prompt,
                "system_prompt": system_prompt,
                "context_strategy_info": context_strategy_info,
                "prompt_template_ids": prompt_template,
                "metric_ids": metric,
            }
        ]
        runner_args = {}
        runner_args["attack_strategies"] = attack_strategy

        # load runner, perform red teaming and close the runner

        runner = api_load_runner(active_session["session_id"])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(runner.run_red_teaming(runner_args))
        runner.close()
        _reload_session(active_session["session_id"])
        update_chat_display()
    except Exception as e:
        print(f"[run_attack_module]: str({e})")


def _reload_session(runner_id: str) -> None:
    """
    Reloads the session metadata for the given runner ID and updates the active session.

    Args:
        runner_id (str): The ID of the runner for which the session metadata needs to be reloaded.
    """
    global active_session
    try:
        session_metadata = api_load_session(runner_id)
        if not session_metadata:
            print(
                "[Session] Cannot find a session with the existing Runner ID. Please try again."
            )
            return
        active_session.update(session_metadata)
    except Exception as e:
        print(f"[reload_session]: str({e})")


def delete_session(args) -> None:
    """
    Deletes a session after confirming with the user.

    Args:
        args (object): The arguments object. It should have a 'session' attribute
                       which is the ID of the session to delete.
    """
    # Confirm with the user before deleting a session
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the session (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Session deletion cancelled.[/]")
        return
    try:
        api_delete_session(args.session)
        print("[delete_session]: Session deleted.")
    except Exception as e:
        print(f"[delete_session]: {str(e)}")


# use session arguments
use_session_args = cmd2.Cmd2ArgumentParser(
    description="Use an existing red teaming session by specifying the runner ID.",
    epilog="Example:\n use_session 'my-runner'",
)
use_session_args.add_argument(
    "runner_id",
    type=str,
    help="The ID of the runner which contains the session you want to use.",
)

# new session arguments
new_session_args = cmd2.Cmd2ArgumentParser(
    description="Creates a new red teaming session.",
    epilog=(
        "Example(create new runner): new_session my-runner -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu\n"
        "Example(load existing runner): new_session my-runner -c add_previous_prompt -p mmlu"
    ),
)

new_session_args.add_argument(
    "runner_id",
    type=str,
    help="ID of the runner. Creates a new runner if runner does not exist.",
)

new_session_args.add_argument(
    "-e",
    "--endpoints",
    type=str,
    help="List of endpoint(s) for the runner that is only compulsory for creating a new runner.",
    nargs="?",
)

new_session_args.add_argument(
    "-c",
    "--context_strategy",
    type=str,
    help=(
        "Name of the context_strategy to be used - indicate context strategy here if you wish to use with "
        "the selected attack."
    ),
    nargs="?",
)
new_session_args.add_argument(
    "-p",
    "--prompt_template",
    type=str,
    help=(
        "Name of the prompt template to be used - indicate prompt template here if you wish to use with "
        "the selected attack."
    ),
    nargs="?",
)

# automated red teaming arguments
automated_rt_session_args = cmd2.Cmd2ArgumentParser(
    description="Runs automated red teaming in the current session.",
    epilog=(
        'Example:\n run_attack_module sample_attack_module "this is my prompt" -s "test system prompt" '
        '-c "add_previous_prompt" -p "mmlu" -m "bleuscore"'
    ),
)

automated_rt_session_args.add_argument(
    "attack_module_id", type=str, help="ID of the attack module."
)

automated_rt_session_args.add_argument(
    "prompt", type=str, help="Prompt to be used for the attack."
)

automated_rt_session_args.add_argument(
    "-s",
    "--system_prompt",
    type=str,
    help="System Prompt to be used for the attack. If not specified, the default system prompt will be used.",
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-c",
    "--context_strategy",
    type=str,
    help="Name of the context strategy module to be used.",
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-n",
    "--num_of_prev_prompts",
    type=str,
    help="The number of previous prompts to use with the context strategy.",
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-p",
    "--prompt-template",
    type=str,
    help="Name of the prompt template to be used.",
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-m", "--metric", type=str, help="Name of the metric module to be used.", nargs="?"
)


# Delete session arguments
delete_session_args = cmd2.Cmd2ArgumentParser(
    description="Delete a session",
    epilog="Example:\n delete_session my-test-runner",
)

delete_session_args.add_argument(
    "session", type=str, help="The runner ID of the session to delete"
)


# Add bookmark prompt arguments
add_bookmark_prompt_args = cmd2.Cmd2ArgumentParser(
    description="Bookmark a prompt",
    epilog="Example:\n bookmark_prompt openai-connector 2 my-bookmarked-prompt",
)

add_bookmark_prompt_args.add_argument(
    "endpoint",
    type=str,
    help="Endpoint which the prompt was sent to.",
)

add_bookmark_prompt_args.add_argument(
    "prompt_id",
    type=int,
    help="ID of the prompt (the leftmost column)",
)

add_bookmark_prompt_args.add_argument(
    "bookmark_name",
    type=str,
    help="Name of the bookmark",
)

# Delete bookmark prompt arguments
delete_bookmark_prompt_args = cmd2.Cmd2ArgumentParser(
    description="Delete a bookmark",
    epilog="Example:\n delete_bookmark 2",
)

delete_bookmark_prompt_args.add_argument(
    "bookmark_id",
    type=int,
    help="ID of the bookmark",
)

# View bookmark prompt arguments
view_bookmark_prompt_args = cmd2.Cmd2ArgumentParser(
    description="View a bookmark",
    epilog="Example:\n view_bookmark 2",
)

view_bookmark_prompt_args.add_argument(
    "bookmark_id",
    type=int,
    help="ID of the bookmark",
)

# Export bookmarks arguments
export_bookmarks_args = cmd2.Cmd2ArgumentParser(
    description="Exports bookmarks as a JSON file",
    epilog='Example:\n export_bookmarks "my list of exported bookmarks"',
)

export_bookmarks_args.add_argument(
    "bookmark_list_name",
    type=str,
    help="Name of the bookmark",
)
