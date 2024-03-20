import asyncio
import uuid
from typing import Any, TypedDict
from slugify import slugify
from dependency_injector.wiring import inject

from moonshot.src.benchmarking.executors.benchmark_executor_types import BenchmarkExecutorTypes

from .... import api as moonshot_api
from ..types.types import CookbookTestRunProgress
from ..services.benchmark_test_state import BenchmarkTestState
from ..schemas.recipe_executor_create_dto import RecipeExecutorCreateDTO
from ..status_updater.webhook import Webhook
from ..schemas.cookbook_executor_create_dto import CookbookExecutorCreateDTO
from ..services.base_service import BaseService

class BenchmarkTaskInfo(TypedDict):
    async_task: asyncio.Task[Any]
    status: CookbookTestRunProgress | None
class BenchmarkTestManager(BaseService):
    @inject
    def __init__(self, benchmark_test_state: BenchmarkTestState, webhook: Webhook) -> None:
        self.benchmark_test_state = benchmark_test_state
        self.webhook = webhook
        super().__init__()

    def generate_unique_task_id(self) -> str:
        unique_id = str(uuid.uuid4())
        return f"task_{unique_id}"

    def add_task(self, executor_id: str, task: asyncio.Task[Any]) -> None:
        self.benchmark_test_state.add_task(executor_id, task)

    def remove_task(self, executor_id: str) -> BenchmarkTaskInfo:
        return self.benchmark_test_state.remove_task(executor_id)
    
    def cancel_task(self, executor_id: str) -> None:
        return self.benchmark_test_state.cancel_task(executor_id)
    
    def update_state(self, updates: CookbookTestRunProgress):
        self.benchmark_test_state.update_state(updates)

    def on_task_completed(self, task: asyncio.Task[Any]) -> None:
        self.logger.debug(f"Task {task.get_name()} has completed")

    #TODO - get executor id from excutor instance somehow
    def get_executor_id(self, type: BenchmarkExecutorTypes, name: str) -> str:
        # This is a temporary workaround to get exec id without awaiting the long running execution
        # Unable to run execute separately because instance creation needs to be in the same async task
        # Use the same slugify pattern that ms lib uses to get the ID upfront
        # Review and refactor required for this - ID needs to be from MS lib
        prefix = (
                "recipe-"
                if type == BenchmarkExecutorTypes.RECIPE
                else "cookbook-"
            )
        id = slugify(prefix + name, lowercase=True)
        return id

    def create_executor_and_execute(self, executor_input_data: CookbookExecutorCreateDTO | RecipeExecutorCreateDTO) -> None:
        try:
            if isinstance(executor_input_data, CookbookExecutorCreateDTO):
                executor = moonshot_api.api_create_cookbook_executor(
                    name=executor_input_data.name,
                    cookbooks=executor_input_data.cookbooks,
                    endpoints=executor_input_data.endpoints,
                    num_of_prompts=executor_input_data.num_of_prompts,
                    progress_callback_func=self.webhook.on_executor_update
                )
            else:
                executor = moonshot_api.api_create_recipe_executor(
                    name=executor_input_data.name,
                    recipes=executor_input_data.recipes,
                    endpoints=executor_input_data.endpoints,
                    num_of_prompts=executor_input_data.num_of_prompts,
                    progress_callback_func=self.webhook.on_executor_update
                )
        except Exception as e:
            self.logger.error(f"Failed to execute benchmark - {e}")
            raise Exception(f"Unexpected error in core library - {e}")
        executor.execute()
        executor.close_executor()

    # Note: schedule_test_task must be run within an async context. 
    # It should be within Uvicorn's async context in this application.
    def schedule_test_task(self, executor_input_data: CookbookExecutorCreateDTO | RecipeExecutorCreateDTO) -> str:
        task_id = self.generate_unique_task_id()
        # benchmark.execute is long running I/O bound. Executing it in separate thread
        # Note: executor instance must be created in the same thread as it is executed because
        # SQLite, by default, restricts database connection objects to the thread in which they were created
        if isinstance(executor_input_data, CookbookExecutorCreateDTO):
            type = BenchmarkExecutorTypes.COOKBOOK
            exec_benchmark_coroutine = asyncio.to_thread(self.create_executor_and_execute, executor_input_data)
        else:
            type = BenchmarkExecutorTypes.RECIPE
            exec_benchmark_coroutine = asyncio.to_thread(self.create_executor_and_execute, executor_input_data) 
        
        task = asyncio.create_task(exec_benchmark_coroutine, name=task_id)
        def on_executor_completion(task: asyncio.Task[Any]):
            if task.exception():
                self.logger.error(f"Executor {task.get_name()} has failed - {task.exception()}")
            else:
                self.logger.debug(f"Executor {task.get_name()} has completed")
        task.add_done_callback(on_executor_completion)
        # Id getter needs review. Read comments in function
        id = self.get_executor_id(type, executor_input_data.name)
        self.add_task(id, task)
        return id
