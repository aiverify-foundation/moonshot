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
    api_get_bookmark,
    api_insert_bookmark,
    api_load_runner,
    api_load_session,
)
from moonshot.integrations.cli.active_session_cfg import active_session
from moonshot.integrations.cli.cli_errors import (
    ERROR_RED_TEAMING_ADD_BOOKMARK_ENDPOINT_VALIDATION,
    ERROR_RED_TEAMING_ADD_BOOKMARK_ENDPOINT_VALIDATION_1,
    ERROR_RED_TEAMING_ADD_BOOKMARK_NO_ACTIVE_SESSION,
    ERROR_RED_TEAMING_LIST_SESSIONS_FIND_VALIDATION,
    ERROR_RED_TEAMING_LIST_SESSIONS_PAGINATION_VALIDATION,
    ERROR_RED_TEAMING_LIST_SESSIONS_PAGINATION_VALIDATION_1,
    ERROR_RED_TEAMING_NEW_SESSION_ENDPOINTS_VALIDATION,
    ERROR_RED_TEAMING_NEW_SESSION_FAILED_TO_USE_SESSION,
    ERROR_RED_TEAMING_NEW_SESSION_PARAMS_VALIDATION,
    ERROR_RED_TEAMING_NEW_SESSION_PARAMS_VALIDATION_1,
    ERROR_RED_TEAMING_SHOW_PROMPTS_NO_ACTIVE_SESSION_VALIDATION,
    ERROR_RED_TEAMING_USE_BOOKMARK_NO_ACTIVE_SESSION,
    ERROR_RED_TEAMING_USE_SESSION_NO_SESSION_METADATA_VALIDATION,
    ERROR_RED_TEAMING_USE_SESSION_RUNNER_ID_TYPE_VALIDATION,
    ERROR_RED_TEAMING_USE_SESSION_RUNNER_ID_VALIDATION,
)
from moonshot.integrations.cli.utils.process_data import filter_data
from moonshot.src.redteaming.session.session import Session

console = Console()


def new_session(args) -> None:
    """
    Creates a new red teaming session or loads an existing one.

    This function either creates a new runner and session or loads an existing runner based on the provided arguments.
    It updates the global active_session with the session metadata and displays the chat history.

    Args:
        args (Namespace): The arguments passed to the function, containing:
            - runner_id (str): The ID of the runner.
            - context_strategy (str, optional): The context strategy to be used.
            - prompt_template (str, optional): The prompt template to be used.
            - endpoints (str, optional): The list of endpoints for the runner."""
    global active_session  # noqa: F824

    try:
        required_parameters = [("runner_id", str)]
        optional_parameters = [("context_strategy", str), ("prompt_template", str)]
        # Check if required parameters exist in args
        for param, param_type in required_parameters:
            param_value = getattr(args, param, None)
            if not param_value:
                raise ValueError(
                    ERROR_RED_TEAMING_NEW_SESSION_PARAMS_VALIDATION.format(param=param)
                )
            if not isinstance(param_value, param_type):
                raise TypeError(
                    ERROR_RED_TEAMING_NEW_SESSION_PARAMS_VALIDATION_1.format(
                        param=param, param_type=param_type.__name__
                    )
                )

        # Check the type of optional parameters if they exist
        for param, param_type in optional_parameters:
            param_value = getattr(args, param, None)
            if param_value is not None and not isinstance(param_value, param_type):
                raise TypeError(
                    ERROR_RED_TEAMING_NEW_SESSION_PARAMS_VALIDATION_1.format(
                        param=param, param_type=param_type.__name__
                    )
                )

        runner_id = args.runner_id
        context_strategy = args.context_strategy if args.context_strategy else ""
        prompt_template = args.prompt_template if args.prompt_template else ""
        endpoints = []

        # Check if literal eval param is correct type after eval
        if hasattr(args, "endpoints") and args.endpoints:
            endpoints = literal_eval(args.endpoints)
            if not isinstance(endpoints, list):
                raise TypeError(ERROR_RED_TEAMING_NEW_SESSION_ENDPOINTS_VALIDATION)

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
            session_metadata = api_load_session(runner.id)
            if session_metadata:
                active_session.update(session_metadata)
                if active_session["context_strategy"]:
                    active_session[
                        "cs_num_of_prev_prompts"
                    ] = Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
                print(f"[new_session] Using session: {active_session['session_id']}")
                update_chat_display()
            else:
                raise RuntimeError(ERROR_RED_TEAMING_NEW_SESSION_FAILED_TO_USE_SESSION)
    except Exception as e:
        print(f"[new_session]: {str(e)}")


