from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..services.metric_service import MetricService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Metric"])


@router.get("/api/v1/metrics")
@inject
def get_all_metrics(
    metric_service: MetricService = Depends(Provide[Container.metric_service]),
) -> list[dict]:
    """
    Retrieve all metrics from the database.

    Args:
        metric_service (MetricService): The service responsible for retrieving metrics.

    Returns:
        list[str]: A list of all metrics.

    Raises:
        HTTPException: An error with status code 404 if no metrics are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
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
    metric_service: MetricService = Depends(Provide[Container.metric_service]),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete a metric from the database by its ID.

    Args:
        metric_id (str): The unique identifier of the metric to delete.
        metric_service (MetricService): The service responsible for deleting the metric.

    Returns:
        dict[str, str] | tuple[dict[str, str], int]: A message indicating the successful deletion of the metric,
        or an HTTPException with an appropriate status code.

    Raises:
        HTTPException: An error with status code 404 if the metric is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        metric_service.delete_metric(metric_id)
        return {"message": "Metric deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete metric: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete metric: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete metric: {e.msg}"
            )


@router.post("/api/v1/metric/update-config")
@inject
def update_metric_config(
    metric_id: str,
    update_args: dict,
    metric_service: MetricService = Depends(Provide[Container.metric_service]),
) -> bool:
    try:
        return metric_service.update_metric_config(metric_id, update_args)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete metric config: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete metric config: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete metric config: {e.msg}"
            )


@router.post("/api/v1/metric/delete-config")
@inject
def delete_metric_config(
    metric_id: str,
    metric_service: MetricService = Depends(Provide[Container.metric_service]),
) -> bool:
    try:
        return metric_service.delete_metric_config(metric_id)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete metric config: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete metric config: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete metric_config: {e.msg}"
            )
