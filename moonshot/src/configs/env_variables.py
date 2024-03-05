import importlib.resources
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
    ENABLE_MULTIPROCESSING = env_vars.get("ENABLE_MULTIPROCESSING", "true")
