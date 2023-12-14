import logging
from typing import Any

from transformers import pipeline

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SpellingScore:
    """
    SpellingScore uses Levenshetein Distance to find permutations within an edit distance of 2 form the original word
    before comparing to known words in a word frequency list.
    This code uses pyspellchecker (https://pypi.org/project/pyspellchecker/).
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        results = {}
        total_number_of_words = 0
        total_number_of_misspelled = 0

        fix_spelling = pipeline(
            "text2text-generation", model="oliverguhr/spelling-correction-english-base"
        )

        index = 0
        for response in output_response:
            this_result = {}

            corrected = fix_spelling(response, max_length=4096)[0]["generated_text"]
            corrected_split = corrected.split()
            difference = list(set(response.split()) - set(corrected_split))

            if len(corrected) != len(response):
                this_result["corrected"] = corrected
                this_result[
                    "error"
                ] = "Length of corrected text is not the same as given generated output."
            else:
                this_result["misspell"] = difference
                this_result["total_number_of_words"] = len(response)
                this_result["total_number_of_misspelled"] = len(difference)

            total_number_of_words += len(response)
            total_number_of_misspelled += len(difference)
            results[index] = this_result
            index += 1

        scores = {
            "corrected": results,
            "spelling_score": (total_number_of_words - total_number_of_misspelled)
            / total_number_of_words,
        }
        return {"spellingscore": scores}
