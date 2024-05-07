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
) -> dict:
    """
    Add a new recipe to the database.

    Args:
        recipe_data (RecipeCreateDTO): The data transfer object containing the recipe details.
        recipe_service (RecipeService): The service responsible for creating the recipe.

    Returns:
        Dict[str, str]: A message indicating the successful creation of the recipe.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
) -> list:
    """
    Get all the recipes from the database.

    Args:
        tags (str): Filter parameter to filter recipes by tags.
        sort_by (str): Filter parameter to sort recipes by a specific field.
        count (bool): Flag to indicate whether to include the count of recipes.
        recipe_service (RecipeService): The service responsible for retrieving recipes.

    Returns:
        List: A list of recipes.

    Raises:
        HTTPException: An error with status code 404 if no recipes are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
) -> list[str]:
    """
    Get all the recipe names from the database.

    Args:
        recipe_service (RecipeService): The service responsible for retrieving recipe names.

    Returns:
        List[str]: A list of recipe names.

    Raises:
        HTTPException: An error with status code 404 if no recipe names are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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


@router.get("/api/v1/recipes/ids/")
@inject
def get_recipe_by_ids(
    recipe_id: str = Query(None, description="Get recipes to query"),
    recipe_service: RecipeService = Depends(Provide[Container.recipe_service]),
) -> list[RecipeResponseDTO]:
    """
    Get a recipe from the database by its ID.

    Args:
        recipe_id (str): The unique identifier of the recipe to retrieve.
        recipe_service (RecipeService): The service responsible for retrieving the recipe.

    Returns:
        List[Union[RecipeResponseDTO, None]]: A list containing the recipe or None if not found.

    Raises:
        HTTPException: An error with status code 404 if the recipe is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
) -> dict[str, str]:
    """
    Update an existing recipe in the database by its ID.

    Args:
        recipe_data (RecipeCreateDTO): The data transfer object containing the updated recipe details.
        recipe_id (str): The unique identifier of the recipe to update.
        recipe_service (RecipeService): The service responsible for updating the recipe.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A message indicating the successful update of the recipe,
        or an HTTPException with an appropriate status code.

    Raises:
        HTTPException: An error with status code 404 if the recipe is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
    Delete a recipe from the database by its ID.

    Args:
        recipe_id (str): The unique identifier of the recipe to delete.
        recipe_service (RecipeService): The service responsible for deleting the recipe.

    Returns:
        Union[Dict[str, str], Tuple[Dict[str, str], int]]: A message indicating the successful deletion of the recipe,
        or an HTTPException with an appropriate status code.

    Raises:
        HTTPException: An error with status code 404 if the recipe is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
