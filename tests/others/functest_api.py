from tests.others.functest_connectors import test_run_connector_api, test_run_connector_endpoints_api
from tests.others.functest_cookbooks import test_run_cookbook_api
from tests.others.functest_datasets import test_run_datasets_api
from tests.others.functest_metrics import test_run_metric_api
from tests.others.functest_recipes import test_run_recipe_api
from tests.others.functest_results import test_run_result_api
from tests.others.functest_runner import test_run_runner_api


if __name__ == "__main__":
    # Test connector apis
    test_run_connector_endpoints_api()
    test_run_connector_api()

    # Test datasets api
    test_run_datasets_api()

    # Test recipes api
    test_run_recipe_api()

    # Test cookbooks api
    test_run_cookbook_api()

    # Test runner api
    test_run_runner_api()

    # Test metric api
    test_run_metric_api()

    # Test result api
    test_run_result_api()
    