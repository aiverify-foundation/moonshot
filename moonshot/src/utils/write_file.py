import json
from pathlib import Path


def write_json_file(data: dict, filepath: str) -> None:
    """
    Writes dictionary data to a JSON file.

    Args:
        data (dict): The dictionary to be written to the JSON file.
        filepath (str): The path to the JSON file.
    """
    # Create directories if they don't exist
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
