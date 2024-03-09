import asyncio
import os
import logging
from contextlib import asynccontextmanager
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .container import Container
from .routes.redteam import router as red_team_router
from .routes.benchmark import router as benchmarking_router
from .routes.dev_testing import router as dev_router

logger = logging.getLogger(__name__)
class CustomFastAPI(FastAPI):
    container: Container

async def monitor_tasks(loop: asyncio.AbstractEventLoop):
    while True:
        tasks = asyncio.all_tasks(loop)
        for task in tasks:
            logger.debug(task)
        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("APP_ENV") == "DEV":
        loop = asyncio.get_running_loop()
        loop.create_task(monitor_tasks(loop))
    yield

async def log_request_origin(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    origin = request.headers.get('origin')
    print(f"Request origin: {origin}")
    response = await call_next(request)
    return response

def create_app() -> CustomFastAPI:
    logger.debug(os.getenv("APP_ENV"))
    container: Container = Container()
    container.config.from_yaml("./config.yml")
    assert container.config.log.level() == "DEBUG"

    allowed_origins_raw = os.getenv("ALLOWED_ORIGINS")
    allowed_origins = allowed_origins_raw.split(",") if allowed_origins_raw else []
    app: CustomFastAPI = CustomFastAPI(lifespan=lifespan)

    if os.getenv("APP_ENV") == "DEV":
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

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        modified_errors: list[str] = []
        for error in exc.errors():
            # Remove the 'url' key from the error detail if it exists
            if 'url' in error:
                del error['url']
            modified_errors.append(error)

        logger.error(f"Validation error for request {request.url}: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"error": exc.errors()},
        )

    return app

