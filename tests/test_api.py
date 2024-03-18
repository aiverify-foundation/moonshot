from tests.results.test_connectors import test_run_connector_api
from tests.results.test_cookbooks import test_run_cookbook_api
from tests.results.test_executor import test_run_benchmark_recipe_executor_api, test_run_benchmark_cookbook_executor_api
from tests.results.test_metrics import test_run_metric_api
from tests.results.test_recipes import test_run_recipe_api
from tests.results.test_results import test_run_result_api


if __name__ == "__main__":
    # Test connector apis
    test_run_connector_api()

    # Test recipes api
    test_run_recipe_api()

    # Test cookbooks api
    test_run_cookbook_api()

    # Test executor api
    test_run_benchmark_recipe_executor_api()
    test_run_benchmark_cookbook_executor_api()

    # Test resume run

    # Test metric api
    test_run_metric_api()

    # Test result api
    test_run_result_api()
    