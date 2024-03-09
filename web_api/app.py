import asyncio
import os
from contextlib import asynccontextmanager
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .container import Container
from .routes.redteam import router as red_team_router
from .routes.benchmark import router as benchmarking_router
from .routes.dev_testing import router as dev_router

environment = os.getenv("APP_ENV")
class CustomFastAPI(FastAPI):
    container: Container

async def monitor_tasks(loop: asyncio.AbstractEventLoop):
    while True:
        tasks = asyncio.all_tasks(loop)
        print(f"==== Current Tasks: {len(tasks)} ====")
        for task in tasks:
            print(task)
        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if environment == "DEV":
        loop = asyncio.get_running_loop()
        loop.create_task(monitor_tasks(loop))
    yield

async def startup_event():
    if environment == "DEV":
        loop = asyncio.get_running_loop()
        loop.create_task(monitor_tasks(loop))

def create_app() -> CustomFastAPI:
    container: Container = Container()
    container.init_resources()
    allowed_origins_raw = os.getenv("ALLOWED_ORIGINS")
    allowed_origins = allowed_origins_raw.split(",") if allowed_origins_raw else []
    app: CustomFastAPI = CustomFastAPI(lifespan=lifespan)
    async def log_request_origin(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        origin = request.headers.get('origin')
        print(f"Request origin: {origin}")
        response = await call_next(request)
        return response
    if environment == "DEV":
        app.middleware("http")(log_request_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.container = container
    app.include_router(red_team_router)
    app.include_router(benchmarking_router)
    app.include_router(dev_router)
    return app

