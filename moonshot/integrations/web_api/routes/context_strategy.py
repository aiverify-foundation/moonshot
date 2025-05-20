from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..services.context_strategy_service import ContextStrategyService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Context Strategy"])


@router.get("/api/v1/context-strategies")
@inject
def get_all_context_strategies(
    context_strategy_service: ContextStrategyService = Depends(
        Provide[Container.context_strategy_service]
    ),
) -> list[dict]:
    """
    Retrieve all context strategies from the database.

    Args:
        context_strategy_service (ContextStrategyService): The service responsible for retrieving context strategies.

    Returns:
        list[dict]: A list of context strategies with details.

    Raises:
        HTTPException: An error with status code 404 if no context strategies are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return context_strategy_service.get_ctx_strategy()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404,
                detail=f"Failed to retrieve context strategies: {e.msg}",
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400,
                detail=f"Failed to retrieve context strategies: {e.msg}",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve context strategies: {e.msg}",
            )


@router.get("/api/v1/context-strategies/name")
@inject
def get_all_context_strategies_name(
    context_strategy_service: ContextStrategyService = Depends(
        Provide[Container.context_strategy_service]
    ),
) -> list[str]:
    """
    Retrieve all context strategies from the database.

    Args:
        context_strategy_service (ContextStrategyService): The service responsible for retrieving context strategies.

    Returns:
        list[str]: A list of context strategies.

    Raises:
        HTTPException: An error with status code 404 if no context strategies are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return context_strategy_service.get_ctx_strategy_name()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404,
                detail=f"Failed to retrieve context strategies: {e.msg}",
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400,
                detail=f"Failed to retrieve context strategies: {e.msg}",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve context strategies: {e.msg}",
            )


@router.delete("/api/v1/context-strategies/{ctx_strategy_name}")
@inject
def delete_context_strategy(
    ctx_strategy_name: str,
    context_strategy_service: ContextStrategyService = Depends(
        Provide[Container.context_strategy_service]
    ),
) -> dict[str, bool]:
    """
    Delete a context strategy from the database by its name.

    Args:
        ctx_strategy_name (str): The name of the context strategy to delete.
        context_strategy_service (ContextStrategyService): The service responsible for deleting the context strategy.

    Returns:
        dict[str, bool]: A dictionary with a key 'success' indicating the result of the deletion operation.

    Raises:
        HTTPException: An error with status code 404 if the context strategy is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        context_strategy_service.delete_ctx_strategy(ctx_strategy_name)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete context strategy: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete context strategy: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete context strategy: {e.msg}"
            )
