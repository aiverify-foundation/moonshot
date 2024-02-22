# api/__init__.py
import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes.redteam import router as red_team_router
from .routes.benchmark import router as benchmarking_router
from .routes.dev_testing import router as dev_router

async def monitor_tasks(loop: asyncio.AbstractEventLoop):
    while True:
        tasks = asyncio.all_tasks(loop)
        print(f"==== Current Tasks: {len(tasks)} ====")
        for task in tasks:
            print(task)
        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("APP_ENV") == "DEV":
        loop = asyncio.get_running_loop()
        loop.create_task(monitor_tasks(loop))
    yield

async def startup_event():
    if os.getenv("APP_ENV") == "DEV":
        loop = asyncio.get_running_loop()
        loop.create_task(monitor_tasks(loop))

app = FastAPI(lifespan=lifespan)

def init_api():
    app.include_router(red_team_router)
    app.include_router(benchmarking_router)
    app.include_router(dev_router)
    return app