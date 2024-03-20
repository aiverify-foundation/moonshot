from moonshot.api import api_delete_metric, api_get_all_metric


# ------------------------------------------------------------------------------
# Metrics APIs Test
# ------------------------------------------------------------------------------
def test_get_all_metrics():
    # List all metrics
    print(api_get_all_metric())


def test_delete_metric():
    # Delete metric if do not exists
    try:
        api_delete_metric("bertscore123")
        print("Delete metric if exist: FAILED")
    except Exception as ex:
        print(f"Delete metric if do not exist: PASSED")

    # Delete metric if exists
    # Write a new metric: "../../moonshot/data/metrics/my_metrics.py
    path = "moonshot/data/metrics/my_metrics.py"
    with open(path, "w") as file:
        file.write("# This is a new file for metrics")
    try:
        api_delete_metric("my_metrics")
        print("Delete metric if exist: PASSED")
    except Exception as ex:
        print("Delete metric if exist: FAILED")


def test_run_metric_api():
    # List all metrics
    print("=" * 100, "\nTest listing all metrics")
    test_get_all_metrics()

    # delete metric
    print("=" * 100, "\nTest deleting metrics")
    test_delete_metric()

    # List all metrics
    print("=" * 100, "\nTest listing all metrics")
    test_get_all_metrics()
