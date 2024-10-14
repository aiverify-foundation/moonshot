from __future__ import annotations

from pathlib import Path

from pydantic import validate_call
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Cookbook:
    def __init__(self, cb_args: CookbookArguments) -> None:
        self.id = cb_args.id
        self.name = cb_args.name
        self.description = cb_args.description
        self.tags = cb_args.tags
        self.categories = cb_args.categories
        self.recipes = cb_args.recipes

    @classmethod
    def load(cls, cb_id: str) -> Cookbook:
        """
        This method loads a cookbook from a JSON file.

        It uses the cookbook ID to construct the file path for the JSON file in the designated cookbook directory.
        The method then reads the JSON file and returns the cookbook information as a Cookbook instance.

        Args:
            cb_id (str): The unique identifier of the cookbook.

        Returns:
            Cookbook: An instance of the Cookbook class populated with the loaded cookbook information.
        """
        return cls(Cookbook.read(cb_id))

    @staticmethod
    def create(cb_args: CookbookArguments) -> str:
        """
        This method is responsible for creating a new cookbook and storing its details in a JSON file.

        The function accepts `cb_args` parameter which contains the necessary details for creating a new cookbook.
        It generates a unique ID for the cookbook by slugifying the cookbook name. After that, it constructs a
        dictionary with the cookbook's details and writes this information to a JSON file. The JSON file is named after
        the cookbook ID and is stored in the directory specified by `EnvironmentVars.COOKBOOKS`.

        If the operation encounters any error, an exception is raised and the error message is printed.

        Args:
            cb_args (CookbookArguments): An object that holds the necessary details for creating a new cookbook.

        Returns:
            str: The unique ID of the newly created cookbook.

        Raises:
            RuntimeError: If any of the recipes specified in the cookbook does not exist.
            Exception: If there is an error during the file writing process or any other operation within the method.
        """
        try:
            cb_id = slugify(cb_args.name, lowercase=True)
            cb_info = {
                "name": cb_args.name,
                "description": cb_args.description,
                "tags": Cookbook.get_tags_in_recipes(cb_args.recipes),
                "categories": Cookbook.get_categories_in_recipes(cb_args.recipes),
                "recipes": cb_args.recipes,
            }

            # check if the cookbook exists
            if Storage.is_object_exists(EnvVariables.COOKBOOKS.name, cb_id, "json"):
                raise RuntimeError(f"Cookbook with ID '{cb_id}' already exists.")

            # check if recipes in list exist before creating cookbook
            for recipe in cb_args.recipes:
                if not Storage.is_object_exists(
                    EnvVariables.RECIPES.name, recipe, "json"
                ):
                    raise RuntimeError(f"{recipe} recipe does not exist.")

            # Write as json output
            Storage.create_object(EnvVariables.COOKBOOKS.name, cb_id, cb_info, "json")
            return cb_id

        except Exception as e:
            logger.error(f"Failed to create cookbook: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def read(cb_id: str) -> CookbookArguments:
        """
        Fetches and returns the details of a specified cookbook by its ID.

        This method takes a cookbook ID, searches for its corresponding JSON file in the directory set by
        `EnvironmentVars.COOKBOOKS`, and constructs a CookbookArguments object with the cookbook's details.

        If the process encounters any issues, such as the file not existing or being inaccessible, it logs the error
        and raises an exception.

        Args:
            cb_id (str): The unique identifier of the cookbook to fetch.

        Returns:
            CookbookArguments: An instance filled with the cookbook's details.

        Raises:
            RuntimeError: If the cookbook ID is empty or the specified cookbook does not exist.
            Exception: For any issues encountered during the file reading or data parsing process.
        """
        try:
            if not cb_id:
                raise RuntimeError("Cookbook ID is empty.")

            cookbook_details = Cookbook._read_cookbook(cb_id)
            if not cookbook_details:
                raise RuntimeError(f"Cookbook with ID '{cb_id}' does not exist.")

            return CookbookArguments(**cookbook_details)

        except Exception as e:
            logger.error(f"Failed to read cookbook: {str(e)}")
            raise

    @staticmethod
    def _read_cookbook(cb_id: str) -> dict:
        """
        Retrieves the cookbook's information from a JSON file.

        This internal method is designed to fetch the details of a specific cookbook by its ID. It searches for the
        corresponding JSON file within the directory specified by `EnvVariables.COOKBOOKS`. The method returns a
        dictionary containing the cookbook's information.

        Args:
            cb_id (str): The unique identifier of the cookbook whose information is being retrieved.

        Returns:
            dict: A dictionary with the cookbook's information.
        """
        cookbook_info = {"id": cb_id}
        cookbook_info.update(
            Storage.read_object(EnvVariables.COOKBOOKS.name, cb_id, "json")
        )
        return cookbook_info

    @staticmethod
    def update(cb_args: CookbookArguments) -> bool:
        """
        Updates the details of an existing cookbook.

        This method accepts a CookbookArguments object, converts it to a dictionary, and writes the updated
        information to the corresponding JSON file in the directory defined by `EnvVariables.COOKBOOKS`.

        Args:
            cb_args (CookbookArguments): An object containing the updated details of the cookbook.

        Returns:
            bool: True if the update was successful.

        Raises:
            Exception: If there's an error during the update process.
        """
        try:
            # check if recipes in list exist before creating cookbook
            for recipe in cb_args.recipes:
                if not Storage.is_object_exists(
                    EnvVariables.RECIPES.name, recipe, "json"
                ):
                    raise RuntimeError(f"{recipe} recipe does not exist.")

            # Serialize the CookbookArguments object to a dictionary and remove derived properties
            cb_info = cb_args.to_dict()
            cb_info.pop("id", None)  # The 'id' is derived and should not be written

            # Write the updated cookbook information to the storage
            Storage.create_object(
                EnvVariables.COOKBOOKS.name, cb_args.id, cb_info, "json"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to update cookbook: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def delete(cb_id: str) -> bool:
        """
        Deletes a cookbook identified by its ID.

        This method removes the cookbook's JSON file from the storage, using the `Storage.delete_object` method.
        The `EnvVariables.COOKBOOKS` environment variable specifies the directory where the cookbook files are stored.

        Args:
            cb_id (str): The unique identifier of the cookbook to be deleted.

        Returns:
            bool: True if the deletion was successful.

        Raises:
            Exception: If there's an error during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.COOKBOOKS.name, cb_id, "json")
            return True

        except Exception as e:
            logger.error(f"Failed to delete cookbook: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[CookbookArguments]]:
        """
        Retrieves and returns all available cookbooks.

        This method scans the directory specified by `EnvironmentVars.COOKBOOKS` and identifies all stored cookbook
        files. It excludes any files that contain "__" in their names. For each valid cookbook file, the method reads
        the file content and constructs a CookbookArguments object encapsulating the cookbook's details.
        Both the CookbookArguments object and the cookbook ID are then appended to their respective lists.

        Returns:
            tuple[list[str], list[CookbookArguments]]: A tuple where the first element is a list of cookbook IDs and
            the second element is a list of CookbookArguments objects representing the details of each cookbook.

        Raises:
            Exception: If an error occurs during the file reading process or any other operation within the method.
        """
        try:
            retn_cbs = []
            retn_cbs_ids = []

            cbs = Storage.get_objects(EnvVariables.COOKBOOKS.name, "json")
            for cb in cbs:
                if "__" in cb:
                    continue

                cb_info = CookbookArguments(**Cookbook._read_cookbook(Path(cb).stem))
                retn_cbs.append(cb_info)
                retn_cbs_ids.append(cb_info.id)

            return retn_cbs_ids, retn_cbs

        except Exception as e:
            logger.error(f"Failed to get available cookbooks: {str(e)}")
            raise e

    @staticmethod
    def get_categories_in_recipes(recipes: list[str]) -> list[str]:
        return list(
            {
                category
                for recipe_id in recipes
                for category in Recipe.read(recipe_id).categories
            }
        )

    @staticmethod
    def get_tags_in_recipes(recipes: list[str]) -> list[str]:
        return list(
            {tag for recipe_id in recipes for tag in Recipe.read(recipe_id).tags}
        )
