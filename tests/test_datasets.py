from moonshot.src.api.api_dataset import api_delete_dataset, api_get_all_datasets, api_get_all_datasets_name

# ------------------------------------------------------------------------------
# Datasets APIs Test
# ------------------------------------------------------------------------------
def test_delete_datasets():
    # Delete dataset if do not exists
    try:
        api_delete_dataset("dataset123")
        print("Delete dataset if exist: FAILED")
    except Exception as ex:
        print(f"Delete dataset if do not exist: PASSED")

    # Delete dataset if exists
    try:
        api_delete_dataset("advglue-all")
        print("Delete dataset if exist: PASSED")
    except Exception:
        print("Delete dataset if exist: FAILED")


def test_get_all_datasets():
    print(api_get_all_datasets())


def test_get_all_datasets_name():
    print(api_get_all_datasets_name())


def test_run_datasets_api():
    # ------------------------------------------------------------------------------
    # Datasets APIs Test
    # ------------------------------------------------------------------------------
    # Delete datasets
    print("=" * 100, "\nTest deleting datasets")
    test_delete_datasets()

    # List all datasets
    print("=" * 100, "\nTest listing all dataset")
    test_get_all_datasets()

    # List all datasets names
    print("=" * 100, "\nTest listing all dataset names")
    test_get_all_datasets_name()
