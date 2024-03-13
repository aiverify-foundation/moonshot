import json
import os
from slugify import slugify
from moonshot.api import (
    api_create_endpoint,
    api_read_endpoint,
    api_update_endpoint,
    api_delete_endpoint,
    api_get_all_endpoints,
    api_get_all_endpoints_names,
    api_create_connector,
    api_create_connectors,
    api_get_all_connectors,
    api_create_cookbook,
    api_read_cookbook,
    api_read_cookbooks,
    api_update_cookbook,
    api_delete_cookbook,
    api_get_all_cookbooks,
    api_get_all_cookbooks_names,
    api_create_recipe,
    api_read_recipe,
    api_read_recipes,
    api_update_recipe,
    api_delete_recipe,
    api_get_all_recipes,
    api_get_all_recipes_names,
)
from moonshot.src.configs.env_variables import EnvironmentVars

def check_file_exists(file_path):
    """
    Check if a file exists in the system.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def slugify_id(name):
    return slugify(name, lowercase=True)

def fetch_files_in_dir(dir_path):
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f != "placeholder"]


# ------------------------------------------------------------------------------
# Connector and Connector endpoints APIs Test
# ------------------------------------------------------------------------------
def test_create_connector_endpoint():
    name="My New GPT35"
    connector_type="openai-gpt35"
    uri="1234"
    token="1234"
    max_calls_per_second=256
    max_concurrency=1
    params={
        "hello": "world"
    }   
    
    api_create_endpoint(
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        params
    )
    
    assert check_file_exists(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{slugify_id(name)}.json")

def test_read_connector_endpoint():
    expected_output = {
        'name': "My New GPT35",
        'connector_type':"openai-gpt35",
        'uri':"1234",
        'token':"1234",
        'max_calls_per_second':256,
        'max_concurrency':1,
        'params':{
            "hello": "world"
        } 
    }
    actual_output = api_read_endpoint("my-new-gpt35")

    # Check if all key-value pairs in expected_output are present in actual_output (unable to determine created-datetime)
    for key, value in expected_output.items():
        assert key in actual_output
        assert actual_output[key] == value

def test_update_connector_endpoint():
    original_expected_output = {
        'name': "My New GPT35",
        'connector_type':"openai-gpt35",
        'uri':"1234",
        'token':"1234",
        'max_calls_per_second':256,
        'max_concurrency':1,
        'params':{
            "hello": "world"
        } 
    }

    if all(api_read_endpoint("my-new-gpt35").get(key) == value for key, value in original_expected_output.items()):
        name="My New GPT35"
        connector_type="openai-gpt35"
        uri="4567"
        token="4567"
        max_calls_per_second=10
        max_concurrency=10
        params={
            "hello": "world"
        }

        api_update_endpoint(
            name,
            connector_type,
            uri,
            token,
            max_calls_per_second,
            max_concurrency,
            params
        )

        expected_update_output = {
            'name': "My New GPT35",
            'connector_type':"openai-gpt35",
            'uri':"4567",
            'token':"4567",
            'max_calls_per_second':10,
            'max_concurrency':10,
            'params':{
                "hello": "world"
            } 
        }

        actual_output = api_read_endpoint("my-new-gpt35")
        # Check if all key-value pairs in expected_output are present in actual_output (unable to determine created-datetime)
        for key, value in expected_update_output.items():
            assert key in actual_output
            assert actual_output[key] == value
    else:
        assert False

def test_delete_connector_endpoint():
    conn_to_delete = "my-new-gpt35"
    #check file exist first before deleting
    if check_file_exists(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{slugify_id(conn_to_delete)}.json"):
        api_delete_endpoint(conn_to_delete)
        assert not check_file_exists(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{slugify_id(conn_to_delete)}.json")
    else:
        assert False

def test_get_all_connector_endpoints():
    #Just checking if number of connector endpoints matches
    api_read_connector_endpoints = api_get_all_endpoints()
    connector_endpoints_in_dir = fetch_files_in_dir(EnvironmentVars.CONNECTORS_ENDPOINTS)

    assert len(api_read_connector_endpoints) == len(connector_endpoints_in_dir)

def test_get_all_connector_endpoints_name():
    api_read_connector_endpoints = api_get_all_endpoints_names()

    connector_endpoints_in_dir = fetch_files_in_dir(EnvironmentVars.CONNECTORS_ENDPOINTS)
    retn_conn_name = []
    for conn_name in connector_endpoints_in_dir:
        conn_filepath = f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{conn_name}"
        with open(conn_filepath, "r", encoding="utf-8") as json_file:
            conn_info = json.load(json_file)
            retn_conn_name.append(conn_info['id'])
        
    assert set(api_read_connector_endpoints) == set(retn_conn_name)

def test_create_connector():
    name="My New GPT35"
    connector_type="openai-gpt35"
    uri="1234"
    token="1234"
    max_calls_per_second=256
    max_concurrency=1
    params={
        "hello": "world"
    }   
    
    api_create_endpoint(
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        params
    )

    # Create new connector
    assert api_create_connectors(["my-new-gpt35", "my-new-gpt35", "my-new-gpt35"])

    # Delete file after assertion
    api_delete_endpoint("my-new-gpt35")

def test_create_connectors():
    name="My New GPT35"
    connector_type="openai-gpt35"
    uri="1234"
    token="1234"
    max_calls_per_second=256
    max_concurrency=1
    params={
        "hello": "world"
    }   
    
    api_create_endpoint(
        name,
        connector_type,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        params
    )

    # Create new connector
    assert api_create_connector("my-new-gpt35")

    # Delete file after assertion
    api_delete_endpoint("my-new-gpt35")

def test_get_all_connectors():
    expected_output = ['hf-llama2-13b-gptq', 'openai-gpt4', 'claude2', 'openai-gpt35', 'openai-gpt35-turbo-16k', 'hf-gpt2']
    assert set(expected_output) == set(api_get_all_connectors())
    
# ------------------------------------------------------------------------------
# Cookbook APIs Test
# ------------------------------------------------------------------------------
def test_create_cookbook():

    name="my-pytest-cookbook"
    description="This cookbook was created by PyTest."
    recipes=["my-recipe1","my-recipe2"]

    api_create_cookbook(
        name,
        description,
        recipes
    )

    assert check_file_exists(f"{EnvironmentVars.COOKBOOKS}/{slugify_id(name)}.json")

def test_read_cookbook():
    expected_output = {
        'id': 'my-pytest-cookbook', 
        'name' : 'my-pytest-cookbook',
        'description': "This cookbook was created by PyTest.",
        'recipes': ["my-recipe1","my-recipe2"]
    }

    assert api_read_cookbook("my-pytest-cookbook") == expected_output

def test_read_cookbooks():
    expected_output = [{
        'id': 'my-pytest-cookbook', 
        'name' : 'my-pytest-cookbook',
        'description': "This cookbook was created by PyTest.",
        'recipes': ["my-recipe1","my-recipe2"]
    } for _ in range(3)]

    assert api_read_cookbooks(["my-pytest-cookbook","my-pytest-cookbook","my-pytest-cookbook"]) == expected_output

def test_update_cookbook():
    original_expected_output = {
        'id': 'my-pytest-cookbook', 
        'name' : 'my-pytest-cookbook',
        'description': "This cookbook was created by PyTest.",
        'recipes': ["my-recipe1","my-recipe2"]
    } 

    if api_read_cookbook("my-pytest-cookbook") == original_expected_output:
        id = 'my-pytest-cookbook'
        name = 'my-pytest-cookbook'
        description = "This cookbook has been updated by PyTest."
        recipes = ["my-recipe2","my-recipe5"]

        api_update_cookbook(
            name,
            description,
            recipes
        )

        expected_update_output = {
            'id': 'my-pytest-cookbook', 
            'name' : 'my-pytest-cookbook',
            'description': "This cookbook has been updated by PyTest.",
            'recipes': ["my-recipe2","my-recipe5"]
        }

        assert api_read_cookbook("my-pytest-cookbook") == expected_update_output
    else:
        assert False

def test_delete_cookbook():
    cb_to_delete = "my-pytest-cookbook"
    #check file exist first before deleting
    if check_file_exists(f"{EnvironmentVars.COOKBOOKS}/{slugify_id(cb_to_delete)}.json"):
        api_delete_cookbook(cb_to_delete)
        assert not check_file_exists(f"{EnvironmentVars.COOKBOOKS}/{slugify_id(cb_to_delete)}.json")
    else:
        assert False

def test_get_all_cookbooks():
    #Just checking if number of cookbook matches
    api_read_cookbook_from_api = api_get_all_cookbooks()
    cookbook_in_dir = fetch_files_in_dir(EnvironmentVars.COOKBOOKS)

    assert len(api_read_cookbook_from_api) == len(cookbook_in_dir)

def test_get_all_cookbook_names():
    cookbook_names_from_api = api_get_all_cookbooks_names()

    cookbook_in_dir = fetch_files_in_dir(EnvironmentVars.COOKBOOKS)
    retn_cookbook_ids = []
    for cb_id in cookbook_in_dir:
        cb_filepath = f"{EnvironmentVars.COOKBOOKS}/{cb_id}"
        with open(cb_filepath, "r", encoding="utf-8") as json_file:
            cb_info = json.load(json_file)
            retn_cookbook_ids.append(cb_info['id'])
        
    assert  cookbook_names_from_api == retn_cookbook_ids

# ------------------------------------------------------------------------------
# Recipes APIs Test
# ------------------------------------------------------------------------------

def test_create_recipe():
    name="my-pytest-recipe"
    description = "This recipe was created by PyTest."
    tags=["robustness"]
    datasets=["dataset1", "dataset2"]
    prompt_templates=["prompt-template1"]
    metrics=["metrics1","metrics2"]

    api_create_recipe(
        name,
        description,
        tags,
        datasets,
        prompt_templates,
        metrics
    )

    assert check_file_exists(f"{EnvironmentVars.RECIPES}/{slugify_id(name)}.json")

def test_read_recipe():

    expected_output = {
        'id': 'my-pytest-recipe', 
        'name' : 'my-pytest-recipe',
        'description': "This recipe was created by PyTest.",
        'tags': ["robustness"], 
        'datasets': ["dataset1", "dataset2"],
        'prompt_templates': ["prompt-template1"], 
        'metrics': ["metrics1", "metrics2"]
    }

    assert api_read_recipe("my-pytest-recipe") == expected_output

def test_read_recipes():
    expected_output = [{
        'id': 'my-pytest-recipe', 
        'name' : 'my-pytest-recipe',
        'description': "This recipe was created by PyTest.",
        'tags': ["robustness"], 
        'datasets': ["dataset1", "dataset2"],
        'prompt_templates': ["prompt-template1"], 
        'metrics': ["metrics1", "metrics2"]
    } for _ in range(3)]  

    assert api_read_recipes(["my-pytest-recipe","my-pytest-recipe","my-pytest-recipe"]) == expected_output
    
def test_update_recipe():

    original_expected_output = {
        'id': 'my-pytest-recipe', 
        'name' : 'my-pytest-recipe',
        'description': "This recipe was created by PyTest.",
        'tags': ["robustness"], 
        'datasets': ["dataset1", "dataset2"],
        'prompt_templates': ["prompt-template1"], 
        'metrics': ["metrics1", "metrics2"]
    }

    if api_read_recipe("my-pytest-recipe") == original_expected_output:
        name="my-pytest-recipe"
        description = "This recipe has been updated by PyTest"
        tags=["fairness"]
        datasets=["dataset1", "dataset2"]
        prompt_templates=["prompt-template1"]
        metrics=["metrics1","metrics2"]

        api_update_recipe(
            name,
            description,
            tags,
            datasets,
            prompt_templates,
            metrics
        )

        expected_update_output = {
            'id': 'my-pytest-recipe', 
            'name' : 'my-pytest-recipe',
            'description': 'This recipe has been updated by PyTest',
            'tags': ["fairness"], 
            'datasets': ["dataset1", "dataset2"],
            'prompt_templates': ["prompt-template1"], 
            'metrics': ["metrics1", "metrics2"]
        }

        assert api_read_recipe("my-pytest-recipe") == expected_update_output
    else:
        assert False

def test_delete_recipe():
    rec_to_delete = "my-pytest-recipe"
    #check file exist first before deleting
    if check_file_exists(f"{EnvironmentVars.RECIPES}/{slugify_id(rec_to_delete)}.json"):
        api_delete_recipe(rec_to_delete)
        assert not check_file_exists(f"{EnvironmentVars.RECIPES}/{slugify_id(rec_to_delete)}.json")
    else:
        assert False

def test_get_all_recipes():
    #Just checking if number of recipe matches
    recipes_from_api = api_get_all_recipes()
    recipes_in_dir = fetch_files_in_dir(EnvironmentVars.RECIPES)

    assert len(recipes_from_api) == len(recipes_in_dir)

def test_get_all_recipes_names():
    recipes_names_from_api = api_get_all_recipes_names()

    recipes_in_dir = fetch_files_in_dir(EnvironmentVars.RECIPES)
    retn_recs_ids = []
    for rec_id in recipes_in_dir:
        rec_filepath = f"{EnvironmentVars.RECIPES}/{rec_id}"
        with open(rec_filepath, "r", encoding="utf-8") as json_file:
            rec_info = json.load(json_file)
            retn_recs_ids.append(rec_info['id'])
        
    assert  recipes_names_from_api == retn_recs_ids