def use_session(args) -> None:
    """
    Resumes a session by specifying its runner ID and updates the active session.

    Args:
        args (Namespace): The arguments passed to the function.
    """
    global active_session  # noqa: F824

    # Load session metadata
    try:
        if not args.runner_id or args.runner_id is None:
            raise ValueError(ERROR_RED_TEAMING_USE_SESSION_RUNNER_ID_VALIDATION)

        if not isinstance(args.runner_id, str):
            raise TypeError(ERROR_RED_TEAMING_USE_SESSION_RUNNER_ID_TYPE_VALIDATION)

        runner_id = args.runner_id
        session_metadata = api_load_session(runner_id)
        if not session_metadata:
            print(ERROR_RED_TEAMING_USE_SESSION_NO_SESSION_METADATA_VALIDATION)
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


def show_prompts() -> None:
    """
    Shows the chat table in a session so that users don't have to restart a session to view the chat table
    """
    global active_session  # noqa: F824

    if not active_session:
        print(ERROR_RED_TEAMING_SHOW_PROMPTS_NO_ACTIVE_SESSION_VALIDATION)
        return

    update_chat_display()


def end_session() -> None:
    """
    Ends the current session by clearing active_session variable.
    """
    global active_session  # noqa: F824
    active_session.clear()


def list_sessions(args) -> list | None:
    """
    Retrieves and displays the list of sessions.

    This function retrieves the metadata in dict for all sessions and displays them in a tabular format.
    If no sessions are found, a message is printed to the console.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find session(s) with a keyword.
        pagination (str): Optional field to paginate sessions.

    Returns:
        list | None: A list of Session or None if there is no result.
    """
    try:
        session_metadata_list = api_get_all_session_metadata()
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_RED_TEAMING_LIST_SESSIONS_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_RED_TEAMING_LIST_SESSIONS_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_RED_TEAMING_LIST_SESSIONS_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(
                    ERROR_RED_TEAMING_LIST_SESSIONS_PAGINATION_VALIDATION_1
                )

        keyword = args.find.lower() if args.find else ""
        pagination = literal_eval(args.pagination) if args.pagination else ()

        if session_metadata_list:
            filtered_session_metadata_list = filter_data(
                session_metadata_list, keyword, pagination
            )
            if filtered_session_metadata_list:
                _display_sessions(filtered_session_metadata_list)
                return filtered_session_metadata_list

        console.print("[red]There are no sessions found.[/red]")
        return None
    except Exception as e:
        print(f"[list_sessions]: {str(e)}")


def update_chat_display() -> None:
    """
    Updates the chat display for the active session.

    This function retrieves the chat details for the active session and prepares a table display for the chat history.
    The table includes columns for the chat ID, prepared prompts, and the prompt/response pairs.
    If there is no active session, a message is printed to the console.
    """
    global active_session  # noqa: F824

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


def add_bookmark(args) -> None:
    """
    Bookmarks a specific prompt in the active session.

    This function retrieves a specific chat record from the active session based on the provided endpoint and prompt ID.
    If the chat record is found, it inserts a bookmark with the specified name and the details of the chat record.
    If the chat record is not found, it prints an error message.

    Args:
        args (Namespace): The arguments passed to the function, containing:
            - endpoint (str): The endpoint to which the prompt was sent.
            - prompt_id (int): The ID of the prompt (the leftmost column).
            - bookmark_name (str): The name of the bookmark to be created.

    If there is no active session, a message is printed to the console and the function returns.
    """
    global active_session  # noqa: F824

    if active_session:
        try:
            endpoint = args.endpoint
            prompt_id = args.prompt_id
            bookmark_name = args.bookmark_name

            list_of_target_endpoint_chat = active_session.get(
                "list_of_endpoint_chats", None
            )
            target_endpoint_chats = list_of_target_endpoint_chat.get(endpoint, None)
            target_endpoint_chat_record = {}
            if not target_endpoint_chats:
                print(ERROR_RED_TEAMING_ADD_BOOKMARK_ENDPOINT_VALIDATION)
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
                    target_endpoint_chat_record["prepared_prompt"],
                    target_endpoint_chat_record["predicted_result"],
                    target_endpoint_chat_record["context_strategy"],
                    target_endpoint_chat_record["prompt_template"],
                    target_endpoint_chat_record["attack_module"],
                    target_endpoint_chat_record["metric"],
                )
                print("[bookmark_prompt]:", bookmark_message["message"])
            else:
                print(
                    ERROR_RED_TEAMING_ADD_BOOKMARK_ENDPOINT_VALIDATION_1.format(
                        endpoint=endpoint
                    )
                )
        except Exception as e:
            print(f"[bookmark_prompt]: ({str(e)})")
    else:
        print(ERROR_RED_TEAMING_ADD_BOOKMARK_NO_ACTIVE_SESSION)
        return


