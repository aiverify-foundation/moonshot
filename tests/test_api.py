from moonshot.api import (
    api_create_connector, api_create_connectors, api_create_cookbook, api_create_cookbook_executor, api_create_endpoint, api_create_recipe, api_create_recipe_executor, 
    api_delete_cookbook, api_delete_endpoint, api_delete_executor, api_delete_metric, api_delete_recipe, api_get_all_connectors, api_get_all_cookbooks, 
    api_get_all_cookbooks_names, api_get_all_endpoints, api_get_all_endpoints_names, api_get_all_executors, api_get_all_executors_names, api_get_all_metrics, api_get_all_recipes, 
    api_get_all_recipes_names, api_load_executor, api_read_cookbook, api_read_cookbooks, api_read_endpoint, api_read_executor, api_read_recipe, 
    api_read_recipes, api_update_cookbook, api_update_endpoint, api_update_recipe
)

# ------------------------------------------------------------------------------
# Environment variables APIs Test
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Connector and Connector endpoints APIs Test
# ------------------------------------------------------------------------------
def test_create_connector_endpoint():
    api_create_endpoint(
        name="My New GPT4",
        connector_type="openai-gpt4",
        uri="1234",
        token="1234",
        max_calls_per_second=256,
        max_concurrency=1,
        params={
            "hello": "world"
        }    
    )

def test_read_connector_endpoint():
    print(api_read_endpoint("my-new-gpt4"))

def test_update_connector_endpoint():
    api_update_endpoint(
        name="My New GPT4",
        connector_type="openai-gpt4",
        uri="4567",
        token="4567",
        max_calls_per_second=10,
        max_concurrency=10,
        params={
            "hello": "world"
        }
    )

def test_delete_connector_endpoint():
    api_delete_endpoint("my-new-gpt4")

def test_get_all_connector_endpoints():
    print(api_get_all_endpoints())

def test_get_all_connector_endpoints_name():
    print(api_get_all_endpoints_names())

def test_create_connector():
    # Recreate connector endpoint
    test_create_connector_endpoint()

    # Create new connector
    connector = api_create_connector("my-new-gpt4")
    print(connector)
    print("Connector ID: ", connector.id)
    print("Connector Endpoint: ", connector.endpoint)
    print("Connector Token: ", connector.token)
    print("Max Concurrency: ", connector.max_concurrency)
    print("Max Calls Per Second: ", connector.max_calls_per_second)
    print("Additional Params: ", connector.params)
    print("Connector PrePrompt: ", connector.pre_prompt)
    print("Connector PostPrompt: ", connector.post_prompt)
    print("Rate Limiter: ", connector.rate_limiter)
    print("Semaphore: ", connector.semaphore)
    print("Last Call Time: ", connector.last_call_time)
    print("Timeout: ", connector.timeout)
    print("Allow Retries: ", connector.allow_retries)
    print("Retries Times: ", connector.retries_times)

    # Delete connector endpoint
    test_delete_connector_endpoint()

def test_create_connectors():
    # Recreate connector endpoint
    test_create_connector_endpoint()

    # Create new connector
    connectors = api_create_connectors(["my-new-gpt4", "my-new-gpt4", "my-new-gpt4"])
    for connector_no, connector in enumerate(connectors, 1):
        print("-"*100)
        print("Connector No. ", connector_no)
        print("Connector ID: ", connector.id)
        print("Connector Endpoint: ", connector.endpoint)
        print("Connector Token: ", connector.token)
        print("Max Concurrency: ", connector.max_concurrency)
        print("Max Calls Per Second: ", connector.max_calls_per_second)
        print("Additional Params: ", connector.params)
        print("Connector PrePrompt: ", connector.pre_prompt)
        print("Connector PostPrompt: ", connector.post_prompt)
        print("Rate Limiter: ", connector.rate_limiter)
        print("Semaphore: ", connector.semaphore)
        print("Last Call Time: ", connector.last_call_time)
        print("Timeout: ", connector.timeout)
        print("Allow Retries: ", connector.allow_retries)
        print("Retries Times: ", connector.retries_times)

    # Delete connector endpoint
    test_delete_connector_endpoint()

def test_get_all_connectors():
    print(api_get_all_connectors())

