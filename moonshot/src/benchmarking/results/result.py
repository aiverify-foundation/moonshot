from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.benchmarking.results.result_arguments import ResultArguments
from moonshot.src.storage.storage_manager import StorageManager


class Result:
    def __init__(self, res_args: ResultArguments) -> None:
        self.id = res_args.id
        self.name = res_args.name
        self.start_time = res_args.start_time
        self.end_time = res_args.end_time
        self.duration = res_args.duration
        self.recipes = res_args.recipes
        self.cookbooks = res_args.cookbooks
        self.endpoints = res_args.endpoints
        self.num_of_prompts = res_args.num_of_prompts
        self.results = res_args.results
        self.status = res_args.status

    @classmethod
    def load_result(cls, res_id: str) -> Result:
        """
        Loads a result by its ID.

        This method loads a result by its ID. It first checks if the result file exists.
        If it does, it reads the result file and converts the result into a ResultArguments object.
        If the result file does not exist, it raises a RuntimeError.

        Args:
            res_id (str): The ID of the result to load.

        Returns:
            Result: The loaded result instance.

        Raises:
            RuntimeError: If the result file does not exist.
            Exception: If there is an error during result loading.
        """
        # Check if the result file exists. If it does not exist, raise an error.
        if not Path(StorageManager.get_executor_results_filepath(res_id)).exists():
            raise RuntimeError(
                "Unable to load result because the result file does not exists."
            )

        res_info = ResultArguments.from_file(StorageManager.read_result(res_id))
        return cls(res_info)

    @staticmethod
    def create_result(res_args: ResultArguments) -> None:
        """
        Creates a new result.

        This method takes a ResultArguments object as input. It first generates a unique ID for the result by slugifying
        the name of the result. It then constructs a dictionary with the result arguments. This dictionary is then
        converted into a ResultArguments object and written to a file using the StorageManager.

        Args:
            res_args (ResultArguments): The arguments for the result.

        Raises:
            Exception: If there is an error during result creation.
        """
        try:
            # Write as json output
            StorageManager.create_result(res_args.id, res_args.to_dict())

        except Exception as e:
            print(f"Failed to create result: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read_result(res_id: str) -> ResultArguments:
        """
        Reads the result's arguments from the storage.

        This function takes a Result ID as input. It first reads the result's storage using the StorageManager.
        Then, it converts the result into a ResultArguments object. If there is an error during the reading,
        the error is printed and re-raised.

        Args:
            res_id (str): The ID of the result whose arguments are to be read.

        Returns:
            ResultArguments: The arguments of the result.
        """
        try:
            return ResultArguments.from_file(StorageManager.read_result(res_id))

        except Exception as e:
            print(f"Failed to read result: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete_result(res_id: str) -> None:
        """
        Deletes an existing result.

        This function takes a Result ID as input. It first deletes the result's storage using the StorageManager.
        If there is an error during the deletion, the error is printed and re-raised.

        Args:
            res_id (str): The ID of the result to be deleted.

        Raises:
            Exception: If there is an error during result deletion.
        """
        try:
            StorageManager.delete_result(res_id)

        except Exception as e:
            print(f"Failed to delete result: {str(e)}")
            raise e

    @staticmethod
    def get_available_results() -> tuple[list[str], list[ResultArguments]]:
        """
        Retrieves the available results.

        This function retrieves all the available results from the storage using the StorageManager.
        It then converts each result into a ResultArguments object and appends it to a list.
        If there is an error during the retrieval, the error is printed and re-raised.

        Returns:
            tuple[list[str], list[ResultArguments]]: A tuple containing a list of result IDs and a
            list of ResultArguments objects.
        """
        try:
            retn_results = []
            retn_results_ids = []

            results = StorageManager.get_results()
            for res in results:
                if "__" in res:
                    continue

                res_info = ResultArguments.from_file(
                    StorageManager.read_result(Path(res).stem)
                )
                retn_results.append(res_info)
                retn_results_ids.append(res_info.id)

            return retn_results_ids, retn_results

        except Exception as e:
            print(f"Failed to get available results: {str(e)}")
            raise e
