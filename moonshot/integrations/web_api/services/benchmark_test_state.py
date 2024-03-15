import asyncio
from typing import Any, TypedDict
from moonshot.integrations.web_api.services.base_service import BaseService
from moonshot.integrations.web_api.types.types import CookbookTestRunProgress

class BenchmarkTaskInfo(TypedDict):
    async_task: asyncio.Task[Any]
    status: CookbookTestRunProgress | None

class BenchmarkTestState(BaseService):
    state: dict[str, BenchmarkTaskInfo] = {}

    def add_task(self, executor_id: str, task: asyncio.Task[Any]) -> None:
        self.state[executor_id] = {
            "async_task": task,
            "status": None
        }

    def remove_task(self, executor_id: str) -> BenchmarkTaskInfo:
        return self.state.pop(executor_id)
    
    def cancel_task(self, executor_id: str) -> None:
        self.state[executor_id]["async_task"].cancel();
        self.logger.debug(f"Task {executor_id} has been cancelled")

    def update_state(self, updates: CookbookTestRunProgress) -> None:
        self.state[updates["exec_id"]]["status"] = updates

    def get_state(self) -> dict[str, BenchmarkTaskInfo]:
        return self.state