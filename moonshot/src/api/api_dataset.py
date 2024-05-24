from pydantic import validate_call

from moonshot.src.datasets.dataset import Dataset


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
