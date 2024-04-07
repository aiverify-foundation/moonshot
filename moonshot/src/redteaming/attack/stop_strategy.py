from __future__ import annotations

from abc import abstractmethod

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.metrics.metric import Metric
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class StopStrategy:

    @classmethod
    def load(cls, ss_id: str) -> StopStrategy:
        """
        Retrieves a stop strategy instance by its ID.

        This method attempts to load a stop strategy using the provided ID. If the stop strategy instance is found,
        it is returned. If the stop strategy instance does not exist, a RuntimeError is raised.

        Args:
            ss_id (str): The unique identifier of the stop strategy to be retrieved.

        Returns:
            AttackModule: The retrieved stop strategy instance.

        Raises:
            RuntimeError: If the stop strategy instance does not exist.
        """
        stop_strategy_inst = get_instance(
            ss_id,
            Storage.get_filepath(EnvVariables.STOP_STRATEGIES.name, ss_id, "py"),
        )
        if stop_strategy_inst:
            return stop_strategy_inst()
        else:
            raise RuntimeError(
                f"Unable to get defined stop strategy instance - {ss_id}"
            )

    @abstractmethod
    def stop_red_teaming_attack(
        self, no_of_iterations: int, llm_response: str, metric_instances: list[Metric]
    ) -> bool:
        pass
