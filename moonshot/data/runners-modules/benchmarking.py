from __future__ import annotations

import ast
import copy
import time
from itertools import groupby
from operator import attrgetter
from typing import Any, AsyncGenerator

from jinja2 import Template
from pydantic import BaseModel

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.metrics.metric import Metric
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.results.result import Result
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_accessor import DBAccessor
from moonshot.src.storage.storage import Storage


class Benchmarking:
    sql_create_cache_table = """
        CREATE TABLE IF NOT EXISTS cache_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conn_id text NOT NULL,
        rec_id text NOT NULL,
        ds_id text NOT NULL,
        pt_id text NOT NULL,
        random_seed text NOT NULL,
        system_prompt text NOT NULL,
        prompt_index INTEGER NOT NULL,
        prompt text NOT NULL,
        target text NOT NULL,
        predicted_results text NOT NULL,
        duration text NOT NULL
        );
    """
    sql_create_cache_record = """
        INSERT INTO cache_table(conn_id,rec_id,ds_id,pt_id,random_seed,system_prompt,prompt_index,prompt,target,
        predicted_results,duration)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
    """
    sql_read_cache_record = """
        SELECT * from cache_table WHERE rec_id=? AND conn_id=? AND pt_id=? AND prompt=?
    """

    async def generate(
        self,
        event_loop: Any,
        runner_args: dict,
        database_instance: DBAccessor | None,
        endpoints: list[str],
        run_progress: RunProgress,
    ) -> dict:
        """
        Asynchronously generates benchmarking results for cookbooks or recipes.

        This method manages the benchmarking process, which involves executing cookbooks or recipes,
        recording outcomes, and updating the status of completion. It coordinates the setup and execution of
        benchmarking activities based on the input parameters.

        Args:
            event_loop (Any): The event loop where asynchronous tasks will be executed.
            runner_args (dict): A dictionary of parameters for the benchmarking run, including
                                cookbooks, recipes, number of prompts, random seed, and system prompt.
            database_instance (DBAccessor | None): A DBAccessor instance for database operations,
                                                    or None if database interaction is not needed.
            endpoints (str): The endpoints to be utilized in the benchmarking process.
            run_progress (RunProgress): A RunProgress instance to track progress and log errors
                                        throughout the benchmarking process.

        Raises:
            RuntimeError: If it's unclear whether to use cookbooks or recipes for benchmarking, or if
                          obtaining the database instance is unsuccessful when it's required.
        """
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

        # Get required arguments from runner_args
        self.cookbooks = self.runner_args.get("cookbooks", None)
        self.recipes = self.runner_args.get("recipes", None)
        self.num_of_prompts = self.runner_args.get("num_of_prompts", 0)
        self.random_seed = self.runner_args.get("random_seed", 0)
        self.system_prompt = self.runner_args.get("system_prompt", "")

        # ------------------------------------------------------------------------------
        # Part 0: Load common instances
        # ------------------------------------------------------------------------------
        # Load endpoints
        start_time = time.perf_counter()
        self.recipe_connectors = [
            Connector.create(ConnectorEndpoint.read(endpoint))
            for endpoint in self.endpoints
        ]
        print(
            f"[Benchmarking] Load recipe connectors took {(time.perf_counter() - start_time):.4f}s"
        )

        # ------------------------------------------------------------------------------
        # Part 1: Create new cache table if needed
        # ------------------------------------------------------------------------------
        print("[Benchmarking] Part 1: Create new cache table if needed...")
        Storage.create_database_table(
            database_instance, Benchmarking.sql_create_cache_table
        )

        # ------------------------------------------------------------------------------
        # Part 2: Run the recipes and cookbooks
        # ------------------------------------------------------------------------------
        benchmark_results = {}
        start_time = time.perf_counter()
        try:
            if self.cookbooks:
                # Process as benchmark cookbooks test
                print(f"[Benchmarking] Part 2: Running cookbooks ({self.cookbooks})...")

                # Run all cookbooks
                for cookbook_index, cookbook in enumerate(self.cookbooks, 0):
                    print(
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
                    cookbook_index=len(self.cookbooks), results=benchmark_results
                )

            elif self.recipes:
                # Process as benchmark recipes test
                print(f"[Benchmarking] Part 2: Running recipes ({self.recipes})...")

                # Run all recipes
                for recipe_index, recipe in enumerate(self.recipes, 0):
                    print(
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
                    recipe_index=len(self.recipes), results=benchmark_results
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
            print(f"[Benchmarking] Run took {(time.perf_counter() - start_time):.4f}s")

        # ------------------------------------------------------------------------------
        # Part 2: Write results
        # ------------------------------------------------------------------------------
        print("[Benchmarking] Writing results...")
        start_time = time.perf_counter()
        try:
            result_args = ResultArguments(
                # Mandatory values
                id=self.run_progress.run_arguments.runner_id,
                start_time=self.run_progress.run_arguments.start_time,
                end_time=self.run_progress.run_arguments.end_time,
                duration=self.run_progress.run_arguments.duration,
                results=self.run_progress.run_arguments.results,
                status=self.run_progress.run_arguments.status,
                # Additional info
                recipes=self.recipes,
                cookbooks=self.cookbooks,
                endpoints=self.endpoints,
                num_of_prompts=self.num_of_prompts,
                random_seed=self.random_seed,
                system_prompt=self.system_prompt,
            )
            Result.create(result_args)
            print(
                f"[Benchmarking] {id} - Run results written to "
                f"{self.run_progress.run_arguments.results_file}"
            )

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to write results due to error: {str(e)}"
            )

        finally:
            print(
                f"[Benchmarking] Writing results took {(time.perf_counter() - start_time):.4f}s"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Update completion status
        # ------------------------------------------------------------------------------
        print("[Benchmarking] Updating completion status...")
        if self.run_progress.run_arguments.error_messages:
            self.run_progress.notify_progress(
                status=RunStatus.COMPLETED_WITH_ERRORS,
            )
        else:
            self.run_progress.notify_progress(
                status=RunStatus.COMPLETED,
            )
        return self.run_progress.run_arguments.results

    async def _run_recipe(self, recipe_name: str):
        """
        Asynchronously runs a single recipe benchmarking process.

        This method is responsible for executing the benchmarking process for a given recipe. It involves
        loading the recipe instance, executing the generator pipeline to obtain prompts, and performing
        predictions based on those prompts.

        Args:
            recipe_name (str): The name of the recipe to run the benchmarking process on.

        Raises:
            RuntimeError: If the recipe instance is not initialized before attempting to run the generator pipeline.

        Returns:
            None
        """
        # ------------------------------------------------------------------------------
        # Part 1: Load required instances
        # ------------------------------------------------------------------------------
        print("[Benchmarking] Load required instances...")
        start_time = time.perf_counter()
        try:
            # Load recipe
            self.recipe_instance = Recipe.load(recipe_name)
            print(
                f"[Benchmarking] Load recipe instance took {(time.perf_counter() - start_time):.4f}s"
            )

            # Load metrics
            start_time = time.perf_counter()
            self.recipe_metrics = [
                Metric.load(metric) for metric in self.recipe_instance.metrics
            ]
            print(
                f"[Benchmarking] Load recipe metrics took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            error_message = (
                f"Failed to load instances in running recipe due to error: {str(e)}"
            )
            self.run_progress.notify_error(error_message)

        # ------------------------------------------------------------------------------
        # Part 2: Build and execute generator pipeline to get prompts and perform predictions
        # ------------------------------------------------------------------------------
        print("[Benchmarking] Build and execute generator pipeline...")
        start_time = time.perf_counter()
        recipe_predictions = []
        try:
            if self.recipe_instance:
                task = self.event_loop.create_task(self._run_generator_pipeline())
                await task
                recipe_predictions = task.result()
                print(
                    f"[Benchmarking] Predicting prompts for recipe [{self.recipe_instance.id}] took "
                    f"{(time.perf_counter() - start_time):.4f}s"
                )
            else:
                raise RuntimeError("Recipe Instance is not initialised.")

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to build and execute generator pipeline due to error: {str(e)}"
            )

        # ------------------------------------------------------------------------------
        # Part 3: Sort the recipe predictions into groups for recipe
        # ------------------------------------------------------------------------------
        # Sort PromptArguments instances into groups based on the same conn_id, rec_id, ds_id, and pt_id
        print("[Benchmarking] Sort the recipe predictions into groups")
        start_time = time.perf_counter()
        grouped_recipe_preds = {}
        try:
            # Assuming `recipe_preds` is your list of PromptArguments instances
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

            print(
                (
                    f"[Benchmarking] Sort the recipe predictions into groups for recipe [{self.recipe_instance.id}] "
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
        print("[Benchmarking] Performing metrics calculation")
        start_time = time.perf_counter()
        recipe_results = {}
        try:
            for group_recipe_key, group_recipe_value in grouped_recipe_preds.items():
                print(
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
                        metric.get_results(prompts, predicted_results, targets)  # type: ignore ; ducktyping
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
                            "predicted_result": predicted_result,
                            "target": target,
                            "duration": duration,
                        }
                    )

                # Append results for recipe
                recipe_results[group_recipe_key] = {
                    "data": group_data,
                    "results": metrics_result,
                }

            print(
                f"[Benchmarking] Performing metrics calculation for recipe [{self.recipe_instance.id}] "
                f"took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to calculate metrics in executing recipe due to error: {str(e)}"
            )

        finally:
            return recipe_results

    async def _run_generator_pipeline(self):
        """
        Executes the benchmark pipeline using the provided recipe instance and connectors.

        This method orchestrates the benchmarking process by generating prompts from the recipe instance's
        datasets and prompt templates. It then uses the provided connectors to generate predictions from these prompts.
        The benchmarking results are asynchronously yielded, facilitating concurrent processing.

        Args:
            recipe_inst (Recipe): The recipe instance containing the datasets and prompt templates for
            generating prompts.

            recipe_connectors (list[Connector]): A list of connector instances that will be used to
            generate predictions from the prompts.

        Returns:
            AsyncGenerator: An asynchronous generator that yields the benchmarking results, allowing for concurrent
            processing of the pipeline's output.

        Raises:
            Exception: An error is raised if there is a failure during the prompt generation or prediction phases
            of the benchmarking process.
        """
        # Generate prompts based on datasets and replacement in prompt templates
        gen_prompt = self._generate_prompts()

        # Generate predictions based on the gen_prompts on different connectors
        gen_result = self._generate_predictions(gen_prompt)

        try:
            output = []
            async for result in gen_result:
                output.append(copy.deepcopy(result))
            return output

        except Exception as e:
            self.run_progress.notify_error(
                f"[Benchmarking] Failed to consume predictions due to error: {str(e)}"
            )
            return []  # Empty generator

    async def _generate_prompts(self) -> AsyncGenerator[PromptArguments, None]:
        """
        Asynchronously generates prompts by rendering templates with dataset content.

        This coroutine iterates over the datasets and prompt templates associated with the recipe instance,
        rendering prompts using the Jinja2 template engine. If the recipe instance has no associated prompt templates,
        the prompts are generated solely from the datasets.

        Yields:
            PromptArguments: An object containing the rendered prompt and associated metadata, such as the recipe ID,
                             dataset ID, and prompt template ID.

        Raises:
            Exception: If an error occurs during the rendering of prompts or any related operation.
        """
        if self.recipe_instance.prompt_templates:
            for pt_id in self.recipe_instance.prompt_templates:
                pt_info = Storage.read_object_generator(
                    EnvVariables.PROMPT_TEMPLATES.name, pt_id, "json", "template"
                )
                pt = next(pt_info)
                jinja2_template = Template(pt)

                for ds_id in self.recipe_instance.datasets:
                    ds_info = Storage.read_object_generator(
                        EnvVariables.DATASETS.name, ds_id, "json", "examples.item"
                    )
                    for prompt_index, prompt in enumerate(ds_info, 1):
                        try:
                            if (
                                self.num_of_prompts != 0
                                and prompt_index > self.num_of_prompts
                            ):
                                break

                            rendered_prompt = jinja2_template.render(
                                {"prompt": prompt["input"]}
                            )
                            yield PromptArguments(
                                rec_id=self.recipe_instance.id,
                                pt_id=pt_id,
                                ds_id=ds_id,
                                random_seed=self.random_seed,
                                system_prompt=self.system_prompt,
                                connector_prompt=ConnectorPromptArguments(
                                    prompt_index=prompt_index,
                                    prompt=rendered_prompt,
                                    target=prompt["target"],
                                ),
                            )
                        except Exception as e:
                            self.run_progress.notify_error(
                                f"[Benchmarking] Error while generating prompt for prompt_info "
                                f"[rec_id: {self.recipe_instance.id}, ds_id: {ds_id}, pt_id: {pt_id}, "
                                f"prompt_index: {prompt_index}] due to error: {str(e)}"
                            )
                            continue
        else:
            pt_id = "no-template"
            for ds_id in self.recipe_instance.datasets:
                ds_info = Storage.read_object_generator(
                    EnvVariables.DATASETS.name, ds_id, "json", "examples.item"
                )
                for prompt_index, prompt in enumerate(ds_info, 1):
                    try:
                        if (
                            self.num_of_prompts != 0
                            and prompt_index > self.num_of_prompts
                        ):
                            break

                        yield PromptArguments(
                            rec_id=self.recipe_instance.id,
                            pt_id=pt_id,
                            ds_id=ds_id,
                            random_seed=self.random_seed,
                            system_prompt=self.system_prompt,
                            connector_prompt=ConnectorPromptArguments(
                                prompt_index=prompt_index,
                                prompt=prompt["input"],
                                target=prompt["target"],
                            ),
                        )
                    except Exception as e:
                        self.run_progress.notify_error(
                            f"[Benchmarking] Error while generating prompt for prompt_info "
                            f"[rec_id: {self.recipe_instance.id}, ds_id: {ds_id}, pt_id: {pt_id}, "
                            f"prompt_index: {prompt_index}] due to error: {str(e)}"
                        )
                        continue

    async def _generate_predictions(
        self, gen_prompt: AsyncGenerator[PromptArguments, None]
    ):
        """
        Asynchronously generates predictions for a series of prompts using the available recipe connectors and
        caches the results in a database instance.

        This coroutine receives an asynchronous generator that yields prompts, and for each prompt, it interacts
        with each recipe connector to obtain predictions. It checks the cache for existing records before
        querying the connector. If a cache hit occurs, the prompt is updated with the cached data; otherwise,
        the connector is used to generate a prediction which is then cached. The updated prompt information is
        subsequently yielded.

        Args:
            gen_prompt (AsyncGenerator[PromptArguments, None]): An asynchronous generator that yields prompts
            to be processed.

        Yields:
            PromptArguments: The prompt information with updated predictions, either retrieved from the cache
            or obtained from a recipe connector.

        Raises:
            Exception: If an error occurs while reading from the cache or during prediction generation.
        """
        async for prompt_info in gen_prompt:
            for rec_conn in self.recipe_connectors:
                # Create a new prompt info with connection id
                new_prompt_info = PromptArguments(
                    conn_id=rec_conn.id,
                    rec_id=prompt_info.rec_id,
                    pt_id=prompt_info.pt_id,
                    ds_id=prompt_info.ds_id,
                    random_seed=prompt_info.random_seed,
                    system_prompt=prompt_info.system_prompt,
                    connector_prompt=prompt_info.connector_prompt,
                )

                # Attempt to read from database for cache values
                try:
                    cache_record = Storage.read_database_record(
                        self.database_instance,
                        (
                            new_prompt_info.rec_id,
                            new_prompt_info.conn_id,
                            new_prompt_info.pt_id,
                            new_prompt_info.connector_prompt.prompt,
                        ),
                        Benchmarking.sql_read_cache_record,
                    )
                except Exception as e:
                    self.run_progress.notify_error(
                        f"[Benchmarking] Error while reading benchmark cache record for prompt_info "
                        f"[conn_id: {new_prompt_info.conn_id}, rec_id: {new_prompt_info.rec_id}, "
                        f"ds_id: {new_prompt_info.ds_id}, pt_id: {new_prompt_info.pt_id}, "
                        f"prompt_index: {new_prompt_info.connector_prompt.prompt_index}] due to error: {str(e)}"
                    )
                    continue

                # Check if cache record exists. If it exists, we will load from cache else we will get prediction
                try:
                    if cache_record is None:
                        new_prompt_info.connector_prompt = (
                            await Connector.get_prediction(
                                new_prompt_info.connector_prompt, rec_conn
                            )
                        )
                        Storage.create_database_record(
                            self.database_instance,
                            new_prompt_info.to_tuple(),
                            Benchmarking.sql_create_cache_record,
                        )
                    else:
                        new_prompt_info = PromptArguments.from_tuple(cache_record)

                    # Return updated prompt info
                    yield new_prompt_info

                except Exception as e:
                    self.run_progress.notify_error(
                        f"[Benchmarking] Failed to generate prediction for prompt_info "
                        f"[conn_id: {new_prompt_info.conn_id}, rec_id: {new_prompt_info.rec_id}, "
                        f"ds_id: {new_prompt_info.ds_id}, pt_id: {new_prompt_info.pt_id}, "
                        f"prompt_index: {new_prompt_info.connector_prompt.prompt_index}] due to error: {str(e)}"
                    )
                    continue


class PromptArguments(BaseModel):
    conn_id: str = ""  # The ID of the connection, default is an empty string

    rec_id: str  # The ID of the recipe

    ds_id: str  # The ID of the dataset

    pt_id: str  # The ID of the prompt template

    random_seed: int  # The random seed used for generating deterministic results

    system_prompt: str  # The system-generated prompt used for benchmarking

    connector_prompt: ConnectorPromptArguments  # The prompt information to send

    def to_tuple(self) -> tuple:
        """
        Converts the PromptArguments instance into a tuple.

        This method collects all the attributes of the PromptArguments instance and forms a tuple
        with the attribute values in this specific order: conn_id, rec_id, ds_id, pt_id, prompt,
        target, predicted_results, duration.
        This tuple is suitable for serialization tasks, like storing the prompt arguments data
        in a database or transmitting it over a network.

        Returns:
            tuple: A tuple representation of the PromptArguments instance.
        """
        return (
            self.conn_id,
            self.rec_id,
            self.ds_id,
            self.pt_id,
            self.random_seed,
            self.system_prompt,
            self.connector_prompt.prompt_index,
            self.connector_prompt.prompt,
            str(self.connector_prompt.target),
            str(self.connector_prompt.predicted_results),
            str(self.connector_prompt.duration),
        )

    @classmethod
    def from_tuple(cls, cache_record: tuple) -> PromptArguments:
        """
        Converts a tuple into a PromptArguments instance.

        This method accepts a tuple that contains attribute values in the following order:
        conn_id, rec_id, ds_id, pt_id, prompt_index, prompt, target, predicted_results, duration.
        It then constructs a PromptArguments instance using these values.
        This method is primarily used for deserialization tasks, such as retrieving prompt arguments data from a
        database or receiving it over a network.

        Args:
            cache_record (tuple): A tuple containing the attribute values for a PromptArguments instance.

        Returns:
            PromptArguments: A PromptArguments instance constructed from the tuple.
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
            predicted_results = ast.literal_eval(cache_record[10])
        except Exception:
            predicted_results = cache_record[10]

        return cls(
            conn_id=cache_record[1],
            rec_id=cache_record[2],
            ds_id=cache_record[3],
            pt_id=cache_record[4],
            random_seed=cache_record[5],
            system_prompt=cache_record[6],
            connector_prompt=ConnectorPromptArguments(
                prompt_index=cache_record[7],
                prompt=cache_record[8],
                target=target,
                predicted_results=predicted_results,
                duration=float(cache_record[11]),
            ),
        )
