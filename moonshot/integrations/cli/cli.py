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
        logo = " .d8b.  d888888b db    db    .88b  d88.  .d888b.   .d888b.  d8b   db .d8888. db   db  .d888b. d888888b"
        logo += "\n"
        logo += "d8' `8b   `88'   88    88    88'YbdP`88 .8P   Y8. .8P   Y8. 888o  88 88'  YP 88   88 .8P   Y8.   88 "
        logo += "\n"
        logo += "88ooo88    88    Y8    8P    88  88  88 88     88 88     88 88V8o 88 `8bo.   88ooo88 88 O < 88   88\n"
        logo += "88   88    88    `8b  d8'    88  88  88 88     88 88     88 88 V8o88   `Y8b. 88   88 88  v  88   88\n"
        logo += "88   88   .88.    `8bd8'     88  88  88 `8b   d8' `8b   d8' 88  V888 db   8D 88   88 `8b   d8'   88\n"
        logo += "88   88 d888888b    YP       88  88  88  `Y888P'   `Y888P'  88   V8P `8888Y' 88   88  `Y888P'    88\n"

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
