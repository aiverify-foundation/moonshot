from __future__ import annotations

from pathlib import Path

from pydantic import validate_call

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Result:
    @staticmethod
    @validate_call
    def read(result_id: str) -> dict:
        """
        Reads the result data from storage for a given result ID.

        This method attempts to retrieve the result data associated with the specified result ID from storage.
        If the data is found, it is returned as a dictionary. If no data is found, an exception is raised and
        an error message is printed.

        Args:
            result_id (str): The unique identifier of the result to be read.

        Returns:
            dict: A dictionary containing the result data if found.

        Raises:
            Exception: If no result data is found or if an error occurs during the read operation.
        """
        try:
            if result_id:
                return Result._read_result(result_id)
            else:
                raise RuntimeError("Result ID is empty")

        except Exception as e:
            logger.error(f"Failed to read result: {str(e)}")
            raise e

    @staticmethod
    def _read_result(result_id: str) -> dict:
        """
        Reads the result data from storage for a given result ID.

        This method attempts to retrieve the result data associated with the specified result ID from storage.
        If the data is found, it is returned as a dictionary. If no data is found, a RuntimeError is raised.

        Args:
            result_id (str): The unique identifier of the result to be read.

        Returns:
            dict: A dictionary containing the result data.

        Raises:
            RuntimeError: If no result data is found for the given result ID.
        """
        obj_results = Storage.read_object(EnvVariables.RESULTS.name, result_id, "json")
        if obj_results:
            return obj_results
        else:
            raise RuntimeError(f"Unable to get results for {result_id}.")

    @staticmethod
    @validate_call
    def delete(result_id: str) -> bool:
        """
        Deletes the result data associated with the given result ID from storage.

        This method attempts to delete the result data identified by the specified result ID from storage.
        If the deletion is successful, it returns True. If an exception occurs during the deletion process,
        an error message is printed and the exception is re-raised.

        Args:
            result_id (str): The unique identifier of the result to be deleted.

        Returns:
            bool: True if the result data was successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.RESULTS.name, result_id, "json")
            return True

        except Exception as e:
            logger.error(f"Failed to delete result: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[dict]]:
        """
        Retrieves the list of available result IDs and their corresponding result data.

        This method queries the storage to obtain all the result objects, filters out any that are not relevant
        (e.g., internal use objects with "__" in their name), and then reads the result data for each remaining
        result ID. It returns a tuple containing a list of result IDs and a list of dictionaries with the result
        data.

        Returns:
            tuple[list[str], list[dict]]: A tuple with the first element being a list of result IDs and the
            second element being a list of dictionaries containing the result data for each ID.
        """
        try:
            retn_results = []
            retn_results_ids = []

            for result in Storage.get_objects(EnvVariables.RESULTS.name, "json"):
                if "__" in result:
                    continue
                result_info = Result._read_result(Path(result).stem)
                retn_results.append(result_info)
                retn_results_ids.append(Path(result).stem)
            return retn_results_ids, retn_results

        except Exception as e:
            logger.error(f"Failed to get available results: {str(e)}")
            raise e
