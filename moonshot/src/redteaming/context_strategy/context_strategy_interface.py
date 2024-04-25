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
    ):
        pass

    @abstractmethod
    def get_number_of_prev_prompts(self, no_prev_prompts: int):
        pass
