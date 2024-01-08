import os

__app_name__ = "moonshot"
__version__ = "0.1.0"

from dotenv import dotenv_values


class EnvironmentVars:
    LLM_ENDPOINTS = None
    LLM_CONNECTION_TYPES = None
    RECIPES = None
    COOKBOOKS = None
    DATASETS = None
    PROMPT_TEMPLATES = None
    METRICS = None
    METRICS_CONFIG = None
    RESULTS = None
    DATABASES = None
    SESSIONS = None
    ENABLE_MULTIPROCESSING = None


def read_env_file(env_file: str = ".env") -> dict:
    """
    Reads the contents of an environment file and returns them as a dictionary.

    Args:
        env_file (str): The path to the environment file. Defaults to ".env".

    Returns:
        dict: A dictionary containing the key-value pairs from the environment file.
    """
    return dotenv_values(env_file)


def load_env(env_dict: dict = None) -> None:
    """
    Loads env var from the input dictionary or from the system environment variables if no dictionary is provided.

    Args:
        env_dict (dict): A dictionary containing the key-value pairs from the environment file.
    """
    if env_dict is None:
        env_dict = {}

    # Load the new environment variables
    EnvironmentVars.LLM_ENDPOINTS = env_dict.get(
        "LLM_ENDPOINTS", os.environ.get("LLM_ENDPOINTS", "moonshot/data/llm-endpoints")
    )
    EnvironmentVars.LLM_CONNECTION_TYPES = env_dict.get(
        "LLM_CONNECTION_TYPES",
        os.environ.get("LLM_CONNECTION_TYPES", "moonshot/data/llm-connection-types"),
    )
    EnvironmentVars.RECIPES = env_dict.get(
        "RECIPES", os.environ.get("RECIPES", "moonshot/data/recipes")
    )
    EnvironmentVars.COOKBOOKS = env_dict.get(
        "COOKBOOKS", os.environ.get("COOKBOOKS", "moonshot/data/cookbooks")
    )
    EnvironmentVars.DATASETS = env_dict.get(
        "DATASETS", os.environ.get("DATASETS", "moonshot/data/datasets")
    )
    EnvironmentVars.PROMPT_TEMPLATES = env_dict.get(
        "PROMPT_TEMPLATES",
        os.environ.get("PROMPT_TEMPLATES", "moonshot/data/prompt-templates"),
    )
    EnvironmentVars.METRICS = env_dict.get(
        "METRICS", os.environ.get("METRICS", "moonshot/data/metrics")
    )
    EnvironmentVars.METRICS_CONFIG = env_dict.get(
        "METRICS_CONFIG",
        os.environ.get("METRICS_CONFIG", "moonshot/data/metrics/metrics_config.json"),
    )
    EnvironmentVars.RESULTS = env_dict.get(
        "RESULTS", os.environ.get("RESULTS", "moonshot/data/results")
    )
    EnvironmentVars.DATABASES = env_dict.get(
        "DATABASES", os.environ.get("DATABASES", "moonshot/data/databases")
    )
    EnvironmentVars.SESSIONS = env_dict.get(
        "SESSIONS", os.environ.get("SESSIONS", "moonshot/data/sessions")
    )
    EnvironmentVars.ENABLE_MULTIPROCESSING = env_dict.get(
        "ENABLE_MULTIPROCESSING", os.environ.get("ENABLE_MULTIPROCESSING", "true")
    )

    # Set environment variables
    os.environ["LLM_ENDPOINTS"] = EnvironmentVars.LLM_ENDPOINTS
    os.environ["LLM_CONNECTION_TYPES"] = EnvironmentVars.LLM_CONNECTION_TYPES
    os.environ["RECIPES"] = EnvironmentVars.RECIPES
    os.environ["COOKBOOKS"] = EnvironmentVars.COOKBOOKS
    os.environ["DATASETS"] = EnvironmentVars.DATASETS
    os.environ["PROMPT_TEMPLATES"] = EnvironmentVars.PROMPT_TEMPLATES
    os.environ["METRICS"] = EnvironmentVars.METRICS
    os.environ["METRICS_CONFIG"] = EnvironmentVars.METRICS_CONFIG
    os.environ["RESULTS"] = EnvironmentVars.RESULTS
    os.environ["DATABASES"] = EnvironmentVars.DATABASES
    os.environ["SESSIONS"] = EnvironmentVars.SESSIONS
    os.environ["ENABLE_MULTIPROCESSING"] = EnvironmentVars.ENABLE_MULTIPROCESSING


# Load environment variables
config = read_env_file()
load_env(config)
