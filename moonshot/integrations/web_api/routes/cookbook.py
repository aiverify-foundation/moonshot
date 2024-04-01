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
    
@router.get("/v1/cookbooks/{cookbook_id}")
@inject
def get_cookbook_by_id(
    cookbook_id: str,
    cookbook_service: CookbookService = Depends(Provide[Container.cookbook_service])):
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
