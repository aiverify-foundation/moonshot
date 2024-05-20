from typing import Callable

from moonshot.src.runners.runner import Runner

from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from ..types.types import TestRunProgress


class RunnerService(BaseService):
    @exception_handler
    def get_all_runner(self) -> list[dict]:
        """
        Retrieves all runners.

        Returns:
            A list of dictionaries, where each dictionary contains the details of a runner.
        """
        runners = moonshot_api.api_get_all_runner()
        return runners

    @exception_handler
    def get_all_runner_name(self) -> list[str]:
        """
        Retrieves the names of all runners.

        Returns:
            A list of strings, where each string is the name of a runner.
        """
        runners = moonshot_api.api_get_all_runner_name()
        return runners

    @exception_handler
    def get_runner_by_id(self, runner_id: str) -> dict | None:
        """
        Retrieves a runner by its ID.

        Args:
            runner_id: The unique identifier of the runner.

        Returns:
            A dictionary containing the runner's details if found, otherwise None.
        """
        runner = moonshot_api.api_read_runner(runner_id)
        return runner

    @exception_handler
    def delete_run(self, runner_id: str) -> None:
        """
        Deletes a runner by its ID.

        Args:
            runner_id: The unique identifier of the runner to be deleted.
        """
        moonshot_api.api_delete_runner(runner_id)

    @exception_handler
    def create_runner(
        self,
        runner_name: str,
        endpoints: list[str],
        description: str,
        progress_callback_func: Callable[[TestRunProgress], None] = None,
    ) -> Runner:
        """
        Creates a new runner with the specified details.

        Args:
            runner_name: The name of the runner.
            endpoints: A list of endpoints the runner will interact with.
            description: A brief description of the runner.
            progress_callback_func: An optional callback function for progress updates.

        Returns:
            An instance of Runner.
        """
        return moonshot_api.api_create_runner(
            name=runner_name,
            endpoints=endpoints,
            description=description,
            progress_callback_func=progress_callback_func,
        )

    @exception_handler
    def load_runner(
        self,
        runner_id: str,
        progress_callback_func: Callable[[TestRunProgress], None] = None,
    ) -> Runner:
        """
        Loads a runner by its ID.

        Args:
            runner_id: The unique identifier of the runner to be loaded.
            progress_callback_func: An optional callback function for progress updates.

        Returns:
            An instance of Runner.
        """
        return moonshot_api.api_load_runner(
            runner_id, progress_callback_func=progress_callback_func
        )

    @exception_handler
    def get_run_details_by_runner(self, runner_id: str, run_id: int):
        """
        Retrieves the details of a specific run by the runner ID and run ID.

        Args:
            runner_id: The unique identifier of the runner.
            run_id: The unique identifier of the run.

        Returns:
            A dictionary containing the details of the run if found, otherwise an empty dictionary.
        """
        runs = moonshot_api.api_get_all_run(runner_id)
        retn = {}
        run_id_int = int(run_id)
        for run in runs:
            run_id_from_run = int(run.get("run_id"))
            if run_id_from_run == run_id_int:
                retn = {
                    "run_id": run.get("run_id"),
                    "runner_id": run.get("runner_id"),
                    "runner_args": run.get("runner_args"),
                    "endpoints": run.get("endpoints"),
                    "start_time": run.get("start_time"),
                }
        return retn

    @exception_handler
    def get_runs_id_in_runner(self, runner_id) -> list[int]:
        """
        Retrieves a list of run IDs for a given runner.

        Args:
            runner_id: The unique identifier of the runner.

        Returns:
            A list of integers, where each integer is the ID of a run associated with the runner.
        """
        runs = moonshot_api.api_get_all_run(runner_id)
        retn = []
        for run in runs:
            retn.append(run.get("run_id"))
        return retn
