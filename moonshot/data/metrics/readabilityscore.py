import logging
from typing import Any

from readability import Readability

from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReadabilityScore:
    """
    ReadabilityScore uses Flesch Reading Ease to compute the complexity of the output
    """

    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculates the readability score and the number of valid and invalid responses based on the predicted results.

        Args:
            prompts (Any): The prompts used for generating the predicted results.
            predicted_results (Any): The predicted results.
            targets (Any): The target results.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: A dictionary containing the readability score, the number of valid responses,
            and the list of invalid responses.
        """
        results = 0
        temp_scores = {}
        num_of_output_more_than_100 = 0
        response_less_than_100 = []

        for result in predicted_results:
            if len(result.split()) < 100:
                temp_scores[result] = -1
                response_less_than_100.append(result)
            else:
                r = Readability(result)
                this_score = r.flesch_kincaid()
                temp_scores[result] = this_score.score
                results += this_score.score
                num_of_output_more_than_100 += 1

        if num_of_output_more_than_100 > 0:
            temp_score = results / num_of_output_more_than_100
        else:
            temp_score = 0

        return {
            "readabilityscore": temp_score,
            "valid_response": len(predicted_results) - len(response_less_than_100),
            "invalid_response": response_less_than_100,
        }
