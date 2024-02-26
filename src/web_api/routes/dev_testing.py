# api/routes.py
import datetime  # Add this import
from fastapi import APIRouter, HTTPException
from .. import globals 

router = APIRouter()

@router.get("/dev/test/task")
async def test_task():
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  job_with_timestamp = f"task at {timestamp}"
  if globals.BENCHMARK_TEST_QUEUE_MANAGER is not None:
    globals.BENCHMARK_TEST_QUEUE_MANAGER.publish(job_with_timestamp)
  else:
    raise HTTPException(status_code=500, detail="BENCHMARK_TEST_QUEUE_MANAGER is not initialized")

