from fastapi import APIRouter
from web_api.schemas.endpoint_response_model import EndpointDataModel
from web_api.services import benchmarking_service
from web_api.services.utils.exceptions_handler import SessionException

from typing import Any, Optional


router = APIRouter()

@router.get("/v1/llm_endpoints")
def get_all_endpoints() -> list[Optional[EndpointDataModel]]:
    """
    Get all the endpoints from the database
    """
    return benchmarking_service.get_all_endpoints()

@router.post("/v1/llm_endpoints")
def add_new_endpoint(endpoint_data: EndpointDataModel):
    """
    Add a new endpoint to the database
    """
    try:
        benchmarking_service.add_endpoint(endpoint_data)
        return {"message": "Endpoint added successfully"}
    except SessionException as e:
        return {"message": f"Failed to add endpoint: {e}"}, 500
    
@router.get("/v1/connectors")
def get_all_connectors(): 
    #TODO - type check and model validation
    """
    Get all the connectors from the database
    """
    return benchmarking_service.get_all_connectors()
