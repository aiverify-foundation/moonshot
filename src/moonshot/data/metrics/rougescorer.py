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
        """
        Calculate the rouge scores for the given output responses and target values.

        Args:
            output_response (Any): The output responses to evaluate.
            targets (Any): The target values for evaluation.

        Returns:
            dict: A dictionary containing the calculated rouge scores.

        Raises:
            RuntimeError: If there is an error calculating the rouge scores.
        """
        try:
            # Define the test metrics to calculate
            test_metrics = ["rouge1", "rouge2", "rougeLsum"]

            # Initialize average recall, precision, and f-measure lists
            avg_recall = [0.0, 0.0, 0.0]
            avg_precision = [0.0, 0.0, 0.0]
            avg_fmeasure = [0.0, 0.0, 0.0]

            # Initialize the output dictionary and individual scores list
            output_dict = {}
            individual_scores = []

            # Calculate rouge scores for each target-output pair
            print("Attempting to calculate rouge score")
            scorer = rouge_scorer.RougeScorer(test_metrics)
            for target, output in zip(targets, output_response):
                scores = scorer.score(target, output)
                test_metrics_dict = {}
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

            # Add individual scores to the output dictionary
            output_dict["rouge-scores"] = individual_scores

            # Calculate average scores and add them to the output dictionary
            for avg_index, (recall, precision, fmeasure) in enumerate(
                zip(avg_recall, avg_precision, avg_fmeasure)
            ):
                output_dict[f"avg_{test_metrics[avg_index]}"] = {
                    "r": recall / len(targets),
                    "p": precision / len(targets),
                    "f": fmeasure / len(targets),
                }

            # Return the final rouge scores dictionary
            return {"rouge": output_dict}

        except Exception as exception:
            # Raise an error if there is an exception during calculation
            raise RuntimeError(f"Unable to calculate rouge score - {str(exception)}")
