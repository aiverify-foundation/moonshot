from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.datasets.dataset import Dataset
from moonshot.src.recipes.recipe_arguments import RecipeArguments
from moonshot.src.storage.storage import Storage


class Recipe:
    def __init__(self, rec_args: RecipeArguments) -> None:
        self.id = rec_args.id
        self.name = rec_args.name
        self.description = rec_args.description
        self.tags = rec_args.tags
        self.datasets = rec_args.datasets
        self.prompt_templates = rec_args.prompt_templates
        self.metrics = rec_args.metrics
        self.attack_modules = rec_args.attack_modules
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
    def create(rec_args: RecipeArguments) -> None:
        """
        Creates a new recipe and saves its details in a JSON file.

        This method uses the `rec_args` parameter to generate a unique recipe ID by slugifying the recipe name.
        It then builds a dictionary with the recipe's details and writes this information to a JSON file.
        The JSON file is named after the recipe ID and is stored in the directory specified by
        `EnvironmentVars.RECIPES`.
        If any error occurs during the process, an exception is thrown and the error message is printed.

        Args:
            rec_args (RecipeArguments): An object that holds the necessary details to create a new recipe.

        Raises:
            Exception: If an error occurs during the file writing process or any other operation within the method.
        """
        try:
            rec_id = slugify(rec_args.name, lowercase=True)
            rec_info = {
                "id": rec_id,
                "name": rec_args.name,
                "description": rec_args.description,
                "tags": rec_args.tags,
                "datasets": rec_args.datasets,
                "prompt_templates": rec_args.prompt_templates,
                "metrics": rec_args.metrics,
                "attack_modules": rec_args.attack_modules,
                "grading_scale": rec_args.grading_scale,
            }

            # Write as json output
            Storage.create_object(EnvVariables.RECIPES.name, rec_id, rec_info, "json")

        except Exception as e:
            print(f"Failed to create recipe: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
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
            return RecipeArguments(**Recipe._read_recipe(rec_id))

        except Exception as e:
            print(f"Failed to read recipe: {str(e)}")
            raise e

    @staticmethod
    def _read_recipe(rec_id: str) -> dict:
        """
        Reads the recipe details from storage and enriches it with statistics.

        This method retrieves the recipe details by its ID and calculates additional statistics such as the number of
        prompts in each dataset and the total number of prompt templates.

        Args:
            rec_id (str): The unique identifier of the recipe to read.

        Returns:
            dict: A dictionary containing the recipe details along with calculated statistics.

        Raises:
            RuntimeError: If the recipe cannot be found or read from storage.
        """
        obj_results = Storage.read_object(EnvVariables.RECIPES.name, rec_id, "json")
        if obj_results:
            # Calculate statistics for the recipe and update the results dictionary with them
            obj_results["stats"] = {
                "num_of_tags": len(obj_results["tags"]),
                "num_of_datasets": len(obj_results["datasets"]),
                "num_of_datasets_prompts": {
                    dataset_name: Dataset.read(dataset_name).num_of_dataset_prompts
                    for dataset_name in obj_results["datasets"]
                },
                "num_of_prompt_templates": len(obj_results["prompt_templates"]),
                "num_of_metrics": len(obj_results["metrics"]),
                "num_of_attack_modules": len(obj_results["attack_modules"]),
            }
            return obj_results
        else:
            raise RuntimeError(f"Unable to get results for {rec_id}.")

    @staticmethod
    def update(rec_args: RecipeArguments) -> None:
        """
        Updates an existing recipe with new details.

        This method accepts a RecipeArguments object, which encapsulates the updated details for the
        recipe. It then overwrites the existing recipe file with these new details. If the operation encounters
        any issues, an exception is thrown and the error message is logged.

        Args:
            rec_args (RecipeArguments): An instance containing the updated details for the recipe.

        Raises:
            Exception: If an error occurs during the update process.
        """
        try:
            # Convert the recipe arguments to a dictionary
            rec_info = rec_args.to_dict()

            # Write the updated recipe information to the file
            Storage.create_object(
                EnvVariables.RECIPES.name, rec_args.id, rec_info, "json"
            )

        except Exception as e:
            print(f"Failed to update recipe: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete(rec_id: str) -> None:
        """
        Deletes a recipe.

        This method accepts a recipe ID as an argument and attempts to delete the corresponding JSON file from the
        directory defined by `EnvironmentVars.RECIPES`. If the operation encounters any issues, an exception is raised
        and the error message is logged.

        Args:
            rec_id (str): The unique identifier of the recipe to be deleted.

        Raises:
            Exception: If an error occurs during the file deletion process or any other operation within the method.
        """
        try:
            Storage.delete_object(EnvVariables.RECIPES.name, rec_id, "json")

        except Exception as e:
            print(f"Failed to delete recipe: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[RecipeArguments]]:
        """
        Retrieves all available recipes.

        This method searches the storage location specified by `EnvVariables.RECIPES` for recipe files, omitting any
        that include "__" in their filenames. It reads the contents of each valid recipe file and constructs a
        RecipeArguments object with the recipe details. The method accumulates the recipe IDs and the corresponding
        RecipeArguments objects into separate lists, which are then returned together as a tuple.

        Returns:
            tuple[list[str], list[RecipeArguments]]: A tuple containing two elements. The first is a list of recipe
            IDs, and the second is a list of RecipeArguments objects, each representing the details of a recipe.

        Raises:
            Exception: If any issues arise during the retrieval and processing of recipe files.
        """
        try:
            retn_recs = []
            retn_recs_ids = []

            recs = Storage.get_objects(EnvVariables.RECIPES.name, "json")
            for rec in recs:
                if "__" in rec:
                    continue

                rec_info = RecipeArguments(**Recipe._read_recipe(Path(rec).stem))
                retn_recs.append(rec_info)
                retn_recs_ids.append(rec_info.id)

            return retn_recs_ids, retn_recs

        except Exception as e:
            print(f"Failed to get available recipes: {str(e)}")
            raise e
