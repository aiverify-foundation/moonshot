import importlib.resources
from enum import Enum
from typing import Union

from dotenv import dotenv_values

__app_name__ = "moonshot"


class EnvVariables(Enum):
    CONNECTORS_ENDPOINTS = "CONNECTORS_ENDPOINTS"
    CONNECTORS = "CONNECTORS"
    RECIPES = "RECIPES"
    RECIPES_PROCESSING_MODULES = "RECIPES_PROCESSING_MODULES"
    RUNNERS = "RUNNERS"
    COOKBOOKS = "COOKBOOKS"
    DATASETS = "DATASETS"
    PROMPT_TEMPLATES = "PROMPT_TEMPLATES"
    METRICS = "METRICS"
    METRICS_CONFIG = "METRICS_CONFIG"
    CONTEXT_STRATEGY = "CONTEXT_STRATEGY"
    RESULTS = "RESULTS"
    DATABASES = "DATABASES"
    SESSIONS = "SESSIONS"


class EnvironmentVars:
    env_vars = dotenv_values(".env")

    CONNECTORS_ENDPOINTS = env_vars.get(
        EnvVariables.CONNECTORS_ENDPOINTS.value,
        importlib.resources.files(__app_name__).joinpath("data/connectors-endpoints"),
    )
    CONNECTORS = env_vars.get(
        EnvVariables.CONNECTORS.value,
        importlib.resources.files(__app_name__).joinpath("data/connectors"),
    )
    RECIPES = env_vars.get(
        EnvVariables.RECIPES.value,
        importlib.resources.files(__app_name__).joinpath("data/recipes"),
    )
    RECIPES_PROCESSING_MODULES = env_vars.get(
        EnvVariables.RECIPES_PROCESSING_MODULES.value,
        importlib.resources.files(__app_name__).joinpath(
            "data/recipes-processing-modules"
        ),
    )
    RUNNERS = env_vars.get(
        EnvVariables.RUNNERS.value,
        importlib.resources.files(__app_name__).joinpath("data/runners"),
    )
    COOKBOOKS = env_vars.get(
        EnvVariables.COOKBOOKS.value,
        importlib.resources.files(__app_name__).joinpath("data/cookbooks"),
    )
    DATASETS = env_vars.get(
        EnvVariables.DATASETS.value,
        importlib.resources.files(__app_name__).joinpath("data/datasets"),
    )
    PROMPT_TEMPLATES = env_vars.get(
        EnvVariables.PROMPT_TEMPLATES.value,
        importlib.resources.files(__app_name__).joinpath("data/prompt-templates"),
    )
    METRICS = env_vars.get(
        EnvVariables.METRICS.value,
        importlib.resources.files(__app_name__).joinpath("data/metrics"),
    )
    METRICS_CONFIG = env_vars.get(
        EnvVariables.METRICS_CONFIG.value,
        importlib.resources.files(__app_name__).joinpath(
            "data/metrics/metrics_config.json"
        ),
    )
    CONTEXT_STRATEGY = env_vars.get(
        EnvVariables.CONTEXT_STRATEGY.value,
        importlib.resources.files(__app_name__).joinpath("data/context-strategy"),
    )
    RESULTS = env_vars.get(
        EnvVariables.RESULTS.value,
        importlib.resources.files(__app_name__).joinpath("data/results"),
    )
    DATABASES = env_vars.get(
        EnvVariables.DATABASES.value,
        importlib.resources.files(__app_name__).joinpath("data/databases"),
    )
    SESSIONS = env_vars.get(
        EnvVariables.SESSIONS.value,
        importlib.resources.files(__app_name__).joinpath("data/sessions"),
    )

    @staticmethod
    def load_env(env_dict: Union[dict, None] = None) -> None:
        """
        This method is used to load environment variables from a given dictionary.
        If the dictionary is not provided, it will use an empty dictionary.

        The method will set the class attributes with the corresponding values from the dictionary.
        If a key from the class attributes is not found in the dictionary, it will raise a KeyError.

        Args:
            env_dict (Union[dict, None]): A dictionary containing the environment variables to be loaded.
                                          If None, an empty dictionary will be used.

        Raises:
            KeyError: If a key from the class attributes is not found in the provided dictionary.
        """
        if env_dict is None:
            env_dict = dict()

        keys = [e.value for e in EnvVariables]

        for key in keys:
            if key in env_dict:
                setattr(EnvironmentVars, key, env_dict[key])
            else:
                print(
                    f"Unable to set {key}, not found in the provided environment variables."
                )
