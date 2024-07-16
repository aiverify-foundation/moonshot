import json
import logging

import requests
from dependency_injector.wiring import inject
from dotenv import dotenv_values

from ..services.auto_red_team_test_state import AutoRedTeamTestState
from ..services.benchmark_test_state import BenchmarkTestState
from ..types.types import RedTeamTestProgress, TestRunProgress
from .interface.benchmark_progress_callback import InterfaceBenchmarkProgressCallback
from .interface.redteam_progress_callback import InterfaceRedTeamProgressCallback


class MoonshotUIWebhook(
    InterfaceBenchmarkProgressCallback, InterfaceRedTeamProgressCallback
):
    """
    Implementation of the benchmark progress callback.
    This class is responsible for sending the progress data to the webhook exposed by moonshot-ui server.
    """

    @inject
    def __init__(
        self,
        benchmark_test_state: BenchmarkTestState,
        auto_red_team_test_state: AutoRedTeamTestState,
    ) -> None:
        self.benchmark_test_state = benchmark_test_state
        self.auto_red_team_test_state = auto_red_team_test_state
        self.url = str(
            dotenv_values().get(
                "MOONSHOT_UI_CALLBACK_URL",
                "http://localhost:3000/api/v1/benchmarks/status",
            )
        )
        self.art_url = str(
            dotenv_values().get(
                "MOONSHOT_UI_ART_CALLBACK_URL",
                "http://localhost:3000/api/v1/redteaming/status",
            )
        )

    def on_progress_update(self, progress_data: TestRunProgress) -> None:
        logger = logging.getLogger()
        logger.debug(json.dumps(progress_data, indent=2))
        self.benchmark_test_state.update_progress_status(progress_data)

        try:
            response = requests.post(self.url, json=progress_data)
            response.raise_for_status()
            logger.log(level=logging.DEBUG, msg=response.json())
            logger.log(
                level=logging.INFO, msg="Progress data successfully sent to the server."
            )
        except requests.RequestException as e:
            logger.critical(msg=f"Failed to send progress data: {e}")

    def on_art_progress_update(self, progress_data: RedTeamTestProgress) -> None:
        logger = logging.getLogger()
        logger.debug(json.dumps(progress_data, indent=2))
        self.auto_red_team_test_state.update_progress_status(progress_data)
        try:
            response = requests.post(self.art_url, json=progress_data)
            response.raise_for_status()
            logger.log(level=logging.DEBUG, msg=response.json())
            logger.log(
                level=logging.INFO, msg="Progress data successfully sent to the server."
            )
        except requests.RequestException as e:
            logger.critical(msg=f"Failed to send progress data: {e}")
