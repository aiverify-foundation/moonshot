from moonshot.src.api.api_run import api_get_all_run

# ------------------------------------------------------------------------------
# Run APIs Test
# ------------------------------------------------------------------------------
def test_get_all_run(runner_id: str):
    print(api_get_all_run(runner_id))

def test_run_api():
    # Get run info
    print("=" * 100, "\nGetting run information for my-new-runner")
    test_get_all_run("my-new-runner")

    # Get run info
    print("=" * 100, "\nGetting run information for no-runner")
    test_get_all_run("no-runner")

    # Get run info
    print("=" * 100, "\nGetting run information for empty string")
    test_get_all_run("")
    