from __future__ import annotations

import asyncio
import concurrent.futures
import glob
import json
import multiprocessing
import time
from functools import partial
from pathlib import Path

from jinja2 import Template
from slugify import slugify

from moonshot.src.benchmarking.metrics import load_metrics
from moonshot.src.common.connection import Connection, get_multiple_predictions
from moonshot.src.common.db import Database
from moonshot.src.common.env_variables import EnvironmentVars
from moonshot.src.utils.timeit import timeit


class Recipe:
    @classmethod
    def load_from_json_config(cls, recipe_config: str) -> Recipe:
        """
        Loads a recipe from a JSON configuration file.

        Args:
            recipe_config (str): The name of the recipe configuration.

        Returns:
            Recipe: An instance of the Recipe class populated with data from the JSON file.
        """
        with open(f"{EnvironmentVars.RECIPES}/{recipe_config}.json", "r") as json_file:
            file_info = json.load(json_file)
            return cls(
                Path(recipe_config).stem,
                file_info["name"],
                file_info["description"],
                file_info["tags"],
                file_info["dataset"],
                file_info["prompt_templates"],
                file_info["metrics"],
            )

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        tags: list,
        dataset: str,
        prompt_templates: list,
        metrics: list,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.tags = tags
        self.dataset = dataset
        self.prompt_templates = prompt_templates
        self.metrics = metrics

        # Additional variables for loaded info
        self.dataset_info = None
        self.prompt_templates_info = []
        self.metrics_instances = []
        self.generated_prompts_info = {}

    def run(self, number_of_prompts: int, cache_info: dict = None) -> None:
        """
        Runs the recipe.

        Args:
            number_of_prompts (int): The number of prompts from the dataset to generate.
            cache_info (dict): Information about the cache to use that contains previous results (default: None).
        """
        print(f"🔃 Running recipe ({self.name})... do not close this terminal.")
        print("You can start a new terminal to continue working.")

        # Load dataset information
        start_time = time.perf_counter()
        self.dataset_info = json.load(
            open(f"{EnvironmentVars.DATASETS}/{self.dataset}.json", "r" ,encoding = "utf-8")
        )
        print(
            f"[Recipe ({self.id}) - Run] Load dataset information took {(time.perf_counter() - start_time):.4f}s"
        )

        # Load prompt templates information
        start_time = time.perf_counter()
        for template in self.prompt_templates:
            self.prompt_templates_info.append(
                json.load(
                    open(f"{EnvironmentVars.PROMPT_TEMPLATES}/{template}.json", "r" ,encoding = "utf-8")
                )
            )
        print(
            f"[Recipe ({self.id}) - Run] Load prompt templates took {(time.perf_counter() - start_time):.4f}s"
        )

        # Create a new metric instance
        start_time = time.perf_counter()
        self.metrics_instances = load_metrics(self.metrics)
        print(
            f"[Recipe ({self.id}) - Run] Load metrics took {(time.perf_counter() - start_time):.4f}s"
        )

        # Generate all the required prompts
        start_time = time.perf_counter()
        self._generate_prompts_targets(number_of_prompts, cache_info)
        print(
            f"[Recipe ({self.id}) - Run] Generate prompts took {(time.perf_counter() - start_time):.4f}s"
        )

    def _generate_prompts_targets(
        self, number_of_prompts: int, cache_info: dict = None
    ) -> None:
        """
        Generates prompts and targets based on the given number of prompts and cache information.

        Args:
            number_of_prompts (int): The number of prompts to generate.
            cache_info (dict, optional): The cache information. Defaults to None.
        """
        # If the number of prompts is below 1, it means use all data available
        prompts_to_generate = (
            len(self.dataset_info["examples"])
            if number_of_prompts < 1
            else number_of_prompts
        )
        self.generated_prompts_info = {}

        if self.prompt_templates_info:
            for template in self.prompt_templates_info:
                jinja_template = Template(template["template"])

                # Generate prompts and targets
                temp_list = []
                for prompt_index, prompt_set in enumerate(
                    self.dataset_info["examples"], 1
                ):
                    if prompt_index > prompts_to_generate:
                        break

                    rendered_prompt = jinja_template.render(
                        {"prompt": prompt_set["input"]}
                    )
                    target = prompt_set["target"]

                    # Check if this prompt is in the cache for this template
                    cache_output = None

                    if cache_info and template["name"] in cache_info:
                        cache_records = cache_info[template["name"]]
                        for cache_record in cache_records:
                            if (
                                cache_record["prompt"] == rendered_prompt
                                and cache_record["target"] == target
                            ):
                                cache_output = {
                                    "prompt": cache_record["prompt"],
                                    "target": cache_record["target"],
                                    "predicted_result": cache_record[
                                        "predicted_result"
                                    ],
                                    "duration": cache_record["duration"],
                                }
                                break

                    # If not in cache, generate the prompt prediction
                    if cache_output:
                        temp_list.append(cache_output)
                    else:
                        temp_list.append({"prompt": rendered_prompt, "target": target})
                self.generated_prompts_info[template["name"]] = {"data": temp_list}
        else:
            temp_list = []

            for prompt_index, prompt_set in enumerate(self.dataset_info["examples"], 1):
                if prompt_index > prompts_to_generate:
                    break
                prompt = prompt_set["input"]
                target = prompt_set["target"]
                cache_output = None
                if cache_info and "no-template" in cache_info:
                    cache_records = cache_info["no-template"]
                    for cache_record in cache_records:
                        check_prompt = (
                            json.dumps(prompt)
                            if not isinstance(prompt, str)
                            else prompt
                        )
                        check_target = (
                            json.dumps(target)
                            if not isinstance(target, str)
                            else target
                        )
                        if (
                            cache_record["prompt"] == check_prompt
                            and cache_record["target"] == check_target
                        ):
                            cache_output = {
                                "prompt": cache_record["prompt"],
                                "target": cache_record["target"],
                                "predicted_result": cache_record["predicted_result"],
                                "duration": cache_record["duration"],
                            }
                            break

                if cache_output:
                    temp_list.append(cache_output)
                else:
                    temp_list.append({"prompt": prompt, "target": target})

            self.generated_prompts_info["no-template"] = {"data": temp_list}


