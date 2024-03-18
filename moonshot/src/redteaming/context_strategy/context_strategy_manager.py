import glob
import inspect
import os
from pathlib import Path
from typing import Any, Optional

from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.utils.import_modules import (
    create_module_spec,
    import_module_from_spec,
)


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
    ) -> Optional[str]:
        context_strategy_instance = ContextStrategyManager.load_context_strategy_module(
            context_strategy_name
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

    @staticmethod
    def load_context_strategy_module(context_strategy_name: str) -> Any:
        """
        Loads a context strategy module by its name.

        This method attempts to load a context strategy module specified by the context_strategy_name argument.
        It first creates a module specification using the create_module_spec function. If the specification exists,
        it imports the module and iterates through its attributes to find a class that matches the module name.
        If such a class is found, it is returned; otherwise, None is returned.

        Args:
            context_strategy_name (str): The name of the context strategy module to load.

        Returns:
            Optional[Type]: The loaded context strategy class if found, None otherwise.
        """
        module_spec = create_module_spec(
            context_strategy_name,
            f"{EnvironmentVars.CONTEXT_STRATEGY}/{context_strategy_name}.py",
        )

        # Check if the module specification exists
        if module_spec:
            # Import the module
            module = import_module_from_spec(module_spec)

            # Iterate through the attributes of the module
            for attr in dir(module):
                # Get the attribute object
                obj = getattr(module, attr)

                # Check if the attribute is a class and has the same module name as the context strategy name
                if inspect.isclass(obj) and obj.__module__ == context_strategy_name:
                    return obj

        # Return None if no instance of the context strategy class is found
        return None
