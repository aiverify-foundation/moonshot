import logging
import statistics
from typing import Any

from nltk.translate.bleu_score import sentence_bleu

from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BleuScore:
    """
    Bleuscore uses Bleu to return the various rouge scores.
    """

    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
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
        return {"bleu_score": statistics.mean(bleu_scores)}
