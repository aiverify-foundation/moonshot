import argparse

import cmd2

from moonshot.integrations.cli.common.connectors import (
    add_endpoint,
    add_endpoint_args,
    delete_endpoint,
    delete_endpoint_args,
    list_connector_types,
    list_endpoints,
    update_endpoint,
    update_endpoint_args,
    view_endpoint,
    view_endpoint_args,
)
from moonshot.integrations.cli.common.prompt_template import (
    delete_prompt_template,
    delete_prompt_template_args,
    list_prompt_templates,
)


@cmd2.with_default_category("Moonshot Common")
class CommonCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------------
    # List contents
    # ------------------------------------------------------------------------------

    def do_list_connector_types(self, _: cmd2.Statement) -> None:
        list_connector_types()

    def do_list_endpoints(self, _: cmd2.Statement) -> None:
        list_endpoints()

    def do_list_prompt_templates(self, _: cmd2.Statement) -> None:
        list_prompt_templates()

    @cmd2.with_argparser(delete_prompt_template_args)
    def do_delete_prompt_template(self, args: argparse.Namespace) -> None:
        delete_prompt_template(args)

    # ------------------------------------------------------------------------------
    # Add contents
    # ------------------------------------------------------------------------------
    @cmd2.with_argparser(add_endpoint_args)
    def do_add_endpoint(self, args: argparse.Namespace) -> None:
        add_endpoint(args)

    # ------------------------------------------------------------------------------
    # Delete contents
    # ------------------------------------------------------------------------------
    @cmd2.with_argparser(delete_endpoint_args)
    def do_delete_endpoint(self, args: argparse.Namespace) -> None:
        delete_endpoint(args)

    # ------------------------------------------------------------------------------
    # Update contents
    # ------------------------------------------------------------------------------
    @cmd2.with_argparser(update_endpoint_args)
    def do_update_endpoint(self, args: argparse.Namespace) -> None:
        update_endpoint(args)

    # ------------------------------------------------------------------------------
    # View contents
    # ------------------------------------------------------------------------------
    @cmd2.with_argparser(view_endpoint_args)
    def do_view_endpoint(self, args: argparse.Namespace) -> None:
        view_endpoint(args)
