from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from ..container import Container
from ..schemas.cookbook_create_dto import CookbookCreateDTO
from ..services.cookbook_service import CookbookService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter()


@router.post("/api/v1/cookbooks")
@inject
def create_cookbook(
    cookbook_data: CookbookCreateDTO,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> dict:
    """
    Create a new cookbook and add it to the database.

    Args:
        cookbook_data (CookbookCreateDTO): The data transfer object containing cookbook details.
        cookbook_service (CookbookService): The service responsible for creating the cookbook.

    Returns:
        dict: A message indicating the successful creation of the cookbook.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
    tags: Optional[str] = Query(None, description="Filter cookbooks by tags"),
    categories: Optional[str] = Query(
        None, description="Filter cookbooks by categories"
    ),
    count: bool = Query(False, description="Whether to include the count of recipes"),
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> list:
    """
    Retrieve all cookbooks from the database with optional filters.

    Args:
        tags (Optional[str]): Filter cookbooks by tags.
        categories (Optional[str]): Filter cookbooks by categories.
        count (bool): Whether to include the total number of prompts in the response.
        cookbook_service (CookbookService): The service responsible for retrieving cookbooks.

    Returns:
        list: A list of cookbooks that match the given filters.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        cookbooks = cookbook_service.get_all_cookbooks(
            tags=tags, categories=categories, count=count
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
) -> list[Optional[str]]:
    """
    Retrieve the names of all cookbooks from the database.

    Args:
        cookbook_service (CookbookService): The service responsible for retrieving cookbook names.

    Returns:
        list[Optional[str]]: A list of cookbook names.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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


@router.get("/api/v1/cookbooks/ids/")
@inject
def get_cookbook_by_id(
    cookbook_id: Optional[str] = Query(None, description="Get cookbooks to query"),
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> dict:
    """
    Retrieve a cookbook from the database by its ID.

    Args:
        cookbook_id (Optional[str]): The ID of the cookbook to retrieve.
        cookbook_service (CookbookService): The service responsible for retrieving the cookbook.

    Returns:
        dict: The cookbook corresponding to the provided ID.

    Raises:
        HTTPException: An error with status code 404 if the cookbook is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        cookbook = cookbook_service.get_cookbook_by_ids(cookbook_id)
        return cookbook
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve cookbook: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve cookbook: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve cookbook: {e.msg}"
            )


@router.put("/api/v1/cookbooks/{cookbook_id}")
@inject
def update_cookbook(
    cookbook_id: str,
    cookbook_data: CookbookCreateDTO,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service]),
) -> dict:
    """
    Update an existing cookbook in the database.

    Args:
        cookbook_id (str): The ID of the cookbook to update.
        cookbook_data (CookbookCreateDTO): The updated data for the cookbook.
        cookbook_service (CookbookService): The service responsible for updating the cookbook.

    Returns:
        dict: A message indicating the successful update of the cookbook.

    Raises:
        HTTPException: An error with status code 404 if the cookbook is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete an existing cookbook from the database.

    Args:
        cb_id (str): The ID of the cookbook to delete.
        cookbook_service (CookbookService): The service responsible for deleting the cookbook.

    Returns:
        dict[str, str] | tuple[dict[str, str], int]: A message indicating the successful deletion of the cookbook,
        or an HTTPException with an appropriate status code.

    Raises:
        HTTPException: An error with status code 404 if the cookbook is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        cookbook_service.delete_cookbook(cb_id)
        return {"message": "Cookbook deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete endpoint: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete endpoint: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete endpoint: {e.msg}"
            )
