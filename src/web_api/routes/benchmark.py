from fastapi import APIRouter
from web_api.schemas.endpoint_response_model import EndpointDataModel
from web_api.services import benchmarking_service

from typing import Any, Optional

router = APIRouter()

@router.get("/v1/llm_endpoints")
def get_all() -> list[Optional[EndpointDataModel]]:
    """
    Get all the endpoints from the database
    """
    return benchmarking_service.get_all_endpoints()


