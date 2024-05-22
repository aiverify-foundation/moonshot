import asyncio
from typing import Any, TypedDict

from moonshot.integrations.web_api.services.base_service import BaseService
from moonshot.integrations.web_api.types.types import RedTeamTestProgress
from moonshot.src.runners.runner import Runner


class AutoRedTeamTaskInfo(TypedDict):
    async_task: asyncio.Task[Any]
    moonshot_runner: Runner
    status: RedTeamTestProgress | None


class AutoRedTeamTestState(BaseService):
    state: dict[str, AutoRedTeamTaskInfo] = {}

    def add_task(
        self, id: str, task: asyncio.Task[Any], moonshot_runner: Runner
    ) -> None:
        self.state[id] = {
            "async_task": task,
            "moonshot_runner": moonshot_runner,
            "status": None,
        }

    def remove_task(self, id: str) -> AutoRedTeamTaskInfo:
        return self.state.pop(id)

    async def cancel_task(self, id: str) -> None:
        task_info = self.state[id]
        if task_info and not task_info["async_task"].done():
            if task_info["moonshot_runner"]:
                await task_info["moonshot_runner"].cancel()
            task_info["async_task"].cancel()
            self.logger.debug(f"Task {id} has been cancelled")
        else:
            self.logger.debug(f"Task {id} is already completed or does not exist.")

    def update_progress_status(self, updates: RedTeamTestProgress) -> None:
        self.logger.debug(updates)
        self.state[updates["current_runner_id"]]["status"] = updates

    def get_state(self) -> dict[str, AutoRedTeamTaskInfo]:
        return self.state

    def get_progress_status(self, id: str) -> RedTeamTestProgress | None:
        if id in self.state:
            return self.state[id]["status"]
        return None

    def get_all_progress_status(self) -> dict[str, RedTeamTestProgress]:
        return {
            id: task_info["status"]
            for id, task_info in self.state.items()
            if task_info["status"] is not None
        }
