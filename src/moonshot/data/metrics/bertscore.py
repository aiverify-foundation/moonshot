import logging
from typing import Any

import bert_score

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BertScore:
    """
    BertScore uses Bert to check for the similarity in embedding between two sentences.
    Code reference from:
    https://github.com/Tiiiger/bert_score/blob/master/bert_score_cli/score.py
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        # use default roberto model
        score = bert_score.score(
            output_response,
            targets,
            lang="en",
            rescale_with_baseline=True
        )

        avg_scores = [s.mean(dim=0) for s in score]
        precision_value = avg_scores[0].cpu().item()
        recall_value = avg_scores[1].cpu().item()
        f1_value = avg_scores[2].cpu().item()
        return {
            "bertscore": {
                "precision": precision_value,
                "recall": recall_value,
                "f1": f1_value,
            }
        }