class RecipeResult:
    @staticmethod
    def run(recipe_endpoint: tuple[str, str, int, str]) -> tuple[str, str, dict]:
        """
        Runs the recipe with the given recipe endpoint.

        Args:
            recipe_endpoint (tuple[str, str, int, str]): A tuple containing the recipe, endpoint, number of prompts,
            and the database file.

        Returns:
            tuple[str, str, dict]: A tuple containing the recipe, endpoint, and a dictionary of generated prompts
            information.
        """
        recipe, endpoint, number_of_prompts, db_file = recipe_endpoint

        # Read the recipe and endpoint
        conn_instance = Connection.load_from_json_config(endpoint)
        recipe_instance = Recipe.load_from_json_config(recipe)

        # Load the database and cache
        start_time = time.perf_counter()
        db_instance = Database(db_file)
        db_instance.create_connection()
        cache_records = RecipeResult.convert_cache_tuples_to_dict(
            db_instance.read_cache_records(recipe, endpoint)
        )
        print(
            f"[RecipeResult - Run] Load database and cache records took {(time.perf_counter() - start_time):.4f}s"
        )

        try:
            # Generate and query the model with recipe prompts (with/without pre- / post-prompts)
            start_time = time.perf_counter()
            recipe_instance.run(number_of_prompts, cache_records)
            print(
                f"[RecipeResult - Run] Generating recipe prompts took {(time.perf_counter() - start_time):.4f}s "
                f"for {len(recipe_instance.generated_prompts_info)} prompts."
            )

            # Get predictions
            start_time = time.perf_counter()
            updated_prompt_template_list = asyncio.run(
                get_multiple_predictions(
                    recipe_instance.generated_prompts_info,
                    conn_instance,
                    partial(
                        db_instance.append_cache_records,
                        recipe,
                    ),
                )
            )
            print(
                f"[RecipeResult - Run] Querying predictions took {(time.perf_counter() - start_time):.4f}s"
            )

            # Get metrics
            start_time = time.perf_counter()
            for index, updated_prompt_template_info in enumerate(
                updated_prompt_template_list
            ):
                # Get dictionary name using index
                prompt_template_name = list(
                    recipe_instance.generated_prompts_info.keys()
                )[index]

                # Combine output_responses and targets
                metrics_prompts = [
                    prompt_info["prompt"]
                    for prompt_info in updated_prompt_template_info
                ]
                metrics_predicted_results = [
                    prompt_info["predicted_result"]
                    for prompt_info in updated_prompt_template_info
                ]
                metrics_targets = [
                    prompt_info["target"]
                    for prompt_info in updated_prompt_template_info
                ]

                # Get metrics output for this prompt template
                metrics_result = []
                for metric in recipe_instance.metrics_instances:
                    metrics_result.append(
                        metric.get_results(
                            metrics_prompts,
                            metrics_predicted_results,
                            metrics_targets,
                        )
                    )

                # Update the results for this prompt template
                recipe_instance.generated_prompts_info[prompt_template_name] = {
                    "data": updated_prompt_template_info,
                    "results": metrics_result,
                }
            print(
                f"[RecipeResult - Run] Calculate metrics took {(time.perf_counter() - start_time):.4f}s"
            )

            # Write cache records and close connection
            db_instance.write_cache_records()
            db_instance.close_connection()

            return recipe, endpoint, recipe_instance.generated_prompts_info

        except Exception as exception:
            # Write cache records and close connection
            db_instance.write_cache_records()
            db_instance.close_connection()

            raise exception

    @staticmethod
    @timeit
    def convert_cache_tuples_to_dict(cache_records: list) -> dict:
        """
        This static method converts a list of cache records tuples to a dictionary.

        Args:
            cache_records (list): A list of cache record tuples to be converted to a dictionary.

        Returns:
            dict: A dictionary of cache records.
        """
        # Initialize an empty dictionary to store the cache records
        cache_dict = {}

        # Iterate over each cache record in the list
        for cache_record in cache_records:
            # Extract the cache prompt template from the cache record
            cache_prompt_template = cache_record[3]
            cache_dict.setdefault(cache_prompt_template, []).append(
                {
                    "prompt": cache_record[4],
                    "target": cache_record[5],
                    "predicted_result": cache_record[6],
                    "duration": cache_record[7],
                }
            )
        return cache_dict


