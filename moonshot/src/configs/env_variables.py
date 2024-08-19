import importlib.resources
from enum import Enum
from pathlib import Path

from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)

__app_name__ = "moonshot"


class EnvVariables(Enum):
    ATTACK_MODULES = "ATTACK_MODULES"
    BOOKMARKS = "BOOKMARKS"
    CONNECTORS = "CONNECTORS"
    CONNECTORS_ENDPOINTS = "CONNECTORS_ENDPOINTS"
    CONTEXT_STRATEGY = "CONTEXT_STRATEGY"
    COOKBOOKS = "COOKBOOKS"
    DATABASES = "DATABASES"
    DATABASES_MODULES = "DATABASES_MODULES"
    DATASETS = "DATASETS"
    IO_MODULES = "IO_MODULES"
    METRICS = "METRICS"
    PROMPT_TEMPLATES = "PROMPT_TEMPLATES"
    RECIPES = "RECIPES"
    RESULTS = "RESULTS"
    RESULTS_MODULES = "RESULTS_MODULES"
    RUNNERS = "RUNNERS"
    RUNNERS_MODULES = "RUNNERS_MODULES"


class EnvironmentVars:
    env_vars = {}

    ATTACK_MODULES = [
        env_vars.get(EnvVariables.ATTACK_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/attack-modules")),
    ]
    BOOKMARKS = [
        env_vars.get(EnvVariables.BOOKMARKS.value),
        str(
            importlib.resources.files(__app_name__).joinpath(
                "data/generated-outputs/bookmarks"
            )
        ),
    ]
    CONNECTORS = [
        env_vars.get(EnvVariables.CONNECTORS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/connectors")),
    ]
    CONNECTORS_ENDPOINTS = [
        env_vars.get(EnvVariables.CONNECTORS_ENDPOINTS.value),
        str(
            importlib.resources.files(__app_name__).joinpath(
                "data/connectors-endpoints"
            )
        ),
    ]
    CONTEXT_STRATEGY = [
        env_vars.get(EnvVariables.CONTEXT_STRATEGY.value),
        str(importlib.resources.files(__app_name__).joinpath("data/context-strategy")),
    ]
    COOKBOOKS = [
        env_vars.get(EnvVariables.COOKBOOKS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/cookbooks")),
    ]
    DATABASES = [
        env_vars.get(EnvVariables.DATABASES.value),
        str(
            importlib.resources.files(__app_name__).joinpath(
                "data/generated-outputs/databases"
            )
        ),
    ]
    DATABASES_MODULES = [
        env_vars.get(EnvVariables.DATABASES_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/databases-modules")),
    ]
    DATASETS = [
        env_vars.get(EnvVariables.DATASETS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/datasets")),
    ]
    IO_MODULES = [
        env_vars.get(EnvVariables.IO_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/io-modules")),
    ]
    METRICS = [
        env_vars.get(EnvVariables.METRICS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/metrics")),
    ]
    PROMPT_TEMPLATES = [
        env_vars.get(EnvVariables.PROMPT_TEMPLATES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/prompt-templates")),
    ]
    RECIPES = [
        env_vars.get(EnvVariables.RECIPES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/recipes")),
    ]
    RESULTS = [
        env_vars.get(EnvVariables.RESULTS.value),
        str(
            importlib.resources.files(__app_name__).joinpath(
                "data/generated-outputs/results"
            )
        ),
    ]
    RESULTS_MODULES = [
        env_vars.get(EnvVariables.RESULTS_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/results-modules")),
    ]
    RUNNERS = [
        env_vars.get(EnvVariables.RUNNERS.value),
        str(
            importlib.resources.files(__app_name__).joinpath(
                "data/generated-outputs/runners"
            )
        ),
    ]
    RUNNERS_MODULES = [
        env_vars.get(EnvVariables.RUNNERS_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/runners-modules")),
    ]

    @staticmethod
    def load_env(env_dict: dict | None = None) -> None:
        """
        This method is used to load environment variables from a provided dictionary.
        If the dictionary is not provided, it defaults to an empty dictionary.

        The method updates the class attributes with the corresponding values from the dictionary.
        If a key from the class attributes is not found in the dictionary, it will not be updated and a
        message will be printed.

        Args:
            env_dict (dict | None): A dictionary containing the environment variables to be loaded.
                                    If None, an empty dictionary will be used.
        """
        if env_dict is None:
            env_dict = dict()

        keys = [e.value for e in EnvVariables]
        unset_keys = []
        for key in keys:
            if key in env_dict:
                given_path = Path(env_dict[key])
                if given_path.exists():
                    EnvironmentVars.__dict__[key][0] = str(given_path)
                else:
                    logger.warning(
                        f"Unable to set {key}. The provided path {given_path} does not exist. "
                        "The stock set will be used."
                    )
            else:
                unset_keys.append(key)
        if unset_keys:
            logger.warning(
                f"Unable to retrieve the following environment variables: {unset_keys}. The stock set will be used."
            )

    @staticmethod
    def get_file_path(file_type: str, file_name: str, ignore_existance: bool) -> str:
        """
        This method is used to get the file path for a given file type and file name.
        If the ignore existance flag is set to True, it returns the file path even if the file does not exist.

        Args:
            file_type (str): The type of the file (e.g., 'recipe', 'cookbook').
            file_name (str): The name of the file.
            ignore_existance (bool): A flag indicating whether to return the file path
                             even if the file does not exist.

        Returns:
            str: The file path of the file.
        """
        for directory in EnvironmentVars.get_file_directory(file_type):
            file_path = Path(directory) / file_name
            if ignore_existance:
                return str(file_path)
            else:
                if Path(file_path).exists():
                    return str(file_path)
        return ""

    @staticmethod
    def get_file_directory(file_type: str) -> list[str]:
        """
        This method retrieves the directory paths associated with a specified file type.

        Args:
            file_type (str): The type of file for which the directory paths are to be retrieved.

        Returns:
            list[str]: A list containing the directory paths associated with the given file type.
        """
        path_from_user, path_from_resource = getattr(EnvironmentVars, file_type)

        if path_from_user is not None:
            return [path_from_user, path_from_resource]
        else:
            return [path_from_resource]
