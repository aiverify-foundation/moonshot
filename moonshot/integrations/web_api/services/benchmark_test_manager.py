import asyncio
import uuid
from typing import Any, TypedDict
from slugify import slugify
from dependency_injector.wiring import inject

from .... import api as moonshot_api
from ..types.types import CookbookTestRunProgress
from ..services.benchmark_test_state import BenchmarkTestState
from ..schemas.benchmark_runner_dto import BenchmarkRunnerDTO
from ..types.types import BenchmarkCollectionType
from ..status_updater.webhook import Webhook
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

    def create_runner(self, runner_name, endpoints, progress_callback_func):
        return moonshot_api.api_create_runner(name=runner_name, endpoints=endpoints, progress_callback_func=progress_callback_func)

    async def create_executor_and_execute(self, benchmark_input_data: BenchmarkRunnerDTO, benchmark_type : BenchmarkCollectionType) -> None:
        try:
            runner = self.create_runner(benchmark_input_data.run_name, benchmark_input_data.endpoints, self.webhook.on_executor_update)
            if isinstance(benchmark_input_data, BenchmarkRunnerDTO):
                if benchmark_type == BenchmarkCollectionType.COOKBOOK:
                    executor = runner.run_cookbooks(
                        cookbooks=benchmark_input_data.inputs,
                        num_of_prompts=benchmark_input_data.num_of_prompts,
                        random_seed=benchmark_input_data.random_seed,
                        system_prompt=benchmark_input_data.system_prompt,
                    )
                else:
                    executor = runner.run_recipes(
                        recipes=benchmark_input_data.inputs,
                        num_of_prompts=benchmark_input_data.num_of_prompts,
                        random_seed=benchmark_input_data.random_seed,
                        system_prompt=benchmark_input_data.system_prompt,
                    )
        except Exception as e:
            self.logger.error(f"Failed to execute benchmark - {e}")
            raise Exception(f"Unexpected error in core library - {e}")
        
        await executor
        executor.close()

    def schedule_test_task(self, executor_input_data: BenchmarkRunnerDTO, benchmark_type : BenchmarkCollectionType) -> str:
        task_id = self.generate_unique_task_id()

        exec_benchmark_coroutine = self.create_executor_and_execute(executor_input_data,benchmark_type)

        task = asyncio.create_task(exec_benchmark_coroutine, name=task_id)
        def on_executor_completion(task: asyncio.Task[Any]):
            if task.exception():
                self.logger.error(f"Executor {task.get_name()} has failed - {task.exception()}")
            else:
                self.logger.debug(f"Executor {task.get_name()} has completed")
        task.add_done_callback(on_executor_completion)

        # Id getter needs review. Read comments in function
        id = slugify( executor_input_data.run_name, lowercase=True)
        
        self.add_task(id, task)
        return id
