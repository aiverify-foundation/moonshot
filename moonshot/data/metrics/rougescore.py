import logging
from typing import Any

from rouge import Rouge

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RougeScore(MetricInterface):
    def __init__(self):
        self.id = "rougescore"
        self.name = "RougeScore"
        self.description = "RougeScore returns the various rouge scores."
        self.metric_config = self.get_metrics_configuration(self.id)

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the RougeScore class.
        The metadata includes the unique identifier, the name, and the description of the class.

        Returns:
            dict | None: A dictionary containing the 'id', 'name', and 'description' of the RougeScore class,
            or None if not applicable.
        """
        return {"id": self.id, "name": self.name, "description": self.description}

    @timeit
    async def get_results(
        self, prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculates the Rouge scores for the predicted results compared to the target results.

        Args:
            prompts (Any): The prompts used to generate the predicted results.
            predicted_results (Any): The predicted results.
            targets (Any): The target results.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: A dictionary containing the Rouge scores.

        """
        rouge = Rouge()
        scores = rouge.get_scores(predicted_results, targets, avg=True)
        return {"rouge": scores}
