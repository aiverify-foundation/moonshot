import asyncio
import uuid
from typing import Any
from .... import api as moonshot_api
from ..schemas.recipe_executor_create_dto import RecipeExecutorCreateDTO
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

    def create_executor_and_execute(self, executor_input_data: CookbookExecutorCreateDTO | RecipeExecutorCreateDTO) -> None:
        try:
            if isinstance(executor_input_data, CookbookExecutorCreateDTO):
                executor = moonshot_api.api_create_cookbook_executor(
                    name=executor_input_data.name,
                    cookbooks=executor_input_data.cookbooks,
                    endpoints=executor_input_data.endpoints,
                    num_of_prompts=executor_input_data.num_of_prompts,
                    progress_callback_func=Webhook.on_executor_update
                )
            else:
                executor = moonshot_api.api_create_recipe_executor(
                    name=executor_input_data.name,
                    recipes=executor_input_data.recipes,
                    endpoints=executor_input_data.endpoints,
                    num_of_prompts=executor_input_data.num_of_prompts,
                    progress_callback_func=Webhook.on_executor_update
                )
        except Exception as e:
            self.logger.error(f"Failed to execute benchmark - {e}")
            raise Exception(f"Unexpected error in core library - {e}")
        executor.execute()
        executor.close_executor()

    # Note: schedule_test_task must be run within an async context. 
    # It should be within Uvicorn's async context in this application.
    def schedule_test_task(self, executor_input_data: CookbookExecutorCreateDTO | RecipeExecutorCreateDTO) -> asyncio.Task[Any]:
        task_id = self.generate_unique_task_id()
        # benchmark.execute is long running I/O bound. Executing it in separate thread
        # Note: executor instance must be created in the same thread as it is executed because
        # SQLite, by default, restricts database connection objects to the thread in which they were created
        if isinstance(executor_input_data, CookbookExecutorCreateDTO):
            exec_benchmark_coroutine = asyncio.to_thread(self.create_executor_and_execute, executor_input_data)
        else:
            exec_benchmark_coroutine = asyncio.to_thread(self.create_executor_and_execute, executor_input_data) 
        
        task = asyncio.create_task(exec_benchmark_coroutine, name=task_id)
        def on_executor_completion(task: asyncio.Task[Any]):
            if task.exception():
                self.logger.error(f"Executor {task.get_name()} has failed - {task.exception()}")
            else:
                self.logger.debug(f"Executor {task.get_name()} has completed")
        task.add_done_callback(on_executor_completion)
        self.add_task(task)
        return task
