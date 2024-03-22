# Quick Start Guide (Library)
Refer to this [example](https://github.com/moonshot-admin/moonshot/blob/new_dev_main/examples/test-openai-gpt35.ipynb) for the usage of Moonshot.

## Setting Up 

### Step 0: Creating virtual environment
We highly recommend creating a virtual environment to avoid any conflicts in the Python libraries.

### Step 1: Install Moonshot
1. To begin, install Moonshot from the designated source (e.g., GitHub/PyPi).
```
$ git clone git@github.com:moonshot-admin/moonshot.git

OR 

$ pip install projectmoonshot-imda
```

2. Install Required Dependencies
- Ensure that all necessary requirements are installed by executing the appropriate command provided in the documentation.
- If you are installing the project from GitHub, run the following command:
```
$ pip install -r requirements.txt
```
### Step 2: Importing Moonshot
- Import Moonshot as a library to use it. 
```python 
from moonshot.api import (
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
- You can link your own data folder with the library by running the following code snippet:
<!--Instead of using the stock test data provided by the library, you have the option to link your own data folder by running the following code to connect your file directory.-->

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
_Note: When changing the reference folder for data, users will no longer be able to access the stock cookbooks. To access these cookbooks, users should copy over their respctive json files and dependencies._

### Step 4: Connecting End Points
You can establish connectivity to an LLM or LLM application by creating an endpoint within your environment.

- View the list of connector types available in Moonshot with:
```
api_get_all_connector_type()
```
- Create a new endpoint with:
 ```
 api_create_endpoint()
 ```
- The following is a code snippet to create an endpoint:
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

## Benchmarking

### Step 1: Create Custom Recipe/Cookbook (Optional)
You can create a custom recipe consisting of a dataset, metric and prompt templates.

This step allows you to tailor the benchmarking process to your specific need and objective.

- To add a new recipe, use `api_create_recipe()`. The code snippet below uses a dataset and prompt template from the baseline benchmarks available in Moonshot.
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
- To add a new cookbook, use api_craete_cookbook(). 
```python
api_create_cookbook(
    "new-cookbook", # name of cookbook
    "This cookbook is a compiled auto-categorisation cookbook", # description of cookbook
    ["auto-categorisation","auto-categorisation-2"] # list of recipes
)
```

### Step 2: Select Recipe/Cookbook to Run a Benchmark
To run a benchmark, select a recipe or cookbook that aligns with your desired evaluation or analysis objective.

- To start benchmarking using a recipe, use `api_create_recipe_executor()`.
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
- To start benchmarking using a cookbook, use `api_create_cookbook_executor()`.
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
The results will be stored in the `moonshot/data/results` directory or the custom path that is defined during the [Set Up](#step-3-environment-variables-optional) process.

Analyze the output to gain insight into the performance your model/application.

## Red Teaming

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

### Step 3: Remove and Adding Prompt Templates or Context Strategies
Optionally, you can utilize prompt templates and context strategies to customize augment prompts that are sent to the model.

The prompt template provides pre-prompt and post-prompt text are passed into the LLM/LLM application along with your prompt.

A context strategy defines additional information from the chat history that will be appended to your prompt as a 'context'. Examples of a 'context' includes a summary of the previous n-prompts.

```python
context_strategy = "add_previous_prompt"
prompt_template = "test-prompt-template"

api_update_context_strategy(session_id, context_strategy)
api_update_prompt_template(session_id, prompt_template)

# Get updated session
updated_session = api_get_session(session_id)
```

Use these commands to view the list of prompt templates and context strategies.
```python

api_get_all_prompt_template_detail()
api_get_all_context_strategy_name()

```

### Step 4: Analyze Results
Analyze the results from benchmarking or red teaming to assess the security posture or vulnerabilities of the target systems. Interpret the responses to identify potential weaknesses or areas for improvement in the tested environment.
