from typing import Any, Union


def find_keyword(
    keyword: str, target: Union[str, list[str], list[list[str]], list[dict], list, dict]
) -> Any:
    """
    Find the keyword in the target and return the matching elements.

    Args:
        keyword (str): The keyword to search for.
        target: The target to search within.

    Returns:
        Any: The matching elements or None if no match is found.
    """

    # find in single string
    if isinstance(target, str):
        if target.find(keyword) != -1:
            return target
        return ""

    # find in single dict
    elif isinstance(target, dict):
        if any(str(keyword) in str(value).lower() for value in target.values()):
            return target
        return {}

    # find in list
    elif isinstance(target, list):
        # list of string
        if all(isinstance(item, str) for item in target):
            return [item for item in target if str(item).lower().find(keyword) != -1]

        # list of dict
        elif all(isinstance(item, dict) for item in target):
            return [
                item
                for item in target
                if isinstance(item, dict)
                and any(str(keyword) in str(value).lower() for value in item.values())
            ]

    return None
