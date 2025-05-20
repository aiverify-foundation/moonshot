from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..services.benchmark_result_service import BenchmarkResultService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Benchmark Results"])


@router.get("/api/v1/benchmarks/results")
@inject
async def get_all_results(
    benchmark_result_service: BenchmarkResultService = Depends(
        Provide[Container.benchmark_result_service]
    ),
) -> list[dict]:
    """
    Retrieve all benchmark results.

    This endpoint retrieves a list of all benchmark results from the database. Each benchmark result is
    represented as a dictionary containing its associated data.

    Args:
        benchmark_result_service (BenchmarkResultService): The service responsible for fetching benchmark results.

    Returns:
        list[dict]: A list of dictionaries, each representing a single benchmark result.

    Raises:
        HTTPException: Raised if the results file cannot be found (404) or if an unspecified error occurs (500).
    """
    try:
        results = benchmark_result_service.get_all_results()
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve results: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve results: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve results: {e.msg}"
            )


@router.get("/api/v1/benchmarks/results/name")
@inject
async def get_all_results_name(
    benchmark_result_service: BenchmarkResultService = Depends(
        Provide[Container.benchmark_result_service]
    ),
):
    """
    Get all benchmark result names from the database.

    This endpoint retrieves the names of all benchmark results stored in the database.

    Args:
        benchmark_result_service (BenchmarkResultService): The service responsible for fetching
        the names of the benchmark results.

    Returns:
        A list of all benchmark result names.

    Raises:
        HTTPException: An error occurred while trying to find the result names file (404),
                       a validation error occurred (400), or
                       an unspecified error occurred (500).
    """
    try:
        results = benchmark_result_service.get_all_result_name()
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve result name: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve result name: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve result name: {e.msg}"
            )


@router.get("/api/v1/benchmarks/results/{result_id}")
@inject
async def get_one_results(
    result_id: str,
    benchmark_result_service: BenchmarkResultService = Depends(
        Provide[Container.benchmark_result_service]
    ),
):
    """
    Retrieve a single benchmark result by its ID.

    This endpoint fetches the details of a specific benchmark result identified by the provided result_id.

    Args:
        result_id (str): The unique identifier of the benchmark result to retrieve.
        benchmark_result_service (BenchmarkResultService): The service responsible for fetching the benchmark result.

    Returns:
        dict: A dictionary containing the details of the benchmark result.

    Raises:
        HTTPException: An error occurred while trying to find the results file (404) or
                       an unspecified error occurred (500).
    """
    try:
        results = benchmark_result_service.get_result_by_id(result_id)
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve result: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve result: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve result: {e.msg}"
            )


@router.delete("/api/v1/benchmarks/results/{result_id}")
@inject
def delete_result(
    result_id: str,
    benchmark_result_service: BenchmarkResultService = Depends(
        Provide[Container.benchmark_result_service]
    ),
) -> dict[str, str] | tuple[dict[str, str], int]:
    """
    Delete a benchmark result by its ID.

    This endpoint deletes a specific benchmark result identified by the provided result_id.

    Args:
        result_id (str): The unique identifier of the benchmark result to delete.
        benchmark_result_service (BenchmarkResultService): The service responsible for deleting the benchmark result.

    Returns:
        dict[str, str] | tuple[dict[str, str], int]: A message indicating successful deletion,
        or an HTTPException with an appropriate status code.

    Raises:
        HTTPException: An error occurred while trying to delete the result due to the result not being found (404),
                       a validation error occurred (400), or
                       an unspecified error occurred (500).
    """
    try:
        benchmark_result_service.delete_result(result_id)
        return {"message": "Result deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete result: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete result: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete result: {e.msg}"
            )
