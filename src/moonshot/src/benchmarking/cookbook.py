import glob
import json
from pathlib import Path
from typing import Any

from slugify import slugify

from moonshot.src.benchmarking.recipe import run_recipes_with_endpoints
from moonshot.src.common.env_variables import EnvironmentVars


class Cookbook:
    @classmethod
    def load_from_json_config(cls, cookbook_config: str) -> Any:
        """
        Loads an instance of the class from a JSON configuration.
        This class method allows loading an instance of the class from a JSON configuration stored in a file
        or a string.

        Args:
            cookbook_config (str): A JSON configuration representing the instance's parameters.

        Returns:
            An instance of the class created from the JSON configuration.
        """
        with open(
            f"{EnvironmentVars.COOKBOOKS}/{cookbook_config}.json", "r"
        ) as json_file:
            file_info = json.load(json_file)
            return cls(
                Path(cookbook_config).stem,
                file_info["name"],
                file_info["description"],
                file_info["recipes"],
            )

    def __init__(self, id: str, name: str, description: str, recipes: list):
        self.id = id
        self.name = name
        self.description = description
        self.recipes = recipes
        self.results = None

    def run(self, endpoints: list, num_of_prompts: int, db_file: str) -> None:
        """
        Runs the cookbook with the given endpoints, number of prompts, and the database file to write to.

        Args:
            endpoints (list): A list of endpoints to run the recipes with.
            num_of_prompts (int): The number of prompts to use when running the recipes.
            db_file (str): The path to the database file to write the results to.
        """
        print(
            f"🔃 Running cookbook ({self.name})... do not close this terminal.\n"
            f"You can start a new terminal to continue working."
        )

        # Run the recipes with the defined endpoints
        self.results = run_recipes_with_endpoints(
            self.recipes, endpoints, num_of_prompts, db_file
        )


def get_all_cookbooks() -> list:
    """
    This static method retrieves a list of available cookbooks.

    Returns:
        list: A list of available cookbooks. Each item in the list represents a cookbook with details such as
        the name, description, and included recipes.
    """
    return_list = list()
    filepaths = glob.glob(f"{EnvironmentVars.COOKBOOKS}/*.json")
    for filepath in filepaths:
        if "__" in filepath:
            continue

        with open(filepath, "r") as json_file:
            file_info = json.load(json_file)

            # Add filename (id)
            file_info["filename"] = Path(filepath).stem

            return_list.append(file_info)
    return return_list


def get_cookbook(cookbook_name: str) -> dict:
    """
    This static method retrieves the desired cookbook.

    Args:
        cookbook_name (str): The name of a cookbook.

    Returns:
        dict: Each item in the list represents a cookbook with details such as
        the name, description, and included recipes.
    """
    cookbook_filename = slugify(cookbook_name)
    filepath = f"{EnvironmentVars.COOKBOOKS}/{cookbook_filename}.json"
    with open(filepath, "r") as json_file:
        file_info = json.load(json_file)
        return file_info


def add_new_cookbook(name: str, description: str, recipes: list) -> None:
    """
    This static method allows adding a new cookbook with the specified name, description, and a list of recipes.

    Args:
        name (str): The name or identifier of the new cookbook.
        description (str): A brief description of the new cookbook, providing information
        about its purpose or content.
        recipes (list): A list of recipes to be included in the new cookbook.

    Returns:
        None: This static method does not return any value.
    """
    cookbook_info = {"name": name, "description": description, "recipes": recipes}
    cookbook_filename = slugify(name)
    with open(
        f"{EnvironmentVars.COOKBOOKS}/{cookbook_filename}.json", "w"
    ) as json_file:
        json.dump(cookbook_info, json_file, indent=2)


def run_cookbooks_with_endpoints(
    cookbooks: list[str], endpoints: list[str], num_of_prompts: int, db_file: str
) -> dict:
    """
    Runs a list of cookbooks using a list of endpoints.
    This static method allows running a list of cookbooks using a list of endpoints and returns the results
    as a dictionary.

    Args:
        cookbooks (list[str]): A list of recipe names to be executed.
        endpoints (list[str]): A list of endpoint names where the cookbooks will be executed.
        num_of_prompts (int): The number of generated prompts to be run against.
        db_file (str): The path to the database file.

    Returns:
        dict: A dictionary containing the results of running the cookbooks. The dictionary may include
        information about the success of each recipe execution and any output data or errors.
    """
    print(
        f"Running cookbooks {cookbooks} with endpoints {endpoints}. Caching results in {db_file}."
    )

    # Create cookbooks
    cookbook_result = dict()
    for cookbook in cookbooks:
        cookbook_instance = Cookbook.load_from_json_config(cookbook)
        cookbook_instance.run(endpoints, num_of_prompts, db_file)
        cookbook_result.update({cookbook: cookbook_instance.results})
    return cookbook_result