def use_bookmark(args) -> None:
    """
    Updates the current session with the details from a specified bookmark.

    This function retrieves the details of a bookmark by its ID and updates the active session's context strategy
    and prompt template with the bookmark's details. If the bookmark includes an attack module, it crafts a CLI
    command for the user to copy and paste. Otherwise, it provides the bookmarked prompt for manual red teaming.

    Args:
        args (Namespace): The arguments passed to the function, containing:
            - bookmark_name (str): The ID of the bookmark to use.

    If there is no active session, a message is printed to the console and the function returns.
    """
    global active_session  # noqa: F824
    if active_session:
        try:
            bookmark_name = args.bookmark_name
            bookmark_details = api_get_bookmark(bookmark_name)
            if bookmark_details:
                bookmarked_prompt = bookmark_details["prepared_prompt"]

                # automated redteaming: craft CLI command for user to copy and paste
                if bookmark_details["attack_module"]:
                    attack_module = bookmark_details["attack_module"]
                    run_attack_module_cmd = (
                        f'run_attack_module {attack_module} "{bookmarked_prompt}"'
                    )
                    console.print(
                        f"[bold yellow]Copy this command and paste it below:[/]\n{run_attack_module_cmd}\n"
                    )

                # manual redteaming: return prompt for user to copy and paste
                else:
                    console.print(
                        f"[bold yellow]Copy this prompt and paste it below: [/]\n{bookmarked_prompt}\n"
                    )
                return
        except Exception as e:
            print(f"[use_bookmark]: {str(e)}")
    else:
        print(ERROR_RED_TEAMING_USE_BOOKMARK_NO_ACTIVE_SESSION)
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
            bookmark_name (str): The identifier of the bookmark to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting a bookmark
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the bookmark (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Bookmark deletion cancelled.[/]")
        return
    try:
        bookmark_message = api_delete_bookmark(args.bookmark_name)
        print("[delete_bookmark]:", bookmark_message["message"])
    except Exception as e:
        print(f"[delete_bookmark]: {str(e)}")


def list_bookmarks(args) -> list | None:
    """
    List all available bookmarks.

    This function retrieves all available bookmarks by calling the api_get_all_bookmarks function from the
    moonshot.api module.
    It then displays the retrieved bookmarks using the _display_bookmarks function.
    If no bookmarks are found, a message is printed to the console.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find bookmark(s) with a keyword.
        pagination (str): Optional field to paginate bookmarks.

    Returns:
        list | None: A list of Bookmark or None if there is no result.
    """
    try:
        bookmarks_list = api_get_all_bookmarks()
        keyword = args.find.lower() if args.find else ""
        pagination = literal_eval(args.pagination) if args.pagination else ()

        if bookmarks_list:
            filtered_bookmarks_list = filter_data(bookmarks_list, keyword, pagination)
            if filtered_bookmarks_list:
                _display_bookmarks(filtered_bookmarks_list)
                return filtered_bookmarks_list

        console.print("[red]There are no bookmarks found.[/red]")
        return None

    except Exception as e:
        print(f"[list_bookmarks]: {str(e)}")


def _display_bookmarks(bookmarks_list) -> None:
    """
    Display the list of bookmarks in a tabular format.

    This function takes a list of bookmarks dictionaries and displays each bookmark's details in a table.
    The table includes an autogenerated index, name, prepared prompt, response and bookmark time.
    If the list is empty, it prints a message indicating that no bookmarks are found.

    Args:
        bookmarks_list (list): A list of dictionaries, where each dictionary contains the details of a bookmark.
    """

    table = Table(
        title="Bookmark List", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("ID.", justify="left", width=5)
    table.add_column("Name", justify="left", width=20)
    table.add_column("Prepared Prompt", justify="left", width=50)
    table.add_column("Predicted Response", justify="left", width=50)
    table.add_column("Bookmark Time", justify="left", width=20)
    for idx, bookmark in enumerate(bookmarks_list, 1):
        (
            name,
            prompt,
            prepared_prompt,
            response,
            context_strategy,
            prompt_template,
            attack_module,
            metric,
            bookmark_time,
            *other_args,
        ) = bookmark.values()
        idx = bookmark.get("idx", idx)

        table.add_section()
        table.add_row(
            str(idx),
            name,
            prepared_prompt,
            response,
            bookmark_time,
        )
    console.print(table)


def view_bookmark(args) -> None:
    """
    Displays the details of a specific bookmark by its ID.

    Args:
        args (Namespace): The arguments passed to the function, containing the bookmark ID.
    """

    try:
        bookmark_info = api_get_bookmark(args.bookmark_name)
        _display_bookmark(bookmark_info)
    except Exception as e:
        print(f"[view_bookmark]: {str(e)}")


def _display_bookmark(bookmark_info: dict) -> None:
    """
    Display the filtered bookmark in a tabular format.

    This function takes a list of bookmarks dictionaries and displays the target bookmark's details in a table.
    The table includes the bookmark name, prompt, prepared prompt, response, context strategy, prompt template,
    attack module, metric and bookmark time. If the list is empty, it prints a message indicating that no bookmarks
    are found.

    Args:
        bookmark_info (dict): A dictionary which contains the details of a bookmark.
    """
    if bookmark_info:
        table = Table(
            title="Bookmark List", show_lines=True, expand=True, header_style="bold"
        )
        table.add_column("Name", justify="left", width=10)
        table.add_column("Prompt", justify="left", width=30)
        table.add_column("Prepared Prompt", justify="left", width=30)
        table.add_column("Predicted Response", justify="left", width=30)
        table.add_column("Context Strategy", justify="left", width=5)
        table.add_column("Prompt Template", justify="left", width=5)
        table.add_column("Attack Module", justify="left", width=5)
        table.add_column("Metric", justify="left", width=5)
        table.add_column("Bookmark Time", justify="left", width=5)
        (
            name,
            prompt,
            prepared_prompt,
            response,
            context_strategy,
            prompt_template,
            attack_module,
            metric,
            bookmark_time,
        ) = bookmark_info.values()
        table.add_section()
        table.add_row(
            name,
            prompt,
            prepared_prompt,
            response,
            context_strategy,
            prompt_template,
            attack_module,
            metric,
            bookmark_time,
        )
        console.print(table)
    else:
        console.print("[red]There are no bookmarks found.[/red]")


def export_bookmarks(args) -> None:
    """
    Exports all bookmarks to a JSON file.

    Args:
        args (Namespace): The arguments passed to the function, containing the name of the export file.
    """
    try:
        file_path = api_export_bookmarks(export_file_name=args.bookmark_list_name)
        print(f"Bookmarks exported successfully. Written to: {file_path}")
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
        print(f"[manual_red_teaming]: ({str(e)})")


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
        # context strategy and prompt template should come from the session instead of the command

        if args.prompt_template:
            prompt_template = [args.prompt_template]
        elif active_session["prompt_template"]:
            prompt_template = [active_session["prompt_template"]]
        else:
            prompt_template = []

        if args.context_strategy:
            context_strategy = args.context_strategy
            num_of_prev_prompts = (
                args.cs_num_of_prev_prompts
                if args.cs_num_of_prev_prompts
                else Session.DEFAULT_CONTEXT_STRATEGY_PROMPT
            )
        elif active_session["context_strategy"]:
            context_strategy = active_session["context_strategy"]
            num_of_prev_prompts = active_session["cs_num_of_prev_prompts"]
        else:
            context_strategy = []
            num_of_prev_prompts = Session.DEFAULT_CONTEXT_STRATEGY_PROMPT

        optional_arguments = (
            literal_eval(args.optional_args) if args.optional_args else {}
        )

        metric = [args.metric] if args.metric else []
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
                "optional_params": optional_arguments,
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
    global active_session  # noqa: F824
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
        if not args.session or args.session is None:
            raise ValueError("Invalid or missing required parameter: session")

        if not isinstance(args.session, str):
            raise TypeError("Invalid type for parameter: session. Expecting type str.")

        api_delete_session(args.session)
        print("[delete_session]: Session deleted.")
    except Exception as e:
        print(f"[delete_session]: {str(e)}")


def _display_sessions(sessions: list) -> None:
    """
    Display a list of sessions.

    This function takes a list of sessions and displays them in a table format. If the list is empty, it prints a
    message indicating that no sessions were found.

    Args:
        sessions (list): A list of sessions.

    Returns:
        None
    """

    table = Table(
        title="Session List", show_lines=True, expand=True, header_style="bold"
    )
    table.add_column("No.", justify="left", width=2)
    table.add_column("Session ID", justify="left", width=20)
    table.add_column("Contains", justify="left", width=78)

    for idx, session_data in enumerate(sessions, 1):
        (
            session_id,
            endpoints,
            created_epoch,
            created_datetime,
            prompt_template,
            context_strategy,
            cs_num_of_prev_prompts,
            attack_module,
            metric,
            system_prompt,
            *other_args,
        ) = session_data.values()
        idx = session_data.get("idx", idx)
        session_info = f"[red]id: {session_id}[/red]\n\nCreated: {created_datetime}"
        contains_info = f"[blue]Endpoints:[/blue] {endpoints}\n\n"
        table.add_row(str(idx), session_info, contains_info)
    console.print(table)


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
        'Example:\n run_attack_module sample_attack_module "this is my prompt" -s "test system prompt" -m bleuscore'
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
    help=(
        "Name of the context strategy module to be used. If this is set, it will overwrite the context strategy"
        " set in the session while running this attack module."
    ),
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-n",
    "--cs_num_of_prev_prompts",
    type=str,
    help=(
        "The number of previous prompts to use with the context strategy. If this is set, it will overwrite the"
        " number of previous prompts set in the session while running this attack module."
    ),
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-p",
    "--prompt_template",
    type=str,
    help="Name of the prompt template to be used. If this is set, it will overwrite the prompt template set in"
    " the session while running this attack module.",
    nargs="?",
)

automated_rt_session_args.add_argument(
    "-m", "--metric", type=str, help="Name of the metric module to be used.", nargs="?"
)

automated_rt_session_args.add_argument(
    "-o",
    "--optional_args",
    type=str,
    help="Optional parameters to input into the red teaming module.",
    nargs="?",
)

# Delete session arguments
delete_session_args = cmd2.Cmd2ArgumentParser(
    description="Delete a session",
    epilog="Example:\n delete_session my-test-runner",
)

delete_session_args.add_argument(
    "session", type=str, help="The runner ID of the session to delete"
)


# List sessions arguments
list_sessions_args = cmd2.Cmd2ArgumentParser(
    description="List all sessions.",
    epilog='Example:\n list_sessions -f "my-sessions"',
)

list_sessions_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find session(s) with keyword",
    nargs="?",
)

