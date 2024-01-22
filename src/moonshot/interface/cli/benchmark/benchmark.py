import argparse

import cmd2

from moonshot.interface.cli.benchmark.connection import *
from moonshot.interface.cli.benchmark.cookbook import *
from moonshot.interface.cli.benchmark.recipe import *
from moonshot.interface.cli.benchmark.results import *
from moonshot.interface.cli.benchmark.run import *


@cmd2.with_default_category("Moonshot Benchmarking")
class BenchmarkCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @cmd2.with_argparser(add_endpoint_args)
    def do_add_endpoint(self, args: argparse.Namespace) -> None:
        add_endpoint(args)

    @cmd2.with_argparser(add_cookbook_args)
    def do_add_cookbook(self, args: argparse.Namespace) -> None:
        add_cookbook(args)

    def do_list_cookbooks(self, _: cmd2.Statement) -> None:
        list_cookbooks()

    @cmd2.with_argparser(view_cookbook_args)
    def do_view_cookbook(self, args: argparse.Namespace) -> None:
        view_cookbook(args)

    @cmd2.with_argparser(run_cookbook_args)
    def do_run_cookbook(self, args: argparse.Namespace) -> None:
        run_cookbook(args)

    @cmd2.with_argparser(add_recipe_args)
    def do_add_recipe(self, args: argparse.Namespace) -> None:
        add_recipe(args)

    def do_list_recipes(self, args: argparse.Namespace) -> None:
        list_recipes()

    @cmd2.with_argparser(run_recipe_args)
    def do_run_recipe(self, args: argparse.Namespace) -> None:
        run_recipe(args)

    def do_list_results(self, _: cmd2.Statement) -> None:
        list_results()

    @cmd2.with_argparser(view_results_args)
    def do_view_results(self, args: argparse.Namespace) -> None:
        view_results(args)

    def do_list_runs(self, _: cmd2.Statement) -> None:
        list_runs()

    @cmd2.with_argparser(resume_run_args)
    def do_resume_run(self, args: argparse.Namespace) -> None:
        resume_run(args)
