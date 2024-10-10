from pydantic import validate_call

from moonshot.src.datasets.dataset import Dataset
from moonshot.src.datasets.dataset_arguments import DatasetArguments


# ------------------------------------------------------------------------------
# Datasets APIs
# ------------------------------------------------------------------------------
@validate_call
def api_delete_dataset(ds_id: str) -> bool:
    """
    Deletes a dataset identified by its unique dataset ID.

    Args:
        ds_id (str): The unique identifier for the dataset to be deleted.

    Returns:
        bool: True if the dataset was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return Dataset.delete(ds_id)


def api_get_all_datasets() -> list[dict]:
    """
    This function retrieves all available datasets and returns them as a list of dictionaries. Each dictionary
    represents a result and contains its information.

    Returns:
        list[dict]: A list of dictionaries, each representing a result.
    """
    _, datasets = Dataset.get_available_items()
    return [dataset.to_dict() for dataset in datasets]


def api_get_all_datasets_name() -> list[str]:
    """
    This function retrieves all available datasets names and returns them as a list.

    Returns:
        list[str]: A list of datasets names.
    """
    datasets_name, _ = Dataset.get_available_items()
    return datasets_name


def api_download_dataset(
    name: str, description: str, reference: str, license: str, **kwargs
) -> str:
    """
    Downloads a dataset from Hugging Face and creates a new dataset with the provided details.

    This function takes the name, description, reference, and license for a new dataset as input, along with additional
    keyword arguments for downloading the dataset from Hugging Face. It then creates a new DatasetArguments object with
    these details and an empty id. The id is left empty because it will be generated from the name during the creation
    process. The function then calls the Dataset's create method to create the new dataset.

    Args:
        name (str): The name of the new dataset.
        description (str): A brief description of the new dataset.
        reference (str): A reference link for the new dataset.
        license (str): The license of the new dataset.
        kwargs: Additional keyword arguments for downloading the dataset from Hugging Face.

    Returns:
        str: The ID of the newly created dataset.
    """
    examples = Dataset.download_hf(**kwargs)
    ds_args = DatasetArguments(
        id="",
        name=name,
        description=description,
        reference=reference,
        license=license,
        examples=examples,
    )
    return Dataset.create(ds_args)


def api_convert_dataset(
    name: str, description: str, reference: str, license: str, csv_file_path: str
) -> str:
    """
    Converts a CSV file to a dataset and creates a new dataset with the provided details.

    This function takes the name, description, reference, and license for a new dataset as input, along with the file
    path to a CSV file. It then creates a new DatasetArguments object with these details and an empty id. The id is left
    empty because it will be generated from the name during the creation process. The function then calls the Dataset's
    create method to create the new dataset.

    Args:
        name (str): The name of the new dataset.
        description (str): A brief description of the new dataset.
        reference (str): A reference link for the new dataset.
        license (str): The license of the new dataset.
        csv_file_path (str): The file path to the CSV file.

    Returns:
        str: The ID of the newly created dataset.
    """
    examples = Dataset.convert_data(csv_file_path)
    ds_args = DatasetArguments(
        id="",
        name=name,
        description=description,
        reference=reference,
        license=license,
        examples=examples,
    )
    return Dataset.create(ds_args)
