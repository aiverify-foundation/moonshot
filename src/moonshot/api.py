from typing import Any

from moonshot.src.benchmarking.metrics import run_factscore


def api_run_factscore(prompts: Any, predicted_results: Any, targets: Any) -> dict:
    """
    Runs the `run_factscore` function with the given parameters and returns the result.

    Args:
        prompts (Any): The prompts parameter of the `run_factscore` function.
        predicted_results (Any): The predicted_results parameter of the `run_factscore` function.
        targets (Any): The targets parameter of the `run_factscore` function.

    Returns:
        dict: The result of running the `run_factscore` function.
    """
    return run_factscore(prompts, predicted_results, targets)
