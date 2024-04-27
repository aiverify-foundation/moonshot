from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..container import Container
from ..services.runner_service import RunnerService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.get("/api/v1/runs")
@inject
def get_all_runners(runner_service: RunnerService = Depends(Provide[Container.runner_service])
    ):
    """
    Get all the runs from the database
    """
    try:
        return runner_service.get_all_runner()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve runners: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve runners: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve runners: {e.msg}")   


@router.get("/api/v1/runs/name")
@inject
def get_all_runner_name(runner_service: RunnerService = Depends(Provide[Container.runner_service])
    ):
    """
    Get all the runs name from the database
    """
    try:
        return runner_service.get_all_runner_name()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve runners: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve runners: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve runners: {e.msg}")       
                         

@router.get("/api/v1/runs/{runner_id}")
@inject 
def get_runner_by_id(
    runner_id: str,
    runner_service: RunnerService = Depends(Provide[Container.runner_service])
    ) -> dict | None:
    """
    Get a run from the database
    """
    try:
        run = runner_service.get_runner_by_id(runner_id)
        return run
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve run: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve run: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve run: {e.msg}")


@router.delete("/api/v1/runs/{runner_id}")
@inject
def delete_recipe(
    runner_id: str,
    runner_service: RunnerService = Depends(Provide[Container.runner_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        runner_service.delete_run(runner_id)
        return {"message": "Run deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete run: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete run: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete run: {e.msg}")    
    