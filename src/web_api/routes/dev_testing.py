# api/routes.py
import datetime  # Add this import
from fastapi import APIRouter, HTTPException
from .. import globals 

router = APIRouter()

@router.get("/dev/test/task")
async def test_task():
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  task_with_timestamp = f"task at {timestamp}"
  if globals.SHARED_CHANNELS is not None:
    globals.SHARED_CHANNELS["benchmark_test"].put_nowait(task_with_timestamp)
  else:
    raise HTTPException(status_code=500, detail="SHARED_CHANNELS is not initialized")

