import argparse

import cmd2

from moonshot.integrations.cli.benchmark.cookbook import (
    add_cookbook,
    add_cookbook_args,
    delete_cookbook,
    delete_cookbook_args,
    list_cookbooks,
    list_cookbooks_args,
    run_cookbook,
    run_cookbook_args,
    update_cookbook,
    update_cookbook_args,
    view_cookbook,
    view_cookbook_args,
)
from moonshot.integrations.cli.benchmark.datasets import (
    delete_dataset,
    delete_dataset_args,
    list_datasets,
    list_datasets_args,
    view_dataset,
    view_dataset_args,
)
from moonshot.integrations.cli.benchmark.metrics import (
    delete_metric,
    delete_metric_args,
    list_metrics,
    list_metrics_args,
    view_metric,
    view_metric_args,
)
from moonshot.integrations.cli.benchmark.recipe import (
    add_recipe,
    add_recipe_args,
    delete_recipe,
    delete_recipe_args,
    list_recipes,
    list_recipes_args,
    run_recipe,
    run_recipe_args,
    update_recipe,
    update_recipe_args,
    view_recipe,
    view_recipe_args,
)
from moonshot.integrations.cli.benchmark.result import (
    delete_result,
    delete_result_args,
    list_results,
    list_results_args,
    view_result,
    view_result_args,
)
from moonshot.integrations.cli.benchmark.run import (
    list_runs,
    list_runs_args,
    view_run,
    view_run_args,
)
from moonshot.integrations.cli.benchmark.runner import (
    delete_runner,
    delete_runner_args,
    list_runners,
    view_runner,
    view_runner_args,
)


@cmd2.with_default_category("Moonshot Benchmarking")
class BenchmarkCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------------
    # List contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(list_cookbooks_args)
    def do_list_cookbooks(self, args: argparse.Namespace) -> None:
        list_cookbooks(args)

    @cmd2.with_argparser(list_recipes_args)
    def do_list_recipes(self, args: argparse.Namespace) -> None:
        list_recipes(args)

    @cmd2.with_argparser(list_results_args)
    def do_list_results(self, args: argparse.Namespace) -> None:
        list_results(args)

    def do_list_runners(self, _: cmd2.Statement) -> None:
        list_runners()

    @cmd2.with_argparser(list_runs_args)
    def do_list_runs(self, args: argparse.Namespace) -> None:
        list_runs(args)

    @cmd2.with_argparser(list_metrics_args)
    def do_list_metrics(self, args: argparse.Namespace) -> None:
        list_metrics(args)

    @cmd2.with_argparser(list_datasets_args)
    def do_list_datasets(self, args: argparse.Namespace) -> None:
        list_datasets(args)

    # ------------------------------------------------------------------------------
    # Add contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(add_cookbook_args)
    def do_add_cookbook(self, args: argparse.Namespace) -> None:
        add_cookbook(args)

    @cmd2.with_argparser(add_recipe_args)
    def do_add_recipe(self, args: argparse.Namespace) -> None:
        add_recipe(args)

    # ------------------------------------------------------------------------------
    # Delete contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(delete_cookbook_args)
    def do_delete_cookbook(self, args: argparse.Namespace) -> None:
        delete_cookbook(args)

    @cmd2.with_argparser(delete_recipe_args)
    def do_delete_recipe(self, args: argparse.Namespace) -> None:
        delete_recipe(args)

    @cmd2.with_argparser(delete_result_args)
    def do_delete_result(self, args: argparse.Namespace) -> None:
        delete_result(args)

    @cmd2.with_argparser(delete_runner_args)
    def do_delete_runner(self, args: argparse.Namespace) -> None:
        delete_runner(args)

    @cmd2.with_argparser(delete_metric_args)
    def do_delete_metric(self, args: argparse.Namespace) -> None:
        delete_metric(args)

    @cmd2.with_argparser(delete_dataset_args)
    def do_delete_dataset(self, args: argparse.Namespace) -> None:
        delete_dataset(args)

    # ------------------------------------------------------------------------------
    # Update contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(update_cookbook_args)
    def do_update_cookbook(self, args: argparse.Namespace) -> None:
        update_cookbook(args)

    @cmd2.with_argparser(update_recipe_args)
    def do_update_recipe(self, args: argparse.Namespace) -> None:
        update_recipe(args)

    # ------------------------------------------------------------------------------
    # Run contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(run_cookbook_args)
    def do_run_cookbook(self, args: argparse.Namespace) -> None:
        run_cookbook(args)

    @cmd2.with_argparser(run_recipe_args)
    def do_run_recipe(self, args: argparse.Namespace) -> None:
        run_recipe(args)

    # ------------------------------------------------------------------------------
    # View contents
    # ------------------------------------------------------------------------------

    @cmd2.with_argparser(view_cookbook_args)
    def do_view_cookbook(self, args: argparse.Namespace) -> None:
        view_cookbook(args)

    @cmd2.with_argparser(view_recipe_args)
    def do_view_recipe(self, args: argparse.Namespace) -> None:
        view_recipe(args)

    @cmd2.with_argparser(view_result_args)
    def do_view_result(self, args: argparse.Namespace) -> None:
        view_result(args)

    @cmd2.with_argparser(view_runner_args)
    def do_view_runner(self, args: argparse.Namespace) -> None:
        view_runner(args)

    @cmd2.with_argparser(view_run_args)
    def do_view_run(self, args: argparse.Namespace) -> None:
        view_run(args)

    @cmd2.with_argparser(view_metric_args)
    def do_view_metric(self, args: argparse.Namespace) -> None:
        view_metric(args)

    @cmd2.with_argparser(view_dataset_args)
    def do_view_dataset(self, args: argparse.Namespace) -> None:
        view_dataset(args)
