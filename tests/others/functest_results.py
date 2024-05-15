import shutil

from moonshot.api import (
    api_delete_result,
    api_get_all_result,
    api_get_all_result_name,
    api_read_result,
    api_read_results,
)


# ------------------------------------------------------------------------------
# Results APIs Test
# ------------------------------------------------------------------------------
def test_read_result():
    # Write a new result: "moonshot/data/results/my-new-runner-cookbook.json"
    source_path = "tests/others/results/my-new-runner-cookbook.json"
    destination_path = "moonshot/data/generated-outputs/results/my-new-runner-cookbook.json"
    shutil.copy(source_path, destination_path)
    print(api_read_result("my-new-runner-cookbook"))

    # Write a new result: "moonshot/data/results/my-new-runner-recipe.json"
    source_path = "tests/others/results/my-new-runner-recipe.json"
    destination_path = "moonshot/data/generated-outputs/results/my-new-runner-recipe.json"
    shutil.copy(source_path, destination_path)
    print(api_read_result("my-new-runner-recipe"))


def test_read_results():
    cookbook_result_name = "my-new-runner-cookbook"
    recipe_result_name = "my-new-runner-recipe"
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
        api_delete_result("my-new-runner-cookbook")
        print("Delete results if exist: PASSED")
    except Exception:
        print("Delete results if exist: FAILED")

    # Delete result if exists
    try:
        api_delete_result("my-new-runner-recipe")
        print("Delete results if exist: PASSED")
    except Exception:
        print("Delete results if exist: FAILED")


def test_get_all_result():
    print(api_get_all_result())


def test_get_all_result_name():
    print(api_get_all_result_name())


def test_run_result_api():
    # Read result
    print("=" * 100, "\nTest reading result")
    test_read_result()

    # Read results
    print("=" * 100, "\nTest reading results")
    test_read_results()

    # List all results
    print("=" * 100, "\nTest listing all results")
    test_get_all_result()

    # List all results names
    print("=" * 100, "\nTest listing all results names")
    test_get_all_result_name()

    # Delete result
    print("=" * 100, "\nTest deleting results")
    test_delete_result()
