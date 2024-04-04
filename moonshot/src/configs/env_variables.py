import importlib.resources
from enum import Enum
from pathlib import Path

__app_name__ = "moonshot"


class EnvVariables(Enum):
    CONNECTORS = "CONNECTORS"
    CONNECTORS_ENDPOINTS = "CONNECTORS_ENDPOINTS"
    CONTEXT_STRATEGY = "CONTEXT_STRATEGY"
    COOKBOOKS = "COOKBOOKS"
    DATABASES = "DATABASES"
    DATABASES_MODULES = "DATABASES_MODULES"
    DATASETS = "DATASETS"
    IO_MODULES = "IO_MODULES"
    METRICS = "METRICS"
    METRICS_CONFIG = "METRICS_CONFIG"
    PROMPT_TEMPLATES = "PROMPT_TEMPLATES"
    RECIPES = "RECIPES"
    RECIPES_PROCESSING_MODULES = "RECIPES_PROCESSING_MODULES"
    RESULTS = "RESULTS"
    RUNNERS = "RUNNERS"
    SESSIONS = "SESSIONS"


class EnvironmentVars:
    env_vars = {}

    CONNECTORS = [
        env_vars.get(EnvVariables.CONNECTORS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/connectors"))
    ]
    CONNECTORS_ENDPOINTS = [
        env_vars.get(EnvVariables.CONNECTORS_ENDPOINTS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/connectors-endpoints"))
    ]
    CONTEXT_STRATEGY = [
        env_vars.get(EnvVariables.CONTEXT_STRATEGY.value),
        str(importlib.resources.files(__app_name__).joinpath("data/context-strategy"))
    ]
    COOKBOOKS = [
        env_vars.get(EnvVariables.COOKBOOKS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/cookbooks"))
    ]
    DATABASES = [
        env_vars.get(EnvVariables.DATABASES.value), 
        str(importlib.resources.files(__app_name__).joinpath("data/databases"))
    ]
    DATABASES_MODULES = [
        env_vars.get(EnvVariables.DATABASES_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/databases-modules"))
    ]
    DATASETS = [
        env_vars.get(EnvVariables.DATASETS.value), 
        str(importlib.resources.files(__app_name__).joinpath("data/datasets"))
    ]
    IO_MODULES = [
        env_vars.get(EnvVariables.IO_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/io-modules"))
    ]
    METRICS = [
        env_vars.get(EnvVariables.METRICS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/metrics"))
    ]
    METRICS_CONFIG = [
        env_vars.get(EnvVariables.METRICS_CONFIG.value),
        str(importlib.resources.files(__app_name__).joinpath("data/metrics/metrics_config.json"))
    ]
    PROMPT_TEMPLATES = [
        env_vars.get(EnvVariables.PROMPT_TEMPLATES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/prompt-templates"))
    ]
    RECIPES = [
        env_vars.get(EnvVariables.RECIPES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/recipes"))
    ]
    RECIPES_PROCESSING_MODULES = [
        env_vars.get(EnvVariables.RECIPES_PROCESSING_MODULES.value),
        str(importlib.resources.files(__app_name__).joinpath("data/recipes-processing-modules"))
    ]
    RESULTS = [
        env_vars.get(EnvVariables.RESULTS.value), 
        str(importlib.resources.files(__app_name__).joinpath("data/results"))
    ]
    RUNNERS = [
        env_vars.get(EnvVariables.RUNNERS.value),
        str(importlib.resources.files(__app_name__).joinpath("data/runners"))
    ]
    SESSIONS = [
        env_vars.get(EnvVariables.SESSIONS.value), 
        str(importlib.resources.files(__app_name__).joinpath("data/sessions"))
    ]


    @staticmethod
    def load_env(env_dict: dict | None = None) -> None:
        """
        This method is used to load environment variables from a given dictionary.
        If the dictionary is not provided, it will use an empty dictionary.

        The method will set the class attributes with the corresponding values from the dictionary.
        If a key from the class attributes is not found in the dictionary, it will raise a KeyError.

        Args:
            env_dict (dict | None): A dictionary containing the environment variables to be loaded.
                                          If None, an empty dictionary will be used.

        Raises:
            KeyError: If a key from the class attributes is not found in the provided dictionary.
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
                    print(
                        f"Unable to set {key}. The provided path {given_path} does not exist. ",
                        "The stock set will be used.",
                    )
            else:
                unset_keys.append(key)
        if unset_keys:
            print(
                f"Unable to retrieve the following environment variables: {unset_keys}. The stock set will be used."
            )


    @staticmethod
    def get_file_path(file_type: EnvVariables, file_name: str) -> str:
        """
        This method retrieves the file path for a specific file type and file name.
        
        Args:
            file_type (EnvVariables): The type of file to retrieve.
            file_name (str): The name of the file to retrieve.
        
        Returns:
            str: The file path of the specified file if found.
        
        Raises:
            FileNotFoundError: If the specified file cannot be found in either the user-defined path or the resource path.
        """
        path_from_user, path_from_resource = getattr(EnvironmentVars, file_type.value)

        if path_from_user is not None:
            user_file_path = Path(path_from_user) / file_name
            if Path(user_file_path).exists():
                return str(user_file_path)
        
        resource_file_path = Path(path_from_resource) / file_name
        if Path(resource_file_path).exists():
            return str(resource_file_path)
                
        raise FileNotFoundError(f"{file_name} cannot be found.")
    

    @staticmethod
    def get_file_directory(file_type: EnvVariables) -> str:
        """
        This method retrieves the directory path for a specific file type.
        
        Args:
            file_type (EnvVariables): The type of file to retrieve the directory path for.
        
        Returns:
            str: The directory path of the specified file type.
        """
        path_from_user, path_from_resource = getattr(EnvironmentVars, file_type.value)

        if path_from_user is not None:
            return str(Path(path_from_user))
        
        return str(Path(path_from_resource))
    