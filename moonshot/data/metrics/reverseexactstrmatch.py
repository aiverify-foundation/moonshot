import logging
from typing import Any

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReverseExactStrMatch(MetricInterface):
    # JSON schema as a class variable
    output_schema = {
        "type": "object",
        "properties": {
            "reverse_exact_str_match": {"type": "number"},
            "correct": {"type": "integer"},
            "total": {"type": "integer"},
        },
        "required": ["reverse_exact_str_match", "correct", "total"],
    }

    def __init__(self):
        self.id = "reverseexactstrmatch"
        self.name = "ReverseExactStrMatch"
        self.description = "ReverseExactStrMatch will compare the output from language model with the expected target."
        self.version = "0.1.0"

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Fetches and provides the metadata for the ReverseExactStrMatch class, including its unique identifier,
        the name, a brief description, and the current version of the metric.

        Returns:
            dict: A dictionary encapsulating the metadata of the ReverseExactStrMatch class, detailing 'id', 'name',
            'description', and 'version' keys.
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

        response_dict = {
            "reverse_exact_str_match": float(correct / total),
            "correct": correct,
            "total": total,
        }
        # Validate that the output dict passes json schema validation
        if self.validate_output(response_dict, ReverseExactStrMatch.output_schema):
            return response_dict
        else:
            raise RuntimeError(
                "[ReverseExactStrMatch] Failed json schema validation for output response."
            )
