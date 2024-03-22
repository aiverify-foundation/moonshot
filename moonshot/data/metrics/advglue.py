import logging
from typing import Any
import re

from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AdvGlueExactMatch:
    """
    AdvGlueExactMatch is a special metrics used by AdvGlue dataset.
    """
    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
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
            except Exception as e:
                continue
                
        return {"exact_str_match": float(correct / total), "correct": correct, "total": total}
