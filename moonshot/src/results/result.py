from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.results.result_arguments import ResultArguments
from moonshot.src.storage.storage import Storage


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
    def load(cls, res_id: str) -> Result:
        """
        Loads an existing result.

        This method accepts a result ID as an argument. It uses the 'id' to locate the result file in the storage.
        If the file does not exist, it raises a RuntimeError. If the file exists, it reads the file and converts the
        data into a ResultArguments object. It then returns a new Result instance created from the
        ResultArguments object.

        Args:
            res_id (str): The unique identifier for the result.

        Raises:
            RuntimeError: If the result file does not exist.
        """
        if not Path(
            Storage.get_filepath(EnvVariables.RUNNERS.name, res_id, "json")
        ).exists():
            raise RuntimeError(
                "Unable to load result because the result file does not exists."
            )

        res_info = ResultArguments.from_file(
            Storage.read_object(EnvVariables.RESULTS.name, res_id, "json")
        )
        return cls(res_info)

    @staticmethod
    def create(res_args: ResultArguments) -> None:
        """
        Creates a new result.

        This method accepts a ResultArguments object as an argument. It uses the 'id' attribute from the ResultArguments
        object as a unique identifier for the result. The method then converts the ResultArguments object into a
        dictionary and writes it to a file using the StorageManager.

        Args:
            res_args (ResultArguments): The arguments for the result.

        Raises:
            Exception: If there is an error during result creation.
        """
        try:
            # Format results
            res_args.results = res_args.format_results()

            # Write as json output
            Storage.create_object(
                EnvVariables.RESULTS.name, res_args.id, res_args.to_dict(), "json"
            )

        except Exception as e:
            print(f"Failed to create result: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read(res_id: str) -> ResultArguments:
        """
        Retrieves the arguments of a specific result from the storage.

        This function accepts a Result ID as an argument. It reads the corresponding result's storage,
        and then converts the retrieved data into a ResultArguments object. If an error occurs during the reading
        process, the error message is printed and the error is re-thrown.

        Args:
            res_id (str): The unique identifier of the result whose arguments are to be retrieved.

        Returns:
            ResultArguments: An object encapsulating the arguments of the specified result.
        """
        try:
            return ResultArguments.from_file(
                Storage.read_object(EnvVariables.RESULTS.name, res_id, "json")
            )

        except Exception as e:
            print(f"Failed to read result: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete(res_id: str) -> None:
        """
        Deletes a specified result.

        This function requires a Result ID as an argument. It then proceeds to delete the corresponding
        result's storage.
        If an error occurs during the deletion process, the error message is printed and the error is re-thrown.

        Args:
            res_id (str): The unique identifier of the result that is to be deleted.

        Raises:
            Exception: If an error is encountered during the deletion of the result.
        """
        try:
            Storage.delete_object(EnvVariables.RESULTS.name, res_id, "json")

        except Exception as e:
            print(f"Failed to delete result: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[ResultArguments]]:
        """
        Fetches all available results.

        This method scans the storage and collects all stored result files.
        It excludes any files that contain "__" in their names. For each valid result file, the method reads the file
        content and creates a ResultArguments object encapsulating the result's details.
        Both the ResultArguments object and the result ID are then appended to their respective lists.

        Returns:
            tuple[list[str], list[ResultArguments]]: A tuple where the first element is a list of result IDs and
            the second element is a list of ResultArguments objects representing the details of each result.

        Raises:
            Exception: If an error is encountered during the file reading process or any other operation within
            the method.
        """
        try:
            retn_results = []
            retn_results_ids = []

            results = Storage.get_objects(EnvVariables.RESULTS.name, "json")
            for res in results:
                if "__" in res:
                    continue

                res_info = ResultArguments.from_file(
                    Storage.read_object(
                        EnvVariables.RESULTS.name, Path(res).stem, "json"
                    )
                )
                retn_results.append(res_info)
                retn_results_ids.append(res_info.id)

            return retn_results_ids, retn_results

        except Exception as e:
            print(f"Failed to get available results: {str(e)}")
            raise e
