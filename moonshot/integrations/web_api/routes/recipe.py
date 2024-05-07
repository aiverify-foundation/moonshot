from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from ..container import Container
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..schemas.recipe_response_dto import RecipeResponseDTO
from ..services.recipe_service import RecipeService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter()


@router.post("/api/v1/recipes")
@inject
def create_recipe(
    recipe_data: RecipeCreateDTO,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
):
    """
    Add a new recipe to the database
    """
    try:
        recipe_service.create_recipe(recipe_data)
        return {"message": "Recipe created successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to create recipe: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to create recipe: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to create recipe: {e.msg}"
            )


@router.get("/api/v1/recipes")
@inject
def get_all_recipes(
    tags: str = Query(None, description="Filter recipes by tags"),
    sort_by: str = Query(None, description="Sort recipes by a specific field"),
    count: bool = Query(False, description="Whether to include the count of recipes"),
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
):
    """
    Get all the recipes from the database
    """
    try:
        recipes = recipe_service.get_all_recipes(
            tags=tags, sort_by=sort_by, count=count
        )
        return recipes
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve recipes: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve recipes: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve recipes: {e.msg}"
            )


@router.get("/api/v1/recipes/name")
@inject
def get_all_recipes_name(
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
):
    """
    Get all the recipes name from the database
    """
    try:
        recipes = recipe_service.get_all_recipes_name()
        return recipes
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve recipes name: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve recipes name: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve recipes name: {e.msg}"
            )


@router.get("/api/v1/recipes/ids/")
@inject
def get_recipe_by_ids(
    recipe_id: str = Query(None, description="Get recipes to query"),
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> list[RecipeResponseDTO | None]:
    """
    Get a recipe from the database
    """
    try:
        recipe = recipe_service.get_recipe_by_ids(recipe_id)
        return recipe
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve recipe: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve recipe: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve recipe: {e.msg}"
            )


@router.put("/api/v1/recipes/{recipe_id}")
@inject
async def update_recipe(
    recipe_data: RecipeCreateDTO,
    recipe_id: str,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Update an existing recipe in the database
    """
    try:
        recipe_service.update_recipe(recipe_data, recipe_id)
        return {"message": "Recipe updated successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to update recipe: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to update recipe: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to update recipe: {e.msg}"
            )


@router.delete("/api/v1/recipes/{recipe_id}")
@inject
def delete_recipe(
    recipe_id: str,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> dict[str, str] | tuple[dict[str, str], int]:
    try:
        recipe_service.delete_recipe(recipe_id)
        return {"message": "Recipe deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete recipe: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete recipe: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete recipe: {e.msg}"
            )
