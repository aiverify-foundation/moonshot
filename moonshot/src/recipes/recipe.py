from __future__ import annotations

from pathlib import Path

from pydantic import validate_call
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.datasets.dataset import Dataset
from moonshot.src.recipes.recipe_arguments import RecipeArguments
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Recipe:
    def __init__(self, rec_args: RecipeArguments) -> None:
        self.id = rec_args.id
        self.name = rec_args.name
        self.description = rec_args.description
        self.tags = rec_args.tags
        self.categories = rec_args.categories
        self.datasets = rec_args.datasets
        self.prompt_templates = rec_args.prompt_templates
        self.metrics = rec_args.metrics
        self.grading_scale = rec_args.grading_scale
        self.stats = rec_args.stats

    @classmethod
    def load(cls, rec_id: str) -> Recipe:
        """
        Loads a recipe from persistent storage.

        This method constructs the file path for the recipe's JSON file using the provided recipe ID and the
        predefined recipe directory. It reads the JSON file, deserializes the recipe data, and instantiates a Recipe
        object with the loaded data.

        Args:
            rec_id (str): The unique identifier for the recipe to be loaded.

        Returns:
            Recipe: A Recipe object populated with the data from the recipe's JSON file.
        """
        return cls(Recipe.read(rec_id))

    @staticmethod
    def create(rec_args: RecipeArguments) -> str:
        """
        Creates a new recipe and saves its details in a JSON file.

        This method uses the `rec_args` parameter to generate a unique recipe ID by slugifying the recipe name.
        It then builds a dictionary with the recipe's details and writes this information to a JSON file.
        The JSON file is named after the recipe ID and is stored in the directory specified by
        `EnvironmentVars.RECIPES`.
        If any error occurs during the process, an exception is thrown and the error message is printed.

        Args:
            rec_args (RecipeArguments): An object that holds the necessary details to create a new recipe.

        Returns:
            str: The unique ID of the newly created recipe.

        Raises:
            Exception: If an error occurs during the file writing process or any other operation within the method.
        """
        try:
            rec_id = slugify(rec_args.name, lowercase=True)
            rec_info = {
                "name": rec_args.name,
                "description": rec_args.description,
                "tags": rec_args.tags,
                "categories": rec_args.categories,
                "datasets": rec_args.datasets,
                "prompt_templates": rec_args.prompt_templates,
                "metrics": rec_args.metrics,
                "grading_scale": rec_args.grading_scale,
            }

            # check if the recipe exists
            if Storage.is_object_exists(EnvVariables.RECIPES.name, rec_id, "json"):
                raise RuntimeError(f"Recipe with ID '{rec_id}' already exists.")

            Recipe.check_file_exists(
                EnvVariables.PROMPT_TEMPLATES.name,
                rec_args.prompt_templates,
                "Prompt Template",
                "json",
            )
            Recipe.check_file_exists(
                EnvVariables.DATASETS.name, rec_args.datasets, "Dataset", "json"
            )
            Recipe.check_file_exists(
                EnvVariables.METRICS.name, rec_args.metrics, "Metric", "py"
            )

            # Write as json output
            Storage.create_object(EnvVariables.RECIPES.name, rec_id, rec_info, "json")
            return rec_id

        except Exception as e:
            logger.error(f"Failed to create recipe: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def read(rec_id: str) -> RecipeArguments:
        """
        Retrieves the details of a specific recipe.

        This static method takes a recipe ID as input, locates the corresponding JSON file within the directory
        specified by `EnvironmentVars.RECIPES`, and constructs a RecipeArguments object that contains the details
        of the recipe.

        Args:
            rec_id (str): The unique identifier for the recipe to be retrieved.

        Returns:
            RecipeArguments: A populated object with the recipe's details.

        Raises:
            Exception: If there is an issue reading the file or during any other part of the process.
        """
        try:
            if not rec_id:
                raise RuntimeError("Recipe ID is empty.")

            recipe_details = Recipe._read_recipe(rec_id, {})
            if not recipe_details:
                raise RuntimeError(f"Recipe with ID '{rec_id}' does not exist.")

            return RecipeArguments(**recipe_details)

        except Exception as e:
            logger.error(f"Failed to read recipe: {str(e)}")
            raise e

    @staticmethod
    def _get_datasets_prompt_counts() -> dict:
        """
        Generates a mapping of dataset IDs to their number of prompts.

        This method reads the cache information from the storage, which contains the number of prompts for each dataset.
        It then creates a dictionary mapping each dataset ID to the corresponding number of prompts.

        Returns:
            dict: A dictionary where keys are dataset IDs and values are the number of prompts for that dataset.
        """
        # Calculate statistics for the recipe and update the results dictionary with them
        _, dataset_results = Dataset.get_available_items()
        # Create a mapping of dataset IDs to their number of prompts
        return {
            dataset.id: dataset.num_of_dataset_prompts for dataset in dataset_results
        }

    @staticmethod
    def _read_recipe(rec_id: str, dataset_prompts_count: dict) -> dict:
        """
        Reads the recipe JSON file based on the provided recipe ID and dataset prompts count
        and returns the recipe information as a dictionary.

        Args:
            rec_id (str): The unique identifier for the recipe.
            dataset_prompts_count (dict): A dictionary mapping dataset IDs to their number of prompts.

        Returns:
            dict: A dictionary containing the recipe information.

        Raises:
            RuntimeError: If the recipe file cannot be read or does not exist.
        """
        obj_results = {"id": rec_id}
        recipe_info = Storage.read_object(EnvVariables.RECIPES.name, rec_id, "json")
        if not recipe_info:
            raise RuntimeError(f"Unable to get results for {rec_id}.")
        else:
            obj_results.update(recipe_info)

        # Calculate statistics for the recipe and update the results dictionary with them
        stats = {
            "num_of_tags": len(obj_results["tags"]),
            "num_of_datasets": len(obj_results["datasets"]),
            "num_of_prompt_templates": len(obj_results["prompt_templates"]),
            "num_of_metrics": len(obj_results["metrics"]),
            "num_of_datasets_prompts": {},
        }

        if dataset_prompts_count:
            stats["num_of_datasets_prompts"] = {
                dataset_name: dataset_prompts_count.get(dataset_name, 0)
                for dataset_name in obj_results["datasets"]
            }
        else:
            _, datasets_metadata = Dataset.get_available_items(obj_results["datasets"])
            stats["num_of_datasets_prompts"] = {
                dataset.id: dataset.num_of_dataset_prompts
                for dataset in datasets_metadata
            }

        obj_results["stats"] = stats
        return obj_results

    @staticmethod
    def update(rec_args: RecipeArguments) -> bool:
        """
        Updates the recipe information in the storage based on the provided RecipeArguments object.

        This method processes an instance of RecipeArguments, transforming it into a dictionary format. It ensures
        that certain required files exist before proceeding to update the recipe information in the storage system.
        Upon successful update, it returns True. If any error is encountered during the process, the error message is
        logged, and the exception is propagated upwards.

        Args:
            rec_args (RecipeArguments): An object containing the updated recipe information.

        Returns:
            bool: Indicates whether the recipe update was successful (True) or not (False).

        Raises:
            Exception: Propagates any exceptions that occur during the update process.
        """
        try:
            # Transform RecipeArguments into a dictionary, excluding the 'id' field
            rec_info = rec_args.to_dict()
            rec_info.pop("id", None)  # The 'id' is derived and should not be written

            # Verify existence of related files in storage
            Recipe.check_file_exists(
                EnvVariables.PROMPT_TEMPLATES.name,
                rec_args.prompt_templates,
                "Prompt Template",
                "json",
            )
            Recipe.check_file_exists(
                EnvVariables.DATASETS.name, rec_args.datasets, "Dataset", "json"
            )
            Recipe.check_file_exists(
                EnvVariables.METRICS.name, rec_args.metrics, "Metric", "py"
            )

            # Persist the updated recipe information to storage
            Storage.create_object(
                EnvVariables.RECIPES.name, rec_args.id, rec_info, "json"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to update recipe: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def delete(rec_id: str) -> bool:
        """
        Deletes a recipe identified by its unique ID.

        This method attempts to delete the recipe with the given ID from the storage.
        If the deletion is successful, it returns True. If an exception occurs during the deletion
        process, it prints an error message and re-raises the exception.

        Args:
            rec_id (str): The unique identifier of the recipe to be deleted.

        Returns:
            bool: True if the recipe was successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.RECIPES.name, rec_id, "json")
            return True

        except Exception as e:
            logger.error(f"Failed to delete recipe: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[RecipeArguments]]:
        """
        Retrieves a list of available recipe IDs and their corresponding recipe information.

        This method queries the storage for all available recipes and filters out any system files or directories.
        It then creates a list of RecipeArguments objects with detailed information about each recipe and a list of
        their IDs. Finally, it returns a tuple containing the list of recipe IDs and the list of RecipeArguments
        objects.

        Returns:
            tuple[list[str], list[RecipeArguments]]: A tuple containing a list of recipe IDs and a list of
                                                      RecipeArguments objects for each available recipe.

        Raises:
            Exception: If there's an error during the retrieval process.
        """
        try:
            retn_recs = []
            retn_recs_ids = []

            datasets_prompt_counts = Recipe._get_datasets_prompt_counts()
            recs = Storage.get_objects(EnvVariables.RECIPES.name, "json")
            for rec in recs:
                if "__" in rec:
                    continue

                rec_info = RecipeArguments(
                    **Recipe._read_recipe(Path(rec).stem, datasets_prompt_counts)
                )
                retn_recs.append(rec_info)
                retn_recs_ids.append(rec_info.id)

            return retn_recs_ids, retn_recs

        except Exception as e:
            logger.error(f"Failed to get available recipes: {str(e)}")
            raise e

    @staticmethod
    def check_file_exists(
        env_var_name: str, file_list: list, file_type: str, extension: str
    ) -> None:
        """
        Checks if a specified file exists in the storage.

        Args:
            env_var_name (str): The environment variable name where the file is stored.
            file_name (str): The name of the file to check.
            file_type (str): The type of the file.
            extension (str): The extension of the file.

        Raises:
            RuntimeError: If the file does not exist in the storage.
        """
        for file_name in file_list:
            if file_name and not Storage.is_object_exists(
                env_var_name, file_name, extension
            ):
                raise RuntimeError(f"[Recipe] {file_type} {file_name} does not exist.")
