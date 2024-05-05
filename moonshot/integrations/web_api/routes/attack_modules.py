from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from ..container import Container
from ..services.attack_module_service import AttackModuleService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.get("/api/v1/attack-modules")
@inject
def get_all_attack_module(am_service: AttackModuleService = Depends(Provide[Container.am_service])
    ):
    """
    Get all the attack modules from the database
    """
    try:
        return am_service.get_all_attack_module()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve attack modules: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve attack modules: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve attack modules: {e.msg}")   
