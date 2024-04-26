import logging

from moonshot.src.redteaming.context_strategy.context_strategy_interface import (
    ContextStrategyInterface,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SampleContextStrategy(ContextStrategyInterface):
    """
    This is a dummy context strategy module for users' reference. Users can copy and paste the codes here,
    and create a new Python file in the same directory and change the logic in the methods. Do not change
    the method names.
    """

    def __init__(self):
        self.id = "add_previous_prompt"
        self.name = "Add Previous Prompt"
        self.description = "This is a sample context strategy that adds in previous prompts to the current prompt."
        self.version = "0.1.0"

    @staticmethod
    def add_in_context(
        user_prompt: str, list_of_previous_prompts: list[dict] = []
    ) -> str:
        """
        Adds previous prompts to the current prompt.

        Args:
            user_prompt (str): The current prompt.
            list_of_previous_prompts (list[dict], optional): List of previous prompts. Defaults to [].

        Returns:
            str: The updated prompt with previous prompts added.
        """
        for previous_prompt in list_of_previous_prompts:
            user_prompt += str(previous_prompt.get("prepared_prompt"))
            user_prompt += "\n"
        return user_prompt
