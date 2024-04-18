from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from ..container import Container
from ..services.attack_strategy_service import AttackStrategyService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.get("/v1/attack_strategies")
@inject
def get_all_attack_strategy(as_service: AttackStrategyService = Depends(Provide[Container.as_service])
    ):
    """
    Get all the attack strategies from the database
    """
    try:
        return as_service.get_all_attack_strategies()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve attack strategies: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve attack strategies: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve attack strategies: {e.msg}")   


@router.get("/v1/attack_strategies/{as_id}")
@inject 
def get_attack_strategy_by_id(
    as_id: str,
    as_service: AttackStrategyService = Depends(Provide[Container.as_service])
    ) -> str:
    """
    Get a attack strategy from the database
    """
    try:
        am = as_service.get_attack_strategy_by_id(as_id)
        return am
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve attack strategy: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve attack strategy: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve attack strategy: {e.msg}")
