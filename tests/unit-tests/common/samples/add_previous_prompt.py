from moonshot.src.redteaming.context_strategy.context_strategy_interface import (
    ContextStrategyInterface,
)
from moonshot.src.utils.timeit import timeit


class SampleContextStrategy(ContextStrategyInterface):
    """
    This is a dummy context strategy module for users' reference. Users can copy and paste the codes here,
    and create a new Python file in the same directory and change the logic in the methods. Do not change
    the method names.
    """

    def __init__(self, cs_id: str):
        self.id = cs_id
        self.name = "Add Previous Prompt"
        self.description = "This is a sample context strategy that adds in previous prompts to the current prompt. [Default: 5]"  # noqa: E501

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves and returns the metadata of the SampleContextStrategy class.
        The metadata includes the unique identifier, the name, and the description of the class.

        Returns:
            dict | None: A dictionary containing the 'id', 'name', and 'description' of the SampleContextStrategy class,
            or None if not applicable.
        """
        return {"id": self.id, "name": self.name, "description": self.description}

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
