from ast import literal_eval

import cmd2
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from moonshot.api import api_get_all_sessions
from moonshot.src.redteaming.session import Session

console = Console()


def new_session(args) -> None:
    """
    Add a new session to the session list.
    """
    name = args.name
    description = args.description
    endpoints = literal_eval(args.endpoints)
    context_strategy = args.context_strategy
    prompt_template = args.prompt_template

    # create a new session
    session_instance = Session(name, description, endpoints)

    # set the current session
    Session.current_session = session_instance
    print(
        f"Using session: {session_instance.get_session_id()}. "
        f"Session Chats: {session_instance.get_session_chats()}"
    )

    # Display chat
    update_chat_display()


# def end_session() -> None:
#     """
#     End the current session.
#     """
#     Session.current_session = None


# def list_sessions() -> None:
#     """
#     List all available sessions.
#     """
#     session_list = api_get_all_sessions()
#     if session_list:
#         table = Table("No.", "Session ID", "Contains")
#         for session_index, session_data in enumerate(session_list, 1):
#             (
#                 session_id,
#                 session_name,
#                 session_description,
#                 session_created_epoch,
#                 session_created_datetime,
#                 session_endpoints,
#                 session_metadata_file,
#                 session_chats,
#                 session_prompt_template,
#                 session_context_strategy,
#                 filename,
#             ) = session_data.values()
#             session_info = (
#                 f"[red]id: {session_id}[/red]\n\nCreated: {session_created_datetime}"
#             )

#             contains_info = f"[blue]{session_name}[/blue]\n{session_description}\n\n"
#             contains_info += f"[blue]Endpoints:[/blue]\n{session_endpoints}\n\n"
#             contains_info += f"[blue]Metadata file:[/blue]\n{session_metadata_file}\n\n"
#             contains_info += f"[blue]Chat IDs:[/blue]\n{session_chats}"

#             table.add_section()
#             table.add_row(str(session_index), session_info, contains_info)
#         console.print(table)
#     else:
#         console.print("[red]There are no sessions found.[/red]")


# def use_session(args) -> None:
#     """
#     Use or resume a session by specifying its session ID.
#     """
#     session_id = args.session_id

#     # load a session
#     session_instance: Session = Session.load_session(session_id)

#     # set the current session
#     Session.current_session = session_instance
#     print(
#         f"Using session: {session_instance.get_session_id()}. "
#         f"Session Chats: {session_instance.get_session_chats()}"
#     )

#     # Display chat
#     update_chat_display()


def update_chat_display() -> None:
    """
    Display chats on console
    """
    if Session.current_session:
        num_of_previous_prompts = 10

        # Get session info for display
        session_chats = Session.current_session.get_session_chats()
        session_previous_prompts = Session.current_session.get_session_previous_prompts(
            num_of_previous_prompts
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


# # User session arguments
# use_session_args = cmd2.Cmd2ArgumentParser(
#     description="Use an existing red teaming session.",
#     epilog="Example:\n use_session 'my-session-1'",
# )
# use_session_args.add_argument(
#     "session_id",
#     type=str,
#     help="The ID of the session that you want to use",
# )

# New session arguments
new_session_args = cmd2.Cmd2ArgumentParser(
    description="Add a new red teaming session.",
    epilog="Example:\n new_session 'my_new_session' "
    "'My new session description' "
    "\"['my-openai-gpt35', 'my-openai-gpt4']\"",
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
