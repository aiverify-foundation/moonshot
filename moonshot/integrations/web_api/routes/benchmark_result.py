from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..container import Container
from ..services.benchmark_result_service import BenchmarkResultService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional

router = APIRouter()

@router.get("/v1/benchmarks/results")
@inject
async def get_all_results(
    benchmark_result_service: BenchmarkResultService = Depends(Provide[Container.benchmark_result_service])):
    try:
        results = benchmark_result_service.get_all_results()
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Unable to find results file: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve progress status: {e.msg}")


@router.get("/v1/benchmarks/results/name")
@inject
async def get_all_results_name(
    benchmark_result_service: BenchmarkResultService = Depends(Provide[Container.benchmark_result_service])):
    """
    Get all the recipes name from the database
    """
    try:
        results = benchmark_result_service.get_all_result_name()
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve result name: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve result name: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve result name: {e.msg}")       


@router.get("/v1/benchmarks/results/{result_id}")
@inject
async def get_one_results(
    result_id: str,    
    benchmark_result_service: BenchmarkResultService = Depends(Provide[Container.benchmark_result_service])):
    try:
        results = benchmark_result_service.get_result_by_id(result_id)
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Unable to find results file: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve progress status: {e.msg}")
        
        
@router.delete("/v1/benchmarks/results/{result_id}")
@inject
def delete_result(
    result_id: str,
    benchmark_result_service: BenchmarkResultService = Depends(Provide[Container.benchmark_result_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:
    try:
        benchmark_result_service.delete_result(result_id)
        return {"message": "Result deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete result: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete result: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete result: {e.msg}")    
    