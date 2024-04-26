import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from ..container import Container
from ..services.utils.exceptions_handler import ServiceException
from ..services.metric_service import MetricService

router = APIRouter()

@router.get("/api/v1/metrics")
@inject
def get_all_metrics(
    metric_service: MetricService = Depends(Provide[Container.metric_service])
    ) -> list[str]:
    """
    Get all the metrics from the database
    """
    try:
        return metric_service.get_all_metric()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)

@router.delete("/api/v1/metrics/{metric_id}")
@inject
def delete_metric(
    metric_id: str,
    metric_service: MetricService = Depends(Provide[Container.metric_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        metric_service.delete_metric(metric_id)
        return {"message": "Metric deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete metric: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete metric: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete metric: {e.msg}")    