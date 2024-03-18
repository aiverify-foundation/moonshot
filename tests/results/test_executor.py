from pathlib import Path

from moonshot.api import (
    api_create_cookbook_executor,
    api_create_recipe_executor,
    api_delete_executor,
    api_get_all_executors,
    api_get_all_executors_names,
    api_load_executor,
    api_read_executor,
)


# ------------------------------------------------------------------------------
# Benchmark executor APIs Test
# ------------------------------------------------------------------------------
def executor_callback_fn(progress_args: dict):
    print("=" * 100)
    print("PROGRESS CALLBACK FN: ", progress_args)
    print("=" * 100)


def test_create_recipe_executor():
    bm_executor = api_create_recipe_executor(
        name="my new recipe executor",
        recipes=["bbq", "auto-categorisation"],
        endpoints=["openai-gpt35-lionel", "openai-gpt35-turbo-16k-lionel"],
        num_of_prompts=2,
        progress_callback_func=executor_callback_fn,
    )
    print("Benchmark Executor Attributes:")
    print("ID:", bm_executor.id)
    print("Name:", bm_executor.name)
    print("Type:", bm_executor.type)
    print("Start Time:", bm_executor.start_time)
    print("End Time:", bm_executor.end_time)
    print("Duration:", bm_executor.duration)
    print("Database Instance:", bm_executor.database_instance)
    print("Database File:", bm_executor.database_file)
    print("Error Messages:", bm_executor.error_messages)
    print("Results File:", bm_executor.results_file)
    print("Recipes:", bm_executor.recipes)
    print("Cookbooks:", bm_executor.cookbooks)
    print("Endpoints:", bm_executor.endpoints)
    print("Number of Prompts:", bm_executor.num_of_prompts)
    print("Results:", bm_executor.results)
    print("Status:", bm_executor.status)
    print("Progress Callback Function:", bm_executor.progress_callback_func)
    bm_executor.close_executor()


def test_create_cookbook_executor():
    bm_executor = api_create_cookbook_executor(
        name="my new cookbook executor",
        cookbooks=["bbq-lite-age-cookbook"],
        endpoints=["openai-gpt35-lionel", "openai-gpt35-turbo-16k-lionel"],
        num_of_prompts=2,
        progress_callback_func=executor_callback_fn,
    )
    print("Benchmark Executor Attributes:")
    print("ID:", bm_executor.id)
    print("Name:", bm_executor.name)
    print("Type:", bm_executor.type)
    print("Start Time:", bm_executor.start_time)
    print("End Time:", bm_executor.end_time)
    print("Duration:", bm_executor.duration)
    print("Database Instance:", bm_executor.database_instance)
    print("Database File:", bm_executor.database_file)
    print("Error Messages:", bm_executor.error_messages)
    print("Results File:", bm_executor.results_file)
    print("Recipes:", bm_executor.recipes)
    print("Cookbooks:", bm_executor.cookbooks)
    print("Endpoints:", bm_executor.endpoints)
    print("Number of Prompts:", bm_executor.num_of_prompts)
    print("Results:", bm_executor.results)
    print("Status:", bm_executor.status)
    print("Progress Callback Function:", bm_executor.progress_callback_func)
    bm_executor.close_executor()


def test_load_executor(bm_id: str):
    bm_executor = api_load_executor(bm_id, progress_callback_func=executor_callback_fn)
    print("Benchmark Executor Attributes:")
    print("ID:", bm_executor.id)
    print("Name:", bm_executor.name)
    print("Type:", bm_executor.type)
    print("Start Time:", bm_executor.start_time)
    print("End Time:", bm_executor.end_time)
    print("Duration:", bm_executor.duration)
    print("Database Instance:", bm_executor.database_instance)
    print("Database File:", bm_executor.database_file)
    print("Error Messages:", bm_executor.error_messages)
    print("Results File:", bm_executor.results_file)
    print("Recipes:", bm_executor.recipes)
    print("Cookbooks:", bm_executor.cookbooks)
    print("Endpoints:", bm_executor.endpoints)
    print("Number of Prompts:", bm_executor.num_of_prompts)
    print("Results:", bm_executor.results)
    print("Status:", bm_executor.status)
    print("Progress Callback Function:", bm_executor.progress_callback_func)
    bm_executor.close_executor()


def test_execute_executor(bm_id: str):
    bm_executor = api_load_executor(bm_id, progress_callback_func=executor_callback_fn)
    bm_executor.execute()
    bm_executor.close_executor()


def test_read_executor(bm_id: str):
    print(api_read_executor(bm_id))


def test_delete_executor(bm_id: str):
    # Delete result if do not exists
    try:
        api_delete_executor("executor123")
        print("Delete executor if exist: FAILED")
    except Exception as ex:
        print(f"Delete executor if do not exist: PASSED")

    # Delete result if exists
    try:
        api_delete_executor(bm_id)
        print("Delete executor if exist: PASSED")
    except Exception:
        print("Delete executor if exist: FAILED")


def test_get_all_executors():
    print(api_get_all_executors())


def test_get_all_executors_names():
    print(api_get_all_executors_names())


def test_run_benchmark_recipe_executor_api():
    bm_id = "recipe-my-new-recipe-executor"

    if Path(f"moonshot/data/databases/{bm_id}.db").exists():
        print(f"Database for {bm_id} exists.")

        # Delete executor
        print("=" * 100, "\nTest deleting executors")
        test_delete_executor(bm_id)

    else:
        print(f"Database for {bm_id} does not exist.")

    # Create executor
    print("=" * 100, "\nTest creating recipe executor")
    test_create_recipe_executor()

    # Load executor
    print("=" * 100, "\nTest loading executor")
    test_load_executor(bm_id)

    # Execute the recipe job
    print("=" * 100, "\nTest executing executor")
    test_execute_executor(bm_id)

    # Read executor
    print("=" * 100, "\nTest reading executor")
    test_read_executor(bm_id)

    # List all executor
    print("=" * 100, "\nTest listing all executors")
    test_get_all_executors()

    # List all executor names
    print("=" * 100, "\nTest listing all executors names")
    test_get_all_executors_names()

    # Delete executor
    print("=" * 100, "\nTest deleting executors")
    test_delete_executor(bm_id)


def test_run_benchmark_cookbook_executor_api():
    bm_id = "cookbook-my-new-cookbook-executor"

    if Path(f"moonshot/data/databases/{bm_id}.db").exists():
        print(f"Database for {bm_id} exists.")

        # Delete executor
        print("=" * 100, "\nTest deleting executors")
        test_delete_executor(bm_id)

    else:
        print(f"Database for {bm_id} does not exist.")

    # Create executor
    print("=" * 100, "\nTest creating cookbook executor")
    test_create_cookbook_executor()

    # Load executor
    print("=" * 100, "\nTest loading executor")
    test_load_executor(bm_id)

    # Execute the recipe job
    print("=" * 100, "\nTest executing executor")
    test_execute_executor(bm_id)

    # Read executor
    print("=" * 100, "\nTest reading executor")
    test_read_executor(bm_id)

    # List all executor
    print("=" * 100, "\nTest listing all executors")
    test_get_all_executors()

    # List all executor names
    print("=" * 100, "\nTest listing all executors names")
    test_get_all_executors_names()

    # Delete executor
    print("=" * 100, "\nTest deleting executors")
    test_delete_executor(bm_id)
