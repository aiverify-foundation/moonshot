from __future__ import annotations

import asyncio
import time
from typing import Any, AsyncGenerator

from jinja2 import Template
from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.benchmarking.benchmark_progress import BenchmarkProgress
from moonshot.src.benchmarking.executors.benchmark_executor_arguments import (
    BenchmarkExecutorArguments,
)
from moonshot.src.benchmarking.executors.benchmark_executor_status import (
    BenchmarkExecutorStatus,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)
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
        self.progress = BenchmarkProgress(
            exec_id=str(self.id),
            exec_name=self.name,
            exec_type=self.type.name,
            bm_max_progress_per_recipe=int(100.0 / len(self.recipes))
            if self.recipes
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
    def load_executor(cls, be_id: str) -> BenchmarkExecutor:
        """
        Loads a BenchmarkExecutor instance from the storage.

        This method takes a BenchmarkExecutor ID as an argument, retrieves the corresponding data from the storage,
        and creates a BenchmarkExecutor instance from it. If the executor is successfully loaded, it is returned.
        If there is an error during loading, the error is printed and re-raised.

        Args:
            be_id (str): The ID of the BenchmarkExecutor to be loaded.

        Returns:
            BenchmarkExecutor: The loaded BenchmarkExecutor instance.

        Raises:
            Exception: If there is an error during executor loading.
        """
        db_instance = None
        try:
            db_instance = StorageManager.create_executor_database_connection(be_id)
            be_args = BenchmarkExecutorArguments.from_tuple(
                StorageManager.read_executor_storage(be_id, db_instance)
            )
            be_args.database_instance = db_instance

            return cls(be_args)

        except Exception as e:
            print(f"Failed to load executor: {str(e)}")
            raise e

    @staticmethod
    def update_executor(be_args: BenchmarkExecutorArguments) -> BenchmarkExecutor:
        """
        Updates an existing executor.

        This function takes a BenchmarkExecutorArguments object as input. It first generates a new executor ID
        based on the type and name of the executor. It then deletes the existing executor with the same ID and
        creates a new executor with the updated arguments. If the update is successful, it returns the new executor.
        If there is an error during the update, the error is printed and re-raised.

        Args:
            be_args (BenchmarkExecutorArguments): The updated arguments for the executor.

        Returns:
            BenchmarkExecutor: The updated executor.

        Raises:
            Exception: If there is an error during executor update.
        """
        try:
            prefix = (
                "recipe-"
                if be_args.type == BenchmarkExecutorTypes.RECIPE
                else "cookbook-"
            )
            be_id = slugify(prefix + be_args.name, lowercase=True)
            BenchmarkExecutor.delete_executor(be_id)
            return BenchmarkExecutor.create_executor(be_args)

        except Exception as e:
            print(f"Failed to update executor: {str(e)}")
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

    def execute(self):
        """
        Executes the benchmark based on its type.

        This method checks the type of the benchmark executor and runs the corresponding execution method.
        If the type is RECIPE, it runs the execute_recipe method for each recipe in the recipes list.
        If the type is COOKBOOK, it runs the execute_cookbook method.
        If the type is not recognized, it raises a RuntimeError.

        Raises:
            RuntimeError: If the executor type is not recognized.
        """
        # Execute the benchmark executor based on its type
        if self.type == BenchmarkExecutorTypes.RECIPE:
            print(f"🔃 Running recipes ({self.name})... do not close this terminal.")
            print("You can start a new terminal to continue working.")

            for recipe_index, recipe in enumerate(self.recipes, 0):
                # Update progress
                self._update_execution_progress(
                    BenchmarkExecutorStatus.RUNNING, recipe_index, recipe
                )
                print(
                    f"Running recipe {recipe}... ({recipe_index+1}/{len(self.recipes)})"
                )

                # Execute the recipe
                self._execute_recipe(recipe)

            # Update progress
            self._update_execution_progress(
                BenchmarkExecutorStatus.COMPLETED, len(self.recipes), ""
            )

        elif self.type == BenchmarkExecutorTypes.COOKBOOK:
            self._execute_cookbook()

        else:
            print("Invalid executor type.")
            raise RuntimeError("Invalid executor type.")

    def _execute_recipe(self, recipe: str):
        """
        Executes a single recipe.

        This method takes a recipe as an argument and performs the following steps:
        1. Loads the recipe instance.
        2. Loads the recipe endpoints instances.
        3. Builds a generator pipeline to get prompts and perform predictions.
        4. Generates the metrics results.

        Args:
            recipe (str): The recipe to be executed.

        Raises:
            Exception: If there is an error during any of the steps.
        """
        # ------------------------------------------------------------------------------
        # Part 1: Load instances
        # ------------------------------------------------------------------------------
        print("Part 1: Loading various instances...")
        start_time = time.perf_counter()
        recipe_inst = Recipe.load_recipe(recipe)
        print(f"Load recipe instance took {(time.perf_counter() - start_time):.4f}s")

        start_time = time.perf_counter()
        recipe_eps = [
            ConnectorManager.create_connector(ConnectorManager.read_endpoint(endpoint))
            for endpoint in self.endpoints
        ]
        print(
            f"Load recipe endpoints instances took {(time.perf_counter() - start_time):.4f}s"
        )

        start_time = time.perf_counter()
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
        # Part 3: Generate the metrics results
        # ------------------------------------------------------------------------------
        # Load metrics for recipe
        print(recipe_preds)

    def _execute_cookbook(self):
        pass

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

    def _update_execution_progress(
        self, status: BenchmarkExecutorStatus, current_index: int, recipe_name: str
    ) -> None:
        """
        Updates the execution progress of the benchmark.

        This method updates the status, end time, duration, and progress of the benchmark execution.
        It also updates the executor with the benchmark arguments.

        Args:
            status (BenchmarkExecutorStatus): The status of the benchmark execution.
            current_index (int): The current index of the recipe being executed.
            recipe_name (str): The name of the recipe being executed.
        """
        self.status = status
        self.end_time = time.time()
        self.duration = int(self.end_time - self.start_time)
        self.progress.update_progress(
            current_index, recipe_name, self.duration, self.status.name, self.results
        )
        if self.database_instance:
            StorageManager.update_executor_progress(
                self._get_current_benchmark_arguments().to_tuple(),
                self.database_instance,
            )
        else:
            print("Unable to update executor progress: db_instance is not initialised.")