def get_all_recipes() -> list:
    """
    This function retrieves a list of available recipes.

    Returns:
        list: A list of available recipes. Each item in the list represents a recipe.
    """
    filepaths = [
        Path(fp).stem
        for fp in glob.iglob(f"{EnvironmentVars.RECIPES}/*.json")
        if "__" not in fp
    ]
    return get_recipes(filepaths)


def get_recipes(desired_recipes: list) -> list:
    """
    Retrieves a list of desired recipes.

    Args:
        desired_recipes (list): A list of recipe names to retrieve.

    Returns:
        list: A list of desired recipes, where each recipe is represented as a dictionary or an object.
    """
    recipes = []
    for recipe_name in desired_recipes:
        recipe_filename = slugify(recipe_name, lowercase=False)
        filepath = f"{EnvironmentVars.RECIPES}/{recipe_filename}.json"
        with open(filepath, "r",encoding = "utf-8") as json_file:
            recipe_info = json.load(json_file)
            recipe_info["filename"] = Path(filepath).stem
            recipes.append(recipe_info)
    return recipes


def add_new_recipe(
    name: str,
    description: str,
    tags: list[str],
    dataset: str,
    prompt_templates: list[str],
    metrics: list[str],
) -> None:
    """
    Adds a new recipe.
    This method allows adding a new recipe with the specified name, description, tags, dataset,
    prompt templates, and a list of metrics.

    Args:
        name (str): The name or identifier of the new recipe.
        description (str): A brief description of the new recipe, providing information about its
        purpose or content.
        tags (list[str]): A list of tags to be included in the new recipe.
        dataset (str): The dataset to be used.
        prompt_templates (list[str]): A list of prompt templates to be included in the new recipe.
        metrics (list[str]): A list of metrics to be included in the new recipe.
    """
    recipe_info = {
        "name": name,
        "description": description,
        "tags": tags,
        "dataset": dataset,
        "prompt_templates": prompt_templates,
        "metrics": metrics,
    }
    recipe_filename = slugify(name, lowercase=False)
    with open(f"{EnvironmentVars.RECIPES}/{recipe_filename}.json", "w") as json_file:
        json.dump(recipe_info, json_file, indent=2)


def run_recipes_with_endpoints(
    recipes: list[str], endpoints: list[str], num_of_prompts: int, db_file: str
) -> dict:
    """
    Runs a list of recipes using a list of endpoints.
    This static method allows running a list of recipes using a list of endpoints and returns the results
    as a dictionary.

    Args:
        recipes (list[str]): A list of recipe names to be executed.
        endpoints (list[str]): A list of endpoint names where the recipes will be executed.
        num_of_prompts (int): The number of generated prompts to be run against.
        db_file (str): The path to the database file.

    Returns:
        dict: A dictionary containing the results of running the recipes.
        The dictionary may include information about the success of each recipe execution
        and any output data or errors.
    """
    print(
        f"Running recipes {recipes} with endpoints {endpoints}. Caching results in {db_file}."
    )

    recipe_endpoint_results = {}
    if str(EnvironmentVars.ENABLE_MULTIPROCESSING).lower() == "true":
        # Use multiprocessing to process each individual recipe
        print("[MULTIPROCESSING] Running recipes in parallel.")
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=multiprocessing.cpu_count()
        ) as executor:
            # Create different combination of recipe and connection (4 recipe results for 2 recipes * 2 endpoints)
            recipe_endpoint_combinations = [
                (recipe, endpoint, num_of_prompts, db_file)
                for recipe in recipes
                for endpoint in endpoints
            ]
            print(
                f"Spawning {multiprocessing.cpu_count()} processes to run {len(recipe_endpoint_combinations)} recipes."
            )

            futures = {
                executor.submit(RecipeResult.run, recipe_endpoint): recipe_endpoint
                for recipe_endpoint in recipe_endpoint_combinations
            }
            for future in concurrent.futures.as_completed(futures):
                recipe, endpoint, generated_prompts_info = future.result()
                recipe_endpoint_results[f"{recipe}_{endpoint}"] = generated_prompts_info

        return recipe_endpoint_results

    else:
        # Create different combination of recipe and connection (4 recipe results for 2 recipes * 2 endpoints)
        print("[SEQUENTIAL] Running recipes in sequence.")
        recipe_endpoint_combinations = [
            (recipe, endpoint, num_of_prompts, db_file)
            for recipe in recipes
            for endpoint in endpoints
        ]
        for recipe_endpoint in recipe_endpoint_combinations:
            recipe, endpoint, generated_prompts_info = RecipeResult.run(recipe_endpoint)
            recipe_endpoint_results[f"{recipe}_{endpoint}"] = generated_prompts_info

        return recipe_endpoint_results
