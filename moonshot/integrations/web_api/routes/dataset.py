import os
import tempfile

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from ..container import Container
from ..schemas.dataset_create_dto import CSV_Dataset_DTO, HF_Dataset_DTO
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.dataset_service import DatasetService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Datasets"])


@router.post("/api/v1/datasets/file")
@inject
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(..., min_length=1),
    description: str = Form(default="", min_length=1),
    license: str = Form(default=""),
    reference: str = Form(default=""),
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service]),
) -> str:
    """
    Convert a CSV dataset to the desired format.

    Args:
        dataset_data (CSV_Dataset_DTO): The data required to convert the dataset.
        dataset_service (DatasetService, optional): The service responsible for converting the dataset.
        Defaults to Depends(Provide[Container.dataset_service]).

    Returns:
        str: The path to the newly created dataset.

    Raises:
        HTTPException: An error with status code 404 if the dataset file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """

    # Create a temporary file with a secure random name
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(file.filename)[1]
    ) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        temp_file_path = tmp_file.name

    try:
        # Create the DTO with the form data including optional fields
        dataset_data = CSV_Dataset_DTO(
            name=name,
            description=description,
            license=license,
            reference=reference,
            file_path=temp_file_path,
        )
        return dataset_service.convert_dataset(dataset_data)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to convert dataset: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to convert dataset: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to convert dataset: {e.msg}"
            )
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/api/v1/datasets/hf")
@inject
def download_dataset(
    dataset_data: HF_Dataset_DTO,
    dataset_service: DatasetService = Depends(Provide[Container.dataset_service]),
) -> str:
    """
    Download a dataset from Hugging Face using the provided dataset data.

    Args:
        dataset_data (HF_Dataset_DTO): The data required to download the dataset.
        dataset_service (DatasetService, optional): The service responsible for downloading the dataset.
        Defaults to Depends(Provide[Container.dataset_service]).

    Returns:
        str: The path to the newly downloaded dataset.

    Raises:
        HTTPException: An error with status code 404 if the dataset file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return dataset_service.download_dataset(dataset_data)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to download dataset: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to download dataset: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to download dataset: {e.msg}"
            )


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
