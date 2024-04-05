from __future__ import annotations

from abc import abstractmethod

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class ContextStrategy:
    def __init__(self) -> None:
        pass

    @classmethod
    def load(cls, cs_id: str) -> ContextStrategy:
        """
        Retrieves a context strategy module instance by its ID.

        This method attempts to load a context strategy instance using the provided ID. If the context strategy instance
        is found, it is returned. If the context strategy instance does not exist, a RuntimeError is raised.

        Args:
            cs_id (str): The unique identifier of the context strategy to be retrieved.

        Returns:
            ContextStrategy: The retrieved context strategy instance.

        Raises:
            RuntimeError: If the context strategy instance does not exist.
        """
        context_strategy_inst = get_instance(
            cs_id,
            Storage.get_filepath(EnvVariables.CONTEXT_STRATEGY.name, cs_id, "py"),
        )
        if context_strategy_inst:
            return context_strategy_inst()
        else:
            raise RuntimeError(
                f"Unable to get defined context strategy instance - {cs_id}"
            )

    @abstractmethod
    def add_in_context(
        self, user_prompt: str, list_of_previous_prompts: list[dict] = []
    ):
        pass

    @abstractmethod
    def get_number_of_prev_prompts(self, no_prev_prompts: int):
        pass
