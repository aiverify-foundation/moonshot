import glob
import json

from moonshot.src.common.env_variables import EnvironmentVars


def get_prompt_templates() -> list:
    """
    Gets a list of prompt templates.
    This static method retrieves a list of prompt templates available.

    Returns:
        list: A list of prompt templates.
    """
    return_list = list()
    filepaths = glob.glob(f"{EnvironmentVars.PROMPT_TEMPLATES}/*.json")
    for filepath in filepaths:
        if "__" in filepath:
            continue
        with open(filepath, "r") as json_file:
            file_info = json.load(json_file)
            return_list.append(file_info)
    return return_list


def get_prompt_template_names() -> list:
    """
    Gets a list of prompt template names.
    This static method retrieves a list of prompt template names available.

    Returns:
        list: A list of prompt template names.
    """
    prompt_template_name_list = []
    for item in get_prompt_templates():
        prompt_template_name_list.append(item["name"])
    return prompt_template_name_list
