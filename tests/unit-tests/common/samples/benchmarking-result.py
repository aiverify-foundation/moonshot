import time
from datetime import datetime

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class BenchmarkingResult:
    def generate(self, runner_results: ResultArguments) -> ResultArguments | None:
        """
        Generates the benchmarking results based on the runner's results.

        This method takes the results from the benchmark runner and processes them to generate a comprehensive
        report. It includes metadata generation, result computation, and storage of the results. If the runner
        results are not provided, it raises a RuntimeError. Upon successful generation of the results, it returns
        the updated ResultArguments object containing the results.

        Args:
            runner_results (ResultArguments): An object containing the benchmark runner's results.

        Returns:
            ResultArguments | None: The updated ResultArguments object with the generated results, or None if
            the generation fails.

        Raises:
            RuntimeError: If the runner results are not provided or if any error occurs during the result
            generation process.
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
            logger.info(
                f"[BenchmarkingResult] Generate results took {(time.perf_counter() - start_time):.4f}s"
            )
            return runner_results

        except Exception as e:
            logger.info(
                f"[BenchmarkingResult] Generate results took {(time.perf_counter() - start_time):.4f}s"
            )
            raise RuntimeError(
                f"[BenchmarkingResult] Failed to generate results due to error: {str(e)}"
            )

    def _generate_metadata(self, results_args: ResultArguments) -> dict:
        """
        Generates metadata for the ResultArguments object.

        This method extracts and formats metadata from the ResultArguments object, which includes
        the unique identifier, start and end times, duration, status, and additional parameters
        such as recipes, cookbooks, endpoints, number of prompts, random seed, and system prompt.

        Args:
            results_args (ResultArguments): An object containing the benchmark runner's results.

        Returns:
            dict: A dictionary containing the formatted metadata.
        """
        return {
            "id": results_args.id,
            "start_time": datetime.fromtimestamp(results_args.start_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "end_time": datetime.fromtimestamp(results_args.end_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "duration": results_args.duration,
            "status": results_args.status.name.lower(),
            "recipes": results_args.params.get("recipes"),
            "cookbooks": results_args.params.get("cookbooks"),
            "endpoints": results_args.params.get("endpoints"),
            "prompt_selection_percentage": results_args.params.get(
                "prompt_selection_percentage"
            ),
            "random_seed": results_args.params.get("random_seed"),
            "system_prompt": results_args.params.get("system_prompt"),
        }

    def _generate_result(self, result_args: ResultArguments) -> dict:
        """
        Generates a result dictionary based on the presence of cookbooks or recipes.

        This method checks if the 'cookbooks' or 'recipes' keys are present in the
        result_args parameters. It then dynamically calls the appropriate method to
        generate results for either cookbooks or recipes. The result is a dictionary
        with a single key ('cookbooks' or 'recipes') and the generated result.

        Args:
            result_args (ResultArguments): An object containing parameters and raw results
                                           for the benchmarking process.

        Returns:
            dict: A dictionary with a single key-value pair where the key is either
                  'cookbooks' or 'recipes', and the value is the result returned by
                  the corresponding method.

        Raises:
            RuntimeError: If neither 'cookbooks' nor 'recipes' are present in the
                          result_args parameters.
        """
        cookbooks = result_args.params.get("cookbooks")
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
        Generates a list of formatted results for each cookbook.

        This method iterates over the provided cookbooks, initializes a dictionary for each,
        generates results for the recipes within that cookbook, populates the cookbook dictionary
        with details and summary information from its recipes, and appends it to the list of
        formatted results.

        Args:
            cookbooks: A list of cookbook identifiers.
            results: A dictionary containing raw results keyed by cookbook identifiers.

        Returns:
            A list of dictionaries, each representing a formatted cookbook result.
        """
        formatted_results = []
        for cookbook in cookbooks:
            cookbook_dict = self._initialize_cookbook_dict(cookbook)
            recipes = self._generate_recipes_result(
                list(results[cookbook].keys()), results[cookbook]
            )
            self._populate_cookbook_details_and_summary(cookbook_dict, recipes)

            formatted_results.append(cookbook_dict)
        return formatted_results

    def _initialize_cookbook_dict(self, cookbook: str) -> dict:
        """
        Initializes a dictionary for a cookbook with default values.

        This method creates a dictionary with an identifier for the cookbook, an empty list for recipes,
        an empty list for the overall evaluation summary, and a count of total number of prompts set to zero.

        Args:
            cookbook: The identifier of the cookbook.

        Returns:
            A dictionary with keys 'id', 'recipes', 'overall_evaluation_summary', and 'total_num_of_prompts'.
        """
        return {
            "id": cookbook,
            "recipes": [],
            "overall_evaluation_summary": [],
            "total_num_of_prompts": 0,
        }

    def _populate_cookbook_details_and_summary(
        self, cookbook_dict: dict, recipes: list
    ) -> None:
        """
        Populates the cookbook dictionary with details and summary information from its recipes.

        This method processes each recipe to update the total number of prompts in the cookbook,
        checks for grading scale consistency across recipes, collects grades for each model,
        and determines the worst grade for each model to append to the cookbook's overall evaluation summary.

        Args:
            cookbook_dict: A dictionary representing a cookbook to be populated with details and summary.
            recipes: A list of dictionaries, each representing a recipe with its details and evaluation summary.
        """
        grading_scale_keys = None
        is_grading_scale_consistent = True
        recipe_grades = {}

        # Initialize the overall_evaluation_summary list and total_num_of_prompts in the cookbook dictionary
        cookbook_dict["overall_evaluation_summary"] = []
        cookbook_dict["total_num_of_prompts"] = 0
        cookbook_dict["recipes"] = recipes

        for recipe in recipes:
            # Add the number of prompts from the current recipe to the total
            cookbook_dict["total_num_of_prompts"] += recipe["total_num_of_prompts"]

            # Initialize grading scale keys if not already set, and check for consistency
            current_grading_scale_keys = list(recipe["grading_scale"].keys())
            if grading_scale_keys is None:
                grading_scale_keys = current_grading_scale_keys
            elif grading_scale_keys != current_grading_scale_keys:
                is_grading_scale_consistent = False

            # Collect grades for each model from the recipe's evaluation summary
            for evaluation in recipe["evaluation_summary"]:
                model_id = evaluation["model_id"]
                grade = evaluation["grade"]
                recipe_grades.setdefault(model_id, []).append(grade)

        # Determine the worst grade for each model based on the grading scale
        for model_id, grades in recipe_grades.items():
            overall_grade = "-"
            if is_grading_scale_consistent:
                overall_grade = self._get_worst_grade(grading_scale_keys, grades)

            # Append the overall evaluation summary for the model to the cookbook dictionary
            cookbook_dict["overall_evaluation_summary"].append(
                {"model_id": model_id, "overall_grade": overall_grade}
            )

    def _get_worst_grade(
        self, grading_scale_keys: list[str] | None, grades: list[str]
    ) -> str:
        """
        Determines the worst grade from a list of grades based on a given grading scale.

        The worst grade is the one with the highest rank in the grading scale, where a higher rank
        means a worse grade. If the grading scale is not provided or a grade is not in the grading scale,
        a placeholder "-" is returned.

        Args:
            grading_scale_keys: A list of grade strings ordered from best to worst,
            or None if no grading scale is provided.

            grades: A list of grade strings to evaluate.

        Returns:
            The worst grade string from the list of grades, or "-" if the grading scale is None
            or a grade is not found in the grading scale.
        """
        if grading_scale_keys is None:
            return "-"  # Return placeholder if grading scale is None

        # Create a reverse mapping from grade to its rank (0 is best, the last index is worst)
        grade_rank = {grade: rank for rank, grade in enumerate(grading_scale_keys)}

        # Validate that all results are in the grading scale
        for grade in grades:
            if grade not in grade_rank:
                return "-"  # Return placeholder if grade is not in the grading scale

        # Initialize the worst grade with the first result
        worst_grade = grades[0]

        # Iterate through the results to find the worst grade
        for grade in grades:
            if grade_rank[grade] > grade_rank[worst_grade]:
                worst_grade = grade

        return worst_grade

    def _generate_recipes_result(self, recipes: list[str], results: dict) -> list:
        """
        Generates a list of dictionaries containing formatted results for each recipe.

        This method processes the raw results for each recipe, extracts unique sets of endpoints,
        datasets, and prompt templates, initializes a dictionary for recipe details, and populates
        it with details and summary information.

        Args:
            recipes: A list of recipe identifiers.
            results: A dictionary containing raw results keyed by recipe identifiers.

        Returns:
            A list of dictionaries, each representing the formatted results for a recipe.
        """
        formatted_results = []
        for recipe in recipes:
            recipe_results = results.get(recipe, {})
            recipe_grading_scale = Recipe.load(recipe).grading_scale
            (
                unique_endpoints,
                unique_datasets,
                unique_prompt_templates,
            ) = self._get_unique_sets(recipe_results)

            recipe_dict = self._initialize_recipe_dict(recipe, recipe_grading_scale)
            self._populate_recipe_details_and_summary(
                recipe_dict,
                recipe,
                unique_endpoints,
                unique_datasets,
                unique_prompt_templates,
                recipe_results,
                recipe_grading_scale,
            )

            formatted_results.append(recipe_dict)
        return formatted_results

    def _get_unique_sets(
        self, recipe_results: dict
    ) -> tuple[set[str], set[str], set[str]]:
        """
        Extracts unique endpoints, datasets, and prompt templates from the recipe results.

        This method iterates over the keys of the recipe results dictionary, which are tuples
        containing the endpoint, dataset, and prompt template identifiers. It collects unique
        values for each of these identifiers and returns them as sets.

        Args:
            recipe_results: A dictionary with keys as tuples containing identifiers for endpoints,
                            datasets, and prompt templates, and values as the corresponding results.

        Returns:
            A tuple containing three sets: unique endpoints, unique datasets, and unique prompt templates.
        """
        unique_endpoints = set()
        unique_datasets = set()
        unique_prompt_templates = set()
        for key_ep, _, key_ds, key_pt in recipe_results.keys():
            unique_endpoints.add(key_ep)
            unique_datasets.add(key_ds)
            unique_prompt_templates.add(key_pt)
        return unique_endpoints, unique_datasets, unique_prompt_templates

    def _initialize_recipe_dict(self, recipe: str, recipe_grading_scale: dict) -> dict:
        """
        Initializes a dictionary to store details and evaluation summary for a recipe.

        This method creates a dictionary with the recipe identifier, an empty list for details,
        an empty list for evaluation summary, the grading scale for the recipe, and initializes
        the total number of prompts to zero.

        Args:
            recipe: The identifier of the recipe.
            recipe_grading_scale: A dictionary representing the grading scale of the recipe.

        Returns:
            A dictionary with keys 'id', 'details', 'evaluation_summary', 'grading_scale',
            and 'total_num_of_prompts', initialized for storing recipe results.
        """
        return {
            "id": recipe,
            "details": [],
            "evaluation_summary": [],
            "grading_scale": recipe_grading_scale,
            "total_num_of_prompts": 0,
        }

    def _populate_recipe_details_and_summary(
        self,
        recipe_dict: dict,
        recipe: str,
        unique_endpoints: set[str],
        unique_datasets: set[str],
        unique_prompt_templates: set[str],
        recipe_results: dict,
        recipe_grading_scale: dict,
    ) -> None:
        """
        Populates the recipe dictionary with details and summary information for each endpoint.

        This method processes each unique endpoint to calculate the number of prompts and average grade value.
        It updates the total number of prompts in the recipe dictionary and appends an evaluation summary
        for each endpoint, including its identifier, number of prompts, average grade value, and determined grade.

        Args:
            recipe_dict: A dictionary representing a recipe to be populated with details and summary.
            recipe: The identifier of the recipe.
            unique_endpoints: A set of unique endpoint identifiers.
            unique_datasets: A set of unique dataset identifiers.
            unique_prompt_templates: A set of unique prompt template identifiers.
            recipe_results: A dictionary containing the results keyed by a tuple of endpoint, recipe,
                            dataset, and prompt template identifiers.
            recipe_grading_scale: A dictionary representing the grading scale of the recipe.
        """
        for ep in unique_endpoints:
            (
                ep_num_of_prompts,
                ep_avg_grade_value,
            ) = self._calculate_prompts_and_grades(
                ep,
                recipe,
                unique_datasets,
                unique_prompt_templates,
                recipe_results,
                recipe_dict,
            )
            recipe_dict["total_num_of_prompts"] += ep_num_of_prompts
            evaluation_summary_dict = {
                "model_id": ep,
                "num_of_prompts": ep_num_of_prompts,
                "avg_grade_value": ep_avg_grade_value,
                "grade": self._determine_grade(
                    ep_avg_grade_value, recipe_grading_scale
                ),
            }
            recipe_dict["evaluation_summary"].append(evaluation_summary_dict)

    def _calculate_prompts_and_grades(
        self,
        ep: str,
        recipe: str,
        unique_datasets: set,
        unique_prompt_templates: set,
        recipe_results: dict,
        recipe_dict: dict,
    ) -> tuple[int, float | None]:
        """
        Calculates the total number of prompts and the average grade value for a given endpoint.

        This method iterates over all unique datasets and prompt templates, compiles details for each
        combination, and aggregates the total number of prompts and their corresponding grade values.
        It then computes the average grade value across all datasets and prompt templates for the endpoint.

        Args:
            ep: The identifier of the model endpoint.
            recipe: The identifier of the recipe.
            unique_datasets: A set of unique dataset identifiers.
            unique_prompt_templates: A set of unique prompt template identifiers.
            recipe_results: A dictionary containing the results keyed by a tuple of endpoint, recipe,
                            dataset, and prompt template identifiers.
            recipe_dict: A dictionary to which the prompt details will be appended.

        Returns:
            A tuple containing the total number of prompts and the average grade value for the endpoint.
            The average grade value is None if there are no grade values or if any are None.
        """
        ep_num_of_prompts = 0
        ep_total_grade_value_list = []
        for ds in unique_datasets:
            for pt in unique_prompt_templates:
                key = (ep, recipe, ds, pt)
                if key in recipe_results:
                    pt_dict = {
                        "model_id": ep,
                        "dataset_id": ds,
                        "prompt_template_id": pt,
                        "data": recipe_results[key]["data"],
                        "metrics": recipe_results[key]["results"],
                    }
                    recipe_dict["details"].append(pt_dict)

                    # Add the number of prompts and total grade value
                    ep_num_of_prompts += len(pt_dict["data"])
                    ep_total_grade_value_list.append(
                        self._get_grading_criteria_value(pt_dict["metrics"])
                    )

        # calculate the average grade value
        total_num_of_pt_dict = len(unique_datasets) * len(unique_prompt_templates)
        if any(value is None for value in ep_total_grade_value_list):
            # has None values
            ep_avg_grade_value = None
        elif ep_total_grade_value_list:
            # no None values
            ep_avg_grade_value = sum(ep_total_grade_value_list) / total_num_of_pt_dict
        else:
            # Empty list
            ep_avg_grade_value = None
        return ep_num_of_prompts, ep_avg_grade_value

    def _get_grading_criteria_value(self, metrics: list[dict]) -> float | None:
        """
        Extracts the grading criteria value from the first entry in the metrics list.

        This method retrieves the grading criteria value, which is expected to be the first value
        in the grading criteria dictionary contained within the first dictionary of the metrics list.

        Args:
            metrics: A list of dictionaries, each containing a 'grading_criteria' key with a dictionary value.

        Returns:
            The first grading criteria value as a float if available, otherwise None.

        Raises:
            RuntimeError: If the metrics list is empty or the grading criteria is missing or invalid.
        """
        if not metrics:
            raise RuntimeError("[BenchmarkingResult] 'metrics' is empty.")
        grading_criteria_dict = metrics[0].get("grading_criteria")
        if grading_criteria_dict is None or not isinstance(grading_criteria_dict, dict):
            raise RuntimeError(
                f"[BenchmarkingResult] Missing or invalid 'grading_criteria' in metrics: {metrics}"
            )
        # Retrieve the first value from the grading_criteria dictionary
        grading_criteria_value = next(iter(grading_criteria_dict.values()), None)
        return grading_criteria_value

    def _determine_grade(
        self, average_grade: float | None, grading_scale: dict
    ) -> str | None:
        """
        Determines the grade based on the average grade and a given grading scale.

        This method compares the average grade against the grading scale ranges to find the corresponding grade.
        If the average grade is None or does not fit within any range of the grading scale, the method returns None.

        Args:
            average_grade (float | None): The average grade to be evaluated against the grading scale.
            grading_scale (dict): A dictionary where keys are grade strings and values are tuples representing
                                  the lower and upper bounds of the grade range (inclusive).

        Returns:
            str | None: The grade string if the average grade falls within a range in the grading scale, otherwise None.
        """
        # If the average grade is None, immediately return None
        if average_grade is None:
            return None

        # Iterate through the grading scale to find where the average grade fits
        average_grade_int = int(average_grade)
        for grade, (lower_bound, upper_bound) in grading_scale.items():
            if lower_bound <= average_grade_int <= upper_bound:
                return grade

        # If the average grade does not fit any range in the grading scale, return None
        return None
