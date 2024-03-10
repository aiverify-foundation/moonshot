import asyncio
import uuid
from typing import Any
import moonshot.api as moonshot_api
from ..status_updater.webhook import Webhook
from ..schemas.cookbook_executor_create_dto import CookbookExecutorCreateDTO
from ..services.base_service import BaseService


class BenchmarkTestManager(BaseService):
    async_test_tasks: dict[str, asyncio.Task[Any]] = {}

    def generate_unique_task_id(self) -> str:
        unique_id = str(uuid.uuid4())
        return f"task_{unique_id}"

    def add_task(self, task: asyncio.Task[Any]) -> None:
        self.async_test_tasks[task.get_name()] = task

    def remove_task(self, task_id: str) -> asyncio.Task[Any]:
        return self.async_test_tasks.pop(task_id)
    
    def cancel_task(self, task_id: str) -> None:
        self.async_test_tasks[task_id].cancel();
        self.logger.debug(f"Task {task_id} has been cancelled")

    def on_task_completed(self, task: asyncio.Task[Any]) -> None:
        self.logger.debug(f"Task {task.get_name()} has completed")

    def create_executor_and_execute(self, cookbook_executor_data: CookbookExecutorCreateDTO) -> None:
        executor = moonshot_api.api_create_cookbook_executor(
            name=cookbook_executor_data.name,
            cookbooks=cookbook_executor_data.cookbooks,
            endpoints=cookbook_executor_data.endpoints,
            num_of_prompts=cookbook_executor_data.num_of_prompts,
            progress_callback_func=Webhook.on_executor_update
        )
        executor.execute()
        executor.close_executor()

    # Note: schedule_test_task must be run within an async context. 
    # It should be within Uvicorn's async context in this application.
    def schedule_test_task(self, cookbook_executor_data: CookbookExecutorCreateDTO) -> asyncio.Task[Any]:
        task_id = self.generate_unique_task_id()
        # benchmark.execute is long running I/O bound. Executing it in separate thread
        # Note: executor instance must be created in the same thread as it is executed because
        # SQLite, by default, restricts database connection objects to the thread in which they were created
        exec_benchmark_coroutine = asyncio.to_thread(self.create_executor_and_execute, cookbook_executor_data)
        task = asyncio.create_task(exec_benchmark_coroutine, name=task_id)
        def on_executor_completion(task: asyncio.Task[Any]):
            self.logger.debug(f"Executor {task.get_name()} has completed")
        task.add_done_callback(on_executor_completion)
        self.add_task(task)
        return task
