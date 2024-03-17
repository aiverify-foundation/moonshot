import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SampleContextStrategy:
    """
    This is a dummy context strategy module for users' reference. Users can copy and paste the codes here,
    and create a new Python file in the same directory and change the logic in the methods. Do not change
    the method names.
    """

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
        for previous_prompt in list_of_previous_prompts[
            : SampleContextStrategy.get_number_of_prev_prompts()
        ]:
            user_prompt += previous_prompt.get("prepared_prompt")
            user_prompt += "\n"
        return user_prompt

    @staticmethod
    def get_number_of_prev_prompts() -> int:
        """
        A temporary method to store the number of previous prompts required for context strategy.

        Returns:
            int: The number of previous prompts required for context strategy.
        """
        num_previous_prompts = 5
        return num_previous_prompts
