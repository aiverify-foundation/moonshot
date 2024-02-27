# api/routes.py
import datetime  # Add this import
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from web_api.queue.interface.queue_connection import InterfaceQueueConnection

from ..container import Container

router = APIRouter()

@router.get("/dev/test/task")
@inject
async def test_task(
  benchmarking_test_queue: InterfaceQueueConnection = Depends(Provide["benchmarking_test_queue"])
  ):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  job_with_timestamp = f"task at {timestamp}"
  if benchmarking_test_queue is not None:
    benchmarking_test_queue.publish(job_with_timestamp)
  else:
    raise HTTPException(status_code=500, detail="BENCHMARK_TEST_QUEUE_MANAGER is not initialized")

