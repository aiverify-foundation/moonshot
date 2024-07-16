import argparse

import cmd2

from moonshot.integrations.cli.redteam.attack_module import (
    delete_attack_module,
    delete_attack_module_args,
    list_attack_modules,
    list_attack_modules_args,
)
from moonshot.integrations.cli.redteam.context_strategy import (
    clear_context_strategy,
    delete_context_strategy,
    delete_context_strategy_args,
    list_context_strategies,
    list_context_strategies_args,
    use_context_strategy,
    use_context_strategy_args,
)
from moonshot.integrations.cli.redteam.prompt_template import (
    clear_prompt_template,
    use_prompt_template,
    use_prompt_template_args,
)
from moonshot.integrations.cli.redteam.session import (
    add_bookmark,
    add_bookmark_args,
    automated_rt_session_args,
    delete_bookmark,
    delete_bookmark_args,
    delete_session,
    delete_session_args,
    end_session,
    export_bookmarks,
    export_bookmarks_args,
    list_bookmarks,
    list_bookmarks_args,
    list_sessions,
    list_sessions_args,
    new_session,
    new_session_args,
    run_attack_module,
    show_prompts,
    use_bookmark,
    use_bookmark_args,
    use_session,
    use_session_args,
    view_bookmark,
    view_bookmark_args,
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

    @cmd2.with_argparser(list_sessions_args)
    def do_list_sessions(self, args: argparse.Namespace) -> None:
        list_sessions(args)

    @cmd2.with_argparser(use_session_args)
    def do_use_session(self, args: argparse.Namespace) -> None:
        use_session(args)

    @cmd2.with_argparser(use_prompt_template_args)
    def do_use_prompt_template(self, args: argparse.Namespace) -> None:
        use_prompt_template(args)

    def do_clear_prompt_template(self, _: cmd2.Statement) -> None:
        clear_prompt_template()

    @cmd2.with_argparser(list_context_strategies_args)
    def do_list_context_strategies(self, args: argparse.Namespace) -> None:
        list_context_strategies(args)

    @cmd2.with_argparser(use_context_strategy_args)
    def do_use_context_strategy(self, args: argparse.Namespace) -> None:
        use_context_strategy(args)

    def do_clear_context_strategy(self, _: cmd2.Statement) -> None:
        clear_context_strategy()

    @cmd2.with_argparser(automated_rt_session_args)
    def do_run_attack_module(self, args: argparse.Namespace) -> None:
        run_attack_module(args)

    @cmd2.with_argparser(list_attack_modules_args)
    def do_list_attack_modules(self, args: argparse.Namespace) -> None:
        list_attack_modules(args)

    @cmd2.with_argparser(delete_session_args)
    def do_delete_session(self, args: argparse.Namespace) -> None:
        delete_session(args)

    @cmd2.with_argparser(delete_context_strategy_args)
    def do_delete_context_strategy(self, args: argparse.Namespace) -> None:
        delete_context_strategy(args)

    @cmd2.with_argparser(delete_attack_module_args)
    def do_delete_attack_module(self, args: argparse.Namespace) -> None:
        delete_attack_module(args)

    @cmd2.with_argparser(add_bookmark_args)
    def do_add_bookmark(self, args: argparse.Namespace) -> None:
        add_bookmark(args)

    @cmd2.with_argparser(use_bookmark_args)
    def do_use_bookmark(self, args: argparse.Namespace) -> None:
        use_bookmark(args)

    @cmd2.with_argparser(delete_bookmark_args)
    def do_delete_bookmark(self, args: argparse.Namespace) -> None:
        delete_bookmark(args)

    @cmd2.with_argparser(list_bookmarks_args)
    def do_list_bookmarks(self, args: argparse.Namespace) -> None:
        list_bookmarks(args)

    @cmd2.with_argparser(view_bookmark_args)
    def do_view_bookmark(self, args: argparse.Namespace) -> None:
        view_bookmark(args)

    @cmd2.with_argparser(export_bookmarks_args)
    def do_export_bookmarks(self, args: argparse.Namespace) -> None:
        export_bookmarks(args)

    def do_show_prompts(self, _: cmd2.Statement) -> None:
        show_prompts()
