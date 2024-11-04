from moonshot.src.api.api_runner import api_get_all_runner, api_load_runner
from moonshot.src.runs.run import Run
from moonshot.src.runs.run_arguments import RunArguments


# ------------------------------------------------------------------------------
# Run APIs
# ------------------------------------------------------------------------------
def api_get_all_run(runner_id: str = "") -> list[dict]:
    """
    Retrieves all runs for a given runner ID or for all runners if no ID is provided.

    This function calls an internal API to get available runs and then converts each run into a dictionary format.

    Args:
        runner_id (str, optional): The ID of the runner to retrieve runs for. If empty, runs for all runners
                                   are retrieved.

    Returns:
        list[dict]: A list of dictionaries, each representing a run's data.
    """
    _, runs = _api_get_available_runs(runner_id)
    return [run.to_dict() for run in runs]


def _api_get_available_runs(
    runner_id: str = "",
) -> tuple[list[str], list[RunArguments]]:
    """
    Retrieves available runs and their corresponding runner IDs.

    This function fetches information about available runs based on the provided runner ID. If no runner ID is
    provided, it fetches runs for all runners. It returns a tuple containing a list of runner IDs and a list of
    RunArguments instances representing the runs.

    Args:
        runner_id (str, optional): The ID of the runner for which to retrieve run information. If empty, information
                                   for all runners is retrieved.

    Returns:
        tuple[list[str], list[RunArguments]]: A tuple containing a list of runner IDs and a list of RunArguments
                                              instances for the corresponding runs.
    """
    # Lists to hold runner IDs and Run instances.
    runners_ids = []
    runs = []

    # Retrieve information for all runners.
    runners_info = api_get_all_runner()

    # Load the specified runner, or all runners if no ID is provided.
    if runner_id:
        runner_instances = (
            [api_load_runner(runner_id)]
            if any(runner_id == runner_info.get("id") for runner_info in runners_info)
            else []
        )
    else:
        runner_instances = [
            api_load_runner(str(runner_info.get("id"))) for runner_info in runners_info
        ]

    # Collect runs from each runner instance.
    for runner_instance in runner_instances:
        # Only proceed if the runner has an associated database instance.
        if runner_instance.database_instance:
            # Fetch all runs from the database associated with the runner.
            all_runs = Run.get_all_runs(runner_instance.database_instance)
            # Record the runner ID and the runs.
            runners_ids.append(runner_instance.id)
            runs.extend(all_runs)

    # Return the runner IDs and their runs.
    return runners_ids, runs
