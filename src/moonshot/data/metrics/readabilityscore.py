import logging
from typing import Any

from readability import Readability

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ReadabilityScore:
    """
    ReadabilityScore uses Flesch Reading Ease to compute the complexity of the output
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        results = 0
        temp_scores = {}
        num_of_output_more_than_100 = 0
        response_less_than_100 = []

        for response in output_response:
            if len(response.split()) < 100:
                temp_scores[response] = -1
                response_less_than_100.append(response)
            else:
                r = Readability(response)
                this_score = r.flesch_kincaid()
                temp_scores[response] = this_score.score
                results += this_score.score
                num_of_output_more_than_100 += 1

        if num_of_output_more_than_100 > 0:
            temp_score = results / num_of_output_more_than_100
        else:
            temp_score = 0

        return {
            "readabilityscore": temp_score,
            "valid_response": len(output_response) - len(response_less_than_100),
            "invalid_response": response_less_than_100,
        }
