from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..schemas.endpoint_create_dto import EndpointCreateDTO
from ..container import Container
from ..schemas.endpoint_response_model import EndpointDataModel
from ..services.endpoint_service import EndpointService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional

router = APIRouter()

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

@router.delete("/v1/llm_endpoints/{endpoint_id}")
@inject
async def delete_endpoint(
    endpoint_id: str,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:
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
def get_all_connectors(endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service])): 
    #TODO - type check and model validation
    return endpoint_service.get_all_connectors() 