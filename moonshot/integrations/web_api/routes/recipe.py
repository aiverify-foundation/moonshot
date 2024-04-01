from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..container import Container
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..services.recipe_service import RecipeService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.get("/v1/recipes")
@inject
def get_all_recipes(recipe_service: RecipeService = Depends(Provide[Container.recipe_service])):
    try:
        return recipe_service.get_all_recipes()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve recipes: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve recipes: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve recipes: {e.msg}")   

@router.post("/v1/recipes")
@inject
def create_recipe(
    recipe_data: RecipeCreateDTO,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service])
    ):
    try:
        recipe_service.create_recipe(recipe_data)
        return {"message": "Recipe created successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to create recipe: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to create recipe: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to create recipe: {e.msg}")    

@router.delete("/v1/recipes/{recipe_id}")
@inject
async def delete_recipe(
    recipe_id: str,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        recipe_service.delete_recipe(recipe_id)
        return {"message": "Recipe deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete recipe: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete recipe: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete recipe: {e.msg}")    
    
