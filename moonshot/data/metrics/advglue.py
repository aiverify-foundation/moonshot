import logging
from typing import Any

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AdvGlueExactMatch(MetricInterface):
    def __init__(self):
        self.id = "advglue"
        self.name = "AdvGlueExactMatch"
        self.description = (
            "AdvGlueExactMatch is a special metrics used by AdvGlue dataset."
        )
        self.metric_config = self.get_metrics_configuration(self.id)

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the AdvGlueExactMatch class.
        The metadata includes the unique identifier, the name, and the description of the class.

        Returns:
            dict | None: A dictionary containing the 'id', 'name', and 'description' of the AdvGlueExactMatch class,
            or None if not applicable.
        """
        return {"id": self.id, "name": self.name, "description": self.description}

    @timeit
    async def get_results(
        self, prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculates the accuracy of the predicted results by comparing them to the target results.

        Args:
            prompts (Any): The prompts used for prediction.
            predicted_results (Any): The predicted results.
            targets (Any): The target results.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the accuracy of the predicted results.
        """
        correct = 0
        total = len(predicted_results)

        for idx, (result, target) in enumerate(zip(predicted_results, targets)):
            try:
                result_split = result.split(",")

                actual_result = result_split[-1].split("=")[1]

                if actual_result == target:
                    correct += 1
            except Exception:
                continue

        return {
            "exact_str_match": float(correct / total),
            "correct": correct,
            "total": total,
        }
