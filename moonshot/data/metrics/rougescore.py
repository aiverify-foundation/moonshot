import logging
from typing import Any

from rouge import Rouge

from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RougeScore:
    """
    RougeScore returns the various rouge scores.
    """

    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
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
        return {"rouge": scores}
