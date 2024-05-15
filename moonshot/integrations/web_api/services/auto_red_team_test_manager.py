import asyncio
import uuid
from typing import Any

from dependency_injector.wiring import inject

from moonshot.src.runners.runner import Runner

from ..services.auto_red_team_test_state import AutoRedTeamTestState
from ..services.base_service import BaseService
from ..services.runner_service import RunnerService
from ..status_updater.interface.redteam_progress_callback import (
    InterfaceRedTeamProgressCallback,
)
from ..types.types import RedTeamTestProgress


class AutoRedTeamTestManager(BaseService):
    @inject
    def __init__(
        self,
        auto_red_team_test_state: AutoRedTeamTestState,
        progress_status_updater: InterfaceRedTeamProgressCallback,
        runner_service: RunnerService,
    ) -> None:
        """
        Initialize the SessionService with dependencies.

        Args:
            progress_status_updater (InterfaceRedTeamProgressCallback): The callback interface for progress updates.
            runner_service (RunnerService): The service for managing runners.
        """
        self.auto_red_team_test_state = auto_red_team_test_state
        self.progress_status_updater = progress_status_updater
        self.runner_service = runner_service
        super().__init__()

    def generate_unique_task_id(self) -> str:
        unique_id = str(uuid.uuid4())
        return f"task_{unique_id}"

    def add_task(
        self, executor_id: str, task: asyncio.Task[Any], moonshot_runner: Runner
    ) -> None:
        self.auto_red_team_test_state.add_task(executor_id, task, moonshot_runner)

    def remove_task(self, executor_id: str) -> None:
        self.auto_red_team_test_state.remove_task(executor_id)

    async def cancel_task(self, executor_id: str) -> None:
        await self.auto_red_team_test_state.cancel_task(executor_id)

    def update_progress_status(self, updates: RedTeamTestProgress):
        self.auto_red_team_test_state.update_progress_status(updates)

    def on_task_completed(self, task: asyncio.Task[Any]) -> None:
        self.logger.debug(f"Task {task.get_name()} has completed")

    async def schedule_art_task(
        self, art_args: dict, active_runner: Runner, batch_size: int
    ) -> str:
        task_id = self.generate_unique_task_id()

        auto_redteam_coroutine = self.send_art_prompt(
            art_args, active_runner, batch_size
        )

        task = asyncio.create_task(auto_redteam_coroutine, name=task_id)

        def on_executor_completion(task: asyncio.Task[Any]):
            if task.exception():
                self.logger.error(
                    f"Executor {task.get_name()} has failed - {task.exception()}"
                )
            else:
                self.logger.debug(f"Executor {task.get_name()} has completed")

        task.add_done_callback(on_executor_completion)

        self.add_task(active_runner.id, task, active_runner)
        return active_runner.id

    async def send_art_prompt(self, art_args, active_runner: Runner, batch_size: int):
        await active_runner.run_red_teaming(
            {"attack_strategies": [art_args], "chat_batch_size": batch_size}
        )