def test_run_connector_api():
    # ------------------------------------------------------------------------------
    # Connector endpoints APIs Test
    # ------------------------------------------------------------------------------
    # Create connector endpoint
    print("="*100,"\nTest creating connector endpoint")
    test_create_connector_endpoint()

    # Read connector endpoint
    print("="*100,"\nTest reading connector endpoint")
    test_read_connector_endpoint()

    # Update connector endpoint
    print("="*100,"\nTest updating connector endpoint")
    test_update_connector_endpoint()

    # Delete connector endpoint
    print("="*100,"\nTest deleting connector endpoint")
    test_delete_connector_endpoint()

    # List all connector endpoints
    print("="*100,"\nTest listing all connector endpoints")
    test_get_all_connector_endpoints()

    # List all connector endpoints names
    print("="*100,"\nTest listing all connector endpoints names")
    test_get_all_connector_endpoints_name()

    # ------------------------------------------------------------------------------
    # Connector APIs Test
    # ------------------------------------------------------------------------------
    # Create new connector
    print("="*100,"\nTest creating new connector")
    test_create_connector()

    # Create new connectors
    print("="*100,"\nTest creating new connectors")
    test_create_connectors()

    # Create new connectors
    print("="*100,"\nTest getting all connectors")
    test_get_all_connectors()

# ------------------------------------------------------------------------------
# Cookbook APIs Test
# ------------------------------------------------------------------------------
def test_create_cookbook():
    api_create_cookbook(
        name="my new cookbook",
        description="This is a cookbook that consists of a subset of Bias Benchmark for QA (BBQ) recipes for age.",
        recipes=["my-recipe1","my-recipe2"]
    )

def test_read_cookbook():
    print(api_read_cookbook("my-new-cookbook"))

def test_read_cookbooks():
    cookbooks = api_read_cookbooks(["my-new-cookbook", "my-new-cookbook", "my-new-cookbook"])
    for cookbook_no, cookbook in enumerate(cookbooks, 1):
        print("-"*100)
        print("Cookbook No. ", cookbook_no)
        print(cookbook)

def test_update_cookbook():
    api_update_cookbook(
        name="my new cookbook",
        description="My new cookbook description",
        recipes=["my-recipe2","my-recipe5"]
    )

def test_delete_cookbook():
    api_delete_cookbook("my-new-cookbook")

def test_get_all_cookbooks():
    print(api_get_all_cookbooks())

def test_get_all_cookbooks_names():
    print(api_get_all_cookbooks_names())

def test_run_cookbook_api():
    # Create cookbook
    print("="*100,"\nTest creating cookbook")
    test_create_cookbook()

    # Read cookbook
    print("="*100,"\nTest reading cookbook")
    test_read_cookbook()

    # Update cookbook
    print("="*100,"\nTest updating cookbook")
    test_update_cookbook()

    # Read cookbooks
    print("="*100,"\nTest reading cookbooks")
    test_read_cookbooks()

    # Delete cookbook
    print("="*100,"\nTest deleting cookbooks")
    test_delete_cookbook()
    
    # List all cookbooks
    print("="*100,"\nTest listing all cookbooks")
    test_get_all_cookbooks()

    # List all cookbooks names
    print("="*100,"\nTest listing all cookbooks names")
    test_get_all_cookbooks_names()

# ------------------------------------------------------------------------------
# Recipes APIs Test
# ------------------------------------------------------------------------------
def test_create_recipe():
    api_create_recipe(
        name="my new recipe",
        description="Consists of adversarially perturned and benign MNLI and MNLIMM datasets. MNLI consists is a crowd-sourced collection of sentence pairs with textual entailment annotations. Given a premise sentence and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis.",
        tags=["robustness"],
        datasets=["dataset1", "dataset2"],
        prompt_templates=["prompt-template1"],
        metrics=["metrics1","metrics2"]
    )

def test_read_recipe():
    print(api_read_recipe("my-new-recipe"))

def test_read_recipes():
    recipes = api_read_recipes(["my-new-recipe", "my-new-recipe", "my-new-recipe"])
    for recipe_no, recipe in enumerate(recipes, 1):
        print("-"*100)
        print("Recipe No. ", recipe_no)
        print(recipe)

