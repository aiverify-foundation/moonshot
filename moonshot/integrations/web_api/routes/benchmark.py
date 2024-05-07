from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.benchmark_runner_dto import BenchmarkRunnerDTO
from ..services.benchmark_test_state import BenchmarkTestState
from ..services.benchmarking_service import BenchmarkingService
from ..services.utils.exceptions_handler import ServiceException
from ..types.types import BenchmarkCollectionType

router = APIRouter()


@router.post("/api/v1/benchmarks")
@inject
async def benchmark_executor(
    type: BenchmarkCollectionType,
    data: BenchmarkRunnerDTO,
    benchmarking_service: BenchmarkingService = Depends(
        Provide[Container.benchmarking_service]
    ),
):
    try:
        if type is BenchmarkCollectionType.COOKBOOK:
            id = await benchmarking_service.execute_cookbook(data)
        elif type is BenchmarkCollectionType.RECIPE:
            id = await benchmarking_service.execute_recipe(data)
        else:
            raise HTTPException(status_code=400, detail="Invalid query parameter: type")
        if id:
            return {"message": "Execution task created", "id": id}
    except ServiceException as e:
        raise HTTPException(
            status_code=500, detail=f"Unable to create and execute benchmark: {e}"
        )


@router.get("/api/v1/benchmarks/status")
@inject
def get_benchmark_progress(
    benchmark_state: BenchmarkTestState = Depends(
        Provide[Container.benchmark_test_state]
    ),
):
    try:
        state = benchmark_state.get_state()
        if not state:
            return {}
        for _, item in state.items():
            item.pop("async_task", None)
            # Flatten the "status" dictionary into the task dictionary
            if "status" in item:
                status = item.pop("status")
                item.update(status)

        return state
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve progress status: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve progress status: {e.msg}"
            )


@router.post("/api/v1/benchmarks/cancel/{runner_id}")
@inject
async def cancel_benchmark_executor(
    runner_id: str,
    benchmarking_service: BenchmarkingService = Depends(
        Provide[Container.benchmarking_service]
    ),
):
    try:
        await benchmarking_service.cancel_executor(runner_id)
    except ServiceException as e:
        raise HTTPException(status_code=500, detail=f"Unable to cancel benchmark: {e}")
