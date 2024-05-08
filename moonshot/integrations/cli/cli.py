import cmd2
from cmd2 import Statement
from rich.console import Console

from moonshot.integrations.cli.active_session_cfg import active_session
from moonshot.integrations.cli.benchmark.benchmark import BenchmarkCommandSet
from moonshot.integrations.cli.common.common import CommonCommandSet
from moonshot.integrations.cli.initialisation.initialisation import (
    InitialisationCommandSet,
)
from moonshot.integrations.cli.redteam.redteam import RedTeamCommandSet
from moonshot.integrations.cli.redteam.session import (
    manual_red_teaming,
    update_chat_display,
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

    def default(self, statement: Statement) -> None:
        # if there is an active session, anything entered other than recognised commands
        # will be considered prompts
        if active_session:
            user_prompt = statement.command + " " + statement
            user_prompt = user_prompt.strip()
            manual_red_teaming(user_prompt)
            # Update chat display with response
            update_chat_display()

    def postcmd(self, stop, line):
        if active_session:
            if active_session["context_strategy"]:
                cs_prompt = f"CS: ({active_session['context_strategy']},{active_session['cs_num_of_prev_prompts']})] > "
            else:
                cs_prompt = f"CS: {active_session['context_strategy']}]> "
            self.prompt = (
                f"moonshot ({active_session['session_id']}) "
                f"[PT: {active_session['prompt_template']}, "
                f"{cs_prompt}"
            )
        else:
            self.prompt = "moonshot > "
        return stop
