import importlib.resources
from typing import Union

from dotenv import dotenv_values

__app_name__ = "moonshot"


class EnvironmentVars:
    env_vars = dotenv_values(".env")

    CONNECTORS_ENDPOINTS = env_vars.get(
        "CONNECTORS_ENDPOINTS",
        importlib.resources.files(__app_name__).joinpath("data/connectors-endpoints"),
    )
    CONNECTORS = env_vars.get(
        "CONNECTORS",
        importlib.resources.files(__app_name__).joinpath("data/connectors"),
    )
    RECIPES = env_vars.get(
        "RECIPES", importlib.resources.files(__app_name__).joinpath("data/recipes")
    )
    COOKBOOKS = env_vars.get(
        "COOKBOOKS", importlib.resources.files(__app_name__).joinpath("data/cookbooks")
    )
    DATASETS = env_vars.get(
        "DATASETS", importlib.resources.files(__app_name__).joinpath("data/datasets")
    )
    PROMPT_TEMPLATES = env_vars.get(
        "PROMPT_TEMPLATES",
        importlib.resources.files(__app_name__).joinpath("data/prompt-templates"),
    )
    METRICS = env_vars.get(
        "METRICS", importlib.resources.files(__app_name__).joinpath("data/metrics")
    )
    METRICS_CONFIG = env_vars.get(
        "METRICS_CONFIG",
        importlib.resources.files(__app_name__).joinpath(
            "data/metrics/metrics_config.json"
        ),
    )
    CONTEXT_STRATEGY = env_vars.get(
        "CONTEXT_STRATEGY",
        importlib.resources.files(__app_name__).joinpath("data/context-strategy"),
    )
    RESULTS = env_vars.get(
        "RESULTS", importlib.resources.files(__app_name__).joinpath("data/results")
    )
    DATABASES = env_vars.get(
        "DATABASES", importlib.resources.files(__app_name__).joinpath("data/databases")
    )
    SESSIONS = env_vars.get(
        "SESSIONS", importlib.resources.files(__app_name__).joinpath("data/sessions")
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

        keys = [
            "CONNECTORS_ENDPOINTS",
            "CONNECTORS",
            "RECIPES",
            "COOKBOOKS",
            "DATASETS",
            "PROMPT_TEMPLATES",
            "METRICS",
            "METRICS_CONFIG",
            "CONTEXT_STRATEGY",
            "RESULTS",
            "DATABASES",
            "SESSIONS",
        ]

        for key in keys:
            if key in env_dict:
                setattr(EnvironmentVars, key, env_dict[key])
            else:
                print(
                    f"Unable to set {key}, not found in the provided environment variables."
                )
