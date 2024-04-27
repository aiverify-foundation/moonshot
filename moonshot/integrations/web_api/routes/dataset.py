from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from ..container import Container
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.dataset_service import DatasetService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.get("/api/v1/datasets")
@inject
def get_all_datasets(dataset_service: DatasetService = Depends(Provide[Container.dataset_service])
    ):
    """
    Get all the dataset from the database
    """
    try:
        return dataset_service.get_all_datasets()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve datasets: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve datasets: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve datasets: {e.msg}")   


@router.get("/api/v1/datasets/{dataset_id}")
@inject 
def get_dataset_by_id(
    dataset_id: str,
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service])
    ) -> DatasetResponseDTO | None:
    """
    Get a dataset from the database
    """
    try:
        dataset = dataset_service.get_dataset_by_id(dataset_id)
        return dataset
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve dataset: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve dataset: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve dataset: {e.msg}")
