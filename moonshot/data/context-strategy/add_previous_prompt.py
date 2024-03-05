import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ContextOne:
    """
    This is a dummy context strategy module for users' reference. Users can copy and paste the codes here,
    and create a new Python file in the same directory and change the logic in the methods. Do not change
    the method names.
    """

    @staticmethod
    def add_in_context(
        prompt_without_context: str = None, list_of_previous_prompts: list = None
    ) -> str:
        """
        The method to process and insert the context. i.e. summarise the 5 previous prompts by calling another LLM.
        Insert the logic to create context in this method.
        Args:
            prompt_without_context (str, optional): The original prompt without context.
            list_of_previous_prompts (list, optional): The list of previous prompts in dict.
                The dict contains the following fields:
                - chat_id (int): ID of the chat
                - connection_id (str): ID of the connection
                - context_strategy (str): The context strategy that was used for that prompt (if any)
                - prompt_template (str): The name of the prompt template that was used (if any)
                - prompt (str): The original prompt that was entered (without context and prompt template)
                - prepared_prompt (str): The final prompt that was sent to the LLM
                  (with context and prompt template if any)
                - predicted_result (str): The response from the LLM

        Returns:
            str: The context to be sent with the prompt.
        """

        combined_contextualised_previous_prompt = "Context:"
        for previous_prompt_dict in list_of_previous_prompts:
            previous_prompt_str = previous_prompt_dict.get("prompt")
            combined_contextualised_previous_prompt += previous_prompt_str
        return combined_contextualised_previous_prompt + "\n"

    @staticmethod
    def get_number_of_prev_prompts() -> int:
        """
        A temporary method to store the number of previous prompts required for context strategy.

        Returns:
            int: The number of previous prompts required for context strategy.
        """
        num_previous_prompts = 1
        return num_previous_prompts
