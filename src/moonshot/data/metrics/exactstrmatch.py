import logging
from typing import Any

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExactStrMatch:
    """
    ExactStrMatch will compare the output from language model with the expected target.
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        correct = 0
        total = len(output_response)

        for idx, (output, target) in enumerate(zip(output_response, targets)):
            if output == target:
                correct += 1
        return {"exact_str_match": float(correct / total)}
