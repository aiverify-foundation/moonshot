import logging
import statistics
from typing import Any

from nltk.translate.bleu_score import sentence_bleu

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BleuScore:
    """
    Bleuscore uses Bleu to return the various rouge scores.
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        bleu_scores = []
        for idx, (output, target) in enumerate(zip(output_response, targets)):
            output_split = output.split()
            target_split = target.split()

            score = sentence_bleu(output_split, target_split)
            bleu_scores.append(score)
        return {"bleu_score": statistics.mean(bleu_scores)}
