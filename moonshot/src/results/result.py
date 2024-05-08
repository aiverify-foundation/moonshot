from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.storage.storage import Storage


class Result:
    def __init__(self, result_args: ResultArguments) -> None:
        self.id = result_args.id
        self.start_time = result_args.start_time
        self.end_time = result_args.end_time
        self.duration = result_args.duration
        self.raw_results = result_args.raw_results
        self.results = result_args.results
        self.status = result_args.status
        self.params = result_args.params

    @classmethod
    def load(cls, result_id: str) -> Result:
        """
        Loads a result instance by its ID.

        This method attempts to load a result instance using the provided ID by reading the corresponding data from
        storage. It then instantiates a Result object with the loaded data.

        Args:
            result_id (str): The unique identifier of the result to be retrieved.

        Returns:
            Result: The instantiated result object with the loaded data.
        """
        return cls(Result.read(result_id))

    @staticmethod
    @validate_arguments
    def read(result_id: str) -> ResultArguments:
        """
        Reads the result data for a given result ID and returns a ResultArguments instance.

        This method attempts to read the result data associated with the provided result ID. If successful, it
        returns a ResultArguments instance created from the retrieved data. If an error occurs, it prints an error
        message and re-raises the exception.

        Args:
            result_id (str): The unique identifier of the result to be read.

        Returns:
            ResultArguments: An instance of ResultArguments containing the result data.

        Raises:
            Exception: If any error occurs during the reading process.
        """
        try:
            return ResultArguments(**Result._read_result(result_id))

        except Exception as e:
            print(f"Failed to read result: {str(e)}")
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
    @validate_arguments
    def delete(result_id: str) -> None:
        """
        Deletes the result data for a given result ID.

        This method attempts to delete the result data associated with the provided result ID from storage.
        If an error occurs during the deletion process, it prints an error message and re-raises the exception.

        Args:
            result_id (str): The unique identifier of the result to be deleted.

        Raises:
            Exception: If any error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.RESULTS.name, result_id, "json")

        except Exception as e:
            print(f"Failed to delete result: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[ResultArguments]]:
        """
        Retrieves all available result items.

        This method searches the storage for result objects, excluding any filenames that contain "__".
        It reads the contents of each valid result file and constructs a ResultArguments object with the result details.
        The method accumulates the result IDs and the corresponding ResultArguments objects into separate lists,
        which are then returned together as a tuple.

        Returns:
            tuple[list[str], list[ResultArguments]]: A tuple containing two elements. The first is a list of result
            IDs, and the second is a list of ResultArguments objects, each representing the details of a result.

        Raises:
            Exception: If any issues arise during the retrieval and processing of result files.
        """
        try:
            retn_results = []
            retn_results_ids = []

            for result in Storage.get_objects(EnvVariables.RESULTS.name, "json"):
                if "__" in result:
                    continue
                result_info = ResultArguments(**Result._read_result(Path(result).stem))
                retn_results.append(result_info)
                retn_results_ids.append(result_info.id)
            return retn_results_ids, retn_results

        except Exception as e:
            print(f"Failed to get available results: {str(e)}")
            raise e
