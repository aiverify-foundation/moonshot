import cmd2
from rich.console import Console

from moonshot.integrations.cli.benchmark.benchmark import BenchmarkCommandSet
from moonshot.integrations.cli.initialisation.initialisation import (
    InitialisationCommandSet,
)

console = Console()


class CommandLineInterface(cmd2.Cmd):
    def __init__(self):
        super().__init__(terminators=[])
        self.prompt = "moonshot > "
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

    # def default(self, statement: Statement) -> None:
    #     if Session.current_session:
    #         current_session = Session.current_session
    #         user_prompt = statement.command + " " + statement
    #         user_prompt = user_prompt.strip()
    #         current_session.send_prompt(user_prompt)

    #         # Update chat display
    #         update_chat_display()

    # def postcmd(self, stop, line):
    #     if Session.current_session:
    #         current_session = Session.current_session
    #         self.prompt = (
    #             f"moonshot ({current_session.get_session_id()}) "
    #             f"[PT: {current_session.get_session_prompt_template()}, "
    #             f"CS: {current_session.get_session_context_strategy()}] > "
    #         )
    #     else:
    #         self.prompt = "moonshot > "
    #     return stop
