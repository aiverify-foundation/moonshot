from __future__ import annotations

from pathlib import Path

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class ContextStrategy:
    def __init__(self, cs_id: str) -> None:
        self.id = cs_id

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
            return context_strategy_inst(cs_id)
        else:
            raise RuntimeError(
                f"Unable to get defined context strategy instance - {cs_id}"
            )

    @staticmethod
    def get_all_context_strategies() -> list[str]:
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
            EnvVariables.CONTEXT_STRATEGY.name, "py"
        )
        for context_strategy in context_strategy_files:
            filepaths.append(Path(context_strategy).stem)
        return filepaths

    @staticmethod
    def delete(cs_id: str) -> bool:
        """
        Deletes a context strategy module instance by its ID.

        This method attempts to delete a context strategy instance using the provided ID.
        If the deletion is successful, it returns True.

        If an error occurs during the deletion process, it prints an error message and re-raises the exception.

        Args:
            cs_id (str): The unique identifier of the context strategy to be deleted.

        Returns:
            bool: True if the deletion was successful.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.CONTEXT_STRATEGY.name, cs_id, "py")
            return True

        except Exception as e:
            logger.error(f"Failed to delete context strategy: {str(e)}")
            raise e

    @staticmethod
    def process_prompt_cs(
        user_prompt: str,
        context_strategy_name: str,
        db_instance: DBInterface,
        endpoint_id,
        num_of_previous_chats: int,
    ) -> str:
        """
        Process the user prompt using the specified context strategy.

        Args:
            user_prompt (str): The user prompt to process.
            context_strategy_name (str): The name of the context strategy to use.
            db_instance (DBInterface): The database interface instance.
            endpoint_id: The ID of the endpoint.
            num_of_previous_chats (int): The number of previous chats to add.

        Returns:
            str: The processed user prompt based on the context strategy.
        """
        from moonshot.src.redteaming.session.chat import Chat

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
            context_strategy_instance = context_strategy_instance(context_strategy_name)
            return context_strategy_instance.add_in_context(user_prompt, list_of_chats)
        else:
            logger.error(
                "Cannot load context strategy. Make sure the name of the context strategy is correct."
            )
            return ""
