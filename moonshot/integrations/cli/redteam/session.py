import asyncio
from ast import literal_eval

import cmd2
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.api import (
    api_create_session,
    api_get_all_session_detail,
    api_get_session,
    api_get_session_chats_by_session_id,
    api_send_prompt,
)
from moonshot.src.configs.active_session_cfg import active_session

console = Console()


def new_session(args) -> None:
    """
    Creates a new session with the specified parameters and updates the active session configuration.

    This function takes command line arguments, extracts the necessary parameters for creating a new session,
    and then calls the API to create the session. Upon successful creation, it updates the global active session
    configuration to reflect the newly created session's metadata and refreshes the chat display to show the
    current session's chats.

    Args:
        args: A namespace with the session parameters. Expected to have 'name', 'description', 'endpoints',
              'context_strategy'(optional), and 'prompt_template'(optional).
    """
    global active_session
    name = args.name
    description = args.description
    endpoints = literal_eval(args.endpoints)
    context_strategy = args.context_strategy
    prompt_template = args.prompt_template

    # Create a new session
    session_instance = api_create_session(
        name, description, endpoints, context_strategy, prompt_template
    )

    # Set session metadata to active session
    active_session.update(session_instance.metadata.to_dict())
    print(f"Using session: {active_session['session_id']}.")
    update_chat_display()


def end_session() -> None:
    """
    Ends the current session.
    """
    global active_session
    active_session.clear()


def list_sessions() -> None:
    """
    Fetches and displays a list of all sessions in a formatted table.

    This function retrieves a list of all sessions using the API and displays them in a table format.
    Each row in the table represents a session, showing its index number, session ID, and details such as
    the session name, description, endpoints, and chat IDs. If no sessions are found, it displays a message
    indicating that there are no sessions available.
    """
    session_list = api_get_all_session_detail()
    if session_list:
        table = Table(title="Session List", show_lines=True)
        table.add_column("No.", style="dim", width=6)
        table.add_column("Session ID", justify="center")
        table.add_column("Contains", justify="left")

        for session_index, session_data in enumerate(session_list, 1):
            session_id = session_data.get("session_id", "")
            name = session_data.get("name", "")
            description = session_data.get("description", "")
            endpoints = ", ".join(session_data.get("endpoints", []))
            created_datetime = session_data.get("created_datetime", "")
            chat_ids = ", ".join(map(str, session_data.get("chat_ids", [])))

            session_info = f"[red]id: {session_id}[/red]\n\nCreated: {created_datetime}"
            contains_info = f"[blue]{name}[/blue]\n{description}\n\n"
            contains_info += f"[blue]Endpoints:[/blue] {endpoints}\n\n"
            contains_info += f"[blue]Chat IDs:[/blue] {chat_ids}"

            table.add_row(str(session_index), session_info, contains_info)
        console.print(Panel(table))
    else:
        console.print("[red]There are no sessions found.[/red]", style="bold")


def use_session(args) -> None:
    """
    Resumes a session by specifying its session ID.
    """
    global active_session
    session_id = args.session_id

    # load a session
    session_instance = api_get_session(session_id)
    if not session_instance:
        print("Cannot find a session with the existing Session ID. Please try again.")
        return

    # set the current session
    active_session.update(session_instance.metadata.to_dict())
    print(f"Using session: {active_session['session_id']}. ")
    # Display chat
    update_chat_display()


def send_prompt(session_id: str, user_prompt: str) -> None:
    """
    Sends a user-defined prompt to the specified session.

    This function asynchronously sends a prompt, provided by the user, to a session identified by its session ID.
    It leverages the `api_send_prompt` function to facilitate the interaction between the user and the session,
    enabling dynamic input and further customization of the session's behavior based on user input.

    Args:
        session_id (str): The unique identifier of the session to which the prompt is to be sent.
        user_prompt (str): The prompt text defined by the user to be sent to the session.
    """
    asyncio.run(api_send_prompt(session_id, user_prompt))


def update_chat_display() -> None:
    """
    Updates the chat display for the active session.

    This function retrieves the chat details for the active session and prepares a table display for the chat history.
    The table includes columns for the chat ID, prepared prompts, and the prompt/response pairs.
    If there is no active session, a message is printed to the console.
    """
    global active_session

    if active_session:
        list_of_chats_with_details = api_get_session_chats_by_session_id(
            active_session["session_id"]
        )

        # Prepare for table display
        table = Table(expand=True)
        table_list = []
        for chat_with_details in list_of_chats_with_details:
            table.add_column(chat_with_details["chat_id"], justify="center")
            new_table = Table(expand=True)
            new_table.add_column("Prepared Prompts", justify="left", style="cyan")
            new_table.add_column("Prompt/Response", justify="left")

            list_of_chat_history = chat_with_details["chat_history"]
            for prompt in list_of_chat_history:
                new_table.add_row(
                    prompt["prepared_prompt"],
                    f"[magenta]{prompt['prompt']}[/magenta] \n|---> [green]{prompt['predicted_result']}[/green]",
                )
                new_table.add_section()
            table_list.append(new_table)
            table.add_row(*table_list)

        # # Display table
        panel = Panel.fit(
            Columns([table], expand=True),
            title=active_session["session_id"],
            border_style="red",
            title_align="left",
        )
        console.print(panel)

    else:
        console.print("[red]There are no active session.[/red]")


# User session arguments
use_session_args = cmd2.Cmd2ArgumentParser(
    description="Use an existing red teaming session.",
    epilog="Example:\n use_session 'my-session-1'",
)
use_session_args.add_argument(
    "session_id",
    type=str,
    help="The ID of the session that you want to use",
)

# New session arguments
new_session_args = cmd2.Cmd2ArgumentParser(
    description="Add a new red teaming session.",
    epilog="Example:\n new_session 'my_new_session' "
    "'My new session description' "
    "\"['my-openai-gpt35', 'my-openai-gpt4']\" "
    "'my_context_strategy_name' "
    "'my_prompt_template_name'",
)
new_session_args.add_argument("name", type=str, help="Name of the new session")
new_session_args.add_argument(
    "description", type=str, help="Description of the new session"
)
new_session_args.add_argument(
    "endpoints",
    type=str,
    help="Endpoints of the new session",
)

new_session_args.add_argument(
    "context_strategy", type=str, help="Name of the context strategy module", nargs="?"
)

new_session_args.add_argument(
    "prompt_template", type=str, help="Name of the prompt template", nargs="?"
)