list_sessions_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate session(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)

# Add bookmark arguments
add_bookmark_args = cmd2.Cmd2ArgumentParser(
    description="Bookmark a prompt",
    epilog="Example:\n add_bookmark openai-connector 2 my-bookmarked-prompt",
)

add_bookmark_args.add_argument(
    "endpoint",
    type=str,
    help="Endpoint which the prompt was sent to.",
)

add_bookmark_args.add_argument(
    "prompt_id",
    type=int,
    help="ID of the prompt (the leftmost column)",
)

add_bookmark_args.add_argument(
    "bookmark_name",
    type=str,
    help="Name of the bookmark",
)

# Use bookmark arguments
use_bookmark_args = cmd2.Cmd2ArgumentParser(
    description="Use a bookmarked prompt",
    epilog="Example:\n use_bookmark my_bookmark",
)

use_bookmark_args.add_argument(
    "bookmark_name",
    type=str,
    help="Name of the bookmark",
)


# Delete bookmark arguments
delete_bookmark_args = cmd2.Cmd2ArgumentParser(
    description="Delete a bookmark",
    epilog="Example:\n delete_bookmark my_bookmarked_prompt",
)

delete_bookmark_args.add_argument(
    "bookmark_name",
    type=str,
    help="Name of the bookmark",
)

# View bookmark arguments
view_bookmark_args = cmd2.Cmd2ArgumentParser(
    description="View a bookmark",
    epilog="Example:\n view_bookmark my_bookmarked_prompt",
)

view_bookmark_args.add_argument(
    "bookmark_name",
    type=str,
    help="Name of the bookmark you want to view",
)

# Export bookmarks arguments
export_bookmarks_args = cmd2.Cmd2ArgumentParser(
    description="Exports bookmarks as a JSON file",
    epilog='Example:\n export_bookmarks "my_list_of_exported_bookmarks"',
)

export_bookmarks_args.add_argument(
    "bookmark_list_name",
    type=str,
    help="Name of the exported bookmarks JSON file you want to save as (without the .json extension)",
)


# List bookmarks arguments
list_bookmarks_args = cmd2.Cmd2ArgumentParser(
    description="List all bookmarks.",
    epilog="Example:\n list_bookmarks -f my_bookmark",
)

list_bookmarks_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find bookmark(s) with keyword",
    nargs="?",
)

list_bookmarks_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate bookmark(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
