from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.storage.storage import Storage


class Cookbook:
    def __init__(self, cb_args: CookbookArguments) -> None:
        self.id = cb_args.id
        self.name = cb_args.name
        self.description = cb_args.description
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
        cb_info = Storage.read_object(EnvVariables.COOKBOOKS.name, cb_id, "json")
        return cls(CookbookArguments(**cb_info))

    @staticmethod
    def create(cb_args: CookbookArguments) -> None:
        """
        This method is responsible for creating a new cookbook and storing its details in a JSON file.

        The function accepts `cb_args` parameter which contains the necessary details for creating a new cookbook.
        It generates a unique ID for the cookbook by slugifying the cookbook name. After that, it constructs a
        dictionary with the cookbook's details and writes this information to a JSON file. The JSON file is named after
        the cookbook ID and is stored in the directory specified by `EnvironmentVars.COOKBOOKS`.

        If the operation encounters any error, an exception is raised and the error message is printed.

        Args:
            cb_args (CookbookArguments): An object that holds the necessary details for creating a new cookbook.

        Raises:
            Exception: If there is an error during the file writing process or any other operation within the method.
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
            Storage.create_object(EnvVariables.COOKBOOKS.name, cb_id, cb_info, "json")

        except Exception as e:
            print(f"Failed to create cookbook: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read(cb_id: str) -> CookbookArguments:
        """
        Retrieves the details of a specified cookbook.

        This method accepts a cookbook ID as an argument, locates the corresponding JSON file in the directory
        defined by `EnvironmentVars.COOKBOOKS`, and returns a CookbookArguments object that encapsulates the cookbook's
        details. If any error occurs during the process, an exception is raised and the error message is logged.

        Args:
            cb_id (str): The unique identifier of the cookbook to be retrieved.

        Returns:
            CookbookArguments: An object encapsulating the details of the retrieved cookbook.

        Raises:
            Exception: If there's an error during the file reading process or any other operation within the method.
        """
        try:
            return CookbookArguments(
                **Storage.read_object(EnvVariables.COOKBOOKS.name, cb_id, "json")
            )

        except Exception as e:
            print(f"Failed to read cookbook: {str(e)}")
            raise e

    @staticmethod
    def update(cb_args: CookbookArguments) -> None:
        """
        Modifies an existing cookbook with provided details.

        This method accepts a CookbookArguments object, which holds the updated information for the
        cookbook. It directly modifies the existing cookbook file with the new details. If any error arises during the
        operation, an exception is thrown and the error is logged.

        Args:
            cb_args (CookbookArguments): An instance encapsulating the updated details for the cookbook.

        Raises:
            Exception: If an error is encountered during the update process.
        """
        try:
            # Convert the cookbook arguments to a dictionary
            cb_info = cb_args.to_dict()

            # Write the updated cookbook information to the file
            Storage.create_object(
                EnvVariables.COOKBOOKS.name, cb_args.id, cb_info, "json"
            )

        except Exception as e:
            print(f"Failed to update cookbook: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete(cb_id: str) -> None:
        """
        Deletes a cookbook.

        This method accepts a cookbook ID (cb_id) as an argument and attempts to delete the corresponding JSON file
        from the directory specified by `EnvironmentVars.COOKBOOKS`. If the operation encounters any issues, an
        exception is raised and the error message is logged.

        Args:
            cb_id (str): The unique identifier of the cookbook to be deleted.

        Raises:
            Exception: If an error occurs during the file deletion process or any other operation within the method.
        """
        try:
            Storage.delete_object(EnvVariables.COOKBOOKS.name, cb_id, "json")

        except Exception as e:
            print(f"Failed to delete cookbook: {str(e)}")
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

                cb_info = CookbookArguments(
                    **Storage.read_object(
                        EnvVariables.COOKBOOKS.name, Path(cb).stem, "json"
                    )
                )
                retn_cbs.append(cb_info)
                retn_cbs_ids.append(cb_info.id)

            return retn_cbs_ids, retn_cbs

        except Exception as e:
            print(f"Failed to get available cookbooks: {str(e)}")
            raise e
