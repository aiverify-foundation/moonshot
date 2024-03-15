from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.benchmarking.recipes.recipe_arguments import RecipeArguments
from moonshot.src.storage.storage_manager import StorageManager


class Recipe:
    def __init__(self, rec_args: RecipeArguments) -> None:
        self.id = rec_args.id
        self.name = rec_args.name
        self.description = rec_args.description
        self.tags = rec_args.tags
        self.datasets = rec_args.datasets
        self.prompt_templates = rec_args.prompt_templates
        self.metrics = rec_args.metrics

    @classmethod
    def load_recipe(cls, rec_id: str) -> Recipe:
        """
        Loads a recipe from a JSON file.

        This method reads the recipe information from a JSON file specified by the recipe ID. It constructs
        the file path using the recipe ID and the designated directory for recipes. The method
        then reads the JSON file and returns the recipe information as a dictionary.

        Args:
            rec_id (str): The ID of the recipe.

        Returns:
            Recipe: An instance of the Recipe class with the loaded recipe information.
        """
        rec_info = StorageManager.read_recipe(rec_id)
        return cls(RecipeArguments(**rec_info))

    @staticmethod
    def create_recipe(rec_args: RecipeArguments) -> None:
        """
        Creates a new recipe and stores its information in a JSON file.

        This method takes the arguments provided in the `rec_args` parameter, generates a unique recipe ID by
        slugifying the recipe name, and then constructs a dictionary with the recipe's information. It then
        writes this information to a JSON file named after the recipe ID within the directory specified by
        `EnvironmentVars.RECIPES`. If the operation fails for any reason, an exception is raised
        and the error is printed.

        Args:
            rec_args (RecipeArguments): An object containing the necessary information to create a
            new recipe.

        Raises:
            Exception: If there is an error during file writing or any other operation within the method.
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
            }

            # Write as json output
            StorageManager.create_recipe(rec_id, rec_info)

        except Exception as e:
            print(f"Failed to create recipe: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read_recipe(rec_id: str) -> RecipeArguments:
        """
        Reads a recipe and returns its information.

        This method takes a recipe ID as input, reads the corresponding JSON file from the directory specified by
        `EnvironmentVars.RECIPES`, and returns a RecipeArguments object containing the recipe's information.

        Args:
            rec_id (str): The ID of the recipe.

        Returns:
            RecipeArguments: An object containing the recipe's information.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        try:
            return RecipeArguments(**StorageManager.read_recipe(rec_id))

        except Exception as e:
            print(f"Failed to read recipe: {str(e)}")
            raise e

    @staticmethod
    def update_recipe(rec_args: RecipeArguments) -> None:
        """
        Updates an existing recipe with new information.

        This method takes a RecipeArguments object as input, which contains the new information for the
        recipe. It directly updates the existing recipe file with the new information. If the operation fails
        for any reason, an exception is raised and the error is printed.

        Args:
            rec_args (RecipeArguments): An object containing the new information for the recipe.

        Raises:
            Exception: If there is an error during the update operation.
        """
        try:
            # Convert the recipe arguments to a dictionary
            rec_info = rec_args.to_dict()

            # Write the updated recipe information to the file
            StorageManager.create_recipe(rec_args.id, rec_info)

        except Exception as e:
            print(f"Failed to update recipe: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete_recipe(rec_id: str) -> None:
        """
        Deletes a recipe.

        This method takes a recipe ID as input, deletes the corresponding JSON file from the directory specified by
        `EnvironmentVars.RECIPES`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            rec_id (str): The ID of the recipe to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        try:
            StorageManager.delete_recipe(rec_id)

        except Exception as e:
            print(f"Failed to delete recipe: {str(e)}")
            raise e

    @staticmethod
    def get_available_recipes() -> tuple[list[str], list[RecipeArguments]]:
        """
        Returns a list of available recipes.

        This method retrieves all the recipes stored in the directory specified by `EnvironmentVars.RECIPES`.
        It ignores any files with "__" in their names. For each valid recipe file, it reads the file and constructs
        a RecipeArguments object with the recipe's information. It then appends the RecipeArguments object and the
        recipe ID to their respective lists.

        Returns:
            tuple[list[str], list[RecipeArguments]]: A tuple containing a list of recipe IDs and a list of
            RecipeArguments objects.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        try:
            retn_recs = []
            retn_recs_ids = []

            recs = StorageManager.get_recipes()
            for rec in recs:
                if "__" in rec:
                    continue

                rec_info = RecipeArguments(**StorageManager.read_recipe(Path(rec).stem))
                retn_recs.append(rec_info)
                retn_recs_ids.append(rec_info.id)

            return retn_recs_ids, retn_recs

        except Exception as e:
            print(f"Failed to get available recipes: {str(e)}")
            raise e
