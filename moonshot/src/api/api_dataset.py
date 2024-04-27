from moonshot.src.datasets.dataset import Dataset


# ------------------------------------------------------------------------------
# Datasets APIs
# ------------------------------------------------------------------------------
def api_delete_dataset(ds_id: str) -> None:
    """
    Deletes a dataset.

    This method takes a dataset ID as input, deletes the corresponding JSON file from the directory specified by
    `EnvironmentVars.datasets`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        ds_id (str): The ID of the dataset to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    Dataset.delete(ds_id)


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
