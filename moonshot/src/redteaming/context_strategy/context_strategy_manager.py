import glob
import os
from pathlib import Path

from moonshot.src.configs.env_variables import EnvironmentVars, EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class ContextStrategyManager:
    def __init__(self):
        pass

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
        context_strategy_file_path = f"{EnvironmentVars.CONTEXT_STRATEGY}"
        filepaths = [
            Path(fp).stem
            for fp in glob.iglob(f"{context_strategy_file_path}/*.py")
            if "__" not in fp
        ]
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
            os.remove(f"{EnvironmentVars.CONTEXT_STRATEGY}/{context_strategy_name}.py")
        except OSError as e:
            print(
                f"Failed to delete Context Strategy file: {e.filename} - {e.strerror}"
            )
        else:
            print(
                f"Successfully deleted Context Strategy file: - {context_strategy_name}"
            )

    @staticmethod
    def process_prompt_cs(
        user_prompt: str, context_strategy_name: str, list_of_chats: list[dict]
    ) -> str | None:
        context_strategy_instance = get_instance(
            context_strategy_name,
            Storage.get_filepath(
                EnvVariables.CONTEXT_STRATEGY.name, context_strategy_name, "py"
            ),
        )

        if context_strategy_instance:
            context_strategy_instance = context_strategy_instance()
            # TODO make number of previous prompts an input from user.
            # Currently it is configured in the context strategy module itself
            return context_strategy_instance.add_in_context(user_prompt, list_of_chats)
        else:
            print(
                "Cannot load context strategy. Make sure the name of the context strategy is correct."
            )
            return None
