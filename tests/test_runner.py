import asyncio
from moonshot.src.api.api_runner import (
    api_create_cookbook_runner, api_create_recipe_runner, api_delete_runner, api_get_all_runner, 
    api_get_all_runner_name, api_load_runner, api_read_runner
)

# ------------------------------------------------------------------------------
# Support Functions
# ------------------------------------------------------------------------------
def runner_callback_fn(progress_args: dict):
    print("=" * 100)
    print("PROGRESS CALLBACK FN: ", progress_args)
    print("=" * 100)

def test_create_recipe_runner(name: str):
    bm_runner = api_create_recipe_runner(
        name=name,
        recipes=["bbq", "auto-categorisation"],
        endpoints=["openai-gpt35-lionel", "openai-gpt35-turbo-16k-lionel"],
        num_of_prompts=2,
        progress_callback_func=runner_callback_fn,
    )
    print("Benchmark Runner Attributes:")
    print("ID:", bm_runner.id)
    print("Name:", bm_runner.name)
    print("RunType:", bm_runner.run_type)
    print("Recipes:", bm_runner.recipes)
    print("Cookbooks:", bm_runner.cookbooks)
    print("Endpoints:", bm_runner.endpoints)
    print("Number of Prompts:", bm_runner.num_of_prompts)
    print("Database Instance:", bm_runner.database_instance)
    print("Database File:", bm_runner.database_file)
    print("Progress Callback Function:", bm_runner.progress_callback_func)
    bm_runner.close()

def test_create_cookbook_runner(name: str):
    bm_runner = api_create_cookbook_runner(
        name=name,
        cookbooks=["bbq-lite-age-cookbook"],
        endpoints=["openai-gpt35-lionel", "openai-gpt35-turbo-16k-lionel"],
        num_of_prompts=2,
        progress_callback_func=runner_callback_fn,
    )
    print("Benchmark Runner Attributes:")
    print("ID:", bm_runner.id)
    print("Name:", bm_runner.name)
    print("RunType:", bm_runner.run_type)
    print("Recipes:", bm_runner.recipes)
    print("Cookbooks:", bm_runner.cookbooks)
    print("Endpoints:", bm_runner.endpoints)
    print("Number of Prompts:", bm_runner.num_of_prompts)
    print("Database Instance:", bm_runner.database_instance)
    print("Database File:", bm_runner.database_file)
    print("Progress Callback Function:", bm_runner.progress_callback_func)
    bm_runner.close()

def test_load_runner(runner_id: str):
    bm_runner = api_load_runner(runner_id, progress_callback_func=runner_callback_fn)
    print("Benchmark Runner Attributes:")
    print("ID:", bm_runner.id)
    print("Name:", bm_runner.name)
    print("RunType:", bm_runner.run_type)
    print("Recipes:", bm_runner.recipes)
    print("Cookbooks:", bm_runner.cookbooks)
    print("Endpoints:", bm_runner.endpoints)
    print("Number of Prompts:", bm_runner.num_of_prompts)
    print("Database Instance:", bm_runner.database_instance)
    print("Database File:", bm_runner.database_file)
    print("Progress Callback Function:", bm_runner.progress_callback_func)
    bm_runner.close()

def test_run_runner(runner_id: str):
    run_runner = api_load_runner(runner_id, progress_callback_func=runner_callback_fn)
    asyncio.run(run_runner.run())
    run_runner.close()

def test_read_runner(runner_id: str):
    print(api_read_runner(runner_id))

def test_delete_runner(runner_id: str):
    # Delete result if do not exists
    try:
        api_delete_runner("runner123")
        print("Delete runner if exist: FAILED")
    except Exception as ex:
        print(f"Delete runner if do not exist: PASSED")

    # Delete result if exists
    try:
        api_delete_runner(runner_id)
        print("Delete runner if exist: PASSED")
    except Exception:
        print("Delete runner if exist: FAILED")

def test_get_all_runner():
    print(api_get_all_runner())

def test_get_all_runner_name():
    print(api_get_all_runner_name())

# ------------------------------------------------------------------------------
# Run Runner Functions
# ------------------------------------------------------------------------------
def test_run_runner_recipe_api():
    bm_runner_name = "my new recipe bm runner"
    bm_runner_id = "my-new-recipe-bm-runner"

    # Create runner
    print("=" * 100, "\nTest creating recipe runner")
    test_create_recipe_runner(bm_runner_name)

    # Load runner
    print("=" * 100, "\nTest loading runner")
    test_load_runner(bm_runner_id)

    # Run the runner job
    print("=" * 100, "\nTest executing runner")
    test_run_runner(bm_runner_id)

    # Run the runner job
    print("=" * 100, "\nTest executing runner")
    test_run_runner(bm_runner_id)

    # Run the runner job
    print("=" * 100, "\nTest executing runner")
    test_run_runner(bm_runner_id)

    # Read runner
    print("=" * 100, "\nTest reading runner")
    test_read_runner(bm_runner_id)

    # List all runner
    print("=" * 100, "\nTest listing all runner")
    test_get_all_runner()

    # List all runner names
    print("=" * 100, "\nTest listing all runner name")
    test_get_all_runner_name()

    # Delete runner
    print("=" * 100, "\nTest deleting runners")
    test_delete_runner(bm_runner_id)

def test_run_runner_cookbook_api():
    bm_runner_name = "my new cookbook bm runner"
    bm_runner_id = "my-new-cookbook-bm-runner"

    # Create runner
    print("=" * 100, "\nTest creating cookbook runner")
    test_create_cookbook_runner(bm_runner_name)

    # Load runner
    print("=" * 100, "\nTest loading runner")
    test_load_runner(bm_runner_id)

    # Run the runner job
    print("=" * 100, "\nTest executing runner")
    test_run_runner(bm_runner_id)

    # Run the runner job
    print("=" * 100, "\nTest executing runner")
    test_run_runner(bm_runner_id)

    # Run the runner job
    print("=" * 100, "\nTest executing runner")
    test_run_runner(bm_runner_id)

    # Read runner
    print("=" * 100, "\nTest reading runner")
    test_read_runner(bm_runner_id)

    # List all runner
    print("=" * 100, "\nTest listing all runner")
    test_get_all_runner()

    # List all runner names
    print("=" * 100, "\nTest listing all runner name")
    test_get_all_runner_name()

    # Delete runner
    print("=" * 100, "\nTest deleting runners")
    test_delete_runner(bm_runner_id)
