import logging

from moonshot.src.redteaming.context_strategy.context_strategy_interface import (
    ContextStrategyInterface,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


NUM_PREVIOUS_PROMPTS = 5


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
        Adds previous prompts to the user prompt.

        Args:
            user_prompt (str): The current user prompt.
            list_of_previous_prompts (list, optional): List of previous prompts to add. Defaults to None. It contains
            dictionaries of chats:
                chat_record_id: The chat ID,
                conn_id: The connection ID,
                context_strategy: The name of the context strategy used,
                prompt_template: The name of the prompt template used,
                prompt: The user's original prompt,
                prepared_prompt: The user's prompt after being modified by prompt template and/or
                context strategy (if any)
                predicted_result: The returned results from the LLM,
                duration: The amount of time taken to run the prompt,
                prompt_time: The time when the prompt was made

        Returns:
            str: The updated user prompt with previous prompts added.
        """
        for previous_prompt in list_of_previous_prompts[:NUM_PREVIOUS_PROMPTS]:
            user_prompt += previous_prompt.get("prepared_prompt")
            user_prompt += "\n"
        return user_prompt
