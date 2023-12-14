import logging
from typing import Any

from rouge import Rouge

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RougeScore:
    """
    RougeScore returns the various rouge scores.
    """

    @staticmethod
    def get_results(output_response: Any, targets: Any) -> dict:
        rouge = Rouge()
        scores = rouge.get_scores(output_response, targets, avg=True)
        return {"rouge": scores}
