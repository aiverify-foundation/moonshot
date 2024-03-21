import argparse

import cmd2

from moonshot.integrations.cli.redteam.context_strategy import (
    clear_context_strategy,
    list_context_strategies,
    use_context_strategy,
    use_context_strategy_args,
)
from moonshot.integrations.cli.redteam.prompt_template import (
    clear_prompt_template,
    use_prompt_template,
    use_prompt_template_args,
)
from moonshot.integrations.cli.redteam.session import (
    end_session,
    list_sessions,
    new_session,
    new_session_args,
    use_session,
    use_session_args,
)


@cmd2.with_default_category("Moonshot RedTeaming")
class RedTeamCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @cmd2.with_argparser(new_session_args)
    def do_new_session(self, args: argparse.Namespace) -> None:
        new_session(args)

    def do_end_session(self, _: cmd2.Statement) -> None:
        end_session()

    def do_list_sessions(self, _: cmd2.Statement) -> None:
        list_sessions()

    @cmd2.with_argparser(use_session_args)
    def do_use_session(self, args: argparse.Namespace) -> None:
        use_session(args)

    @cmd2.with_argparser(use_prompt_template_args)
    def do_use_prompt_template(self, args: argparse.Namespace) -> None:
        use_prompt_template(args)

    def do_clear_prompt_template(self, _: cmd2.Statement) -> None:
        clear_prompt_template()

    def do_list_context_strategies(self, _: cmd2.Statement) -> None:
        list_context_strategies()

    @cmd2.with_argparser(use_context_strategy_args)
    def do_use_context_strategy(self, args: argparse.Namespace) -> None:
        use_context_strategy(args)

    def do_clear_context_strategy(self, _: cmd2.Statement) -> None:
        clear_context_strategy()
