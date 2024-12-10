from __future__ import annotations

import ast
import asyncio
import copy
import json
import random
import time
from itertools import groupby
from operator import attrgetter
from typing import Any, AsyncGenerator

from jinja2 import Template
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors.connector_response import ConnectorResponse
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.datasets.dataset import Dataset
from moonshot.src.metrics.metric import Metric
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger
from pydantic import BaseModel

# Create a logger for this module
logger = configure_logger(__name__)


class Benchmarking:
    sql_create_runner_cache_record = """
        INSERT INTO runner_cache_table(connection_id,recipe_id,dataset_id,prompt_template_id,attack_module_id,
        prompt_index,prompt,target,predicted_results,duration,random_seed,system_prompt)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """
    sql_read_runner_cache_record = """
        SELECT * from runner_cache_table WHERE connection_id=? AND recipe_id=? 
        AND dataset_id=? AND prompt_template_id=? AND prompt=?
    """
    BATCH_SIZE = 10
    QUEUE_SIZE = 10

    async def generate(
        self,
        event_loop: Any,
        runner_args: dict,
        database_instance: DBInterface | None,
        endpoints: list[str],
        run_progress: RunProgress,
        cancel_event: asyncio.Event,
    ) -> ResultArguments | None:
        """
        Asynchronously generates results based on the provided runner arguments and stores them in the database.

        This method orchestrates the benchmarking process by preparing the environment, running the recipes and
        cookbooks and collecting the results

        It leverages the provided database instance to cache and retrieve runner data.

        Args:
            event_loop (Any): The event loop in which asynchronous tasks will be scheduled.
            runner_args (dict): A dictionary containing arguments for the runner.
            database_instance (DBInterface | None): The database interface for storing and retrieving runner data.
            endpoints (list[str]): A list of endpoint identifiers to be used in the benchmarking process.
            run_progress (RunProgress): An object to report the progress of the run.
            cancel_event (asyncio.Event): An event to signal cancellation of the process.

        Returns:
            ResultArguments | None: The result arguments object containing the results of the benchmarking process,
            or None if the process is cancelled or fails to generate results.
        """
        try:
            if not database_instance:
                error_message = "[Benchmarking] Failed to get database instance"
                self.run_progress.notify_error(error_message)
                raise RuntimeError(error_message)

            # Store parsed values
            self.event_loop = event_loop
            self.runner_args = runner_args
            self.database_instance = database_instance
            self.endpoints = endpoints
            self.run_progress = run_progress
            self.cancel_event = cancel_event

            # Get required arguments from runner_args
            self.cookbooks = self.runner_args.get("cookbooks", None)
            self.recipes = self.runner_args.get("recipes", None)
            self.prompt_selection_percentage = self.runner_args.get(
                "prompt_selection_percentage", 100
            )
            self.random_seed = self.runner_args.get("random_seed", 0)
            self.system_prompt = self.runner_args.get("system_prompt", "")

            # Perform validation on prompt_selection_percentage
            if (
                self.prompt_selection_percentage < 1
                or self.prompt_selection_percentage > 100
            ):
                raise RuntimeError(
                    "The 'prompt_selection_percentage' argument must be between 1 - 100."
                )

            # ------------------------------------------------------------------------------
            # Part 0: Load common instances
            # ------------------------------------------------------------------------------
            # Load endpoints
            start_time = time.perf_counter()
            self.recipe_connectors = [
                Connector.create(ConnectorEndpoint.read(endpoint))
                for endpoint in self.endpoints
            ]
            logger.debug(
                f"[Benchmarking] Load recipe connectors took {(time.perf_counter() - start_time):.4f}s"
            )

            # Set connector system prompt
            start_time = time.perf_counter()
            for connector in self.recipe_connectors:
                connector.set_system_prompt(self.system_prompt)
            logger.debug(
                f"[Benchmarking] Set connectors system prompt took {(time.perf_counter() - start_time):.4f}s"
            )

            # ------------------------------------------------------------------------------
            # Part 1: Run the recipes and cookbooks
            # ------------------------------------------------------------------------------
            benchmark_results = {}
            start_time = time.perf_counter()
            try:
                if self.cookbooks:
                    # Process as benchmark cookbooks test
                    logger.info(
                        f"[Benchmarking] Running cookbooks ({self.cookbooks})..."
                    )

                    # Run all cookbooks
                    for cookbook_index, cookbook in enumerate(self.cookbooks, 0):
                        logger.info(
                            f"[Benchmarking] Running cookbook {cookbook}... ({cookbook_index+1}/{len(self.cookbooks)})"
                        )

                        self.run_progress.notify_progress(
                            cookbook_index=cookbook_index,
                            cookbook_name=cookbook,
                            cookbook_total=len(self.cookbooks),
                            recipe_index=-1,
                            recipe_name="",
                            recipe_total=-1,
                        )

                        # Run the cookbook
                        benchmark_results[cookbook] = await self._run_cookbook(cookbook)

                    # Update progress
                    self.run_progress.notify_progress(
                        cookbook_index=len(self.cookbooks),
                        raw_results=benchmark_results,
                    )

                elif self.recipes:
                    # Process as benchmark recipes test
                    logger.info(f"[Benchmarking] Running recipes ({self.recipes})...")

                    # Run all recipes
                    for recipe_index, recipe in enumerate(self.recipes, 0):
                        logger.info(
                            f"[Benchmarking] Running recipe {recipe}... ({recipe_index+1}/{len(self.recipes)})"
                        )

                        self.run_progress.notify_progress(
                            recipe_index=recipe_index,
                            recipe_name=recipe,
                            recipe_total=len(self.recipes),
                        )

                        # Run the recipe
                        benchmark_results[recipe] = await self._run_recipe(recipe)

                    # Update progress
                    self.run_progress.notify_progress(
                        recipe_index=len(self.recipes), raw_results=benchmark_results
                    )

                else:
                    # Unable to identify type
                    self.run_progress.notify_error(
                        "[Benchmarking] Failed to identify if benchmarking with cookbooks or recipes."
                    )

            except Exception as e:
                self.run_progress.notify_error(
                    f"[Benchmarking] Failed to run due to error: {str(e)}"
                )

            finally:
                logger.info(
                    f"[Benchmarking] Run took {(time.perf_counter() - start_time):.4f}s"
                )

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to generate benchmarking due to error: {str(e)}"
            )

        finally:
            logger.debug("[Benchmarking] Updating completion status...")
            if self.cancel_event.is_set():
                self.run_progress.notify_progress(
                    status=RunStatus.CANCELLED,
                )
            elif self.run_progress.run_arguments.error_messages:
                self.run_progress.notify_progress(
                    status=RunStatus.COMPLETED_WITH_ERRORS,
                )
            else:
                self.run_progress.notify_progress(
                    status=RunStatus.COMPLETED,
                )

        # ------------------------------------------------------------------------------
        # Prepare ResultArguments
        # ------------------------------------------------------------------------------
        logger.debug("[Benchmarking] Preparing results...")
        start_time = time.perf_counter()
        result_args = None
        try:
            result_args = ResultArguments(
                # Mandatory values
                id=self.run_progress.run_arguments.runner_id,
                start_time=self.run_progress.run_arguments.start_time,
                end_time=self.run_progress.run_arguments.end_time,
                duration=self.run_progress.run_arguments.duration,
                status=self.run_progress.run_arguments.status,
                raw_results=self.run_progress.run_arguments.raw_results,
                params={
                    "recipes": self.recipes,
                    "cookbooks": self.cookbooks,
                    "endpoints": self.endpoints,
                    "prompt_selection_percentage": self.prompt_selection_percentage,
                    "random_seed": self.random_seed,
                    "system_prompt": self.system_prompt,
                },
            )

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to prepare results due to error: {str(e)}"
            )

        finally:
            logger.info(
                f"[Benchmarking] Preparing results took {(time.perf_counter() - start_time):.4f}s"
            )
            return result_args

    async def _run_cookbook(self, cookbook_name: str) -> dict:
        """
        Asynchronously runs all the recipes within a given cookbook.

        This method takes the name of a cookbook, loads the cookbook instance, and then
        asynchronously runs each recipe contained within it. The results of each recipe run
        are collected and returned.

        Args:
            cookbook_name (str): The name of the cookbook to run.

        Returns:
            dict: A dictionary containing the results of each recipe run, keyed by recipe name.

        Raises:
            Exception: If loading the cookbook instance fails or if an error occurs during
            the running of a recipe.
        """
        # ------------------------------------------------------------------------------
        # Part 1: Load required instances
        # ------------------------------------------------------------------------------
        logger.debug("[Benchmarking] Load required instances...")
        start_time = time.perf_counter()
        self.cookbook_instance = None
        try:
            # Load cookbook
            start_time = time.perf_counter()
            self.cookbook_instance = Cookbook.load(cookbook_name)
            logger.debug(
                f"[Benchmarking] Load cookbook instance took {(time.perf_counter() - start_time):.4f}s"
            )
        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to load instances in running cookbook due to error: {str(e)}"
            )

        # ------------------------------------------------------------------------------
        # Part 2: Run cookbook recipes
        # ------------------------------------------------------------------------------
        logger.debug("[Benchmarking] Running cookbook recipes...")
        recipes_results = {}
        start_time = time.perf_counter()
        try:
            if self.cookbook_instance:
                # Run all recipes
                for recipe_index, recipe_name in enumerate(
                    self.cookbook_instance.recipes, 0
                ):
                    logger.debug(
                        f"[Benchmarking] Running recipe {recipe_name}... "
                        f"({recipe_index+1}/{len(self.cookbook_instance.recipes)})"
                    )

                    # Update progress
                    self.run_progress.notify_progress(
                        recipe_index=recipe_index,
                        recipe_name=recipe_name,
                        recipe_total=len(self.cookbook_instance.recipes),
                    )

                    # Run the recipe
                    recipes_results[recipe_name] = await self._run_recipe(recipe_name)

                # Update progress
                self.run_progress.notify_progress(
                    recipe_index=len(self.cookbook_instance.recipes),
                )
                logger.debug(
                    "[Benchmarking] Running cookbook "
                    f"[{self.cookbook_instance.id}] took {(time.perf_counter() - start_time):.4f}s"
                )

            else:
                raise RuntimeError("Cookbook instance is not initialised.")

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to load instances in running cookbook due to error: {str(e)}"
            )

        finally:
            return recipes_results

    async def _run_recipe(self, recipe_name: str) -> dict:
        """
        Asynchronously runs a single recipe benchmarking process and returns the results.

        This method is responsible for orchestrating the benchmarking process for a specified recipe. It includes
        the steps of loading the recipe instance, executing the generator pipeline to produce prompts, and
        generating predictions for those prompts. The results of the benchmarking process are then returned.

        Args:
            recipe_name (str): The name of the recipe for which the benchmarking process is to be executed.

        Raises:
            RuntimeError: If the recipe instance is not initialized prior to running the generator pipeline.

        Returns:
            dict: A dictionary containing the benchmarking results for the recipe.
        """
        # ------------------------------------------------------------------------------
        # Part 1: Load required instances
        # ------------------------------------------------------------------------------
        logger.debug("[Benchmarking] Load required instances...")
        start_time = time.perf_counter()
        self.recipe_instance = None
        try:
            # Load recipe
            self.recipe_instance = Recipe.load(recipe_name)
            logger.debug(
                f"[Benchmarking] Load recipe instance took {(time.perf_counter() - start_time):.4f}s"
            )

            # Load metrics
            start_time = time.perf_counter()
            self.recipe_metrics = [
                Metric.load(metric) for metric in self.recipe_instance.metrics
            ]
            logger.debug(
                f"[Benchmarking] Load recipe metrics took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to load instances in running recipe due to error: {str(e)}"
            )
            raise e

        # ------------------------------------------------------------------------------
        # Part 2: Build and execute generator pipeline to get prompts and perform predictions
        # ------------------------------------------------------------------------------
        logger.debug("[Benchmarking] Build and execute generator pipeline...")
        start_time = time.perf_counter()
        recipe_predictions = []
        try:
            if self.recipe_instance:
                task = self.event_loop.create_task(
                    self._run_generator_pipeline(self.cancel_event)
                )
                await task
                recipe_predictions = task.result()
                logger.debug(
                    f"[Benchmarking] Predicting prompts for recipe [{self.recipe_instance.id}] took "
                    f"{(time.perf_counter() - start_time):.4f}s"
                )
            else:
                raise RuntimeError("Recipe Instance is not initialized.")

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to build and execute generator pipeline due to error: {str(e)}"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Sort the recipe predictions into groups for recipe
        # ------------------------------------------------------------------------------
        # Sort PromptArguments instances into groups based on the same conn_id, rec_id, ds_id, and pt_id
        logger.debug("[Benchmarking] Sorting the recipe predictions into groups")
        start_time = time.perf_counter()
        grouped_recipe_preds = {}
        try:
            # Assuming `recipe_predictions` is your list of PromptArguments instances
            recipe_predictions.sort(
                key=attrgetter("conn_id", "rec_id", "ds_id", "pt_id")
            )

            # Now group them and generate separate lists for each group
            grouped_recipe_preds = {
                key: {
                    "prompts": [pred.connector_prompt.prompt for pred in group_list],
                    "predicted_results": [
                        pred.connector_prompt.predicted_results for pred in group_list
                    ],
                    "targets": [pred.connector_prompt.target for pred in group_list],
                    "durations": [
                        pred.connector_prompt.duration for pred in group_list
                    ],
                }
                for key, group in groupby(
                    recipe_predictions,
                    key=attrgetter("conn_id", "rec_id", "ds_id", "pt_id"),
                )
                for group_list in [list(group)]
            }

            logger.debug(
                (
                    f"[Benchmarking] Sorted the recipe predictions into groups for recipe [{self.recipe_instance.id}] "
                    f"took {(time.perf_counter() - start_time):.4f}s"
                )
            )

        except Exception as e:
            self.run_progress.notify_error(
                "[Benchmarking] Failed to sort recipe predictions into groups in executing recipe due to "
                f"error: {str(e)}"
            )

        # ------------------------------------------------------------------------------
        # Part 4: Generate the metrics results
        # ------------------------------------------------------------------------------
        logger.debug("[Benchmarking] Performing metrics calculation")
        start_time = time.perf_counter()
        recipe_results = {}
        try:
            for group_recipe_key, group_recipe_value in grouped_recipe_preds.items():
                logger.debug(
                    (
                        f"[Benchmarking] Running metrics for conn_id ({group_recipe_key[0]}), "
                        f"recipe_id ({group_recipe_key[1]}), dataset_id ({group_recipe_key[2]}), "
                        f"prompt_template_id ({group_recipe_key[3]})"
                    )
                )

                metrics_result = []
                prompts = group_recipe_value["prompts"]
                predicted_results = group_recipe_value["predicted_results"]
                targets = group_recipe_value["targets"]
                for metric in self.recipe_metrics:
                    metrics_result.append(
                        await metric.get_results(prompts, predicted_results, targets)  # type: ignore ; ducktyping
                    )

                # Format the results to have data and metrics results.
                group_data = []
                durations = group_recipe_value["durations"]
                for prompt, predicted_result, target, duration in zip(
                    prompts, predicted_results, targets, durations
                ):
                    group_data.append(
                        {
                            "prompt": prompt,
                            "predicted_result": predicted_result.to_dict(),
                            "target": target,
                            "duration": duration,
                        }
                    )

                # Append results for recipe
                recipe_results[group_recipe_key] = {
                    "data": group_data,
                    "results": metrics_result,
                }

            logger.debug(
                f"[Benchmarking] Performing metrics calculation for recipe [{self.recipe_instance.id}] "
                f"took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to calculate metrics in executing recipe due to error: {str(e)}"
            )

        finally:
            return recipe_results

    async def _run_generator_pipeline(self, cancel_event: asyncio.Event) -> list:
        """
        Orchestrates the execution of the benchmark pipeline using the provided recipe instance and connectors.

        This method manages the benchmarking process by generating prompts from the datasets and prompt templates
        specified in the recipe instance. It then employs the given connectors to produce predictions based on these
        prompts. The results of the benchmarking are provided through an asynchronous generator, enabling parallel
        processing of the pipeline's output.

        Args:
            cancel_event (asyncio.Event): An event that, when set, signals the pipeline to gracefully cancel
            the benchmarking process.

        Returns:
            list: A list of benchmarking results that have been asynchronously generated, allowing for concurrent
            processing of the pipeline's output.

        Raises:
            Exception: An exception is raised if an error occurs during the prompt generation or prediction phases
            of the benchmarking process.
        """
        try:
            # Generate prompts based on datasets and replacement in prompt templates
            gen_prompt = self._generate_prompts()

            # Create an asynchronous queue
            queue = asyncio.Queue(
                maxsize=Benchmarking.QUEUE_SIZE
            )  # Adjust the maxsize to control concurrency

            # Producer coroutine to generate prompts and put them into the queue in batches
            async def producer():
                try:
                    batch = []
                    async for prompt in gen_prompt:
                        if cancel_event.is_set():
                            logger.warning(
                                "[Benchmarking] Cancellation flag is set. Cancelling producer..."
                            )
                            break
                        batch.append(prompt)
                        if len(batch) == Benchmarking.BATCH_SIZE:
                            # Put the entire batch into the queue
                            await queue.put(batch)
                            batch = []  # Reset the batch

                    # If there are prompts left in the partial batch, put them in the queue
                    if batch:
                        await queue.put(batch)
                finally:
                    # Signal the consumers that production is done or cancelled
                    await queue.put(None)

            # Consumer coroutine to process batches of prompts from the queue
            async def consumer():
                output = []
                while True:
                    batch = await queue.get()  # Retrieve a batch from the queue
                    if batch is None:  # Check for the end of the queue
                        queue.task_done()
                        break
                    if cancel_event.is_set():  # Check for cancellation
                        logger.warning(
                            "[Benchmarking] Cancellation flag is set. Cancelling consumer..."
                        )
                        queue.task_done()
                        break

                    # Dispatch the batch to all connectors
                    batch_tasks = [
                        self._generate_predictions(batch, connector, cancel_event)
                        for connector in self.recipe_connectors
                    ]
                    results = await asyncio.gather(*batch_tasks, return_exceptions=True)

                    # Process results and handle exceptions
                    for result in results:
                        if isinstance(result, Exception):
                            # Handle exceptions from _generate_predictions
                            self.run_progress.notify_error(
                                f"[Benchmarking] Error while generating predictions: {str(result)}"
                            )
                        else:
                            output.append(result)

                    queue.task_done()
                return output

            # Start the producer and consumer coroutines
            producer_task = asyncio.create_task(producer())
            consumer_task = asyncio.create_task(consumer())

            # Wait for the producer to finish generating prompts
            await producer_task

            # Collect results from all consumers
            results = await asyncio.gather(consumer_task, return_exceptions=True)

            # Flatten the list of results since each consumer returns a list of results
            # and flatten another additional layer if any sublist contains further nested lists
            output = [
                item
                for sublist in results
                if isinstance(sublist, list)
                for subsublist in sublist
                if isinstance(subsublist, list)
                for item in subsublist
            ]
            return output

        except Exception as e:
            # Handle any exceptions that occur during the setup and execution of the pipeline
            self.run_progress.notify_error(
                f"[Benchmarking] Error during generator pipeline execution: {str(e)}"
            )
            return []  # Return an empty list in case of error

    async def _generate_prompts(self) -> AsyncGenerator[PromptArguments, None]:
        """
        Asynchronously generates and yields prompts for benchmarking tasks.

        This coroutine traverses through the datasets and prompt templates linked to the recipe instance,
        creating prompts by applying the Jinja2 template engine to the dataset contents.
        In the absence of prompt templates, the dataset contents are directly used to generate the prompts.

        Yields:
            PromptArguments: A structured object encapsulating the rendered prompt along with its metadata, including
                             identifiers for the recipe, dataset, and prompt template.

        Raises:
            Exception: If any issue arises during the prompt rendering process or
                       while performing associated operations.
        """
        pt_id = "no-template"
        templates = {}
        if self.recipe_instance.prompt_templates:
            for pt_id in self.recipe_instance.prompt_templates:
                # Retrieve the prompt template information from storage as a generator
                pt_info_gen = Storage.read_object_with_iterator(
                    EnvVariables.PROMPT_TEMPLATES.name,
                    pt_id,
                    "json",
                    iterator_keys=["template"],
                )
                # Get the first item from the generator, which contains the template data
                pt_info = next(pt_info_gen["template"])
                # Create a Jinja2 template from the retrieved template data
                templates[pt_id] = Template(pt_info)

        # This section of code iterates over datasets and templates to render prompts and yield them.
        # If no templates are available, it yields the modified prompts from the datasets after
        # applying the attack module.
        for ds_id in self.recipe_instance.datasets:
            async for prompt_index, prompt in self._get_dataset_prompts(ds_id):
                modified_prompts = [("", prompt["input"])]

                # If templates are available, render the modified prompts using the templates
                if templates:
                    for pt_id, jinja2_template in templates.items():
                        try:
                            # Render the modified prompt using the Jinja2 template
                            for (
                                modified_attack_module_id,
                                modified_prompt,
                            ) in modified_prompts:
                                rendered_prompt = jinja2_template.render(
                                    {"prompt": modified_prompt}
                                )
                                prompt_args = await self._yield_prompt_arguments(
                                    pt_id,
                                    ds_id,
                                    modified_attack_module_id,
                                    prompt_index,
                                    rendered_prompt,
                                    prompt["target"],
                                )
                                yield prompt_args
                        except Exception as e:
                            self.run_progress.notify_error(
                                f"[Benchmarking] Error while rendering template for prompt_info "
                                f"[rec_id: {self.recipe_instance.id}, ds_id: {ds_id}, pt_id: {pt_id}, "
                                f"prompt_index: {prompt_index}] due to error: {str(e)}"
                            )
                # If no templates are available, yield the modified prompts directly
                else:
                    for modified_attack_module_id, modified_prompt in modified_prompts:
                        prompt_args = await self._yield_prompt_arguments(
                            pt_id,
                            ds_id,
                            modified_attack_module_id,
                            prompt_index,
                            modified_prompt,
                            prompt["target"],
                        )
                        yield prompt_args

    async def _get_dataset_prompts(
        self, ds_id: str
    ) -> AsyncGenerator[tuple[int, dict], None]:
        """
        Asynchronously retrieves prompts from a dataset based on the specified dataset ID.

        This method calculates the total number of prompts in the dataset and generates a list of prompt indices.
        If a specific number of prompts is requested (num_of_prompts), it will randomly select that many prompts
        using the provided random seed. Otherwise, it will retrieve all prompts. Each prompt is then fetched and
        yielded along with its index.

        Args:
            ds_id (str): The ID of the dataset from which to retrieve prompts.

        Yields:
            tuple[int, dict]: A tuple containing the index of the prompt and the prompt data itself.
        """
        # Retrieve dataset arguments
        ds_args = Dataset.read(ds_id)

        # Generate a list of prompt indices based on prompt_selection_percentage and random_seed
        self.num_of_prompts = int(
            (self.prompt_selection_percentage / 100) * ds_args.num_of_dataset_prompts
        )
        if self.num_of_prompts == ds_args.num_of_dataset_prompts:
            prompt_indices = range(ds_args.num_of_dataset_prompts)
        else:
            random.seed(self.random_seed)
            prompt_indices = random.sample(
                range(ds_args.num_of_dataset_prompts), self.num_of_prompts
            )
        logger.debug(
            f"[Benchmarking] Dataset {ds_id}, using {len(prompt_indices)} of {ds_args.num_of_dataset_prompts} prompts."
        )

        # Iterate over the dataset examples and yield prompts based on the generated indices
        prompts_gen_index = 0
        for prompts_data in ds_args.examples:
            if prompts_gen_index in prompt_indices:
                yield prompts_gen_index, prompts_data
            prompts_gen_index += 1

    async def _yield_prompt_arguments(
        self,
        pt_id: str,
        ds_id: str,
        attack_module_id: str,
        prompt_index: int,
        prompt_text: str,
        target: str,
    ) -> PromptArguments:
        """
        Asynchronously prepares the arguments required for a prompt.

        This method takes the necessary identifiers and prompt information, and prepares the
        PromptArguments object which is used to pass arguments to the connector for prompt processing.

        Args:
            pt_id (str): The ID of the prompt template.
            ds_id (str): The ID of the dataset.
            attack_module_id (str): The ID of the attack module.
            prompt_index (int): The index of the prompt in the dataset.
            prompt_text (str): The text of the prompt.
            target (str): The target for the prompt.

        Returns:
            PromptArguments: An instance of PromptArguments containing all the necessary information
            for processing the prompt.
        """
        return PromptArguments(
            rec_id=self.recipe_instance.id,
            pt_id=pt_id,
            ds_id=ds_id,
            random_seed=self.random_seed,
            system_prompt=self.system_prompt,
            attack_module_id=attack_module_id,
            connector_prompt=ConnectorPromptArguments(
                prompt_index=prompt_index,
                prompt=prompt_text,
                target=target,
            ),
        )

    async def _generate_predictions(
        self,
        prompt_batch: list[PromptArguments],
        connector: Connector,
        cancel_event: asyncio.Event,
    ) -> list:
        """
        Asynchronously generates predictions for a batch of prompts using the specified connector.

        This method takes a batch of PromptArguments, which contain information about the prompts to be processed,
        and uses the provided connector to generate predictions for each prompt. It handles any exceptions that
        occur during the generation process and notifies the run progress of any errors.

        Args:
            prompt_batch (list[PromptArguments]): A list of PromptArguments to generate predictions for.
            connector (Connector): The connector instance to use for generating predictions.
            cancel_event (asyncio.Event): An event to signal if the operation should be cancelled.

        Returns:
            list: A list of generated predictions or exceptions if any occurred during prediction generation.
        """
        # Create a coroutine for each prompt in the batch
        tasks = [
            self._process_single_prompt(prompt_info, connector, cancel_event)
            for prompt_info in prompt_batch
        ]

        # Run all the coroutines concurrently and gather results
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                # Handle exceptions from _process_single_prompt
                self.run_progress.notify_error(
                    f"[Benchmarking] Error while generating prediction: {str(result)}"
                )
            else:
                processed_results.append(result)

        return processed_results

    async def _process_single_prompt(
        self,
        prompt_info: PromptArguments,
        connector: Connector,
        cancel_event: asyncio.Event,
    ) -> PromptArguments | None:
        """
        Processes a single prompt to generate a prediction or retrieve it from cache.

        This method takes a single PromptArguments object, uses the provided connector to generate a prediction,
        and caches the result in the database. If a cache record already exists for the given prompt, it retrieves
        the result from the cache instead of generating a new prediction.

        Args:
            prompt_info (PromptArguments): The prompt information for which to generate a prediction.
            connector (Connector): The connector to use for generating the prediction.
            cancel_event (asyncio.Event): An event that signals if the operation should be cancelled.

        Returns:
            PromptArguments | None: The updated PromptArguments object with the prediction result, or None if the
            operation was cancelled or an exception occurred during prediction generation or caching.
        """
        if cancel_event.is_set():
            logger.warning(
                "[Benchmarking] Cancellation flag is set. Cancelling predictions..."
            )
            return None  # Return None for cancelled operations

        # Create a new prompt info with connection id
        new_prompt_info = copy.deepcopy(prompt_info)
        new_prompt_info.conn_id = connector.id

        # Attempt to read from database for cache values
        try:
            cache_record = Storage.read_database_record(
                self.database_instance,
                (
                    new_prompt_info.conn_id,
                    new_prompt_info.rec_id,
                    new_prompt_info.ds_id,
                    new_prompt_info.pt_id,
                    new_prompt_info.connector_prompt.prompt,
                ),
                Benchmarking.sql_read_runner_cache_record,
            )
        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Error while reading benchmark cache record for prompt_info "
                f"[conn_id: {new_prompt_info.conn_id}, rec_id: {new_prompt_info.rec_id}, "
                f"ds_id: {new_prompt_info.ds_id}, pt_id: {new_prompt_info.pt_id}, "
                f"prompt_index: {new_prompt_info.connector_prompt.prompt_index}] due to error: {str(e)}"
            )
            cache_record = None

        # If cache record does not exist, perform prediction and cache the result
        if cache_record is None:
            try:
                new_prompt_info.connector_prompt = await Connector.get_prediction(
                    new_prompt_info.connector_prompt, connector
                )
                Storage.create_database_record(
                    self.database_instance,
                    new_prompt_info.to_tuple(),
                    Benchmarking.sql_create_runner_cache_record,
                )
            except Exception as e:
                self.run_progress.notify_error(
                    f"[Benchmarking] Failed to generate prediction for prompt_info "
                    f"[conn_id: {new_prompt_info.conn_id}, rec_id: {new_prompt_info.rec_id}, "
                    f"ds_id: {new_prompt_info.ds_id}, pt_id: {new_prompt_info.pt_id}, "
                    f"prompt_index: {new_prompt_info.connector_prompt.prompt_index}] due to error: {str(e)}"
                )
                return None
        else:
            # Load result from cache
            new_prompt_info = PromptArguments.from_tuple(cache_record)

        # Return result
        return new_prompt_info


