import argparse

import cmd2

from moonshot.integrations.cli.common.connectors import (
    add_endpoint,
    add_endpoint_args,
    delete_endpoint,
    delete_endpoint_args,
    list_connector_types,
    list_connector_types_args,
    list_endpoints,
    list_endpoints_args,
    update_endpoint,
    update_endpoint_args,
    view_endpoint,
    view_endpoint_args,
)
from moonshot.integrations.cli.common.dataset import (
    convert_dataset,
    convert_dataset_args,
    download_dataset,
    download_dataset_args,
)
from moonshot.integrations.cli.common.prompt_template import (
    delete_prompt_template,
    delete_prompt_template_args,
    list_prompt_templates,
    list_prompt_templates_args,
)


@cmd2.with_default_category("Moonshot Common")
class CommonCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------------
    # List contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(list_connector_types_args)
    def do_list_connector_types(self, args: argparse.Namespace) -> None:
        list_connector_types(args)

    @cmd2.with_argparser(list_endpoints_args)
    def do_list_endpoints(self, args: argparse.Namespace) -> None:
        list_endpoints(args)

    @cmd2.with_argparser(list_prompt_templates_args)
    def do_list_prompt_templates(self, args: argparse.Namespace) -> None:
        list_prompt_templates(args)

    @cmd2.with_argparser(delete_prompt_template_args)
    def do_delete_prompt_template(self, args: argparse.Namespace) -> None:
        delete_prompt_template(args)

    # ------------------------------------------------------------------------------
    # Add contents
    # ------------------------------------------------------------------------------
    @cmd2.with_argparser(add_endpoint_args)
    def do_add_endpoint(self, args: argparse.Namespace) -> None:
        add_endpoint(args)

    @cmd2.with_argparser(convert_dataset_args)
    def do_convert_dataset(self, args: argparse.Namespace) -> None:
        convert_dataset(args)

    @cmd2.with_argparser(download_dataset_args)
    def do_download_dataset(self, args: argparse.Namespace) -> None:
        download_dataset(args)

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
