from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.datasets.dataset_arguments import DatasetArguments
from moonshot.src.storage.storage import Storage


class Dataset:
    @staticmethod
    @validate_arguments
    def read(ds_id: str) -> DatasetArguments:
        """
        Fetches the details of a given dataset.

        This method takes a dataset ID as input, finds the corresponding JSON file in the directory
        specified by `EnvVariables.DATASETS`, and returns a DatasetArguments object
        that contains the dataset's details. If any error arises during the process, an exception is raised and the
        error message is logged.

        Args:
            ds_id (str): The unique ID of the dataset to be fetched.

        Returns:
            DatasetArguments: An object encapsulating the details of the fetched dataset.

        Raises:
            Exception: If there's an error during the file reading process or any other operation within the method.
        """
        try:
            return DatasetArguments(**Dataset._read_dataset(ds_id))

        except Exception as e:
            print(f"Failed to read dataset: {str(e)}")
            raise e

    @staticmethod
    def _read_dataset(ds_id: str) -> dict:
        """
        Retrieves dataset information from storage and augments it with metadata.

        This method takes a dataset ID, locates the corresponding JSON file within the directory
        specified by `EnvVariables.DATASETS`, and constructs a dictionary that includes the dataset's
        core details, as well as metadata such as the creation datetime and the count of dataset prompts.

        Args:
            ds_id (str): The unique identifier of the dataset to be retrieved.

        Returns:
            dict: A dictionary with the dataset's core information, enriched with metadata like the creation datetime
                  and the total number of prompts contained within the dataset.
        """
        # Read the basic dataset information
        dataset_info = Storage.read_object_with_iterator(
            obj_type=EnvVariables.DATASETS.name,
            obj_id=ds_id,
            obj_extension="json",
            json_keys=["name", "description", "license", "reference"],
            iterator_keys=["examples.item"],
        )

        # Add additional parameters - [id, num_of_dataset_prompts, creation_date]
        # Append the dataset ID to the dataset_info
        dataset_info["id"] = ds_id

        # Use Storage.count_objects to get the number of examples in a memory-efficient way
        dataset_info["num_of_dataset_prompts"] = Storage.count_objects(
            EnvVariables.DATASETS.name, ds_id, "json", "examples.item"
        )

        # Assign the creation date to the dataset_info
        creation_datetime = Storage.get_creation_datetime(
            EnvVariables.DATASETS.name, ds_id, "json"
        )
        dataset_info["created_date"] = creation_datetime.replace(
            microsecond=0
        ).isoformat(" ")

        return dataset_info

    @staticmethod
    @validate_arguments
    def delete(ds_id: str) -> None:
        """
        Deletes a dataset given its unique identifier.

        This method attempts to delete the dataset corresponding to the provided `ds_id` from the storage.
        If the deletion process encounters any issues, it logs the error message and re-raises the exception.

        Args:
            ds_id (str): The unique identifier of the dataset to be deleted.

        Raises:
            Exception: If there's an error during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.DATASETS.name, ds_id, "json")

        except Exception as e:
            print(f"Failed to delete dataset: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[DatasetArguments]]:
        """
        Retrieves the IDs and details of all available datasets.

        This method queries the storage for all dataset objects, filters out any non-dataset items based on naming
        conventions, and then constructs a list of DatasetArguments objects containing the details of each dataset.
        It returns a tuple containing a list of dataset IDs and a list of DatasetArguments objects.

        Returns:
            tuple[list[str], list[DatasetArguments]]: A tuple with two elements. The first element is a list of
            dataset IDs, and the second element is a list of DatasetArguments objects representing the details of
            each dataset.

        Raises:
            Exception: If there's an error during the retrieval process.
        """
        try:
            retn_datasets = []
            retn_datasets_ids = []

            datasets = Storage.get_objects(EnvVariables.DATASETS.name, "json")
            for ds in datasets:
                if "__" in ds:
                    continue

                ds_info = DatasetArguments(**Dataset._read_dataset(Path(ds).stem))
                retn_datasets.append(ds_info)
                retn_datasets_ids.append(ds_info.id)

            return retn_datasets_ids, retn_datasets

        except Exception as e:
            print(f"Failed to get available datasets: {str(e)}")
            raise e
