from ast import literal_eval

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from moonshot.src.api.api_cookbook import api_read_cookbooks
from moonshot.src.api.api_recipe import api_read_recipes
from moonshot.src.api.api_result import api_read_result
from moonshot.src.report_analysis.report_analysis_interface import (
    ReportAnalysisInterface,
)
from moonshot.src.utils.timeit import timeit


class ResultsComparator(ReportAnalysisInterface):
    # JSON schema as a class variable
    output_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "ResultsComparatorOutput",
        "description": "Schema for the output of ResultsComparator",
        "type": "object",
        "properties": {
            "id": {
                "description": "The identifier of the results comparator.",
                "type": "string",
            },
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cookbook_id": {
                            "description": (
                                "The identifier of the cookbook, if applicable. '-' indicates not applicable."
                            ),
                            "type": "string",
                        },
                        "recipe_id": {
                            "description": "The identifier of the recipe.",
                            "type": "string",
                        },
                        "dataset_id": {
                            "description": "The identifier of the dataset used.",
                            "type": "string",
                        },
                        "prompt_template": {
                            "description": "The identifier of the prompt template used.",
                            "type": "string",
                        },
                        "result_id": {
                            "description": "The identifier of the result.",
                            "type": "string",
                        },
                        "endpoint_id": {
                            "description": "The identifier of the endpoint.",
                            "type": "string",
                        },
                        "metrics": {
                            "description": "The metrics obtained from the result, in JSON string format.",
                            "type": "string",
                        },
                    },
                    "required": [
                        "cookbook_id",
                        "recipe_id",
                        "dataset_id",
                        "prompt_template",
                        "result_id",
                        "endpoint_id",
                        "metrics",
                    ],
                },
            },
        },
        "required": ["id", "results"],
    }

    def __init__(self):
        self.id = "results-comparator"
        self.name = "ResultsComparator"
        self.description = "Allows for comparison of benchmarking results across runs for specific models"
        self.version = "0.1.0"
        self.required_arguments = {
            "result_ids": "The result ids to be compared",
            "endpoint_ids": "The endpoint ids to be compared",
        }

    @timeit
    def validate_output(self, output: dict) -> bool:
        """
        Validates the given output against the defined JSON schema.

        Args:
            output (dict): The output data to validate.

        Returns:
            bool: True if the output is valid, False otherwise.
        """
        try:
            validate(instance=output, schema=self.output_schema)
            return True
        except ValidationError as e:
            print(f"Validation Error: {e}")
            return False

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the ResultsComparator class,
        including its name, description, version, and required arguments.

        Returns:
            dict: A dictionary with the metadata of the ResultsComparator class,
            encompassing 'name', 'description', 'version', and 'required_arguments'.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "required_arguments": self.required_arguments,
        }

    @timeit
    def generate_analysis(self, ra_args: dict) -> dict | None:
        """
        Generates an analysis based on the provided arguments for the ResultsComparator class.
        This method requires two specific arguments: "result_ids" and "endpoint_ids".
        It begins by verifying the presence of these required arguments within the provided dictionary.
        If confirmed, it proceeds to extract these arguments.

        For each "result_id" specified, the method invokes external functions to fetch corresponding runner
        and result information. This information is then compiled into a dictionary, keyed by "result_id",
        which collectively forms the analysis output.

        Args:
            ra_args (dict): A dictionary containing the arguments for analysis. Must include "result_ids" and
            "endpoint_ids" for successful execution.

        Returns:
            dict: A compilation of runner and result information for each specified "result_id".
            Each entry is keyed by "result_id".

        Raises:
            RuntimeError: Thrown if either "result_ids" or "endpoint_ids" are missing from the provided arguments.
        """
        # ------------------ PART 1 ------------------
        # Get required arguments
        if ra_args.get("result_ids") and ra_args.get("endpoint_ids"):
            result_ids = ra_args["result_ids"]
            endpoint_ids = ra_args["endpoint_ids"]
        else:
            raise RuntimeError("[ResultsComparator] Failed to get required arguments.")

        # ------------------ PART 2 ------------------
        # Gather all the runner and result information for results and
        # Gather how many cookbooks and recipes are there in total and format in dict for output
        overall_extracted_results = {}
        overall_possible_results = {}
        for result_id in result_ids:
            result_info = api_read_result(result_id)
            overall_possible_results.update(
                self.get_possible_results(result_info, endpoint_ids)
            )
            overall_extracted_results.update(
                self.extract_results_based_on_endpoint(result_info, endpoint_ids)
            )

        # ------------------ PART 3 ------------------
        # Update overall_extracted_results -> overall_possible_results
        # Sort the keys
        for key in overall_extracted_results:
            if key in overall_possible_results:
                overall_possible_results[key] = overall_extracted_results[key]

        # Sort the keys of the dictionary
        sorted_keys = sorted(overall_possible_results.keys())

        # ------------------ PART 4 ------------------
        # Output overall_possible_results in JSON format
        response_dict = {"id": self.id, "results": []}
        for key in sorted_keys:
            (
                cookbook_id,
                recipe_id,
                dataset_id,
                prompt_template,
                result_id,
                endpoint_id,
            ) = literal_eval(key)
            response_dict["results"].append(
                {
                    "cookbook_id": cookbook_id,
                    "recipe_id": recipe_id,
                    "dataset_id": dataset_id,
                    "prompt_template": prompt_template,
                    "result_id": result_id,
                    "endpoint_id": endpoint_id,
                    "metrics": overall_possible_results[key],
                }
            )

        # ------------------ PART 5 ------------------
        # Validate that the output dict passes json schema validation
        if self.validate_output(response_dict):
            return response_dict
        else:
            raise RuntimeError(
                "[ResultsComparator] Failed json schema validation for output response."
            )

    def get_possible_results(self, result_info: dict, endpoint_ids: list) -> dict:
        """
        Extracts possible results from given result information and endpoint IDs.

        This method processes the result information to determine if the runner is a cookbook or a recipe. Based on the
        type, it iterates through the relevant data structures to compile a dictionary of possible results. Each key in
        the dictionary is a string representation of a tuple containing identifiers for the cookbook (if applicable),
        recipe, dataset, prompt template, result, and endpoint. The value for each key is a placeholder, indicating the
        structure for potential results.

        Args:
            result_info (dict): A dictionary containing metadata about the result, including whether it pertains to a
                                cookbook or a recipe, and the relevant identifiers.
            endpoint_ids (list): A list of endpoint IDs for which to extract possible results.

        Returns:
            dict: A dictionary where each key is a unique identifier tuple converted to a string, and each value is a
                  placeholder. This dictionary represents all possible results given the input parameters.
        """
        # Check if runner is a cookbook or a recipe
        if result_info["metadata"]["recipes"]:
            # Get possible result as a recipe
            possible_result_dict = {}
            for recipe_info in api_read_recipes(result_info["metadata"]["recipes"]):
                for dataset in recipe_info["datasets"]:
                    for prompt_template in recipe_info["prompt_templates"]:
                        for endpoint_id in endpoint_ids:
                            possible_result_dict.update(
                                {
                                    str(
                                        (
                                            "-",
                                            recipe_info["id"],
                                            dataset,
                                            prompt_template,
                                            result_info["metadata"]["id"],
                                            endpoint_id,
                                        )
                                    ): "-"
                                }
                            )
            return possible_result_dict

        elif result_info["metadata"]["cookbooks"]:
            # Process result as a cookbook
            possible_result_dict = {}
            for cookbook_info in api_read_cookbooks(
                result_info["metadata"]["cookbooks"]
            ):
                for recipe_info in api_read_recipes(cookbook_info["recipes"]):
                    for dataset in recipe_info["datasets"]:
                        for prompt_template in recipe_info["prompt_templates"]:
                            for endpoint_id in endpoint_ids:
                                possible_result_dict.update(
                                    {
                                        str(
                                            (
                                                cookbook_info["id"],
                                                recipe_info["id"],
                                                dataset,
                                                prompt_template,
                                                result_info["metadata"]["id"],
                                                endpoint_id,
                                            )
                                        ): "-"
                                    }
                                )
            return possible_result_dict

        else:
            # Unknown runner type
            raise RuntimeError("[ResultsComparator] Failed to identify runner type.")

    def extract_results_based_on_endpoint(
        self, result_info: dict, endpoint_ids: list
    ) -> dict:
        """
        This function extracts the results from the provided result_info based on the specified endpoint_ids.
        It initially determines if the result_info includes any recipes. If present, it processes these as recipes by
        calling the _extract_result_recipe function.

        In the absence of recipes within result_info, the function then checks for the presence of cookbooks.
        If found, it processes these as cookbooks by calling the _extract_result_cookbook function.
        Should the result_info lack both recipes and cookbooks, a RuntimeError is raised to indicate the inability
        to process the input.

        Args:
            result_info (dict): The dictionary containing information about the results.
            endpoint_ids (list): The list of endpoint identifiers for which results are to be extracted.

        Returns:
            dict: A dictionary where each key is a tuple representing the identifiers of the extracted results,
            and each value is the corresponding result metrics.

        Raises:
            RuntimeError: Raised if the result_info does not include any identifiable recipes or cookbooks.
        """
        # Check if runner is a cookbook or a recipe
        if result_info["metadata"]["recipes"]:
            # Process result as a recipe
            return self._extract_result_recipe(
                result_info["metadata"]["id"],
                result_info["results"]["recipes"],
                endpoint_ids,
            )

        elif result_info["metadata"]["cookbooks"]:
            # Process result as a cookbook
            return self._extract_result_cookbook(
                result_info["metadata"]["id"],
                result_info["results"]["cookbooks"],
                endpoint_ids,
            )

        else:
            # Unknown runner type
            raise RuntimeError("[ResultsComparator] Failed to identify runner type.")

    def _extract_result_recipe(
        self, result_id: str, recipe_results: dict, endpoint_ids: list
    ) -> dict:
        """
        Extracts results from a recipe execution based on specified endpoint IDs.
        It iterates through the given recipe results, filtering for models that match the provided endpoint IDs.
        For each matching model, it traverses the datasets and prompt templates, constructing a dictionary with keys as
        tuples comprising a placeholder for cookbook ID (indicated by "-"), recipe ID, dataset ID, prompt template ID,
        result ID, model ID, and values as the corresponding metrics.

        Args:
            result_id (str): The unique identifier of the result.
            recipe_results (dict): A dictionary containing the results of the recipe execution, structured by model,
            dataset, and prompt template.
            endpoint_ids (list): A list of model endpoint identifiers to filter the results by.

        Returns:
            dict: A dictionary with keys as tuples of identifiers (cookbook placeholder, recipe ID, dataset ID,
            prompt template ID, result ID, model ID) and values as the metrics associated with each identifier set.
        """
        extracted_result_dict = {}
        for recipe in recipe_results:
            for recipe_model in [
                model for model in recipe["models"] if model["id"] in endpoint_ids
            ]:
                for dataset in recipe_model["datasets"]:
                    for prompt_template in dataset["prompt_templates"]:
                        extracted_result_dict.update(
                            {
                                str(
                                    (
                                        "-",
                                        recipe["id"],
                                        dataset["id"],
                                        prompt_template["id"],
                                        result_id,
                                        recipe_model["id"],
                                    )
                                ): str(prompt_template["metrics"])
                            }
                        )
        return extracted_result_dict

    def _extract_result_cookbook(
        self, result_id: str, cookbook_results: dict, endpoint_ids: list
    ) -> dict:
        """
        Extracts and organizes results from a cookbook execution, focusing on specified model endpoints.
        This method navigates through each cookbook in the provided cookbook_results, delving into each recipe
        contained within those cookbooks.

        It specifically targets recipes that include models identified by the endpoint_ids.
        Within these recipes, the method iterates over the datasets and prompt_templates, compiling a dictionary.
        The keys of this dictionary are tuples that encapsulate the cookbook ID, recipe ID, dataset ID,
        prompt_template ID, result_id, and model ID.

        The values correspond to the metrics associated with these identifiers.
        The resulting dictionary, which neatly organizes the extracted results, is then returned.

        Args:
            result_id (str): The unique identifier for the analysis result.
            cookbook_results (dict): A dictionary containing the execution results of the cookbook,
            structured by cookbook and recipe.
            endpoint_ids (list): A list of model endpoint identifiers, used to filter the results that are extracted.

        Returns:
            dict: A structured dictionary where each key is a tuple of identifiers
            (cookbook ID, recipe ID, dataset ID, prompt_template ID, result_id, model ID) and
            each value is the associated metrics.
        """
        extracted_result_dict = {}
        for cookbook in cookbook_results:
            for recipe in cookbook["recipes"]:
                for recipe_model in [
                    model for model in recipe["models"] if model["id"] in endpoint_ids
                ]:
                    for dataset in recipe_model["datasets"]:
                        for prompt_template in dataset["prompt_templates"]:
                            extracted_result_dict.update(
                                {
                                    str(
                                        (
                                            cookbook["id"],
                                            recipe["id"],
                                            dataset["id"],
                                            prompt_template["id"],
                                            result_id,
                                            recipe_model["id"],
                                        )
                                    ): str(prompt_template["metrics"])
                                }
                            )
        return extracted_result_dict
