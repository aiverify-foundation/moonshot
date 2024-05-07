from abc import abstractmethod

from moonshot.src.utils.timeit import timeit


class ContextStrategyInterface:
    @abstractmethod
    @timeit
    def get_metadata(self) -> dict | None:
        """
        Abstract method to retrieve metadata from the context strategy.

        Returns:
            dict | None: Returns a dictionary containing the metadata of the context strategy, or None if the
            operation was unsuccessful.
        """
        pass

    @abstractmethod
    def add_in_context(
        self, user_prompt: str, list_of_previous_prompts: list[dict] = []
    ) -> None:
        """
        Abstract method to add a user prompt and list of previous prompts to the context strategy.

        Args:
            user_prompt (str): The user prompt to be added to the context strategy.
            list_of_previous_prompts (list[dict], optional): List of previous prompts. Defaults to [].

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_number_of_prev_prompts(self, no_prev_prompts: int) -> int:
        """
        Abstract method to get the number of previous prompts to be retrieved from the context strategy.

        Args:
            no_prev_prompts (int): The number of previous prompts to retrieve.

        Returns:
            int: The number of previous prompts to be retrieved.
        """
        pass
