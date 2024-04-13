import logging
import statistics
from typing import Any

from nltk.translate.bleu_score import sentence_bleu

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BleuScore(MetricInterface):
    # JSON schema as a class variable
    output_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "BleuScoreResponse",
        "description": "Schema for the response of BleuScore metric calculation.",
        "type": "object",
        "properties": {
            "bleu_score": {
                "type": "number",
                "description": "The average BLEU score of the predicted results compared to the target results.",
            }
        },
        "required": ["bleu_score"],
    }

    def __init__(self):
        self.id = "bleuscore"
        self.name = "BleuScore"
        self.description = "Bleuscore uses Bleu to return the various rouge scores."
        self.version = "0.1.0"

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the BleuScore class,
        including its identifier, name, description, and version.

        Returns:
            dict: A dictionary containing the metadata of the BleuScore class,
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
        Calculate the BLEU score for a list of predicted results and their corresponding target results.

        Args:
            prompts (Any): The prompts used to generate the predicted results.
            predicted_results (Any): The list of predicted results.
            targets (Any): The list of target results.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the BLEU score.

        Raises:
            None
        """
        bleu_scores = []
        for idx, (result, target) in enumerate(zip(predicted_results, targets)):
            output_split = result.split()
            target_split = target.split()

            score = sentence_bleu(output_split, target_split)
            bleu_scores.append(score)

        response_dict = {"bleu_score": statistics.mean(bleu_scores)}
        # Validate that the output dict passes json schema validation
        if self.validate_output(response_dict, BleuScore.output_schema):
            return response_dict
        else:
            raise RuntimeError(
                "[BleuScore] Failed json schema validation for output response."
            )
