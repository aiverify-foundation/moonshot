import logging
from typing import Any

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExactStrMultiMatch:
    """
    ExactStrMatch will compare the output from language model with (multiple) expected target.
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        correct = 0
        total = len(output_response)

        for idx, (output, target) in enumerate(zip(output_response, targets)):
            if isinstance(target, list):
                if output in target:
                    correct += 1
            else:
                if output == target:
                    correct += 1
        return {"exact_str_multiple_match": float(correct / total)}
