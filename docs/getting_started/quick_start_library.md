# Quick Start Guide (Library)
For an example of how to run Moonshot as a Library using a Jupyter notebook, you can refer to [this link](https://github.com/moonshot-admin/moonshot/blob/new_dev_main/examples/test-openai-gpt35.ipynb).

## Setting Up 

### Step 0: Creating virtual environment
If you have not created a virtual environment, we suggest creating one to avoid any conflicts in the Python libraries.

### Step 1: Install Moonshot
1. To begin, install Moonshot from the designated source (e.g., GitHub/pypi).
```
$ git clone git@github.com:moonshot-admin/moonshot.git

OR 

$ pip install projectmoonshot-imda
```

2. Install Required Dependencies
- Make sure that all necessary requirements are installed by executing the appropriate command provided in the documentation.
- If you are installing the project from GitHub, run the following command:
```
$ pip install -r requirements.txt
```
### Step 2: Importing Moonshot
- Import Moonshot library to use it. 
```python 
from moonshot.api import  import (
    api_create_recipe,
    api_create_cookbook,
    api_create_endpoint,
    api_create_recipe_executor,
    api_create_cookbook_executor,
    api_create_session,
    api_get_session,
    api_get_all_connector_type,
    api_get_all_endpoint,
    api_get_all_cookbook,
    api_get_all_recipe,
    api_get_all_executor,
    api_get_all_session_detail,
    api_get_all_prompt_template_detail,
    api_get_all_context_strategy_name,
    api_get_session_chats_by_session_id,
    api_load_executor,
    api_set_environment_variables,
    api_send_prompt,
    api_update_context_strategy,
    api_update_prompt_template,
)
```
### Step 3: Environment Variables (Optional)
- Instead of using the default data provided by the library, you have the option to link your own datasets by running the following code to connect your file directory.
```python
moonshot_path = "../moonshot/data/"

env = {
    "CONNECTORS_ENDPOINTS": os.path.join(moonshot_path, "connectors-endpoints"),
    "CONNECTORS": os.path.join(moonshot_path, "connectors"),
    "RECIPES": os.path.join(moonshot_path, "recipes"),
    "COOKBOOKS": os.path.join(moonshot_path, "cookbooks"),
    "DATASETS": os.path.join(moonshot_path, "datasets"),
    "PROMPT_TEMPLATES": os.path.join(moonshot_path, "prompt-templates"),
    "METRICS": os.path.join(moonshot_path, "metrics"),
    "METRICS_CONFIG": os.path.join(moonshot_path, "metrics/metrics_config.json"),
    "CONTEXT_STRATEGY": os.path.join(moonshot_path, "context-strategy"),
    "RESULTS": os.path.join(moonshot_path, "results"),
    "DATABASES": os.path.join(moonshot_path, "databases"),
    "SESSIONS": os.path.join(moonshot_path, "sessions"),
}

api_set_environment_variables(env)

```

### Step 4: Connecting End Points
- Establish connectivity by creating an endpoint within your environment.
- To view the list of connector available in Moonshot, you can use the `api_get_all_connector_type()`.
- To create a new endpoint, we can use `api_create_endpoint()`.
```python
api_create_endpoint(
    "test-openai-endpoint", # name: give it a name to retrieve it later
    "openai-gpt35", # connector_type: the model that we want to evaluate
    "", # uri: not required as we use OpenAI library to connect to their models.
    "ADD_NEW_TOKEN_HERE", # token: access token
    10, # max_calls_per_second: the number of max calls per second
    2, # max_concurrency: the number of concurrent call at any one time,
    {
        "temperature": 0
    } # params: any additional required for this model
)
```
- Once an endpoint has been added to Moonshot, we can use this endpoint to evaluate the model later when we run our benchmark or redteam.

## Benchmarking

### Step 1: Create Custom Recipe/Cookbook (Optional)
Optionally, you can create your own custom recipe consisting of a dataset, metric, and prep and post prompts. This step allows you to tailor the benchmarking process to their specific needs and objectives.
- To add a new recipe, we will use `api_create_recipe()`. We will use dataset and prompt template from the default moonshot library as an example.
```python
api_create_recipe(
    "auto-categorisation-2" # name of recipe
    "A duplicate of the existing Auto Categorisation recipe with a different name.", # description of recipe
    [], # tags
    ["auto-categorisation"], # datasets
    ["auto-categorisation"], # prompt templates
    ["relaxstrmatch"] # metrics
)
```
- To add a new cookbook, we will use api_craete_cookbook(). 
```python
api_create_cookbook(
    "new-cookbook", # name of cookbook
    "This cookbook is a compiled auto-categorisation cookbook", # description of cookbook
    ["auto-categorisation","auto-categorisation-2"] # list of recipes
)
```

### Step 2: Select Recipe/Cookbook to Run Benchmark
To perform a benchmarking task, select a recipe or cookbook that aligns with your desired evaluation or analysis objectives.
- To start your recipe benchmarking task, you can use `api_create_recipe_executor()`.
```python
recipes = ["auto-categorisation-2"]
endpoints = ["test-openai-endpoint"]
num_of_prompts = 5 # use a smaller number to test out the function

bm_executor = api_create_recipe_executor(
    "my new recipe executor",
    recipes,
    endpoints,
    num_of_prompts
)
```
- To start your cookbook benchmarking task, you can use `api_create_cookbook_executor()`.
```python
cookbooks = ["new-cookbook"]
endpoints = ["test-openai-endpoint"]
num_of_prompts = 1

bm_executor = api_create_cookbook_executor(
    "my new cookbook executor",
    cookbooks,
    endpoints,
    num_of_prompts
)
```

### Step 3: View Results
Once the benchmarking process is complete, the results will be stored in the `moonshot/data/results` directory, or in the custom path that you have defined during the Set Up process.

Analyze the output to gain insights into the performance or effectiveness of the evaluated system.

## Red Team

### Step 1: Create a Red Teaming session
To begin, create a Red Teaming session with the list of endpoints you wish to test.

```python
endpoints = ["test-openai-endpoint"]

my_rt_session = api_create_session(
    "My Red Teaming Session",
    "Creating a new red teaming description",
    endpoints,
)
```
### Step 2: Store Session ID
- After creating a session, store the `session_id` as a variable for future use.
- This `session_id` will be needed for additional functions and operations.
```python
session_id = my_rt_session.metadata.session_id

# To see session details
show_session(my_rt_session)
```
### Step 2: Send Prompts
Utilize the toolkit to send prompts to the configured endpoints. Create prompts that are specifically crafted to elicit responses or actions from the target LLM or applications.

```python
prompt = "What is the largest fruit"

await api_send_prompt(session_id, prompt)

show_session_chats(api_get_session_chats_by_session_id(session_id))
```

### Step 3: Remove and Adding Prompt Templates or Context Strategy
Optionally, you can remove or add prompt templates and context strategy to customize the toolkit's behavior.

```python
context_strategy = "add_previous_prompt"
prompt_template = "test-prompt-template"

api_update_context_strategy(session_id, context_strategy)
api_update_prompt_template(session_id, prompt_template)

# Get updated session
updated_session = api_get_session(session_id)
```

To view the list of prompt templates and context strategy you can use these commands
```python

api_get_all_prompt_template_detail()
api_get_all_context_strategy_name()

```

### Step 4: Analyze Results
Once prompts have been sent and responses received, analyze the results to assess the security posture or vulnerabilities of the target systems. Interpret the responses to identify potential weaknesses or areas for improvement in the tested environment.
