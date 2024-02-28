import os

__app_name__ = "moonshot"
__version__ = "0.1.0"

import importlib.resources


class EnvironmentVars:
    CONNECTORS_ENDPOINTS = importlib.resources.files(__app_name__).joinpath("data/connectors-endpoints")
    CONNECTORS = importlib.resources.files(__app_name__).joinpath("data/connectors")
    RECIPES = importlib.resources.files(__app_name__).joinpath("data/recipes")
    COOKBOOKS = importlib.resources.files(__app_name__).joinpath("data/cookbooks")
    DATASETS = importlib.resources.files(__app_name__).joinpath("data/datasets")
    PROMPT_TEMPLATES = importlib.resources.files(__app_name__).joinpath("data/prompt-templates")
    METRICS = importlib.resources.files(__app_name__).joinpath("data/metrics")
    METRICS_CONFIG = importlib.resources.files(__app_name__).joinpath("data/metrics/metrics_config.json")
    CONTEXT_STRATEGY = importlib.resources.files(__app_name__).joinpath("data/context-strategy")
    RESULTS = importlib.resources.files(__app_name__).joinpath("data/results")
    DATABASES = importlib.resources.files(__app_name__).joinpath("data/databases")
    SESSIONS = importlib.resources.files(__app_name__).joinpath("data/sessions")
    ENABLE_MULTIPROCESSING = "true"
