from __future__ import annotations

import ast
import time
from itertools import groupby
from operator import attrgetter
from typing import Any, AsyncGenerator, Callable

from jinja2 import Template
from pydantic import BaseModel

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.metrics.metric import Metric
from moonshot.src.recipes.recipe import Recipe
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
        prompt_index INTEGER NOT NULL,
        prompt text NOT NULL,
        target text NOT NULL,
        predicted_results text NOT NULL,
        duration text NOT NULL
        );
    """
    sql_create_cache_record = """
        INSERT INTO cache_table(conn_id,rec_id,ds_id,pt_id,prompt_index,prompt,target,predicted_results,duration)
        VALUES(?,?,?,?,?,?,?,?,?)
    """
    sql_read_cache_record = """
        SELECT * from cache_table WHERE rec_id=? AND conn_id=? AND pt_id=? AND prompt=?
    """

    async def generate(
        self,
        event_loop: Any,
        database_instance: DBAccessor | None,
        num_of_prompts: int,
        recipe_inst: Recipe,
        recipe_eps: list[Connector],
        metrics_insts: list[Metric],
        handle_error_message_callback: Callable,
    ) -> dict:
        self.event_loop = event_loop
        self.database_instance = database_instance
        self.num_of_prompts = num_of_prompts
        self.recipe_instance = recipe_inst
        self.recipe_eps = recipe_eps
        self.metrics_instances = metrics_insts
        self.handle_error_message = handle_error_message_callback

        # ------------------------------------------------------------------------------
        # Part 1: Create new cache table if needed
        # ------------------------------------------------------------------------------
        print("[Benchmarking] Part 1: Create new cache table if needed...")
        # Create cache table
        if database_instance:
            Storage.create_database_table(
                database_instance, Benchmarking.sql_create_cache_table
            )
        else:
            raise RuntimeError("Failed to get database instance.")

        # ------------------------------------------------------------------------------
        # Part 2: Build and execute generator pipeline to get prompts and perform predictions
        # ------------------------------------------------------------------------------
        print(
            "[Benchmarking] Part 2: Building and executing generator pipeline for predicting prompts..."
        )
        recipe_preds = []  # Initialize recipe_preds as an empty list
        try:
            start_time = time.perf_counter()
            if recipe_inst:
                task = self.event_loop.create_task(
                    self._execute_benchmark_pipeline(recipe_inst, recipe_eps)
                )
                await task
                recipe_preds = task.result()
                print(
                    f"[Benchmarking] Predicting prompts for recipe [{recipe_inst.id}] took "
                    f"{(time.perf_counter() - start_time):.4f}s"
                )
            else:
                raise RuntimeError("recipe_inst is None")
        except Exception as e:
            error_message = (
                f"[BenchmarkingError] Failed to build and execute benchmark pipeline in executing recipe "
                f"due to error: {str(e)}"
            )
            self.handle_error_message(error_message)

        # ------------------------------------------------------------------------------
        # Part 3: Sort the recipe predictions into groups for recipe
        # ------------------------------------------------------------------------------
        # Sort PromptArguments instances into groups based on the same conn_id, rec_id, ds_id, and pt_id
        print("[Benchmarking] Part 3: Sort the recipe predictions into groups")
        start_time = time.perf_counter()
        grouped_recipe_preds = {}
        try:
            # Assuming `recipe_preds` is your list of PromptArguments instances
            recipe_preds.sort(key=attrgetter("conn_id", "rec_id", "ds_id", "pt_id"))

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
                    recipe_preds, key=attrgetter("conn_id", "rec_id", "ds_id", "pt_id")
                )
                for group_list in [list(group)]
            }

            print(
                (
                    f"[Benchmarking] Sort the recipe predictions into groups for recipe [{recipe_inst.id}] "
                    f"took {(time.perf_counter() - start_time):.4f}s"
                )
            )

        except Exception as e:
            error_message = (
                f"[BenchmarkingError] Failed to sort recipe predictions into groups in executing recipe "
                f"due to error: {str(e)}"
            )
            handle_error_message_callback(error_message)

        # ------------------------------------------------------------------------------
        # Part 4: Generate the metrics results
        # ------------------------------------------------------------------------------
        # Load metrics for recipe
        print("[Benchmarking] Part 4: Performing metrics calculation")
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
                for metric in metrics_insts:
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
                f"[Benchmarking] Performing metrics calculation for recipe [{recipe_inst.id}] "
                f"took {(time.perf_counter() - start_time):.4f}s"
            )

        except Exception as e:
            error_message = (
                f"[BenchmarkingError] Failed to calculate metrics in executing recipe "
                f"due to error: {str(e)}"
            )
            handle_error_message_callback(error_message)

        finally:
            return recipe_results

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

        try:
            return [result async for result in gen_result]

        except Exception as e:
            error_message = f"[BenchmarkingError] Failed to consume predictions due to error: {str(e)}"
            self.handle_error_message(error_message)
            return []  # Empty generator

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
                pt_info = Storage.read_object_generator(
                    EnvVariables.PROMPT_TEMPLATES.name, pt_id, "json", "template"
                )
                pt = next(pt_info)
                jinja2_template = Template(pt)

                for ds_id in ds_ids:
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
                                rec_id=rec_id,
                                pt_id=pt_id,
                                ds_id=ds_id,
                                connector_prompt=ConnectorPromptArguments(
                                    prompt_index=prompt_index,
                                    prompt=rendered_prompt,
                                    target=prompt["target"],
                                ),
                            )
                        except Exception as e:
                            error_message = (
                                f"[BenchmarkingError] Error while generating prompt for prompt_info "
                                f"[rec_id: {rec_id}, ds_id: {ds_id}, pt_id: {pt_id}, prompt_index: {prompt_index}] "
                                f"due to error: {str(e)}"
                            )
                            self.handle_error_message(error_message)
                            continue
        else:
            pt_id = "no-template"
            for ds_id in ds_ids:
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
                            rec_id=rec_id,
                            pt_id=pt_id,
                            ds_id=ds_id,
                            connector_prompt=ConnectorPromptArguments(
                                prompt_index=prompt_index,
                                prompt=prompt["input"],
                                target=prompt["target"],
                            ),
                        )
                    except Exception as e:
                        error_message = (
                            f"[BenchmarkingError] Error while generating prompt for prompt_info "
                            f"[rec_id: {rec_id}, ds_id: {ds_id}, pt_id: {pt_id}, prompt_index: {prompt_index}] "
                            f"due to error: {str(e)}"
                        )
                        self.handle_error_message(error_message)
                        continue

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
                # Create a new prompt info with connection id
                new_prompt_info = PromptArguments(
                    conn_id=rec_conn.id,
                    rec_id=prompt_info.rec_id,
                    pt_id=prompt_info.pt_id,
                    ds_id=prompt_info.ds_id,
                    connector_prompt=prompt_info.connector_prompt,
                )

                # Attempt to read from database for cache values
                try:
                    cache_record = Storage.read_database_record(
                        database_instance,
                        (
                            new_prompt_info.rec_id,
                            new_prompt_info.conn_id,
                            new_prompt_info.pt_id,
                            new_prompt_info.connector_prompt.prompt,
                        ),
                        Benchmarking.sql_read_cache_record,
                    )
                except Exception as e:
                    error_message = (
                        f"[BenchmarkingError] Error while reading benchmark cache record for prompt_info "
                        f"[conn_id: {new_prompt_info.conn_id}, rec_id: {new_prompt_info.rec_id}, "
                        f"ds_id: {new_prompt_info.ds_id}, pt_id: {new_prompt_info.pt_id}, "
                        f"prompt_index: {new_prompt_info.connector_prompt.prompt_index}] due to error: {str(e)}"
                    )
                    self.handle_error_message(error_message)
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
                            database_instance,
                            new_prompt_info.to_tuple(),
                            Benchmarking.sql_create_cache_record,
                        )
                    else:
                        new_prompt_info = PromptArguments.from_tuple(cache_record)

                    # Return updated prompt info
                    yield new_prompt_info

                except Exception as e:
                    error_message = (
                        f"[BenchmarkingError] Failed to generate prediction for prompt_info "
                        f"[conn_id: {new_prompt_info.conn_id}, rec_id: {new_prompt_info.rec_id}, "
                        f"ds_id: {new_prompt_info.ds_id}, pt_id: {new_prompt_info.pt_id}, "
                        f"prompt_index: {new_prompt_info.connector_prompt.prompt_index}] due to error: {str(e)}"
                    )
                    self.handle_error_message(error_message)
                    continue


class PromptArguments(BaseModel):
    conn_id: str = ""  # The ID of the connection, default is an empty string

    rec_id: str  # The ID of the recipe

    ds_id: str  # The ID of the dataset

    pt_id: str  # The ID of the prompt template

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
            target = ast.literal_eval(cache_record[7])
        except Exception:
            target = cache_record[7]

        try:
            predicted_results = ast.literal_eval(cache_record[8])
        except Exception:
            predicted_results = cache_record[8]

        return cls(
            conn_id=cache_record[1],
            rec_id=cache_record[2],
            ds_id=cache_record[3],
            pt_id=cache_record[4],
            connector_prompt=ConnectorPromptArguments(
                prompt_index=cache_record[5],
                prompt=cache_record[6],
                target=target,
                predicted_results=predicted_results,
                duration=float(cache_record[9]),
            ),
        )
