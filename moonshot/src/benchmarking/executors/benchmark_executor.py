from __future__ import annotations

import asyncio
import time
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import Any, AsyncGenerator, Callable, Union

from jinja2 import Template
from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.benchmarking.cookbooks.cookbook import Cookbook
from moonshot.src.benchmarking.executors.benchmark_executor_arguments import (
    BenchmarkExecutorArguments,
)
from moonshot.src.benchmarking.executors.benchmark_executor_progress import (
    BenchmarkExecutorProgress,
)
from moonshot.src.benchmarking.executors.benchmark_executor_status import (
    BenchmarkExecutorStatus,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)
from moonshot.src.benchmarking.metrics.metric import Metric
from moonshot.src.benchmarking.prompt_arguments import PromptArguments
from moonshot.src.benchmarking.recipes.recipe import Recipe
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_manager import ConnectorManager
from moonshot.src.storage.storage_manager import StorageManager


class BenchmarkExecutor:
    def __init__(self, be_args: BenchmarkExecutorArguments) -> None:
        self.id = be_args.id
        self.name = be_args.name
        self.type = be_args.type
        self.start_time = be_args.start_time
        self.end_time = be_args.end_time
        self.duration = be_args.duration
        self.database_instance = be_args.database_instance
        self.database_file = be_args.database_file
        self.results_file = be_args.results_file
        self.recipes = be_args.recipes
        self.cookbooks = be_args.cookbooks
        self.endpoints = be_args.endpoints
        self.num_of_prompts = be_args.num_of_prompts
        self.results = be_args.results
        self.status = be_args.status
        self.progress_callback_func = be_args.progress_callback_func
        self.benchmark_executor_progress = BenchmarkExecutorProgress(
            exec_id=str(self.id),
            exec_name=self.name,
            exec_type=self.type.name,
            bm_max_progress_per_recipe=int(100.0 / len(self.recipes))
            if len(self.recipes) > 0
            else 0,
            bm_max_progress_per_cookbook=int(100.0 / len(self.cookbooks))
            if len(self.cookbooks) > 0
            else 0,
            bm_progress_callback_func=self.progress_callback_func,
        )

    @classmethod
    def create_executor(cls, be_args: BenchmarkExecutorArguments) -> BenchmarkExecutor:
        """
        Creates a new BenchmarkExecutor instance.

        This method takes a BenchmarkExecutorArguments object as an argument, which contains all the necessary
        information to create a new BenchmarkExecutor. It generates a unique id for the executor based on its type
        and name, and sets up the necessary storage for the executor. If the executor is successfully created, it
        is returned. If there is an error during creation, the error is printed and re-raised.

        Args:
            be_args (BenchmarkExecutorArguments): The arguments to create the executor.

        Returns:
            BenchmarkExecutor: The newly created executor.

        Raises:
            Exception: If there is an error during executor creation.
        """
        try:
            prefix = (
                "recipe-"
                if be_args.type == BenchmarkExecutorTypes.RECIPE
                else "cookbook-"
            )
            be_id = slugify(prefix + be_args.name, lowercase=True)

            # Check if the executor database file already exists. If it does, raise an error to prevent overwriting.
            if Path(StorageManager.get_executor_database_filepath(be_id)).exists():
                raise RuntimeError(
                    "Unable to create executor because the database file exists."
                )

            be_info = {
                "id": be_id,
                "name": be_args.name,
                "type": be_args.type,
                "start_time": be_args.start_time,
                "end_time": be_args.end_time,
                "duration": be_args.duration,
                "database_file": StorageManager.get_executor_database_filepath(be_id),
                "results_file": StorageManager.get_executor_results_filepath(be_id),
                "recipes": be_args.recipes,
                "cookbooks": be_args.cookbooks,
                "endpoints": be_args.endpoints,
                "num_of_prompts": be_args.num_of_prompts,
                "results": be_args.results,
                "status": be_args.status,
                "progress_callback_func": be_args.progress_callback_func,
            }
            be_args = BenchmarkExecutorArguments(**be_info)
            be_args.database_instance = (
                StorageManager.create_executor_database_connection(be_id)
            )
            StorageManager.create_executor_storage(
                be_args.to_tuple(), be_args.database_instance
            )

            # Return an instance of executor
            return cls(be_args)

        except Exception as e:
            print(f"Failed to create executor: {str(e)}")
            raise e

    @classmethod
    def load_executor(
        cls, be_id: str, progress_callback_func: Union[Callable, None] = None
    ) -> BenchmarkExecutor:
        """
        Loads an executor by its ID.

        This method loads an executor by its ID. It first checks if the executor database file exists.
        If it does, it creates a database connection and reads the executor storage.
        It then sets the database instance and progress callback function in the BenchmarkExecutorArguments object.
        If the database file does not exist, it raises a RuntimeError.

        Args:
            be_id (str): The ID of the executor to load.
            progress_callback_func (Union[Callable, None]): The progress callback function for the executor.

        Returns:
            BenchmarkExecutor: The loaded executor instance.

        Raises:
            RuntimeError: If the executor database file does not exist.
            Exception: If there is an error during executor loading.
        """
        db_instance = None
        try:
            # Check if the executor database file exists. If it does not exist, raise an error.
            if not Path(StorageManager.get_executor_database_filepath(be_id)).exists():
                raise RuntimeError(
                    "Unable to create executor because the database file does not exists."
                )

            db_instance = StorageManager.create_executor_database_connection(be_id)
            be_args = BenchmarkExecutorArguments.from_tuple(
                StorageManager.read_executor_storage(be_id, db_instance)
            )
            be_args.database_instance = db_instance
            be_args.progress_callback_func = progress_callback_func

            return cls(be_args)

        except Exception as e:
            print(f"Failed to load executor: {str(e)}")
            raise e

    @staticmethod
    def delete_executor(be_id: str) -> None:
        """
        Deletes an existing executor.

        This function takes a BenchmarkExecutor ID as input. It first deletes the executor's database and results
        using the StorageManager. If there is an error during the deletion, the error is printed and re-raised.

        Args:
            be_id (str): The ID of the executor to be deleted.

        Raises:
            Exception: If there is an error during executor deletion.
        """
        try:
            StorageManager.remove_executor_database(be_id)
            StorageManager.remove_executor_results(be_id)

        except Exception as e:
            print(f"Failed to delete executor: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read_executor_arguments(be_id: str) -> BenchmarkExecutorArguments:
        """
        Reads the executor's arguments from the storage.

        This function takes a BenchmarkExecutor ID as input. It first creates a connection to the executor's database
        using the StorageManager. Then, it reads the executor's storage and converts the result into a
        BenchmarkExecutorArguments object. If there is an error during the reading, the error is printed and re-raised.

        Args:
            be_id (str): The ID of the executor whose arguments are to be read.

        Returns:
            BenchmarkExecutorArguments: The arguments of the executor.

        Raises:
            Exception: If there is an error during executor arguments reading.
        """
        db_instance = None
        try:
            db_instance = StorageManager.create_executor_database_connection(be_id)
            return BenchmarkExecutorArguments.from_tuple(
                StorageManager.read_executor_storage(be_id, db_instance)
            )

        except Exception as e:
            print(f"Failed to read executor: {str(e)}")
            raise e

        finally:
            if db_instance:
                StorageManager.close_executor_database_connection(db_instance)

    @staticmethod
    def get_available_executors() -> tuple[list[str], list[BenchmarkExecutorArguments]]:
        """
        Retrieves all available benchmark executors.

        This function calls the get_executors method to retrieve all available benchmark executors. It then converts
        each executor into a BenchmarkExecutorArguments object using the from_tuple method and returns a tuple of
        two lists:
            a list of executor IDs and a list of BenchmarkExecutorArguments objects.

        Returns:
            tuple[list[str], list[BenchmarkExecutorArguments]]: A tuple of two lists, the first list contains the IDs
            of the executors, and the second list contains the BenchmarkExecutorArguments objects of the executors.

        Raises:
            Exception: If there is an error during executor retrieval.
        """
        try:
            retn_bes = []
            retn_bes_ids = []

            execs = StorageManager.get_executors()
            for exec in execs:
                if "__" in exec:
                    continue

                db_instance = StorageManager.create_executor_database_connection(exec)
                be_info = BenchmarkExecutorArguments.from_tuple(
                    StorageManager.read_executor_storage(exec, db_instance)
                )
                StorageManager.close_executor_database_connection(db_instance)

                retn_bes.append(be_info)
                retn_bes_ids.append(be_info.id)

            return retn_bes_ids, retn_bes

        except Exception as e:
            print(f"Failed to get available executors: {str(e)}")
            raise e

    def close_executor(self) -> None:
        """
        Closes the executor's database connection.

        This method attempts to close the executor's database connection using the database_instance attribute.
        If the database_instance attribute is not None, it calls the close_executor_database_connection method of
        the StorageManager.

        Returns:
            None
        """
        if self.database_instance:
            StorageManager.close_executor_database_connection(self.database_instance)

    async def _execute_benchmark_pipeline(
        self, recipe_inst: Recipe, recipe_connectors: list[Connector]
    ):
        """
        Executes the benchmark pipeline for a given recipe and list of connectors.

        This method takes a recipe instance and a list of connectors, and executes the benchmark pipeline.
        It first generates prompts based on the datasets and replacement in prompt templates from the recipe instance.
        Then, it generates predictions based on the generated prompts on different connectors.
        The results are returned as an asynchronous generator.

        Args:
            recipe_inst (Recipe): The recipe instance to be used for the benchmark pipeline.
            recipe_connectors (list[Connector]): The list of connectors to be used for generating predictions.

        Returns:
            AsyncGenerator: An asynchronous generator that yields the results of the benchmark pipeline.

        Raises:
            Exception: If there is an error during the generation of prompts or predictions.
        """
        # Generate prompts based on datasets and replacement in prompt templates
        gen_prompt = self._generate_prompts(
            recipe_inst.id, recipe_inst.datasets, recipe_inst.prompt_templates
        )

        # Generate predictions based on the gen_prompts on different connectors
        gen_result = self._generate_predictions(
            gen_prompt, recipe_connectors, self.database_instance
        )

        return [result async for result in gen_result]

    async def _generate_prompts(
        self, rec_id: str, ds_ids: list[str], pt_ids: list[str] = []
    ) -> AsyncGenerator[PromptArguments, None]:
        """
        Asynchronously generates prompts based on the provided recipe ID, dataset IDs and prompt template IDs.

        This method uses the dataset IDs and prompt template IDs to retrieve the corresponding datasets and
        prompt templates. It then uses the Jinja2 template engine to render the prompts using the datasets and
        templates. If no prompt template IDs are provided, the method generates prompts using only the datasets.

        Args:
            rec_id (str): The recipe ID.
            ds_ids (list[str]): A list of dataset IDs.
            pt_ids (list[str], optional): A list of prompt template IDs. Defaults to an empty list.

        Yields:
            AsyncGenerator[PromptArguments, None]: An asynchronous generator that yields PromptArguments objects.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        if pt_ids:
            for pt_id in pt_ids:
                pt_info = StorageManager.get_prompt_template_info(pt_id)
                pt = next(pt_info)
                jinja2_template = Template(pt)

                for ds_id in ds_ids:
                    ds_info = StorageManager.get_dataset_info(ds_id)
                    for prompt_index, prompt in enumerate(ds_info, 1):
                        if (
                            self.num_of_prompts != 0
                            and prompt_index > self.num_of_prompts
                        ):
                            break
                        rendered_prompt = jinja2_template.render(
                            {"prompt": prompt["input"]}
                        )
                        retn_prompt = {
                            "rec_id": rec_id,
                            "pt_id": pt_id,
                            "ds_id": ds_id,
                            "prompt_index": prompt_index,
                            "prompt": rendered_prompt,
                            "target": prompt["target"],
                        }
                        yield PromptArguments(**retn_prompt)
        else:
            for ds_id in ds_ids:
                ds_info = StorageManager.get_dataset_info(ds_id)
                for prompt_index, prompt in enumerate(ds_info, 1):
                    if self.num_of_prompts != 0 and prompt_index > self.num_of_prompts:
                        break
                    retn_prompt = {
                        "rec_id": rec_id,
                        "pt_id": "no-template",
                        "ds_id": ds_id,
                        "prompt_index": prompt_index,
                        "prompt": prompt["input"],
                        "target": prompt["target"],
                    }
                    yield PromptArguments(**retn_prompt)

    async def _generate_predictions(
        self,
        gen_prompt: AsyncGenerator[PromptArguments, None],
        recipe_connectors: list[Connector],
        database_instance: Any,
    ):
        """
        This method generates predictions for the given prompts using the provided recipe connectors and
        database instance.

        This method is a coroutine that takes an asynchronous generator of prompts, a list of recipe connectors,
        and a database instance.

        It iterates over the prompts from the generator and for each prompt, it iterates over the recipe connectors.
        For each connector, it updates the prompt with the connector id and checks if the prompt has saved records
        in the cache.
        If there are no saved records, it gets predictions from the connector and creates cache records.
        If there are saved records, it updates the prompt info from the cache records.
        Finally, it yields the updated prompt info.

        Args:
            gen_prompt (AsyncGenerator[PromptArguments, None]): An asynchronous generator of prompts.
            recipe_connectors (list[Connector]): A list of recipe connectors.
            database_instance (Any): A database instance.

        Yields:
            PromptArguments: The updated prompt info.

        Raises:
            Exception: If there is an error during cache reading or any other operation within the method.
        """
        async for prompt_info in gen_prompt:
            for rec_conn in recipe_connectors:
                # Update the prompt info with connection id
                prompt_info.conn_id = rec_conn.id

                # Check if gen_prompt has saved records in cache
                cache_record = StorageManager.read_benchmark_cache_record(
                    (
                        prompt_info.rec_id,
                        prompt_info.conn_id,
                        prompt_info.pt_id,
                        prompt_info.prompt,
                    ),
                    database_instance,
                )
                if cache_record is None:
                    # Get predictions from connector and create cache records
                    updated_prompt_info = await ConnectorManager.get_prediction(
                        prompt_info, rec_conn
                    )
                    StorageManager.create_benchmark_cache_record(
                        updated_prompt_info.to_tuple(), database_instance
                    )
                else:
                    updated_prompt_info = PromptArguments.from_tuple(cache_record)

                # Return updated prompt info
                yield updated_prompt_info

    def benchmark_update_progress(
        self, status: Union[BenchmarkExecutorStatus, None] = None
    ) -> None:
        """
        Updates the progress of the benchmark execution.

        This method updates the progress of the benchmark execution by setting the end time and duration.
        If a status is provided, it updates the status as well.
        If a database instance is available, it updates the executor progress in the database.
        If a database instance is not available, it prints an error message.

        Args:
            status (Union[BenchmarkExecutorStatus, None], optional): The status of the benchmark execution.
            Defaults to None.
        """
        self.end_time = time.time()
        self.duration = int(self.end_time - self.start_time)
        if status:
            self.status = status

        if self.database_instance:
            StorageManager.update_executor_progress(
                self._get_current_benchmark_arguments().to_tuple(),
                self.database_instance,
            )
        else:
            print("Unable to update executor progress: db_instance is not initialised.")

    def execute(self) -> None:
        """
        Executes the benchmark based on its type.

        This method checks the type of the benchmark and executes it accordingly. If the type is 'RECIPE',
        it runs the recipes and updates the progress. If the type is 'COOKBOOK', it loads the cookbook instance,
        iterates over the recipes in the cookbook, updates the progress, executes the recipe, and then updates
        the progress again.

        Raises:
            Exception: If there is an error during the execution of the benchmark.
        """
        # Execute the benchmark executor based on its type
        if self.type == BenchmarkExecutorTypes.RECIPE:
            print(f"🔃 Running recipes ({self.name})... do not close this terminal.")
            print("You can start a new terminal to continue working.")

            # Update progress
            self.benchmark_update_progress(BenchmarkExecutorStatus.RUNNING)
            self.benchmark_executor_progress.update_progress(
                status=self.status.name,
                duration=self.duration,
                results=self.results,
                recipe_total=len(self.recipes),
            )

            for recipe_index, recipe in enumerate(self.recipes, 0):
                print(
                    f"Running recipe {recipe}... ({recipe_index+1}/{len(self.recipes)})"
                )

                # Update progress
                self.benchmark_executor_progress.update_progress(
                    recipe_index=recipe_index,
                    recipe_name=recipe,
                )

                # Execute the recipe
                self._execute_recipe(recipe)

                # Update progress end time and duration
                self.benchmark_update_progress()
                self.benchmark_executor_progress.update_progress(
                    duration=self.duration,
                    results=self.results,
                )

            # TODO: Create a result instance and write

            # Update progress
            self.benchmark_update_progress(BenchmarkExecutorStatus.COMPLETED)
            self.benchmark_executor_progress.update_progress(
                recipe_index=len(self.recipes),
                status=self.status.name,
                duration=self.duration,
                results=self.results,
            )

        elif self.type == BenchmarkExecutorTypes.COOKBOOK:
            print(f"🔃 Running cookbooks ({self.name})... do not close this terminal.")
            print("You can start a new terminal to continue working.")

            # Update progress
            self.benchmark_update_progress(BenchmarkExecutorStatus.RUNNING)
            self.benchmark_executor_progress.update_progress(
                status=self.status.name,
                duration=self.duration,
                results=self.results,
                cookbook_total=len(self.cookbooks),
            )

            for cookbook_index, cookbook in enumerate(self.cookbooks, 0):
                print(
                    f"Running cookbook {cookbook}... ({cookbook_index+1}/{len(self.cookbooks)})"
                )

                # Update progress
                self.benchmark_executor_progress.update_progress(
                    cookbook_index=cookbook_index,
                    cookbook_name=cookbook,
                )

                # Execute the cookbook
                self._execute_cookbook(cookbook)

                # Update progress end time and duration
                self.benchmark_update_progress()
                self.benchmark_executor_progress.update_progress(
                    duration=self.duration,
                    results=self.results,
                )

            # TODO: Create a result instance and write

            # Update progress
            self.benchmark_update_progress(BenchmarkExecutorStatus.COMPLETED)
            self.benchmark_executor_progress.update_progress(
                cookbook_index=len(self.cookbooks),
                status=self.status.name,
                duration=self.duration,
                results=self.results,
            )

        else:
            print("Invalid executor type.")
            raise RuntimeError("Invalid executor type.")

    def _execute_recipe(self, recipe: str) -> None:
        """
        Executes a given recipe.

        This method takes a recipe as input and performs the following steps:
        1. Loads various instances related to the recipe.
        2. Builds a generator pipeline to get prompts and perform predictions.
        3. Sorts the recipe predictions into groups.

        Args:
            recipe (str): The recipe to be executed.
        """
        try:
            # ------------------------------------------------------------------------------
            # Part 1: Load instances
            # ------------------------------------------------------------------------------
            print("Part 1: Loading various instances...")
            start_time = time.perf_counter()
            recipe_inst = Recipe.load_recipe(recipe)
            print(
                f"Load recipe instance took {(time.perf_counter() - start_time):.4f}s"
            )

            start_time = time.perf_counter()
            recipe_eps = [
                ConnectorManager.create_connector(
                    ConnectorManager.read_endpoint(endpoint)
                )
                for endpoint in self.endpoints
            ]
            print(
                f"Load recipe endpoints instances took {(time.perf_counter() - start_time):.4f}s"
            )

            start_time = time.perf_counter()
            metrics_instances = [
                Metric.load_metric(metric) for metric in recipe_inst.metrics
            ]
            print(f"Load metrics took {(time.perf_counter() - start_time):.4f}s")

            # ------------------------------------------------------------------------------
            # Part 2: Build generator pipeline to get prompts and perform predictions
            # ------------------------------------------------------------------------------
            print("Part 2: Building generator pipeline for predicting prompts...")
            start_time = time.perf_counter()
            recipe_preds = asyncio.run(
                self._execute_benchmark_pipeline(recipe_inst, recipe_eps)
            )
            print(
                f"Predicting prompts for recipe [{recipe}] took {(time.perf_counter() - start_time):.4f}s"
            )

            # ------------------------------------------------------------------------------
            # Part 3: Sort the recipe predictions into groups for recipe
            # ------------------------------------------------------------------------------
            # Sort PromptArguments instances into groups based on the same conn_id, rec_id, ds_id, and pt_id
            print("Part 3: Sort the recipe predictions into groups")
            start_time = time.perf_counter()

            # Assuming `recipe_preds` is your list of PromptArguments instances
            recipe_preds.sort(key=attrgetter("conn_id", "rec_id", "ds_id", "pt_id"))

            # Now group them and generate separate lists for each group
            grouped_recipe_preds = {
                key: {
                    "prompts": [pred.prompt for pred in group_list],
                    "predicted_results": [
                        pred.predicted_results for pred in group_list
                    ],
                    "targets": [pred.target for pred in group_list],
                }
                for key, group in groupby(
                    recipe_preds, key=attrgetter("conn_id", "rec_id", "ds_id", "pt_id")
                )
                for group_list in [list(group)]
            }

            print(
                f"Sort the recipe predictions into groups for recipe [{recipe}] took \
                {(time.perf_counter() - start_time):.4f}s"
            )

            # ------------------------------------------------------------------------------
            # Part 4: Generate the metrics results
            # ------------------------------------------------------------------------------
            # Load metrics for recipe
            print("Part 4: Performing metrics calculation")
            start_time = time.perf_counter()

            for group_recipe_key, group_recipe_value in grouped_recipe_preds.items():
                print(
                    f"Running metrics for conn_id ({group_recipe_key[0]}), \
                    recipe_id ({group_recipe_key[1]}), dataset_id ({group_recipe_key[2]}), \
                    prompt_template_id ({group_recipe_key[3]})"
                )

                metrics_result = []
                prompts = group_recipe_value["prompts"]
                predicted_results = group_recipe_value["predicted_results"]
                targets = group_recipe_value["targets"]
                for metric in metrics_instances:
                    metrics_result.append(
                        metric.get_results(prompts, predicted_results, targets)  # type: ignore ; ducktyping
                    )
                self.results[group_recipe_key] = metrics_result

            print(
                f"Performing metrics calculation for recipe [{recipe}] took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            print(f"Failed to execute recipe due to error: {str(e)}")
            raise e

    def _execute_cookbook(self, cookbook: str) -> None:
        """
        Executes a cookbook.

        This method takes a cookbook and executes it. It first loads the cookbook instance and then iterates
        over the recipes in the cookbook. For each recipe, it updates the progress, executes the recipe, and
        then updates the progress again.

        Args:
            cookbook (str): The cookbook to be executed.

        Raises:
            Exception: If there is an error during the execution of the cookbook.
        """
        try:
            # ------------------------------------------------------------------------------
            # Part 1: Load instances
            # ------------------------------------------------------------------------------
            print("Part 1: Loading various instances...")
            start_time = time.perf_counter()
            cookbook_inst = Cookbook.load_cookbook(cookbook)
            print(
                f"Load cookbook instance took {(time.perf_counter() - start_time):.4f}s"
            )

            # ------------------------------------------------------------------------------
            # Part 2: Execute recipes
            # ------------------------------------------------------------------------------
            # Update progress
            self.benchmark_update_progress()
            self.benchmark_executor_progress.update_progress(
                status=self.status.name,
                duration=self.duration,
                results=self.results,
                recipe_total=len(cookbook_inst.recipes),
            )

            for recipe_index, recipe in enumerate(cookbook_inst.recipes, 0):
                print(
                    f"Running recipe {recipe}... ({recipe_index+1}/{len(cookbook_inst.recipes)})"
                )

                # Update progress
                self.benchmark_executor_progress.update_progress(
                    recipe_index=recipe_index,
                    recipe_name=recipe,
                )

                # Execute the recipe
                self._execute_recipe(recipe)

                # Update progress end time and duration
                self.benchmark_update_progress()
                self.benchmark_executor_progress.update_progress(
                    duration=self.duration,
                    results=self.results,
                )

        except Exception as e:
            print(f"Failed to execute recipe due to error: {str(e)}")
            raise e

    def _get_current_benchmark_arguments(self) -> BenchmarkExecutorArguments:
        """
        Constructs the BenchmarkExecutorArguments object.

        This method constructs the BenchmarkExecutorArguments object using the attributes of the BenchmarkExecutor
        instance. It then returns the constructed BenchmarkExecutorArguments object.

        Returns:
            BenchmarkExecutorArguments: The constructed BenchmarkExecutorArguments object.
        """
        return BenchmarkExecutorArguments(
            id=self.id,
            name=self.name,
            type=self.type,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            database_instance=self.database_instance,
            database_file=self.database_file,
            results_file=self.results_file,
            recipes=self.recipes,
            cookbooks=self.cookbooks,
            endpoints=self.endpoints,
            num_of_prompts=self.num_of_prompts,
            results=self.results,
            status=self.status,
            progress_callback_func=self.progress_callback_func,
        )
