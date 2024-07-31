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


def api_create_datasets(
    name: str, description: str, reference: str, license: str, method: str, **kwargs
) -> str:
    """
    This function creates a new dataset.

    This function takes the name, description, reference, and license for a new dataset as input. It then creates a new
    DatasetArguments object with these details and an empty id. The id is left empty because it will be generated
    from the name during the creation process. The function then calls the Dataset's create method to
    create the new dataset.

    Args:
        name (str): The name of the new dataset.
        description (str): A brief description of the new dataset.
        reference (str): A reference link for the new dataset.
        license (str): The license of the new dataset.
        method (str): The method to create new dataset. (csv/hf)
        kwargs: Additional keyword arguments for the Dataset's create method.

    Returns:
        str: The ID of the newly created dataset.
    """
    ds_args = DatasetArguments(
        id="",
        name=name,
        description=description,
        reference=reference,
        license=license,
        examples=None,
    )

    return Dataset.create(ds_args, method, **kwargs)
