import shutil

from moonshot.api import (
    api_delete_result,
    api_get_all_results,
    api_get_all_results_name,
    api_read_result,
    api_read_results,
)


# ------------------------------------------------------------------------------
# Results APIs Test
# ------------------------------------------------------------------------------
def test_read_result():
    # Write a new result: "moonshot/data/results/cookbook-my-new-cookbook-executor.json"
    source_path = "tests/results/cookbook-my-new-cookbook-executor.json"
    destination_path = "moonshot/data/results/cookbook-my-new-cookbook-executor.json"
    shutil.copy(source_path, destination_path)
    print(api_read_result("cookbook-my-new-cookbook-executor"))

    # Write a new result: "moonshot/data/results/recipe-my-new-recipe-executor.json"
    source_path = "tests/results/recipe-my-new-recipe-executor.json"
    destination_path = "moonshot/data/results/recipe-my-new-recipe-executor.json"
    shutil.copy(source_path, destination_path)
    print(api_read_result("recipe-my-new-recipe-executor"))


def test_read_results():
    cookbook_result_name = "cookbook-my-new-cookbook-executor"
    recipe_result_name = "recipe-my-new-recipe-executor"
    results = api_read_results([cookbook_result_name, recipe_result_name])
    for result_no, result in enumerate(results, 1):
        print("-" * 100)
        print("Result No. ", result_no)
        print(result)


def test_delete_result():
    # Delete result if do not exists
    try:
        api_delete_result("result123")
        print("Delete result if exist: FAILED")
    except Exception as ex:
        print(f"Delete result if do not exist: PASSED")

    # Delete result if exists
    try:
        api_delete_result("cookbook-my-new-cookbook-executor")
        print("Delete results if exist: PASSED")
    except Exception:
        print("Delete results if exist: FAILED")

    # Delete result if exists
    try:
        api_delete_result("recipe-my-new-recipe-executor")
        print("Delete results if exist: PASSED")
    except Exception:
        print("Delete results if exist: FAILED")


def test_get_all_results():
    print(api_get_all_results())


def test_get_all_results_names():
    print(api_get_all_results_name())


def test_run_result_api():
    # Read result
    print("=" * 100, "\nTest reading result")
    test_read_result()

    # Read results
    print("=" * 100, "\nTest reading results")
    test_read_results()

    # List all results
    print("=" * 100, "\nTest listing all results")
    test_get_all_results()

    # List all results names
    print("=" * 100, "\nTest listing all results names")
    test_get_all_results_names()

    # Delete result
    print("=" * 100, "\nTest deleting results")
    test_delete_result()
