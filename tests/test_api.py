from moonshot.api import (api_create_connector, api_create_connectors, api_create_endpoint, api_create_recipe, api_delete_endpoint, api_delete_recipe, 
                          api_get_all_connectors, api_get_all_endpoints, api_get_all_endpoints_names, api_get_all_recipes, api_get_all_recipes_names, 
                          api_read_endpoint, api_read_recipe, api_read_recipes, api_update_endpoint, api_update_recipe)

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

if __name__ == "__main__":
    # Test connector apis
    test_run_connector_api()

    # Test recipes api
    test_run_recipe_api()