def test_update_recipe():
    api_update_recipe(
        name="my new recipe",
        description="my new description.",
        tags=["fairness"],
        datasets=["dataset2", "dataset5"],
        prompt_templates=["prompt-template2"],
        metrics=["metrics3"]
    )

def test_delete_recipe():
    api_delete_recipe("my-new-recipe")

def test_get_all_recipes():
    print(api_get_all_recipes())

def test_get_all_recipes_names():
    print(api_get_all_recipes_names())

def test_run_recipe_api():
    # Create recipe
    print("="*100,"\nTest creating recipe")
    test_create_recipe()

    # Read recipe
    print("="*100,"\nTest reading recipe")
    test_read_recipe()

    # Update recipe
    print("="*100,"\nTest updating recipe")
    test_update_recipe()

    # Read recipes
    print("="*100,"\nTest reading recipes")
    test_read_recipes()

    # Delete recipe
    print("="*100,"\nTest deleting recipes")
    test_delete_recipe()
    
    # List all recipes
    print("="*100,"\nTest listing all recipes")
    test_get_all_recipes()

    # List all recipes names
    print("="*100,"\nTest listing all recipes names")
    test_get_all_recipes_names()

# ------------------------------------------------------------------------------
# Metrics APIs Test
# ------------------------------------------------------------------------------
def test_get_all_metrics():
    # List all metrics
    print(api_get_all_metrics())

def test_delete_metric():
    # Delete metric
    api_delete_metric("bertscore")

def test_run_metric_api():
    # List all metrics
    print("="*100,"\nTest listing all metrics")
    test_get_all_metrics()

    # delete metric
    print("="*100,"\nTest deleting metrics")
    test_delete_metric()

    # List all metrics
    print("="*100,"\nTest listing all metrics")
    test_get_all_metrics()

# ------------------------------------------------------------------------------
# Benchmark executor APIs Test
# ------------------------------------------------------------------------------
def executor_callback_fn(progress_args: dict):
    print("="*100)
    print("PROGRESS CALLBACK FN: ", progress_args)
    print("="*100)

def test_create_recipe_executor():
    bm_executor = api_create_recipe_executor(
        name="my new recipe executor",
        recipes=["bbq"],
        endpoints=["openai-gpt35-lionel"],
        num_of_prompts=1,
        progress_callback_func=executor_callback_fn
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
        endpoints=["openai-gpt35-lionel"],
        num_of_prompts=1,
        progress_callback_func=executor_callback_fn
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
    api_delete_executor(bm_id)

def test_get_all_executors():
    print(api_get_all_executors())

def test_get_all_executors_names():
    print(api_get_all_executors_names())

def test_run_benchmark_recipe_executor_api():
    bm_id = "recipe-my-new-recipe-executor"

    # Create executor
    print("="*100,"\nTest creating recipe executor")
    test_create_recipe_executor()

    # Load executor
    print("="*100,"\nTest loading executor")
    test_load_executor(bm_id)

    # Execute the recipe job
    print("="*100,"\nTest executing executor")
    test_execute_executor(bm_id)

    # Read executor
    print("="*100,"\nTest reading executor")
    test_read_executor(bm_id)

    # List all executor
    print("="*100,"\nTest listing all executors")
    test_get_all_executors()

    # List all executor names
    print("="*100,"\nTest listing all executors names")
    test_get_all_executors_names()

    # Delete executor
    print("="*100,"\nTest deleting executors")
    test_delete_executor(bm_id)

def test_run_benchmark_cookbook_executor_api():
    bm_id = "cookbook-my-new-cookbook-executor"

    # Create executor
    print("="*100,"\nTest creating cookbook executor")
    test_create_cookbook_executor()

    # Load executor
    print("="*100,"\nTest loading executor")
    test_load_executor(bm_id)

    # Execute the recipe job
    print("="*100,"\nTest executing executor")
    test_execute_executor(bm_id)

    # Read executor
    print("="*100,"\nTest reading executor")
    test_read_executor(bm_id)

    # List all executor
    print("="*100,"\nTest listing all executors")
    test_get_all_executors()

    # List all executor names
    print("="*100,"\nTest listing all executors names")
    test_get_all_executors_names()

    # Delete executor
    print("="*100,"\nTest deleting executors")
    test_delete_executor(bm_id)

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

    # Test metric api
    test_run_metric_api()
