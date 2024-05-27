from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from ..container import Container
from ..schemas.recipe_create_dto import RecipeCreateDTO, RecipeUpdateDTO
from ..schemas.recipe_response_model import RecipeResponseModel
from ..services.recipe_service import RecipeService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Recipe"])


@router.post("/api/v1/recipes")
@inject
def create_recipe(
    recipe_data: RecipeCreateDTO,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> dict[str, str]:
    """
    Endpoint to add a new recipe to the database.

    Parameters:
        recipe_data (RecipeCreateDTO): The data transfer object containing the recipe details.
        recipe_service (RecipeService): The service layer responsible for the creation logic.

    Returns:
        dict[str, str]: A dictionary with a message indicating the successful creation of the recipe.

    Raises:
        HTTPException: 404 if the recipe cannot be created because the file is not found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
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
    ids: Optional[str] = Query(None, description="Get recipes to query"),
    tags: Optional[str] = Query(None, description="Filter recipes by tags"),
    categories: str = Query(None, description="Filter recipes by categories"),
    sort_by: Optional[str] = Query(
        None, description="Sort recipes by a specific field"
    ),
    count: bool = Query(False, description="Whether to include the count of recipes"),
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> list[RecipeResponseModel]:
    """
    Endpoint to retrieve all recipes from the database, with optional filters, sorting, and count inclusion.

    Parameters:
        ids (str, optional): Filter to retrieve recipes by list of comma separated recipe ids.
        tags (str, optional): Filter to retrieve recipes by tags.
        categories (str, optional): Filter to retrieve recipes by categories.
        sort_by (str, optional): Parameter to sort recipes by a specific field.
        count (bool, optional): Flag to indicate whether to include the count of recipes in the response.
        recipe_service (RecipeService): The service layer responsible for the retrieval logic.

    Returns:
        list[RecipeResponseModel]: A list of recipe, filtered, sorted, and with counts.

    Raises:
        HTTPException: 404 if no recipes are found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
    """
    try:
        recipes = recipe_service.get_all_recipes(
            tags=tags, categories=categories, sort_by=sort_by, count=count, ids=ids
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
) -> list[str]:
    """
    Endpoint to retrieve all recipe names from the database.

    Parameters:
        recipe_service (RecipeService): The service layer responsible for retrieving recipe names.

    Returns:
        list[str]: A list of recipe names.

    Raises:
        HTTPException: 404 if no recipe names are found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
    """
    try:
        recipes = recipe_service.get_all_recipes_name()
        return recipes
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve recipe names: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve recipe names: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve recipe names: {e.msg}"
            )


@router.put("/api/v1/recipes/{recipe_id}")
@inject
async def update_recipe(
    recipe_data: RecipeUpdateDTO,
    recipe_id: str,
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> dict[str, str]:
    """
    Endpoint to update an existing recipe in the database by its ID.

    Parameters:
        recipe_data (RecipeCreateDTO): The data transfer object containing the updated recipe details.
        recipe_id (str): The unique identifier of the recipe to update.
        recipe_service (RecipeService): The service layer responsible for the update logic.

    Returns:
        dict[str, str]: A dictionary with a message indicating the successful update of the recipe.

    Raises:
        HTTPException: 404 if the recipe to be updated cannot be found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
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
) -> dict[str, str]:
    """
    Endpoint to delete a recipe from the database by its ID.

    Parameters:
        recipe_id (str): The unique identifier of the recipe to delete.
        recipe_service (RecipeService): The service layer responsible for the deletion logic.

    Returns:
        dict[str, str]: A dictionary with a message indicating the successful deletion of the recipe.

    Raises:
        HTTPException: 404 if the recipe to be deleted cannot be found.
                       400 if there is a validation error with the provided data.
                       500 for any other internal server error.
    """
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
