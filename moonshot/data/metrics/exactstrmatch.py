import logging
from typing import Any

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExactStrMatch(MetricInterface):
    def __init__(self):
        self.id = "exactstrmatch"
        self.name = "ExactStrMatch"
        self.description = "ExactStrMatch will compare the output from language model with the expected target."
        self.version = "0.1.0"

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the ExactStrMatch class,
        including its identifier, name, description, and version.

        Returns:
            dict: A dictionary containing the metadata of the ExactStrMatch class,
            which includes 'id', 'name', 'description', and 'version'.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
        }

    @timeit
    def get_results(
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
            if result == target:
                correct += 1

        return {"exact_str_match": float(correct / total)}
