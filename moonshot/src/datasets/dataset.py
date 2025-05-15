from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pandas as pd
from datasets import load_dataset
from pydantic import validate_call
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.datasets.dataset_arguments import DatasetArguments
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Dataset:
    cache_name = "cache"
    cache_extension = "json"

    @staticmethod
    @validate_call
    def create(ds_args: DatasetArguments) -> str:
        """
        Creates a new dataset based on the provided arguments and method.

        This method generates a unique dataset ID using the dataset name,
        checks if a dataset with the same ID already exists, and then
        creates the dataset using the specified method. The dataset information
        is then stored as a JSON object.

        Args:
            ds_args (DatasetArguments): The arguments containing dataset
                details such as name, description, reference, license, and examples.

        Returns:
            str: The file path of the created dataset JSON object.

        Raises:
            RuntimeError: If a dataset with the same ID already exists.
            Exception: If any other error occurs during the dataset creation
                process.
        """
        try:
            ds_id = slugify(ds_args.name, lowercase=True)

            # Check if the dataset exists
            if Storage.is_object_exists(EnvVariables.DATASETS.name, ds_id, "json"):
                raise RuntimeError(f"Dataset with ID '{ds_id}' already exists.")

            ds_info = {
                "id": ds_id,
                "name": ds_args.name,
                "description": ds_args.description,
                "reference": ds_args.reference,
                "license": ds_args.license,
            }

            examples = ds_args.examples
            # Write as JSON output
            file_path = Storage.create_object_with_iterator(
                EnvVariables.DATASETS.name,
                ds_id,
                ds_info,
                "json",
                iterator_keys=["examples"],
                iterator_data=examples,
            )

            return file_path
        except Exception as e:
            logger.error(f"Failed to create dataset: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def convert_data(csv_file_path: str) -> Iterator[dict]:
        """
        Converts a CSV file to an iterator of dictionaries.

        This method reads a CSV file and converts its contents into an iterator of dictionaries,
        where each dictionary represents a row in the CSV file.

        Args:
            csv_file_path (str): The file path to the CSV file.

        Returns:
            Iterator[dict]: An iterator of dictionaries representing the CSV data.
        """
        # validate headers
        df_header = pd.read_csv(csv_file_path, nrows=1)
        headers = df_header.columns.tolist()
        required_headers = ["input", "target"]
        if not all(header in headers for header in required_headers):
            raise KeyError(
                f"Required headers not found in the dataset. Required headers are {required_headers}."
            )

        df = pd.read_csv(csv_file_path, chunksize=1)
        # validate dataset
        first_chunk = next(df, None)
        if first_chunk is None or first_chunk.empty:
            raise ValueError("The uploaded file does not contain any data.")

        # Reset df after performing next(df)
        df = pd.read_csv(csv_file_path, chunksize=1)

        result = [chunk.to_dict("records")[0] for chunk in df]
        return iter(result)

    @staticmethod
    @validate_call
    def download_hf(**hf_args) -> Iterator[dict]:
        """
        Downloads a dataset from Hugging Face and converts it to an iterator of dictionaries.

        This method loads a dataset from Hugging Face based on the provided arguments and converts
        its contents into an iterator of dictionaries, where each dictionary contains 'input' and 'target' keys.

        Args:
            hf_args (dict): A dictionary containing the following keys:
                - 'dataset_name' (str): The name of the Hugging Face dataset.
                - 'dataset_config' (str): The configuration of the Hugging Face dataset.
                - 'split' (str): The split of the dataset to load.
                - 'input_col' (list[str]): The list of input columns.
                - 'target_col' (str): The target column.

        Returns:
            Iterator[dict]: An iterator of dictionaries representing the dataset.
        """

        dataset = load_dataset(
            hf_args["dataset_name"], hf_args["dataset_config"], split=hf_args["split"]
        )

        for example in dataset:
            input_data = " ".join([str(example[col]) for col in hf_args["input_col"]])
            target_data = str(example[hf_args["target_col"]])
            yield {"input": input_data, "target": target_data}

    @staticmethod
    @validate_call
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
            if ds_id:
                return DatasetArguments(**Dataset._read_dataset(ds_id))
            else:
                raise RuntimeError("Dataset ID is empty")

        except Exception as e:
            logger.error(f"Failed to read dataset: {str(e)}")
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
    @validate_call
    def delete(ds_id: str) -> bool:
        """
        Deletes a dataset from storage.

        This method attempts to delete the dataset with the given ID from the storage. If the deletion is successful,
        it returns True. If an exception occurs during the deletion process, it prints an error message and re-raises
        the exception.

        Args:
            ds_id (str): The unique identifier of the dataset to be deleted.

        Returns:
            bool: True if the dataset was successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.DATASETS.name, ds_id, "json")
            return True

        except Exception as e:
            logger.error(f"Failed to delete dataset: {str(e)}")
            raise e

    @staticmethod
    def get_cache_information() -> dict:
        """
        Retrieves cache information from the storage.

        This method attempts to read the cache information from the storage and return it as a dictionary.
        If the cache information does not exist or an error occurs, it returns an empty dictionary.

        Returns:
            dict: A dictionary containing the cache information or an empty dictionary if an error occurs
            or if the cache information does not exist.

        Raises:
            Exception: If there's an error during the retrieval process, it is logged and an
            empty dictionary is returned.
        """
        try:
            # Retrieve cache information from the storage and return it as a dictionary
            cache_info = Storage.read_object(
                EnvVariables.DATASETS.name, Dataset.cache_name, Dataset.cache_extension
            )
            return cache_info if cache_info else {}
        except Exception as e:
            logger.error(f"Failed to retrieve cache information: {str(e)}")
            return {}

    @staticmethod
    def write_cache_information(cache_info: dict) -> None:
        """
        Writes the updated cache information to the storage.

        Args:
            cache_info (dict): The cache information to be written.
        """
        try:
            Storage.create_object(
                obj_type=EnvVariables.DATASETS.name,
                obj_id=Dataset.cache_name,
                obj_info=cache_info,
                obj_extension=Dataset.cache_extension,
            )
        except Exception as e:
            logger.error(f"Failed to write cache information: {str(e)}")
            raise e

    @staticmethod
    def get_available_items(
        datasets: list[str] = [],
    ) -> tuple[list[str], list[DatasetArguments]]:
        """
        Retrieves a list of available dataset IDs and their corresponding DatasetArguments objects.

        This method filters out any non-dataset files and the cache file from the list of datasets. It then
        retrieves or updates the dataset information from the cache for each dataset. If the cache is updated
        during this process, it writes the updated cache information back to the storage.

        Args:
            datasets (list[str], optional): A list of dataset file names. If not provided, it will retrieve
                the list of all dataset files from the storage. Defaults to an empty list.

        Returns:
            tuple[list[str], list[DatasetArguments]]: A tuple containing two lists:
                - The first list contains the IDs of the available datasets.
                - The second list contains the corresponding DatasetArguments objects for those IDs.
        """
        try:
            retn_datasets = []
            retn_datasets_ids = []
            ds_cache_info = Dataset.get_cache_information()
            cache_needs_update = False  # Initialize a flag to track cache updates

            if datasets:
                datasets_objects = datasets
            else:
                datasets_objects = Storage.get_objects(
                    EnvVariables.DATASETS.name, "json"
                )

            for ds in datasets_objects:
                if (
                    "__" in ds
                    or f"{Dataset.cache_name}.{Dataset.cache_extension}" in ds
                ):
                    continue

                ds_name = Path(ds).stem
                ds_info, cache_updated = Dataset._get_or_update_dataset_info(
                    ds_name, ds_cache_info
                )
                if cache_updated:
                    cache_needs_update = True  # Set the flag if any cache was updated

                retn_datasets.append(ds_info)
                retn_datasets_ids.append(ds_info.id)

            if cache_needs_update:  # Check the flag after the loop
                Dataset.write_cache_information(ds_cache_info)

            return retn_datasets_ids, retn_datasets

        except Exception as e:
            logger.error(f"Failed to get available datasets: {str(e)}")
            raise e

    @staticmethod
    def _get_or_update_dataset_info(
        ds_name: str, ds_cache_info: dict
    ) -> tuple[DatasetArguments, bool]:
        """
        Retrieves or updates the dataset information from the cache.

        This method checks if the dataset information is already available in the cache and if the file hash matches
        the one stored in the cache. If it does, the information is retrieved from the cache. If not, the dataset
        information is read from the storage, the cache is updated with the new information and the new file hash,
        and a flag is set to indicate that the cache has been updated.

        Args:
            ds_name (str): The name of the dataset.
            ds_cache_info (dict): A dictionary containing the cached dataset information.

        Returns:
            tuple[DatasetArguments, bool]: A tuple containing the DatasetArguments object with the dataset information
                                           and a boolean indicating whether the cache was updated or not.
        """
        file_hash = Storage.get_file_hash(EnvVariables.DATASETS.name, ds_name, "json")
        cache_updated = False

        if ds_name in ds_cache_info and file_hash == ds_cache_info[ds_name]["hash"]:
            ds_metadata = ds_cache_info[ds_name].copy()
            ds_metadata.pop("hash", None)
            ds_info = DatasetArguments(**ds_metadata)
        else:
            ds_info = DatasetArguments(**Dataset._read_dataset(ds_name))
            ds_info.examples = None
            ds_cache_info[ds_name] = ds_info.copy().to_dict()
            ds_cache_info[ds_name]["hash"] = file_hash
            cache_updated = True

        return ds_info, cache_updated
