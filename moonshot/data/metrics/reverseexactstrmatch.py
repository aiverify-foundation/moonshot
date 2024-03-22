import logging
from typing import Any
import re

from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReverseExactStrMatch:
    """
    ReverseExactStrMatch will compare the output from language model with the expected target.
    """
    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
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
                if result.lower() != target.lower() or result.lower() not in target.lower():
                    correct += 1

        
        return {"reverse_exact_str_match": float(correct / total), "correct": correct, "total": total}
