from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..container import Container
from ..services.benchmark_result_service import BenchmarkResultService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional

router = APIRouter()

@router.get("/v1/benchmarks/results/{executor_id}")
@inject
async def get_one_results(
    executor_id: str,    
    benchmark_result_service: BenchmarkResultService = Depends(Provide[Container.benchmark_result_service])):
    try:
        results = benchmark_result_service.get_all_results(executor_id)
        return results
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Unable to find results file: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve progress status: {e.msg}")
        
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

