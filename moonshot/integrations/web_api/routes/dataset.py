from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.dataset_service import DatasetService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter()


@router.get("/api/v1/datasets")
@inject
def get_all_datasets(
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service]),
):
    """
    Get all the dataset from the database
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
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service])
    ) -> list[str] | None:
    """
    Get a dataset from the database
    """
    try:
        dataset = dataset_service.get_all_datasets_name()
        return dataset
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve dataset: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve dataset: {e.msg}"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve dataset: {e.msg}")


@router.delete("/api/v1/datasets/{dataset_id}")
@inject
def delete_dataset(
    dataset_id: str,
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        dataset_service.delete_dataset(dataset_id)
        return {"message": "Dataset deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete dataset: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete dataset: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete dataset: {e.msg}")    
    
