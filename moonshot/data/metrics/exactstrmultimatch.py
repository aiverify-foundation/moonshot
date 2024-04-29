import logging
from typing import Any

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExactStrMultiMatch(MetricInterface):
    def __init__(self):
        self.id = "exactstrmultimatch"
        self.name = "ExactStrMultiMatch"
        self.description = (
            "ExactStrMultiMatch will compare the output from language model with "
            "(multiple) expected target."
        )
        self.metric_config = self.get_metrics_configuration(self.id)

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the ExactStrMultiMatch class.
        The metadata includes the unique identifier, the name, and the description of the class.

        Returns:
            dict | None: A dictionary containing the 'id', 'name', and 'description' of the ExactStrMultiMatch class,
            or None if not applicable.
        """
        return {"id": self.id, "name": self.name, "description": self.description}

    @timeit
    def get_results(
        self, prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculates the accuracy of predicted results based on the targets.

        Args:
            prompts (Any): The prompts used for prediction.
            predicted_results (Any): The predicted results.
            targets (Any): The actual target values.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the accuracy of predicted results as "exact_str_multiple_match".

        """
        correct = 0
        total = len(predicted_results)

        for idx, (result, target) in enumerate(zip(predicted_results, targets)):
            if isinstance(target, list):
                if result in target:
                    correct += 1
            else:
                if result == target:
                    correct += 1

        return {"exact_str_multiple_match": float(correct / total)}
