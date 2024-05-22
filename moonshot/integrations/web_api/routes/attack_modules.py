from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..services.attack_module_service import AttackModuleService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Attack Modules"])


@router.get("/api/v1/attack-modules")
@inject
def get_all_attack_module(
    am_service: AttackModuleService = Depends(Provide[Container.am_service]),
) -> list[str]:
    """
    Retrieve all attack modules from the database.

    Args:
        am_service (AttackModuleService): The service responsible for fetching attack modules.

    Returns:
        list: A list of attack modules if successful.

    Raises:
        HTTPException: An error with status code 404 if attack modules file is not found.
        HTTPException: An error with status code 400 if there is a validation error with the request.
        HTTPException: An error with status code 500 for any other type of server-side error.
    """
    try:
        return am_service.get_all_attack_module()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve attack modules: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve attack modules: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve attack modules: {e.msg}"
            )


@router.get("/api/v1/attack-modules/metadata")
@inject
def get_all_attack_module_metadata(
    am_service: AttackModuleService = Depends(Provide[Container.am_service]),
) -> list:
    try:
        return am_service.get_all_attack_module_metadata()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve attack modules: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve attack modules: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve attack modules: {e.msg}"
            )
