from __future__ import annotations

import asyncio
import time

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.metrics.metric import Metric
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.recipes.recipe_type import RecipeType
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_arguments import RunArguments
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_accessor import DBAccessor
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class Run:
    sql_create_run_record = """
        INSERT INTO run_table (
        run_type,recipes,cookbooks,endpoints,num_of_prompts,results_file,start_time,end_time,duration,
        error_messages,results,status)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """
    sql_update_run_record = """
        UPDATE run_table SET run_type=?,recipes=?,cookbooks=?,endpoints=?,num_of_prompts=?,results_file=?,
        start_time=?,end_time=?,duration=?,error_messages=?,results=?,status=?
        WHERE run_id=(SELECT MAX(run_id) FROM run_table)
    """
    sql_read_run_record = """
        SELECT * from run_table WHERE run_id=(SELECT MAX(run_id) FROM run_table)
    """

    def __init__(self, run_args: RunArguments) -> None:
        # These attributes will be provided by the runner
        self.run_type = run_args.run_type
        self.recipes = run_args.recipes
        self.cookbooks = run_args.cookbooks
        self.endpoints = run_args.endpoints
        self.num_of_prompts = run_args.num_of_prompts
        self.database_instance = run_args.database_instance
        self.results_file = run_args.results_file
        self.progress = run_args.progress

        # These attributes will be usually in default values set in RunArguments
        self.start_time = run_args.start_time
        self.end_time = run_args.end_time
        self.duration = run_args.duration
        self.error_messages = run_args.error_messages
        self.results = run_args.results
        self.status = run_args.status

        # These attributes will be the default processing module
        self.benchmark_processing_module = "benchmarking"
        self.redteam_processing_module = "redteaming"

    @staticmethod
    def load(database_instance: DBAccessor | None) -> RunArguments:
        """
        Loads the latest run data from the database.

        This method retrieves the most recent run data from the database. If the database instance is not provided,
        it raises a RuntimeError. If the database instance is provided, it invokes the read_record method of the
        database instance and returns a RunArguments object created from the retrieved record.

        Returns:
            RunArguments: An object containing the details of the latest run.
        """
        if database_instance:
            run_arguments_info = Storage.read_database_record(
                database_instance,
                (),
                Run.sql_read_run_record,
            )
            if run_arguments_info:
                return RunArguments.from_tuple(run_arguments_info)
            else:
                raise RuntimeError(
                    f"Failed to get database record: {database_instance}"
                )
        else:
            raise RuntimeError(f"Failed to get database instance: {database_instance}")

    def handle_error_message(self, error_message: str) -> None:
        """
        This method is used to handle error messages during the execution of a run. It takes an error message as input,
        prints it, and adds it to the error_messages list. It then updates the progress status to RUNNING_WITH_ERRORS
        and calls the update_progress method to update the progress status and error messages.

        Args:
            error_message (str): The error message to be handled.

        Returns:
            None
        """
        # Print the error message and add to the error messages list
        print(error_message)
        self.error_messages.append(error_message)

        # Update the progress status
        self.update_progress(RunStatus.RUNNING_WITH_ERRORS)
        if self.progress:
            self.progress.update_progress(
                status=self.status.name, error_messages=self.error_messages
            )

    def update_progress(self, status: RunStatus | None = None) -> None:
        """
        This method is used to update the progress of a run. It takes an optional status as input,
        updates the end time and duration of the run, and if a status is provided, updates the run status as well.
        If a database instance is available, it updates the database record with the current run arguments.
        If no database instance is available, it prints an error message.

        Args:
            status (RunStatus | None): The status to be updated. Default is None.

        Returns:
            None
        """
        self.end_time = time.time()
        self.duration = int(self.end_time - self.start_time)
        if status:
            self.status = status

        if self.database_instance:
            Storage.update_database_record(
                self.database_instance,
                self.get_run_arguments().to_tuple(),
                Run.sql_update_run_record,
            )
        else:
            print(
                "[Run] Unable to update run progress: db_instance is not initialised."
            )

    def get_run_arguments(self) -> RunArguments:
        """
        This method is used to get the arguments of a run. It returns a RunArguments object that contains all the
        necessary details of the run such as run_type, recipes, cookbooks, endpoints, num_of_prompts, database_instance,
        results_file, progress, start_time, end_time, duration, error_messages, results, and status.

        Returns:
            RunArguments: An object that contains all the necessary details of the run.
        """
        return RunArguments(
            run_type=self.run_type,
            recipes=self.recipes,
            cookbooks=self.cookbooks,
            endpoints=self.endpoints,
            num_of_prompts=self.num_of_prompts,
            database_instance=self.database_instance,
            results_file=self.results_file,
            progress=self.progress,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            error_messages=self.error_messages,
            results=self.results,
            status=self.status,
        )

    async def run(self) -> None:
        """
        This method is responsible for executing a run.

        The run type is determined by the instance attribute 'run_type'. The method first creates a run record in
        the database if a database instance is available.
        It then checks the run type and runs the appropriate process based on the run type.
        If the run type is RECIPE, it runs all the recipes and updates the progress and results accordingly.
        If the run type is not recognized, it raises a RuntimeError.

        Args:
            None

        Returns:
            None

        Raises:
            RuntimeError: If the run type is not recognized or if the database instance is not available.
        """
        # Create a run record
        if self.database_instance:
            Storage.create_database_record(
                self.database_instance,
                self.get_run_arguments().to_tuple(),
                Run.sql_create_run_record,
            )
        else:
            raise RuntimeError(
                f"Failed to get database instance: {self.database_instance}"
            )

        # Run based on its type
        if self.run_type is RunnerType.RECIPE:
            print(f"🔃 Running recipes ({self.recipes})... do not close this terminal.")
            print("You can start a new terminal to continue working.")

            # Update progress
            self.update_progress(RunStatus.RUNNING)
            if self.progress:
                self.progress.update_progress(
                    status=self.status.name,
                    duration=self.duration,
                )

            # Run all recipes
            for recipe_index, recipe in enumerate(self.recipes, 0):
                print(
                    f"[Run] Running recipe {recipe}... ({recipe_index+1}/{len(self.recipes)})"
                )

                # Update progress
                if self.progress:
                    self.progress.update_progress(
                        recipe_index=recipe_index,
                        recipe_name=recipe,
                        recipe_total=len(self.recipes),
                    )

                # Run the recipe
                self.results[recipe] = await self._run_recipe(recipe)

            # Update progress
            if not self.error_messages:
                self.update_progress(RunStatus.COMPLETED)
                if self.progress:
                    self.progress.update_progress(
                        recipe_index=len(self.recipes),
                        status=self.status.name,
                        duration=self.duration,
                    )
            else:
                self.update_progress(RunStatus.COMPLETED_WITH_ERRORS)
                if self.progress:
                    self.progress.update_progress(
                        recipe_index=len(self.recipes),
                        status=self.status.name,
                        duration=self.duration,
                        error_messages=self.error_messages,
                    )

        elif self.run_type is RunnerType.COOKBOOK:
            print(
                f"🔃 Running cookbooks ({self.cookbooks})... do not close this terminal."
            )
            print("You can start a new terminal to continue working.")

            # Update progress
            self.update_progress(RunStatus.RUNNING)
            if self.progress:
                self.progress.update_progress(
                    status=self.status.name,
                    duration=self.duration,
                )

            # Run all cookbooks
            for cookbook_index, cookbook in enumerate(self.cookbooks, 0):
                print(
                    f"[Run] Running cookbook {cookbook}... ({cookbook_index+1}/{len(self.cookbooks)})"
                )

                # Update progress
                if self.progress:
                    self.progress.update_progress(
                        cookbook_index=cookbook_index,
                        cookbook_name=cookbook,
                        cookbook_total=len(self.cookbooks),
                        recipe_index=-1,
                        recipe_name="",
                        recipe_total=-1,
                    )

                # Run the cookbook
                self.results[cookbook] = await self._run_cookbook(cookbook)

            # Update progress
            if not self.error_messages:
                self.update_progress(RunStatus.COMPLETED)
                if self.progress:
                    self.progress.update_progress(
                        cookbook_index=len(self.cookbooks),
                        status=self.status.name,
                        duration=self.duration,
                    )
            else:
                self.update_progress(RunStatus.COMPLETED_WITH_ERRORS)
                if self.progress:
                    self.progress.update_progress(
                        cookbook_index=len(self.cookbooks),
                        status=self.status.name,
                        duration=self.duration,
                        error_messages=self.error_messages,
                    )

        else:
            print("[Run] Failed to run benchmark due to invalid run type.")
            self.handle_error_message(
                "Failed to run benchmark due to invalid run type."
            )

            # Update progress
            self.update_progress(RunStatus.COMPLETED_WITH_ERRORS)
            if self.progress:
                self.progress.update_progress(
                    status=self.status.name,
                    duration=self.duration,
                    error_messages=self.error_messages,
                )

    async def _run_cookbook(self, cookbook: str) -> dict:
        """
        This method is responsible for running a given cookbook.

        It accepts a cookbook string as an argument. The method first loads the cookbook instance.
        It then iterates over the recipes in the cookbook and invokes the appropriate recipe processing module
        based on the recipe type.
        If the recipe type is not recognized, it raises a RuntimeError.
        If the recipe processing is successful, it returns a dictionary of recipe results.

        Args:
            cookbook (str): The name of the cookbook to be executed.

        Returns:
            dict: A dictionary containing the results of the executed recipes in the cookbook.

        Raises:
            RuntimeError: If the recipe type is not recognized.
        """
        # ------------------------------------------------------------------------------
        # Part 1: Load instances
        # ------------------------------------------------------------------------------
        print("[Run] Part 1: Loading various cookbook instances...")
        cookbook_inst = None
        try:
            start_time = time.perf_counter()
            cookbook_inst = Cookbook.load(cookbook)
            print(
                f"[Run] Load cookbook instance took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            error_message = f"Failed to load instances in running cookbook Part 1 due to error: {str(e)}"
            self.handle_error_message(error_message)

        # ------------------------------------------------------------------------------
        # Part 2: Run recipes
        # ------------------------------------------------------------------------------
        print("[Run] Part 2: Running cookbook recipes...")
        recipe_results = {}
        try:
            start_time = time.perf_counter()
            if cookbook_inst:
                # Update progress
                self.update_progress()
                if self.progress:
                    self.progress.update_progress(
                        status=self.status.name,
                        duration=self.duration,
                    )

                # Run all recipes
                for recipe_index, recipe in enumerate(cookbook_inst.recipes, 0):
                    print(
                        f"[Run] Running recipe {recipe}... ({recipe_index+1}/{len(cookbook_inst.recipes)})"
                    )

                    # Update progress
                    if self.progress:
                        self.progress.update_progress(
                            recipe_index=recipe_index,
                            recipe_name=recipe,
                            recipe_total=len(cookbook_inst.recipes),
                        )

                    # Run the recipe
                    recipe_results[recipe] = await self._run_recipe(recipe)

                # Update progress
                self.update_progress()
                if self.progress:
                    self.progress.update_progress(
                        recipe_index=len(cookbook_inst.recipes),
                        duration=self.duration,
                    )

                print(
                    f"[Run] Running cookbook [{cookbook_inst.id}] took {(time.perf_counter() - start_time):.4f}s"
                )
            else:
                raise RuntimeError("cookbook_inst is None")

        except Exception as e:
            error_message = f"Failed to load instances in running cookbook Part 2 due to error: {str(e)}"
            self.handle_error_message(error_message)

        finally:
            return recipe_results

    async def _run_recipe(self, recipe: str) -> dict:
        """
        This method is responsible for running a given recipe.

        It accepts a recipe string as an argument. The method first loads the recipe instance, recipe endpoints,
        and metrics instances.
        It then invokes the appropriate recipe processing module based on the recipe type.
        If the recipe type is not recognized, it raises a RuntimeError.
        If the recipe processing is successful, it returns a dictionary of recipe results.

        Args:
            recipe (str): The name of the recipe to be executed.

        Returns:
            dict: A dictionary containing the results of the executed recipe.

        Raises:
            RuntimeError: If the recipe type is not recognized.
        """
        # ------------------------------------------------------------------------------
        # Part 0: Get asyncio running loop
        # ------------------------------------------------------------------------------
        print("[Run] Part 0: Loading asyncio running loop...")
        loop = asyncio.get_running_loop()

        # ------------------------------------------------------------------------------
        # Part 1: Load instances
        # ------------------------------------------------------------------------------
        print("[Run] Part 1: Loading various recipe instances...")
        recipe_inst = None
        recipe_eps = []
        metrics_instances = []
        try:
            start_time = time.perf_counter()
            recipe_inst = Recipe.load(recipe)
            print(
                f"[Run] Load recipe instance took {(time.perf_counter() - start_time):.4f}s"
            )

            start_time = time.perf_counter()
            recipe_eps = [
                Connector.create(ConnectorEndpoint.read(endpoint))
                for endpoint in self.endpoints
            ]
            print(
                f"[Run] Load recipe endpoints instances took {(time.perf_counter() - start_time):.4f}s"
            )

            start_time = time.perf_counter()
            metrics_instances = [Metric.load(metric) for metric in recipe_inst.metrics]
            print(f"[Run] Load metrics took {(time.perf_counter() - start_time):.4f}s")

        except Exception as e:
            error_message = f"Failed to load instances in running recipe Part 1 due to error: {str(e)}"
            self.handle_error_message(error_message)

        # ------------------------------------------------------------------------------
        # Part 2: Invoke recipe processing modules to process
        # ------------------------------------------------------------------------------
        print("[Run] Part 2: Invoke recipe processing module...")
        start_time = time.perf_counter()
        recipe_results = {}
        try:
            selected_rec_proc_module = None
            rec_proc_instance = None

            if not recipe_inst:
                raise RuntimeError("recipe_inst is None")

            # Retrieve the recipe processing module
            if recipe_inst.type is RecipeType.BENCHMARK:
                selected_rec_proc_module = self.benchmark_processing_module
            elif recipe_inst.type is RecipeType.REDTEAM:
                selected_rec_proc_module = self.redteam_processing_module
            else:
                raise RuntimeError("recipe type is invalid")

            # Intialize the recipe processing instance
            rec_proc_instance = get_instance(
                selected_rec_proc_module,
                Storage.get_filepath(
                    EnvVariables.RECIPES_MODULES.name,
                    selected_rec_proc_module,
                    "py",
                ),
            )
            if rec_proc_instance:
                rec_proc_instance = rec_proc_instance()
            else:
                raise RuntimeError(
                    f"Unable to get defined recipe processing instance - {selected_rec_proc_module}"
                )

            # Run the rec_proc_instance for it to generate
            print(
                f"[Run] Performing processing for recipe [{recipe}] using processing module: {selected_rec_proc_module}"
            )
            recipe_results = await rec_proc_instance.generate(
                loop,
                self.database_instance,
                self.num_of_prompts,
                recipe_inst,
                recipe_eps,
                metrics_instances,
                self.handle_error_message,
            )

        except Exception as e:
            error_message = (
                f"Failed to invoke recipe processing module in executing recipe Part 2 "
                f"due to error: {str(e)}"
            )
            self.handle_error_message(error_message)

        finally:
            print(
                f"[Run] Performing processing for recipe [{recipe}] took {(time.perf_counter() - start_time):.4f}s"
            )
            return recipe_results
