import time
from datetime import datetime

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.storage.storage import Storage


class BenchmarkingResult:
    def generate(self, runner_results: ResultArguments) -> ResultArguments | None:
        """
        Generates a benchmarking result based on the runner results.

        This method processes the runner results to extract benchmark parameters and generate a result dictionary
        with metadata and results. It then writes the results to a file using the Storage class.

        Args:
            runner_results (ResultArguments): An instance of ResultArguments containing the runner's results
            and metadata.

        Returns:
            ResultArguments | None: The updated ResultArguments instance with the generated results included,
                                    or None if runner_results is not provided.

        Raises:
            RuntimeError: If runner_results is None or if no cookbooks or recipes are provided to format results.
        """
        start_time = time.perf_counter()
        try:
            if not runner_results:
                raise RuntimeError("[BenchmarkingResult] Failed to get runner results")

            # ------------------------------------------------------------------------------
            # Part 1: Generate the result
            # ------------------------------------------------------------------------------
            # Generate results metadata
            runner_results.results["metadata"] = self._generate_metadata(runner_results)

            # Generate results based on available data
            runner_results.results["results"] = self._generate_result(runner_results)

            # ------------------------------------------------------------------------------
            # Part 2: Write to file
            # ------------------------------------------------------------------------------
            Storage.create_object(
                EnvVariables.RESULTS.name,
                runner_results.id,
                runner_results.results,
                "json",
            )
        except Exception as e:
            raise RuntimeError(
                f"[BenchmarkingResult] Failed to generate results due to error: {str(e)}"
            )
        finally:
            print(
                f"[BenchmarkingResult] Generate results took {(time.perf_counter() - start_time):.4f}s"
            )
            return runner_results

    def _generate_metadata(self, results_args: ResultArguments) -> dict:
        """
        Generates a metadata dictionary for the benchmarking results.

        This method extracts relevant metadata from the ResultArguments object and formats it into a dictionary.
        The metadata includes the unique identifier, start and end times formatted as strings, duration of the
        benchmarking, status, and various parameters such as recipes, cookbooks, endpoints, number of prompts,
        random seed, and system prompt.

        Args:
            results_args (ResultArguments): An instance of ResultArguments containing the benchmarking metadata.

        Returns:
            dict: A dictionary containing the formatted metadata.
        """
        return {
            "id": results_args.id,
            "start_time": datetime.fromtimestamp(results_args.start_time).strftime(
                "%Y%m%d-%H%M%S"
            ),
            "end_time": datetime.fromtimestamp(results_args.end_time).strftime(
                "%Y%m%d-%H%M%S"
            ),
            "duration": results_args.duration,
            "status": results_args.status.name.lower(),
            "recipes": results_args.params.get("recipes"),
            "cookbooks": results_args.params.get("cookbooks"),
            "endpoints": results_args.params.get("endpoints"),
            "num_of_prompts": results_args.params.get("num_of_prompts"),
            "random_seed": results_args.params.get("random_seed"),
            "system_prompt": results_args.params.get("system_prompt"),
        }

    def _generate_result(self, result_args: ResultArguments) -> dict:
        """
        Generates a result dictionary based on the provided result arguments.

        This method checks if the result arguments contain 'cookbooks' or 'recipes' and
        calls the appropriate method to generate results for each. If neither is present,
        it raises a RuntimeError.

        Args:
            result_args: An instance of ResultArguments containing parameters and raw results.

        Returns:
            A dictionary with a key of 'cookbooks' or 'recipes' and the generated results.

        Raises:
            RuntimeError: If neither cookbooks nor recipes are present in the result arguments.
        """
        cookbooks = result_args.params.get("cookbook")
        recipes = result_args.params.get("recipes")

        result_key = "cookbooks" if cookbooks else "recipes" if recipes else None
        if result_key:
            result_method = getattr(self, f"_generate_{result_key}_result")
            return {
                result_key: result_method(
                    result_args.params.get(result_key), result_args.raw_results
                )
            }
        else:
            raise RuntimeError(
                "[BenchmarkingResult] No cookbooks or recipes to format results."
            )

    def _generate_cookbooks_result(self, cookbooks: list[str], results: dict) -> list:
        """
        Generates a formatted result for each cookbook.

        This method iterates over the list of cookbooks and compiles a dictionary
        for each one, containing the cookbook ID and the results of its recipes.
        The recipe results are generated by calling the _generate_recipe_result method.

        Args:
            cookbooks: A list of cookbook IDs.
            results: A dictionary containing the raw results for each cookbook.

        Returns:
            A list of dictionaries, each representing the formatted results for a cookbook.
        """
        formatted_results = []
        for cookbook in cookbooks:
            cookbook_dict = {
                "id": cookbook,
                "recipes": self._generate_recipes_result(
                    list(results[cookbook].keys()), results[cookbook]
                ),
            }
            formatted_results.append(cookbook_dict)
        return formatted_results

    def _generate_recipes_result(self, recipes: list[str], results: dict) -> list:
        """
        Generates a formatted result for each recipe.

        This method iterates over the list of recipes and compiles a dictionary
        for each one, containing the recipe ID and the results of its models.
        The models' results are further broken down by unique endpoints, datasets,
        and prompt templates. Each model is associated with a list of datasets,
        and each dataset is associated with a list of prompt templates, which
        contain the actual data and metrics.

        Args:
            recipes: A list of recipe IDs.
            results: A dictionary containing the raw results for each recipe, with
                     keys as tuples of endpoint, recipe, dataset, and prompt template IDs.

        Returns:
            A list of dictionaries, each representing the formatted results for a recipe.
        """
        formatted_results = []
        for recipe in recipes:
            recipe_dict = {
                "id": recipe,
                "details": [],
                "num_of_prompts": [],
                "grading_scale": {},
                "grade": [],
            }
            if results:
                recipe_results = results[recipe]
            else:
                recipe_results = {}

            # Getting unique datasets, endpoints, and prompt templates
            unique_endpoints = set()
            unique_datasets = set()
            unique_prompt_templates = set()
            for key_ep, _, key_ds, key_pt in recipe_results.keys():
                unique_endpoints.add(key_ep)
                unique_datasets.add(key_ds)
                unique_prompt_templates.add(key_pt)

            for ep in unique_endpoints:
                ep_num_of_prompts = 0
                for ds in unique_datasets:
                    for pt in unique_prompt_templates:
                        pt_dict = {
                            "model_id": ep,
                            "dataset_id": ds,
                            "prompt_template_id": pt,
                            "data": recipe_results[(ep, recipe, ds, pt)]["data"],
                            "metrics": recipe_results[(ep, recipe, ds, pt)]["results"],
                        }
                        recipe_dict["details"].append(pt_dict)

                        # Calculate num of prompts
                        ep_num_of_prompts += len(
                            recipe_results[(ep, recipe, ds, pt)]["data"]
                        )

                # Append num_of_prompts
                num_of_prompts_dict = {
                    "model_id": ep,
                    "num_of_prompts": ep_num_of_prompts,
                }
                recipe_dict["num_of_prompts"].append(num_of_prompts_dict)

            # Add grading information
            recipe_grading_scale = Recipe.load(recipe).grading_scale
            recipe_dict["grading_scale"].update(recipe_grading_scale)

            # Add grade information

            formatted_results.append(recipe_dict)
        return formatted_results
