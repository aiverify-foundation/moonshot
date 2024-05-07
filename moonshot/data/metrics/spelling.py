import logging
from typing import Any

from transformers import pipeline

from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SpellingScore(MetricInterface):
    """
    SpellingScore uses Levenshetein Distance to find permutations within an edit distance of 2 form the original word
    before comparing to known words in a word frequency list.
    This code uses pyspellchecker (https://pypi.org/project/pyspellchecker/).
    """

    def __init__(self):
        self.id = "spelling"
        self.name = "SpellingScore"
        self.description = (
            "SpellingScore uses Levenshetein Distance to find permutations within an edit distance of 2 "
            "form the original word before comparing to known words in a word frequency list."
        )
        self.metric_config = self.get_metrics_configuration(self.id)

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the SpellingScore class.
        The metadata includes the unique identifier, the name, and the description of the class.

        Returns:
            dict | None: A dictionary containing the 'id', 'name', and 'description' of the SpellingScore class,
            or None if not applicable.
        """
        return {"id": self.id, "name": self.name, "description": self.description}

    @timeit
    async def get_results(
        self, prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Generate the function comment for the given function body in a markdown code block with
        the correct language syntax.

        Parameters:
            prompts (Any): The prompts for the function.
            predicted_results (Any): The predicted results for the function.
            targets (Any): The targets for the function.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The spellingscore of the results.

        """
        results = {}
        total_number_of_words = 0
        total_number_of_misspelled = 0

        fix_spelling = pipeline(
            "text2text-generation", model="oliverguhr/spelling-correction-english-base"
        )

        index = 0
        for result in predicted_results:
            this_result = {}

            corrected = fix_spelling(result, max_length=4096)[0]["generated_text"]
            corrected_split = corrected.split()
            difference = list(set(result.split()) - set(corrected_split))

            if len(corrected) != len(result):
                this_result["corrected"] = corrected
                this_result[
                    "error"
                ] = "Length of corrected text is not the same as given generated output."
            else:
                this_result["misspell"] = difference
                this_result["total_number_of_words"] = len(result)
                this_result["total_number_of_misspelled"] = len(difference)

            total_number_of_words += len(result)
            total_number_of_misspelled += len(difference)
            results[index] = this_result
            index += 1

        scores = {
            "corrected": results,
            "spelling_score": (total_number_of_words - total_number_of_misspelled)
            / total_number_of_words,
        }
        return {"spellingscore": scores}
