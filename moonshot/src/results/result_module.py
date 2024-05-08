from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class ResultModule:
    @classmethod
    def load(cls, result_module_id: str) -> ResultModule:
        """
        Loads a result module instance by its ID.

        This method attempts to load a result module instance using the provided ID.
        If the result module instance is found, it is instantiated and returned.
        If the result module instance does not exist, a RuntimeError is raised.

        Args:
            result_module_id (str): The unique identifier of the result module to be retrieved.

        Returns:
            ResultModule: The instantiated result module instance.

        Raises:
            RuntimeError: If the result module instance does not exist.
        """
        result_module_instance = get_instance(
            result_module_id,
            Storage.get_filepath(
                EnvVariables.RESULTS_MODULES.name, result_module_id, "py"
            ),
        )
        if result_module_instance:
            return result_module_instance()
        else:
            raise RuntimeError(
                f"Unable to get defined result module instance - {result_module_id}"
            )

    @staticmethod
    @validate_arguments
    def delete(result_module_id: str) -> None:
        """
        Removes a result module using its ID.

        This function attempts to delete a result module using its ID. If the deletion is successful, the function
        returns None. If an error occurs during the deletion process, the error is printed and re-thrown.

        Args:
            result_module_id (str): The ID of the result module to be removed.

        Raises:
            Exception: If there is an error during the deletion process.
        """
        try:
            Storage.delete_object(
                EnvVariables.RESULTS_MODULES.name, result_module_id, "py"
            )

        except Exception as e:
            print(f"Failed to delete result module instance: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Fetches the list of all available result modules.

        This method uses the `get_objects` method from the StorageManager to obtain all Python files in the directory
        defined by the `EnvVariables.RESULTS_MODULES.name` environment variable. It then excludes any files that are
        not intended to be exposed as result modules (those containing "__" in their names).

        The method returns a list of the names of these result modules.

        Returns:
            list[str]: A list of strings, each denoting the name of a result module.

        Raises:
            Exception: If an error occurs during the extraction of result modules.
        """
        try:
            retn_result_module_ids = []
            for result_module_id in Storage.get_objects(
                EnvVariables.RESULTS_MODULES.name, "py"
            ):
                if "__" in result_module_id:
                    continue
                retn_result_module_ids.append(Path(result_module_id).stem)
            return retn_result_module_ids

        except Exception as e:
            print(f"Failed to get available result modules: {str(e)}")
            raise e
