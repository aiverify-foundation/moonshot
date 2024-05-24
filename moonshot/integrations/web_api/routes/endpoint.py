from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.endpoint_create_dto import EndpointCreateDTO, EndpointUpdateDTO
from ..schemas.endpoint_response_model import EndpointDataModel
from ..services.endpoint_service import EndpointService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Endpoint"])


@router.post("/api/v1/llm-endpoints")
@inject
def add_new_endpoint(
    endpoint_data: EndpointCreateDTO,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Add a new endpoint to the database.

    Args:
        endpoint_data (EndpointCreateDTO): The data transfer object containing endpoint details.
        endpoint_service (EndpointService): The service responsible for adding the endpoint.

    Returns:
        dict[str, str]: A message indicating the successful addition of the endpoint.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        endpoint_service.add_endpoint(endpoint_data)
        return {"message": "Endpoint added successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to add endpoint: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to add endpoint: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to add endpoint: {e.msg}"
            )


@router.get("/api/v1/llm-endpoints")
@inject
def get_all_endpoints(
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> list[Optional[EndpointDataModel]]:
    """
    Get all the endpoints from the database.

    Args:
        endpoint_service (EndpointService): The service responsible for retrieving all endpoints.

    Returns:
        list[Optional[EndpointDataModel]]: A list of endpoint data models,
        which may contain None if an endpoint is not found.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        endpoint_models = endpoint_service.get_all_endpoints()
        for endpoint_model in endpoint_models:
            endpoint_model.mask_token()
        return endpoint_models
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to get endpoint: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to get endpoint: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to get endpoint: {e.msg}"
            )


@router.get("/api/v1/llm-endpoints/name")
@inject
def get_all_endpoints_name(
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> list[Optional[str]]:
    """
    Get all the endpoint names from the database.

    Args:
        endpoint_service (EndpointService): The service responsible for retrieving all endpoint names.

    Returns:
        list[Optional[str]]: A list of endpoint names, which may contain None if an endpoint name is not found.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return endpoint_service.get_all_endpoints_names()
    except ServiceException as e:
        error_status_code = 500
        if e.error_code == "FileNotFound":
            error_status_code = 404
        elif e.error_code == "ValidationError":
            error_status_code = 400
        raise HTTPException(
            status_code=error_status_code,
            detail=f"Failed to get endpoint names: {e.msg}",
        )


@router.get("/api/v1/llm-endpoints/{endpoint_id}")
@inject
def get_endpoint(
    endpoint_id: str,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> EndpointDataModel | None:
    """
    Get an endpoint from the database by its ID.

    Args:
        endpoint_id (str): The unique identifier of the endpoint to retrieve.
        endpoint_service (EndpointService): The service responsible for retrieving the endpoint.

    Returns:
        EndpointDataModel | None: The endpoint data model if found, otherwise None.

    Raises:
        HTTPException: An error with status code 404 if the endpoint is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        endpoint_model = endpoint_service.get_endpoint(endpoint_id)
        if endpoint_model:
            endpoint_model.mask_token()
        return endpoint_model
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to get endpoint: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to get endpoint: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to get endpoint: {e.msg}"
            )


@router.put("/api/v1/llm-endpoints/{endpoint_id}")
@inject
async def update_endpoint(
    endpoint_id: str,
    endpoint_data: EndpointUpdateDTO,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Update an existing endpoint in the database by its ID.

    Args:
        endpoint_id (str): The unique identifier of the endpoint to update.
        endpoint_data (EndpointCreateDTO): The data transfer object containing the updated endpoint details.
        endpoint_service (EndpointService): The service responsible for updating the endpoint.

    Returns:
        dict[str, str]: A message indicating the successful update of the endpoint.

    Raises:
        HTTPException: An error with status code 404 if the endpoint is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        endpoint_service.update_endpoint(endpoint_id, endpoint_data)
        return {"message": "Endpoint updated successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to update endpoint: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to update endpoint: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to update endpoint: {e.msg}"
            )


@router.delete("/api/v1/llm-endpoints/{endpoint_id}")
@inject
async def delete_endpoint(
    endpoint_id: str,
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete an existing endpoint from the database by its ID.

    Args:
        endpoint_id (str): The unique identifier of the endpoint to delete.
        endpoint_service (EndpointService): The service responsible for deleting the endpoint.

    Returns:
        dict[str, str]: A message indicating the successful deletion of the endpoint.

    Raises:
        HTTPException: An error with status code 404 if the endpoint is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        endpoint_service.delete_endpoint(endpoint_id)
        return {"message": "Endpoint deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete endpoint: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete endpoint: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete endpoint: {e.msg}"
            )


@router.get("/api/v1/connectors")
@inject
def get_all_connectors(
    endpoint_service: EndpointService = Depends(Provide[Container.endpoint_service]),
) -> list[Optional[str]]:
    """
    Get all the connector types from the database.

    Args:
        endpoint_service (EndpointService): The service responsible for retrieving all connector types.

    Returns:
        list[Optional[str]]: A list of connector types, which may contain None if a connector type is not found.

    Raises:
        HTTPException: An error with status code 404 if the file is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    # TODO - type check and model validation
    try:
        return endpoint_service.get_all_connectors()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to get connector types: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to get connector types: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to get connector types: {e.msg}"
            )
