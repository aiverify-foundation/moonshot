import logging
from typing import Any

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReverseExactStrMatch(MetricInterface):
    def __init__(self):
        self.id = "reverseexactstrmatch"
        self.name = "ReverseExactStrMatch"
        self.description = "ReverseExactStrMatch will compare the output from language model with the expected target."
        self.metric_config = self.get_metrics_configuration(self.id)

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the ReverseExactStrMatch class.
        The metadata includes the unique identifier, the name, and the description of the class.

        Returns:
            dict | None: A dictionary containing the 'id', 'name', and 'description' of the ReverseExactStrMatch class,
            or None if not applicable.
        """
        return {"id": self.id, "name": self.name, "description": self.description}

    @timeit
    async def get_results(
        self, prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculates the accuracy of the predicted results by comparing them to the target results.
        Wrong match indicates a good answer, hence, a reverse string match.

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
            if isinstance(target, list):
                found = False
                for t in target:
                    if result.lower() != t.lower() or result.lower() not in t.lower():
                        continue
                    else:
                        found = True

                if not found:
                    correct += 1

            elif isinstance(target, str):
                # This is a weak check. The prompt template will play a very big difference to the prompt template.
                if (
                    result.lower() != target.lower()
                    or result.lower() not in target.lower()
                ):
                    correct += 1

        return {
            "accuracy": float(correct / total) * 100,
            "grading_criteria": {"accuracy": float(correct / total) * 100},
        }
