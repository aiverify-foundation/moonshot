from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from ..container import Container
from ..schemas.cookbook_create_dto import CookbookCreateDTO, CookbookUpdateDTO
from ..schemas.cookbook_response_model import CookbookResponseModel
from ..services.cookbook_service import CookbookService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Cookbook"])


@router.post("/api/v1/cookbooks")
@inject
def create_cookbook(
    cookbook_data: CookbookCreateDTO,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> dict[str, str]:
    """
    Endpoint to create a new cookbook entry in the database.

    Parameters:
        cookbook_data (CookbookCreateDTO): The DTO containing the details for the new cookbook.
        cookbook_service (CookbookService): The service layer responsible for the creation logic.

    Returns:
        dict[str, str]: A dictionary with a message key indicating successful creation.

    Raises:
        HTTPException: 404 if the cookbook cannot be found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
    """
    try:
        cookbook_service.create_cookbook(cookbook_data)
        return {"message": "Cookbook created successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to create cookbook: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to create cookbook: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to create cookbook: {e.msg}"
            )


@router.get("/api/v1/cookbooks")
@inject
def get_all_cookbooks(
    ids: Optional[str] = Query(None, description="Get recipes to query"),
    tags: Optional[str] = Query(None, description="Filter cookbooks by tags"),
    categories: Optional[str] = Query(
        None, description="Filter cookbooks by categories"
    ),
    categories_excluded: Optional[str] = Query(
        None, description="Filter out (exlude) cookbooks by categories"
    ),
    count: bool = Query(False, description="Whether to include the count of recipes"),
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> list[CookbookResponseModel]:
    """
    Endpoint to retrieve a list of all cookbooks, with optional filtering.

    Parameters:
        ids (Optional[str]): A string to filter cookbooks by ids.
        tags (Optional[str]): A string to filter cookbooks by tags.
        categories (Optional[str]): A string to filter cookbooks by categories.
        categories_excluded (Optional[str]): A string to filter out (exclude) cookbooks by categories.
        count (bool): A flag to decide if the count of recipes should be included.
        cookbook_service (CookbookService): The service layer responsible for retrieval logic.

    Returns:
        list[CookbookResponseModel]: A list of CookbookResponseModel instances that match the filters.

    Raises:
        HTTPException: 404 if no cookbooks could be found.
                       400 if there is a validation error with the filters.
                       500 for any other internal server error.
    """
    try:
        cookbooks = cookbook_service.get_all_cookbooks(
            tags=tags,
            categories=categories,
            count=count,
            ids=ids,
            categories_excluded=categories_excluded,
        )
        return cookbooks
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve cookbooks: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve cookbooks: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve cookbooks: {e.msg}"
            )


@router.get("/api/v1/cookbooks/name")
@inject
def get_all_cookbooks_name(
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> list[str]:
    """
    Endpoint to retrieve the names of all cookbooks in the database.

    Parameters:
        cookbook_service (CookbookService): The service layer responsible for retrieving the names.

    Returns:
        list[str]: A list of strings representing the names of all cookbooks.

    Raises:
        HTTPException: 404 if no cookbook names could be found.
                       400 if there is a validation error.
                       500 for any other internal server error.
    """
    try:
        cookbooks = cookbook_service.get_all_cookbooks_names()
        return cookbooks
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve cookbooks: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve cookbooks: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve cookbooks: {e.msg}"
            )


@router.put("/api/v1/cookbooks/{cookbook_id}")
@inject
def update_cookbook(
    cookbook_id: str,
    cookbook_data: CookbookUpdateDTO,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> dict[str, str]:
    """
    Endpoint to update the details of an existing cookbook in the database.

    Parameters:
        cookbook_id (str): The unique identifier of the cookbook to be updated.
        cookbook_data (CookbookCreateDTO): The DTO containing the updated details for the cookbook.
        cookbook_service (CookbookService): The service layer responsible for the update logic.

    Returns:
        dict[str, str]: A dictionary with a message key indicating successful update.

    Raises:
        HTTPException: 404 if the cookbook with the given ID cannot be found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
    """
    try:
        cookbook_service.update_cookbook(cookbook_data, cookbook_id)
        return {"message": "Cookbook updated successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to update cookbook: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to update cookbook: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to update cookbook: {e.msg}"
            )


@router.delete("/api/v1/cookbooks/{cb_id}")
@inject
def delete_cookbook(
    cb_id: str,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> dict[str, str]:
    """
    Endpoint to delete a cookbook entry from the database using its ID.

    Parameters:
        cb_id (str): The unique identifier of the cookbook to be deleted.
        cookbook_service (CookbookService): The service layer responsible for the deletion logic.

    Returns:
        dict[str, str]: A dictionary with a message key indicating successful deletion.

    Raises:
        HTTPException: 404 if the cookbook with the given ID cannot be found.
                       400 if there is a validation error.
                       500 for any other internal server error.
    """
    try:
        cookbook_service.delete_cookbook(cb_id)
        return {"message": "Cookbook deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete cookbook: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete cookbook: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete cookbook: {e.msg}"
            )
