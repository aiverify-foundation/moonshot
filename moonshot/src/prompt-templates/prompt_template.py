import json

from moonshot.src.storage.storage_manager import StorageManager


def get_prompt_templates() -> list:
    """
    Gets a list of prompt templates.
    This static method retrieves a list of prompt templates available.

    Returns:
        list: A list of prompt templates.
    """
    return [
        json.load(open(filepath, "r", encoding="utf-8"))
        for filepath in StorageManager.get_prompt_templates()
        if "__" not in filepath
    ]


def get_prompt_template_names() -> list:
    """
    Gets a list of prompt template names.
    This method retrieves a list of prompt template names available.

    Returns:
        list: A list of prompt template names.
    """
    return [item["name"] for item in get_prompt_templates()]
