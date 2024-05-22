from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.dataset_service import DatasetService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Datasets"])


@router.get("/api/v1/datasets")
@inject
def get_all_datasets(
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service]),
) -> list[DatasetResponseDTO]:
    """
    Retrieve all datasets from the database.

    Args:
        dataset_service (DatasetService): The service responsible for retrieving datasets.

    Returns:
        list: A list of all datasets.

    Raises:
        HTTPException: An error with status code 404 if no datasets are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return dataset_service.get_all_datasets()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve datasets: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve datasets: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve datasets: {e.msg}"
            )


@router.get("/api/v1/datasets/name")
@inject
def get_all_datasets_name(
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service]),
) -> list[str]:
    """
    Retrieve the names of all datasets from the database.

    Args:
        dataset_service (DatasetService): The service responsible for retrieving dataset names.

    Returns:
        list[str]: A list of dataset names.

    Raises:
        HTTPException: An error with status code 404 if no dataset names are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return dataset_service.get_all_datasets_name()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve dataset names: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve dataset names: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve dataset names: {e.msg}"
            )


@router.delete("/api/v1/datasets/{dataset_id}")
@inject
def delete_dataset(
    dataset_id: str,
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service]),
) -> dict[str, str]:
    """
    Delete a dataset from the database by its ID.

    Args:
        dataset_id (str): The unique identifier of the dataset to delete.
        dataset_service (DatasetService): The service responsible for deleting the dataset.

    Returns:
        dict[str, str]: A message indicating the successful deletion of the dataset.

    Raises:
        HTTPException: An error with status code 404 if the dataset is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        dataset_service.delete_dataset(dataset_id)
        return {"message": "Dataset deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete dataset: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete dataset: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete dataset: {e.msg}"
            )
