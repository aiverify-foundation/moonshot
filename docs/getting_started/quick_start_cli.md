# Quick Start Guide (CLI)

## Setting Up 

### Step 0: Creating virtual environment
We highly recommend creating a virtual environment to avoid any conflicts in the Python libraries.

### Step 1: Install Moonshot
1. To begin, install Moonshot from the designated source (e.g., GitHub/PyPi).
```
$ git clone git@github.com:moonshot-admin/moonshot.git

OR 

$ pip install "projectmoonshot-imda[cli]"
```

2. Install Required Dependencies
- Ensure that all necessary requirements are installed by executing the appropriate command provided in the documentation.
- If you are installing the project from GitHub, run the following command:
```
$ pip install -r requirements.txt
```
### Step 2: Environment Variables (Optional)
- You can link your own data folder with the library by running the following code snippet:
<!--Instead of using the stock test data provided by the library, you have the option to link your own data folder by running the following code to connect your file directory.-->

```json

CONNECTORS = "/path/to/your/connectors"
RECIPES = "/path/to/your/recipes"
COOKBOOKS = "/path/to/your/cookbooks"
DATASETS = "/path/to/your/datasets"
PROMPT_TEMPLATES = "/path/to/your/prompt-templates"
METRICS = "/path/to/your/metrics"
METRICS_CONFIG = "/path/to/your/metrics/metrics_config.json"
CONTEXT_STRATEGY = "/path/to/your/context-strategy"
RESULTS = "/path/to/your/results"
DATABASES = "/path/to/your/databases"
SESSIONS = "/path/to/your/sessions"
```

!!! Note 
    When changing the reference folder for data, users will no longer be able to access the stock cookbooks. To access these cookbooks, users should copy over their respctive json files and dependencies_

### Step 3: Starting Moonshot CLI

There are two available modes to use Moonshot CLI. Command-Based Mode and Interactive Mode.

For a better experience, we recommend using the Interactive Mode. To use interactive mode, run this code:
```
python -m moonshot cli interactive
```

You should see the command prompt change to `moonshot >` like this:
```
moonshot > 
```

For this quick start guide, we will be using Interactive Mode as an example.

To start off, you can use the commmand `help` to view all the available commands in Moonshot CLI.
```
moonshot > help
```

### Step 4: Creating Endpoint
You can establish connectivity to an LLM or LLM application by creating an endpoint with your environment.

- View the list of conenctor type availables in Moonshot with this:
```
moonshot > list_connector_types
```
- Create new endpoint with: 
```
moonshot > add_endpoint openai-gpt35 my-openai-endpoint MY_URI ADD_YOUR_TOKEN_HERE 10 2 "{'temperature': 0}"
```
- To view the parameters required, you can run the command with the help tag.
```
moonshot > add_endpoint -h 
```

## Benchmarking

### Step 1: Creating Custom Recipe/Cookbook (Optional)

You can create a custom recipe consisting of a dataset, metric and prompt templates.

This step allows you to tailor the benchmarking process to your specific need and objective.

- To add a new recipe, use the `add_recipe` command. 
```
 moonshot > add_recipe 'My new recipe' 'I am recipe description' "['tag1','tag2']" "['bbq-lite-age-ambiguous']" "['analogical-similarity','auto-categorisation']" "['bertscore','bleuscore']"
```
- To add a new cookbook, use the `add_cookbook` command.
```
moonshot > add_cookbook 'My new cookbook' 'I am cookbook description' "['analogical-similarity','auto-categorisation']"
```
- To view the parameters required, you can run the command with the help tag.
```
moonshot > add_recipe -h # To view the parameter required to add recipe.
moonshot > add_cookbook -h # To view the paramter required to add cookbook.
```

### Step 2: Select Recipe / Cookbook to Run a Benchmark
To run a benchmark, select a recipe or cookbook that aligns with your desired evaluation or analysis objective.

- To start benchmarking using a recipe, use the `run_recipe` command.
```
moonshot > run_recipe -n 1 "['bbq','auto-categorisation']" "['test-openai-endpoint']"
```
- To start benchmarking using a cookbook, use the `run_cookbook` command.
```
moonshot > run_cookbook -n 1 "['bbq-lite-age-cookbook']" "['test-openai-endpoint']"
```
- To view the parameters required, you can run the command with the help tag.
```
moonshot > run_recipe -h # To view the parameter required to run recipe.
moonshot > run_cookbook -h # To view the paramter required to run cookbook.
```

### Step 3: View Results

- To view the list of result, use the `list_results` command.
```
moonshot > list_results
```
- To view the result, use the `view_result` command.
```
moonshot > view_result cookbook-my-new-cookbook-executor
```
- To view the parameters required, you can run the command with the help tag.
```
moonshot > view_result -h # To view the parameter required to view results.
```

## Red Teaming

### Step 1: Create a Red Teaming session
To begin, create a Red Teaming session with the list of endpoins you wish to test.

- To create a new sesion, use the `new_session` command.
```
moonshot > new_session 'my_new_session' 'My new session description' "['my-openai-gpt35', 'my-openai-gpt4']"
```
- To view the parameters required, you can run the command with the help tag.
```
moonshot > new_session -h # To view the parameter required to create a new session.
```

### Step 2: Using created session.
To start red teaming, you would have to enter the session that you have created.

- To enter the created session, use the `use_session` command. 
```
 use_session 'my-my_new_session'
```
- To view the parameters required, you can run the command with the help tag.
```
moonshot > use_session -h # To view the parameter required to use a session.
```

Once you entered a session, your command prompt should change to look like this with the value of `session_id` being of a certain value. 
```
moonshot (my-new-session_{session_id}) [PT: None, CS: None] >
```

### Step 3: Remove and Adding Prompt Tempaltes or Context Strategies
Optionally, you can utilize prompt templates and context strategies to customize augment prompts that are sent to the model.

The prompt template provides pre-prompt and post-prompt text are passed into the LLM/LLM application along with your prompt.

A context strategy defines additional information from the chat history that will be appended to your prompt as a 'context'. Examples of a 'context' includes a summary of the previous n-prompts.

- To view the list of prompt template and contexst strategy, use this two commands.
```
list_prompt_templates
list_contexst_strategies
```
- To load prompt template, use the `use_prompt_template` command.
```
 use_prompt_template 'analogical-similarity'
```
- To load a context strategy, use the `use_context_strategy` command.
```
 use_context_strategy 'add_previous_prompt'
```

When you have successfully loaded your prompt template and context strategy, your command prompt should look like this: 
```
moonshot (my-new-session_{session_id}) [PT: analogical-similarity, CS: add_previous_prompt] >
```
- To remove prompt template and context strategy, use this two commands.
```
clear_prompt_template
clear_context_strategy
```
Your prompt template and context strategy should be unloaded and your command prompt will look like this: 
```
moonshot (my-new-session_{session_id}) [PT: None, CS: None] >
```
### Step 4: Analyze Results
Analyze the results from benchmarking or red teaming to assess the security posture or vulnerabilities of the target systems. Interpret the responses to identify potential weaknesses or areas for improvement in the tested environment.
