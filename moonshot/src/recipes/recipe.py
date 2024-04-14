from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
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

    @classmethod
    def load(cls, rec_id: str) -> Recipe:
        """
        Loads a recipe from a JSON file.

        This method uses the provided recipe ID to construct the file path to the JSON file in the designated
        recipe directory.
        It then reads the JSON file and returns the recipe information as a Recipe instance.

        Args:
            rec_id (str): The unique identifier of the recipe.

        Returns:
            Recipe: An instance of the Recipe class populated with the loaded recipe information.
        """
        rec_info = Storage.read_object(EnvVariables.RECIPES.name, rec_id, "json")
        return cls(RecipeArguments(**rec_info))

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
        Retrieves a recipe's details.

        This method accepts a recipe ID, reads the corresponding JSON file from the directory defined by
        `EnvironmentVars.RECIPES`, and returns a RecipeArguments object that encapsulates the recipe's details.

        Args:
            rec_id (str): The unique identifier of the recipe.

        Returns:
            RecipeArguments: An object encapsulating the recipe's details.

        Raises:
            Exception: If an error occurs during the file reading process or any other operation within the method.
        """
        try:
            obj_results = Storage.read_object(EnvVariables.RECIPES.name, rec_id, "json")
            if obj_results:
                return RecipeArguments(**obj_results)
            else:
                raise RuntimeError(f"Unable to get results for {rec_id}.")

        except Exception as e:
            print(f"Failed to read recipe: {str(e)}")
            raise e

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
        Fetches all available recipes.

        This method scans the directory defined by `EnvironmentVars.RECIPES` and collects all stored recipe files.
        It excludes any files that contain "__" in their names. For each valid recipe file, the method reads the file
        content and creates a RecipeArguments object encapsulating the recipe's details.
        Both the RecipeArguments object and the recipe ID are then appended to their respective lists.

        Returns:
            tuple[list[str], list[RecipeArguments]]: A tuple where the first element is a list of recipe IDs and
            the second element is a list of RecipeArguments objects representing the details of each recipe.

        Raises:
            Exception: If an error is encountered during the file reading process or any other operation within
            the method.
        """
        try:
            retn_recs = []
            retn_recs_ids = []

            recs = Storage.get_objects(EnvVariables.RECIPES.name, "json")
            for rec in recs:
                if "__" in rec:
                    continue

                rec_info = RecipeArguments(
                    **Storage.read_object(
                        EnvVariables.RECIPES.name, Path(rec).stem, "json"
                    )
                )
                retn_recs.append(rec_info)
                retn_recs_ids.append(rec_info.id)

            return retn_recs_ids, retn_recs

        except Exception as e:
            print(f"Failed to get available recipes: {str(e)}")
            raise e
