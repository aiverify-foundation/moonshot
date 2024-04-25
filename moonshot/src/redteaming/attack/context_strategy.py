from __future__ import annotations

from pathlib import Path
from typing import Any

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.session.chat import Chat
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

    @staticmethod
    def get_all_context_strategy_names() -> list[str]:
        """
        Retrieves the names of all context strategy files.

        This method fetches the names of all context strategy files by scanning the directory specified in the
        EnvironmentVars. It filters out filenames containing double underscores before returning the list
        of context strategy names.

        Returns:
            list: A list of context strategy file names.
        """
        filepaths = []
        context_strategy_files = Storage.get_objects(
            EnvVariables.CONTEXT_STRATEGY.name, "json"
        )
        for context_strategy in context_strategy_files:
            filepaths.append(Path(context_strategy).stem)
        return filepaths

    @staticmethod
    def delete_context_strategy(context_strategy_name: str) -> None:
        """
        Deletes a context strategy file.

        This method attempts to delete the specified context strategy file.
        It constructs the file path using the EnvironmentVars and the context strategy name.
        If the deletion is successful, it prints a success message; otherwise, it prints an error message.

        Args:
            context_strategy_name (str): The name of the context strategy file to delete.

        Returns:
            None
        """
        try:
            Storage.delete_object(
                EnvVariables.CONTEXT_STRATEGY.name, context_strategy_name, "py"
            )

        except Exception as e:
            print(f"Failed to context strategy: {str(e)}")
            raise e

    @staticmethod
    def process_prompt_cs(
        user_prompt: str,
        context_strategy_name: str,
        db_instance: Any,
        endpoint_id,
        num_of_previous_chats: int,
    ) -> str:
        context_strategy_instance = get_instance(
            context_strategy_name,
            Storage.get_filepath(
                EnvVariables.CONTEXT_STRATEGY.name, context_strategy_name, "py"
            ),
        )

        if context_strategy_instance:
            # get the last n chats
            list_of_chats = Chat.get_n_chat_history(
                db_instance, endpoint_id, num_of_previous_chats
            )
            context_strategy_instance = context_strategy_instance()
            return context_strategy_instance.add_in_context(user_prompt, list_of_chats)
        else:
            print(
                "Cannot load context strategy. Make sure the name of the context strategy is correct."
            )
            return ""
