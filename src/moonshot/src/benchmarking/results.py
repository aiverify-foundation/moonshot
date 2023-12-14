import glob
import json
from pathlib import Path

from moonshot.src.common.env_variables import EnvironmentVars


def read_results(results_filename: str) -> dict:
    """
    This static method retrieves the contents of a results file.

    Args:
        results_filename: The file name of the results.

    Returns:
        dict: A dictionary of results.
    """
    with open(f"{EnvironmentVars.RESULTS}/{results_filename}.json", "r") as json_file:
        return json.load(json_file)


def get_all_results() -> list:
    """
    This static method retrieves a list of available results.

    Returns:
        list: A list of available results. Each item in the list represents a result.
    """
    filepaths = [
        Path(fp).stem
        for fp in glob.glob(f"{EnvironmentVars.RESULTS}/*.json")
        if "__" not in fp
    ]
    return filepaths
