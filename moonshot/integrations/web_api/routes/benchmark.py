from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.benchmark_runner_dto import BenchmarkRunnerDTO
from ..services.benchmark_test_state import BenchmarkTestState
from ..services.benchmarking_service import BenchmarkingService
from ..services.utils.exceptions_handler import ServiceException
from ..types.types import BenchmarkCollectionType

router = APIRouter(tags=["Benchmarking"])


@router.post("/api/v1/benchmarks")
@inject
async def benchmark_executor(
    type: BenchmarkCollectionType,
    data: BenchmarkRunnerDTO,
    benchmarking_service: BenchmarkingService = Depends(
        Provide[Container.benchmarking_service]
    ),
) -> dict:
    """
    Execute a benchmark test.

    Args:
        type (BenchmarkCollectionType): The type of benchmark to execute.
        data (BenchmarkRunnerDTO): The data required to execute the benchmark.
        benchmarking_service (BenchmarkingService, optional): The service that will execute the benchmark.

    Returns:
        dict: A dictionary with the 'id' key containing the ID of the created execution task.

    Raises:
        HTTPException: If the provided type is invalid (status code 400) or if the service fails to create
        and execute the benchmark (status code 500).
    """
    try:
        if type is BenchmarkCollectionType.COOKBOOK:
            id = await benchmarking_service.execute_cookbook(data)
            return {"id": id}
        elif type is BenchmarkCollectionType.RECIPE:
            id = await benchmarking_service.execute_recipe(data)
            return {"id": id}
        else:
            raise HTTPException(status_code=400, detail="Invalid query parameter: type")
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
    """
    Retrieve the progress status of all benchmarks.

    Args:
        benchmark_state (BenchmarkTestState, optional): The state service that tracks benchmark progress.

    Returns:
        The progress status of all benchmarks.

    Raises:
        HTTPException: If there is an error retrieving the progress status, with a status code indicating the
        nature of the error (404 for file not found, 400 for validation error).
    """
    try:
        all_status = benchmark_state.get_all_progress_status()
        return all_status
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve progress status: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve progress status: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve progress status: {e.msg}"
            )


@router.post("/api/v1/benchmarks/cancel/{runner_id}")
@inject
async def cancel_benchmark_executor(
    runner_id: str,
    benchmarking_service: BenchmarkingService = Depends(
        Provide[Container.benchmarking_service]
    ),
):
    """
    Cancel a benchmark execution task.

    Args:
        runner_id (str): The ID of the runner executing the benchmark.
        benchmarking_service (BenchmarkingService): The service that will cancel the benchmark execution.

    Returns:
        None

    Raises:
        HTTPException: If the service is unable to cancel the benchmark, with a status code
        500 indicating an internal server error.
    """
    try:
        await benchmarking_service.cancel_executor(runner_id)
    except ServiceException as e:
        raise HTTPException(status_code=500, detail=f"Unable to cancel benchmark: {e}")
