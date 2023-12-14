import logging
from typing import Any

from rouge_score import rouge_scorer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RougeScore:
    """
    RougeScore returns the various rouge scores.
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        try:
            test_metrics = ["rouge1", "rouge2", "rougeLsum"]
            avg_recall = [0.0, 0.0, 0.0]
            avg_precision = [0.0, 0.0, 0.0]
            avg_fmeasure = [0.0, 0.0, 0.0]

            output_dict = dict()
            individual_scores = list()

            print("Attempting to calculate rouge score")
            scorer = rouge_scorer.RougeScorer(test_metrics)
            for index, (target, output) in enumerate(zip(targets, output_response), 0):
                scores = scorer.score(target, output)

                test_metrics_dict = dict()
                for test_metric_index, test_metric in enumerate(test_metrics, 0):
                    # Store each individual rouge score to calculate average score
                    avg_recall[test_metric_index] += scores[test_metric].recall
                    avg_precision[test_metric_index] += scores[test_metric].precision
                    avg_fmeasure[test_metric_index] += scores[test_metric].fmeasure

                    # Store each individual rouge score
                    test_metrics_dict[test_metric] = {
                        "r": scores[test_metric].recall,
                        "p": scores[test_metric].precision,
                        "f": scores[test_metric].fmeasure,
                    }
                    individual_scores.append(test_metrics_dict)

            # Update the output dict
            output_dict["rouge-scores"] = individual_scores

            # Calculate the average precision, recall and fmeasure
            for avg_index, (recall, precision, fmeasure) in enumerate(
                zip(avg_recall, avg_precision, avg_fmeasure), 0
            ):
                output_dict[f"avg_{test_metrics[avg_index]}"] = {
                    "r": recall / len(targets),
                    "p": precision / len(targets),
                    "f": fmeasure / len(targets),
                }
            return {"rouge": output_dict}

        except Exception as exception:
            raise RuntimeError(f"Unable to calculate rouge score - {str(exception)}")
