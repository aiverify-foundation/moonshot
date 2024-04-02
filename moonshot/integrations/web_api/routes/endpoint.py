from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide

from ..schemas.endpoint_create_dto import EndpointCreateDTO
from ..container import Container
from ..schemas.endpoint_response_model import EndpointDataModel
from ..services.endpoint_service import EndpointService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.post("/v1/llm_endpoints")
@inject
def add_new_endpoint(
    endpoint_data: EndpointCreateDTO,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Add a new endpoint to the database
    """
    try:
        endpoint_service.add_endpoint(endpoint_data)
        return {"message": "Endpoint added successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to add endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to add endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to add endpoint: {e.msg}")    
        

@router.get("/v1/llm_endpoints")
@inject
def get_all_endpoints(
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
) -> list[Optional[EndpointDataModel]]:
    """
    Get all the endpoints from the database
    """
    try:
        return endpoint_service.get_all_endpoints()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to get endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to get endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get endpoint: {e.msg}")    


@router.get("/v1/llm_endpoints/name")
@inject
def get_all_endpoints_name(
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
) -> list[Optional[str]]:
    """
    Get all the endpoints name from the database
    """
    try:
        return endpoint_service.get_all_endpoints_names()
    except ServiceException as e:
        error_status_code = 500
        if e.error_code == "FileNotFound":
            error_status_code = 404
        elif e.error_code == "ValidationError":
            error_status_code = 400
        raise HTTPException(status_code=error_status_code, detail=f"Failed to get endpoint: {e.msg}")


@router.get("/v1/llm_endpoints/{endpoint_id}")
@inject
def get_endpoint(
    endpoint_id: str,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
) -> EndpointDataModel | None:
    """
    Get an endpoint from the database
    """
    try:
        return endpoint_service.get_endpoint(endpoint_id)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to get endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to get endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get endpoint: {e.msg}")


@router.put("/v1/llm_endpoints/{endpoint_id}")
@inject
async def update_endpoint(
    endpoint_id: str,
    endpoint_data: EndpointCreateDTO,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Update an existing endpoint in the database
    """
    try:
        endpoint_service.update_endpoint(endpoint_id, endpoint_data)
        return {"message": "Endpoint updated successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to update endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to update endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to update endpoint: {e.msg}")


@router.delete("/v1/llm_endpoints/{endpoint_id}")
@inject
async def delete_endpoint(
    endpoint_id: str,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete an existing endpoint in the database
    """
    try:
        endpoint_service.delete_endpoint(endpoint_id)
        return {"message": "Endpoint deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete endpoint: {e.msg}")      
    
    
@router.get("/v1/connectors")
@inject
def get_all_connectors(
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
    ) -> list[Optional[str]]:
    """
    Get all the connectors type from the database
    """
    #TODO - type check and model validation
    try:
        return endpoint_service.get_all_connectors() 
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete endpoint: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete endpoint: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete endpoint: {e.msg}")      