class PromptArguments(BaseModel):
    conn_id: str = ""  # The ID of the connection, default is an empty string

    rec_id: str  # The ID of the recipe

    ds_id: str  # The ID of the dataset

    pt_id: str  # The ID of the prompt template

    random_seed: int  # The random seed used for generating deterministic results

    system_prompt: str  # The system-generated prompt used for benchmarking

    attack_module_id: str  # The attack module used for generating perturb prompts

    connector_prompt: ConnectorPromptArguments  # The prompt information to send

    def to_tuple(self) -> tuple:
        """
        Converts the PromptArguments instance into a tuple.

        This method aggregates the attributes of the PromptArguments instance into a tuple.
        The tuple is structured with the following attribute values in order:
        conn_id, rec_id, ds_id, pt_id, attack_module_id, prompt_index, prompt, target, predicted_results, duration,
        random_seed, and system_prompt.

        This ordered tuple is particularly useful for serialization purposes, such as storing the PromptArguments data
        in a database or transmitting it across network boundaries.

        Returns:
            tuple: A tuple representation of the PromptArguments instance.
        """
        return (
            self.conn_id,
            self.rec_id,
            self.ds_id,
            self.pt_id,
            self.attack_module_id,
            self.connector_prompt.prompt_index,
            self.connector_prompt.prompt,
            str(self.connector_prompt.target),
            json.dumps(self.connector_prompt.predicted_results.to_dict()),
            str(self.connector_prompt.duration),
            self.random_seed,
            self.system_prompt,
        )

    @classmethod
    def from_tuple(cls, cache_record: tuple) -> PromptArguments:
        """
        Reconstitutes a PromptArguments instance from a tuple representation.

        This method accepts a tuple with values that map to the attributes of a PromptArguments object.
        The expected order of values in the tuple is:
        conn_id, rec_id, ds_id, pt_id, random_seed, system_prompt, attack_module_id, prompt_index, prompt, target,
        predicted_results, and duration. It constructs a new PromptArguments instance using these values.
        The primary purpose of this method is to recreate PromptArguments instances from their serialized form, such as
        data retrieved from a database or received over a network.

        Args:
            cache_record (tuple): A tuple with ordered values that map to the properties of a PromptArguments instance.

        Returns:
            PromptArguments: An instance of PromptArguments initialized with the data from the tuple.
        """
        # The target and predicted_results fields may be stored as strings in the cache_record.
        # ast.literal_eval is used to attempt to convert these strings back into their original data types.
        # If the conversion fails (i.e., the fields are not string representations of Python literals),
        # the original string values are used.
        try:
            target = ast.literal_eval(cache_record[9])
        except Exception:
            target = cache_record[9]

        try:
            predicted_results_dict = json.loads(cache_record[10])
            predicted_results = ConnectorResponse(**predicted_results_dict)
        except Exception:
            predicted_results = cache_record[10]

        return cls(
            conn_id=cache_record[1],
            rec_id=cache_record[2],
            ds_id=cache_record[3],
            pt_id=cache_record[4],
            attack_module_id=cache_record[6],
            connector_prompt=ConnectorPromptArguments(
                prompt_index=cache_record[7],
                prompt=cache_record[8],
                target=target,
                predicted_results=predicted_results,
                duration=float(cache_record[11]),
            ),
            random_seed=cache_record[12],
            system_prompt=cache_record[13],
        )
