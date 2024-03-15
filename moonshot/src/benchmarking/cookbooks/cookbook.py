from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.benchmarking.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.storage.storage_manager import StorageManager


class Cookbook:
    def __init__(self, cb_args: CookbookArguments) -> None:
        self.id = cb_args.id
        self.name = cb_args.name
        self.description = cb_args.description
        self.recipes = cb_args.recipes

    @classmethod
    def load_cookbook(cls, cb_id: str) -> Cookbook:
        """
        Loads a cookbook from a JSON file.

        This method reads the cookbook information from a JSON file specified by the cookbook ID. It constructs
        the file path using the cookbook ID and the designated directory for cookbooks. The method
        then reads the JSON file and returns the cookbook information as a dictionary.

        Args:
            cb_id (str): The ID of the cookbook.

        Returns:
            Cookbook: An instance of the Cookbook class with the loaded cookbook information.
        """
        cb_info = StorageManager.read_cookbook(cb_id)
        return cls(CookbookArguments(**cb_info))

    @staticmethod
    def create_cookbook(cb_args: CookbookArguments) -> None:
        """
        Creates a new cookbook and stores its information in a JSON file.

        This method takes the arguments provided in the `cb_args` parameter, generates a unique cookbook ID by
        slugifying the cookbook name, and then constructs a dictionary with the cookbook's information. It then
        writes this information to a JSON file named after the cookbook ID within the directory specified by
        `EnvironmentVars.COOKBOOKS`. If the operation fails for any reason, an exception is raised
        and the error is printed.

        Args:
            cb_args (CookbookArguments): An object containing the necessary information to create a
            new cookbook.

        Raises:
            Exception: If there is an error during file writing or any other operation within the method.
        """
        try:
            cb_id = slugify(cb_args.name, lowercase=True)
            cb_info = {
                "id": cb_id,
                "name": cb_args.name,
                "description": cb_args.description,
                "recipes": cb_args.recipes,
            }

            # Write as json output
            StorageManager.create_cookbook(cb_id, cb_info)

        except Exception as e:
            print(f"Failed to create cookbook: {str(e)}")
            raise e

    @staticmethod
    def read_cookbook(cb_id: str) -> CookbookArguments:
        """
        Reads a cookbook and returns its information.

        This method takes a cookbook ID as input, reads the corresponding JSON file from the directory specified by
        `EnvironmentVars.COOKBOOKS`, and returns a CookbookArguments object containing the cookbook's information.

        Args:
            cb_id (str): The ID of the cookbook.

        Returns:
            CookbookArguments: An object containing the cookbook's information.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        try:
            return CookbookArguments(**StorageManager.read_cookbook(cb_id))

        except Exception as e:
            print(f"Failed to read cookbook: {str(e)}")
            raise e

    @staticmethod
    def update_cookbook(cb_args: CookbookArguments) -> None:
        """
        Updates an existing cookbook with new information.

        This method takes a CookbookArguments object as input, which contains the new information for the
        cookbook. It directly updates the existing cookbook file with the new information. If the operation fails
        for any reason, an exception is raised and the error is printed.

        Args:
            cb_args (CookbookArguments): An object containing the new information for the cookbook.

        Raises:
            Exception: If there is an error during the update operation.
        """
        try:
            # Convert the cookbook arguments to a dictionary
            cb_info = cb_args.to_dict()

            # Write the updated cookbook information to the file
            StorageManager.create_cookbook(cb_args.id, cb_info)

        except Exception as e:
            print(f"Failed to update cookbook: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete_cookbook(cb_id: str) -> None:
        """
        Deletes a cookbook.

        This method takes a cookbook ID as input, deletes the corresponding JSON file from the directory specified by
        `EnvironmentVars.COOKBOOKS`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            cb_id (str): The ID of the cookbook to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        try:
            StorageManager.delete_cookbook(cb_id)

        except Exception as e:
            print(f"Failed to delete cookbook: {str(e)}")
            raise e

    @staticmethod
    def get_available_cookbooks() -> tuple[list[str], list[CookbookArguments]]:
        """
        Returns a list of available cookbooks.

        This method retrieves all the cookbooks stored in the directory specified by `EnvironmentVars.COOKBOOKS`.
        It ignores any files with "__" in their names. For each valid cookbook file, it reads the file and constructs
        a CookbookArguments object with the cookbook's information. It then appends the CookbookArguments object and the
        cookbook ID to their respective lists.

        Returns:
            tuple[list[str], list[CookbookArguments]]: A tuple containing a list of cookbook IDs and a list of
            CookbookArguments objects.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        try:
            retn_cbs = []
            retn_cbs_ids = []

            cbs = StorageManager.get_cookbooks()
            for cb in cbs:
                if "__" in cb:
                    continue

                cb_info = CookbookArguments(
                    **StorageManager.read_cookbook(Path(cb).stem)
                )
                retn_cbs.append(cb_info)
                retn_cbs_ids.append(cb_info.id)

            return retn_cbs_ids, retn_cbs

        except Exception as e:
            print(f"Failed to get available cookbooks: {str(e)}")
            raise e
