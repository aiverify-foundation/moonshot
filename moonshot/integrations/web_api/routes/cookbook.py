from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..schemas.cookbook_create_dto import CookbookCreateDTO
from ..container import Container
from ..services.cookbook_service import CookbookService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.post("/v1/cookbooks")
@inject
def create_cookbook(
    cookbook_data: CookbookCreateDTO,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])
    ):
    """
    Add a new cookbook to the database
    """
    try:
        cookbook_service.create_cookbook(cookbook_data)
        return {"message": "Cookbook created successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to create cookbook: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to create cookbook: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to create cookbook: {e.msg}")    


@router.get("/v1/cookbooks")
@inject
def get_all_cookbooks(
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])
    ):
    """
    Get all the cookbooks from the database
    """
    try:
        cookbooks = cookbook_service.get_all_cookbooks()
        return cookbooks
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve cookbooks: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve cookbooks: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cookbooks: {e.msg}")    
    

@router.get("/v1/cookbooks/name")
@inject
def get_all_cookbooks_name(
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])
    ) -> list[Optional[str]]:
    """
    Get all the cookbooks name from the database
    """
    try:
        cookbooks = cookbook_service.get_all_cookbooks_names()
        return cookbooks
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve cookbooks: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve cookbooks: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cookbooks: {e.msg}")       


@router.get("/v1/cookbooks/{cookbook_id}")
@inject
def get_cookbook_by_id(
    cookbook_id: str,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])): 
    """
    Get a cookbook from the database
    """
    try:
        cookbook = cookbook_service.get_cookbook_by_id(cookbook_id)
        return cookbook
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve cookbook: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve cookbook: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cookbook: {e.msg}")    


@router.put("/v1/cookbooks/{cookbook_id}")
@inject
def update_cookbook(
    cookbook_id: str,
    cookbook_data: CookbookCreateDTO,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])):
    """
    Update an existing cookbook in the database
    """
    try:
        cookbook_service.update_cookbook(cookbook_data, cookbook_id)
        return {"message": "Cookbook updated successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to update cookbook: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to update cookbook: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to update cookbook: {e.msg}")    
        

@router.delete("/v1/cookbooks/{cb_id}")
@inject
def delete_cookbook(
    cb_id: str,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete an existing cookbook from the database
    """
    try:
        cookbook_service.delete_cookbook(cb_id)
        return {"message": "Cookbook deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete endpoint: {e.msg}") 
