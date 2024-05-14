from moonshot.api import (
    api_create_cookbook,
    api_delete_cookbook,
    api_get_all_cookbook,
    api_get_all_cookbook_name,
    api_read_cookbook,
    api_read_cookbooks,
    api_update_cookbook,
)


# ------------------------------------------------------------------------------
# Cookbook APIs Test
# ------------------------------------------------------------------------------
def test_create_cookbook():
    api_create_cookbook(
        name="my new cookbook",
        description="This is a cookbook that consists of a subset of Bias Benchmark for QA (BBQ) recipes for age.",
        recipes=["my-recipe1", "my-recipe2"],
    )


def test_read_cookbook():
    print(api_read_cookbook("my-new-cookbook"))


def test_read_cookbooks():
    cookbooks = api_read_cookbooks(
        ["my-new-cookbook", "my-new-cookbook", "my-new-cookbook"]
    )
    for cookbook_no, cookbook in enumerate(cookbooks, 1):
        print("-" * 100)
        print("Cookbook No. ", cookbook_no)
        print(cookbook)


def test_update_cookbook():
    api_update_cookbook(
        "my-new-cookbook",
        name="my new cookbook 1234",
        recipes=["my-recipe2", "my-recipe5"],
    )


def test_delete_cookbook():
    # Delete cookbook if do not exists
    try:
        api_delete_cookbook("cookbook123")
        print("Delete cookbook if exist: FAILED")
    except Exception as ex:
        print(f"Delete cookbook if do not exist: PASSED")

    # Delete cookbook if exists
    try:
        api_delete_cookbook("my-new-cookbook")
        print("Delete cookbook if exist: PASSED")
    except Exception:
        print("Delete cookbook if exist: FAILED")


def test_get_all_cookbook():
    print(api_get_all_cookbook())


def test_get_all_cookbook_name():
    print(api_get_all_cookbook_name())


def test_run_cookbook_api():
    # Create cookbook
    print("=" * 100, "\nTest creating cookbook")
    test_create_cookbook()

    # Read cookbook
    print("=" * 100, "\nTest reading cookbook")
    test_read_cookbook()

    # Update cookbook
    print("=" * 100, "\nTest updating cookbook")
    test_update_cookbook()

    # Read cookbook
    print("=" * 100, "\nTest reading cookbook after updating")
    test_read_cookbook()

    # Read cookbooks
    print("=" * 100, "\nTest reading cookbooks")
    test_read_cookbooks()

    # Delete cookbook
    print("=" * 100, "\nTest deleting cookbooks")
    test_delete_cookbook()

    # List all cookbooks
    print("=" * 100, "\nTest listing all cookbook")
    test_get_all_cookbook()

    # List all cookbooks names
    print("=" * 100, "\nTest listing all cookbook name")
    test_get_all_cookbook_name()
