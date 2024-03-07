from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from ..container import Container
from ..schemas.endpoint_response_model import EndpointDataModel
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..services.benchmarking_service import BenchmarkingService
from ..services.utils.exceptions_handler import SessionException
from typing import Any, Optional


router = APIRouter()

@router.get("/v1/llm_endpoints")
@inject
def get_all_endpoints(
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
) -> list[Optional[EndpointDataModel]]:
    """
    Get all the endpoints from the database
    """
    return benchmarking_service.get_all_endpoints()

@router.post("/v1/llm_endpoints")
@inject
def add_new_endpoint(
    endpoint_data: EndpointDataModel,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Add a new endpoint to the database
    """
    try:
        benchmarking_service.add_endpoint(endpoint_data)
        return {"message": "Endpoint added successfully"}
    except SessionException as e:
        return {"message": f"Failed to add endpoint: {e}"}, 500
    
@router.delete("/v1/llm_endpoints/{endpoint_id}")
@inject
async def delete_endpoint(
    endpoint_id: str,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        benchmarking_service.delete_endpoint(endpoint_id)
        return {"message": "Endpoint deleted successfully"}
    except SessionException as e:
        return {"message": f"Failed to delete endpoint: {e}"}, 500
    
@router.get("/v1/connectors")
@inject
def get_all_connectors(benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])): 
    #TODO - type check and model validation
    """
    Get all the connectors from the database
    """
    return benchmarking_service.get_all_connectors()

@router.get("/v1/recipes")
@inject
def get_all_recipes(benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])):
    """
    Get all the recipes from the database
    """
    return benchmarking_service.get_all_recipes()

@router.post("/v1/recipes")
@inject
def create_recipe(
    recipe_data: RecipeCreateDTO,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ):
    """
    Create a new recipe in the database
    """
    try:
        benchmarking_service.create_recipe(recipe_data)
        return {"message": "Recipe created successfully"}
    except SessionException as e:
        return {"message": f"Failed to create recipe: {e}"}, 500

@router.delete("/v1/recipes/{recipe_id}")
@inject
async def delete_recipe(
    recipe_id: str,
    benchmarking_service: BenchmarkingService = Depends(Provide[Container.benchmarking_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        benchmarking_service.delete_recipe(recipe_id)
        return {"message": "Recipe deleted successfully"}
    except SessionException as e:
        return {"message": f"Failed to delete endpoint: {e}"}, 500
