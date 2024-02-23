from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import AsyncGenerator, Union

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
    def load_executor(cls, be_id: str) -> BenchmarkExecutor:
        """
        Loads a benchmark executor from a database.

        This method reads the benchmark executor information from a database specified by the executor ID. It constructs
        the database path using the executor ID and the designated directory for databases. The method
        then reads the database and returns the benchmark executor information as a dictionary.

        Args:
            be_id (str): The ID of the benchmark executor.

        Returns:
            BenchmarkExecutor: An instance of the BenchmarkExecutor class with the loaded executor information.
        """
        be_args = StorageManager.read_executor(be_id)
        if be_args:
            return cls(be_args)
        else:
            raise RuntimeError(f"Failed to load {be_id}.")

    @classmethod
    def create_executor(cls, be_args: BenchmarkExecutorArguments) -> BenchmarkExecutor:
        """
        Creates a new benchmark executor and stores its information in a database.

        This method takes the arguments provided in the `be_args` parameter, generates a unique executor ID by
        slugifying the executor name, and then constructs a dictionary with the executor's information. It then
        writes this information to a database file named after the executor ID within the directory specified by
        `EnvironmentVars.DATABASES`. If the operation fails for any reason, an exception is raised
        and the error is printed.

        Args:
            be_args (BenchmarkExecutorArguments): An object containing the necessary information to create a
            new benchmark executor.

        Returns:
            BenchmarkExecutor: An instance of the BenchmarkExecutor class with the loaded executor information.

        Raises:
            Exception: If there is an error during file writing or any other operation within the method.
        """
        try:
            be_id = slugify(be_args.name, lowercase=True)
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
            # Write as database output
            be_args = StorageManager.create_executor(
                BenchmarkExecutorArguments(**be_info)
            )

            # Return an instance of executor
            return cls(be_args)

        except Exception as e:
            print(f"Failed to create executor: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read_executor(be_id: str) -> Union[BenchmarkExecutorArguments, None]:
        """
        Reads an executor.

        This method reads an executor by loading the executor's database file and reading the metadata record.
        It constructs the file path for the database file using the executor ID and the designated directory for
        databases.
        If the file does not exist, it raises a RuntimeError.
        It then returns the BenchmarkExecutorArguments instance constructed from the metadata record, or None
        if the record could not be found.

        Args:
            be_id (str): The ID of the executor.

        Returns:
            Union[BenchmarkExecutorArguments, None]: The BenchmarkExecutorArguments instance, or None if the
            record could not be found.
        """
        try:
            return StorageManager.read_executor(be_id)

        except Exception as e:
            print(f"Failed to read executor: {str(e)}")
            raise e

    @staticmethod
    def update_executor(be_args: BenchmarkExecutorArguments) -> None:
        """
        Updates an executor.

        This method updates an executor by updating the executor's database file with the new metadata record.
        It constructs the file path for the database file using the executor ID and the designated directory for
        databases.
        If the file does not exist, it raises a RuntimeError.

        Args:
            be_args (BenchmarkExecutorArguments): The updated executor arguments.

        Raises:
            Exception: If there is an error during file updating or any other operation within the method.
        """
        try:
            StorageManager.update_executor(be_args)

        except Exception as e:
            print(f"Failed to update executor: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete_executor(be_id: str) -> None:
        """
        Deletes a benchmark executor from the database and its corresponding results file.

        This method deletes the executor information from the database file and the results file specified by
        the executor ID. It constructs the file paths using the executor ID and the designated directories for
        databases and results. The method then deletes both the database file and the results file.

        Args:
            be_id (str): The ID of the executor.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        try:
            StorageManager.delete_executor(be_id)

        except Exception as e:
            print(f"Failed to delete executor: {str(e)}")
            raise e

    @staticmethod
    def get_available_executors() -> tuple[list[str], list[BenchmarkExecutorArguments]]:
        """
        Returns a list of available executors and their corresponding BenchmarkExecutorArguments.

        This method retrieves all the executors from the storage manager. It then reads the executor information
        for each executor and appends it to a list. Executors with "__" in their names are ignored.

        Returns:
            tuple[list[str], list[BenchmarkExecutorArguments]]: A tuple containing a list of executor IDs and a list
            of BenchmarkExecutorArguments for each executor.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        try:
            retn_be_args = []
            retn_be_ids = []

            bm_executors = StorageManager.get_executors()
            for bm_executor in bm_executors:
                if "__" in bm_executor:
                    continue

                bm_args = StorageManager.read_executor(Path(bm_executor).stem)
                if bm_args:
                    retn_be_args.append(bm_args.to_dict())
                    retn_be_ids.append(bm_args.id)

            return retn_be_ids, retn_be_args

        except Exception as e:
            print(f"Failed to get available executors: {str(e)}")
            raise e

    async def execute_benchmark_pipeline(
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
        gen_prompt = self.generate_prompts(
            recipe_inst.id, recipe_inst.datasets, recipe_inst.prompt_templates
        )

        # Generate predictions based on the gen_prompts on different connectors
        gen_result = self.generate_predictions(gen_prompt, recipe_connectors)

        return [result async for result in gen_result]

    async def generate_prompts(
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

    async def generate_predictions(
        self,
        gen_prompt: AsyncGenerator[PromptArguments, None],
        recipe_connectors: list[Connector],
    ):
        """
        Asynchronously generates predictions for the given prompts using the provided recipe connectors.

        This method takes an asynchronous generator of prompts and a list of recipe connectors. It iterates over
        the prompts and for each prompt, it iterates over the recipe connectors. For each combination of prompt
        and connector, it first checks if there is a saved record in the cache. If there is, it uses that record.
        If there is not, it gets a prediction from the connector and creates a new cache record. It then yields
        the updated prompt information.

        Args:
            gen_prompt (AsyncGenerator[PromptArguments, None]): An asynchronous generator that yields prompts.
            recipe_connectors (list[Connector]): A list of recipe connectors to be used for generating predictions.

        Yields:
            PromptArguments: The updated prompt information.
        """
        async for prompt_info in gen_prompt:
            for rec_conn in recipe_connectors:
                # Update the prompt info with connection id
                prompt_info.conn_id = rec_conn.id

                # Check if gen_prompt has saved records in cache
                updated_prompt_info = StorageManager.read_benchmark_cache_record(
                    self.database_instance, prompt_info
                )
                if updated_prompt_info is None:
                    # Get predictions from connector and create cache records
                    updated_prompt_info = await ConnectorManager.get_prediction(
                        prompt_info, rec_conn
                    )
                    StorageManager.create_benchmark_cache_record(
                        self.database_instance, updated_prompt_info
                    )

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
                self.update_execution_progress(
                    BenchmarkExecutorStatus.RUNNING, recipe_index, recipe
                )
                print(
                    f"Running recipe {recipe}... ({recipe_index+1}/{len(self.recipes)})"
                )

                # Execute the recipe
                self.execute_recipe(recipe)

            # Update progress
            self.update_execution_progress(
                BenchmarkExecutorStatus.COMPLETED, len(self.recipes), ""
            )

        elif self.type == BenchmarkExecutorTypes.COOKBOOK:
            self.execute_cookbook()

        else:
            print("Invalid executor type.")
            raise RuntimeError("Invalid executor type.")

    def execute_recipe(self, recipe: str):
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
            self.execute_benchmark_pipeline(recipe_inst, recipe_eps)
        )
        print(
            f"Predicting prompts for recipe [{recipe}] took {(time.perf_counter() - start_time):.4f}s"
        )

        # ------------------------------------------------------------------------------
        # Part 3: Generate the metrics results
        # ------------------------------------------------------------------------------
        # Load metrics for recipe
        print(recipe_preds)

    def execute_cookbook(self):
        pass

    def get_benchmark_arguments(self) -> BenchmarkExecutorArguments:
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

    def update_execution_progress(
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
        self.update_executor(self.get_benchmark_arguments())
