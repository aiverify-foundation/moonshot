import logging
from typing import Any

from rouge import Rouge

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RougeScore(MetricInterface):
    # JSON schema as a class variable
    output_schema = {
        "type": "object",
        "properties": {
            "rouge": {
                "type": "object",
                "properties": {
                    "rouge-1": {
                        "type": "object",
                        "properties": {
                            "f": {"type": "number"},
                            "p": {"type": "number"},
                            "r": {"type": "number"},
                        },
                        "required": ["f", "p", "r"],
                    },
                    "rouge-2": {
                        "type": "object",
                        "properties": {
                            "f": {"type": "number"},
                            "p": {"type": "number"},
                            "r": {"type": "number"},
                        },
                        "required": ["f", "p", "r"],
                    },
                    "rouge-l": {
                        "type": "object",
                        "properties": {
                            "f": {"type": "number"},
                            "p": {"type": "number"},
                            "r": {"type": "number"},
                        },
                        "required": ["f", "p", "r"],
                    },
                },
                "required": ["rouge-1", "rouge-2", "rouge-l"],
            }
        },
        "required": ["rouge"],
    }

    def __init__(self):
        self.id = "rougescore"
        self.name = "RougeScore"
        self.description = "RougeScore returns the various rouge scores."
        self.version = "0.1.0"

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the RougeScore class,
        including its identifier, name, description, and version.

        Returns:
            dict: A dictionary containing the metadata of the RougeScore class,
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
        response_dict = {"rouge": scores}
        # Validate that the output dict passes json schema validation
        if self.validate_output(response_dict, RougeScore.output_schema):
            return response_dict
        else:
            raise RuntimeError(
                "[RougeScore] Failed json schema validation for output response."
            )
