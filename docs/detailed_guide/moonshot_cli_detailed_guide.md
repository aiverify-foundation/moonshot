
## Run Moonshot using Command Line (CLI)

### (CLI) How to Create Custom Benchmark Tests

In this detailed guide section, you will learn how to run a benchmark in Moonshot. Benchmarks are a set of "exam questions" that can help to evaluate and assess the capabilities and safety of the AI system.

1. Change directory to the root directory of Moonshot.

2. Enter the following command to enter the CLI interactive mode:

        python -m moonshot cli interactive

3. Choose a benchmark type to run and view help:

    !!! warning
        <b>Important information before running your benchmark:</b>

        Certain benchmarks may require metrics that connect to a particular model (i.e. MLCommons cookbooks and recipes like [mlc-cae](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/mlc-cae.json) use the metric [llamaguardannotator](https://github.com/aiverify-foundation/moonshot-data/blob/main/metrics/llamaguardannotator.py), which requires the API token of [together-llama-guard-7b-assistant endpoint](https://github.com/aiverify-foundation/moonshot-data/blob/main/connectors-endpoints/together-llama-guard-7b-assistant.json)).

        Refer to this [list for the requirements](../../faq.md#requirements).


    - Recipe

        To find out more about the required fields to create a recipe:

            run_recipe -h

        To run the help example, enter:

            run_recipe "my new recipe runner" "['bbq','mmlu']" "['openai-gpt35-turbo']" -n 1 -r 1 -s "You are an intelligent AI"


    - Cookbook:

        To find out more about the required fields to create a cookbook:

            run_cookbook -h

        To run the help example, enter:

            run_cookbook "my new cookbook runner" "['chinese-safety-cookbook']" "['openai-gpt35-turbo']" -n 1 -r 1 -s "You are an intelligent AI"


4. View the results:
    - Recipe:

        ![recipe results](./cli/images/recipe_results_table.png)

    - Cookbook:

        ![cookbook results](./cli/images/cookbook_results_table.png)

<!-- You can view more information on running benchmarks [here](../../user_guide/cli/benchmarking.md). -->

## CLI modes

Two modes are available on the Moonshot CLI: Command-Based Mode and Interactive Mode.

<details open>

<summary>Full list of commands in Moonshot</summary>

``` bash
Initialisation
======================================================================================================
interactive           Run the interactive shell.                                                      
list_connect_types    Get a list of available Language Model (LLM) connection types.                  
list_endpoints        Get a list of available Language Model (LLM) endpoints.                         
version               Get the version of the application.                                             

Moonshot Benchmarking
======================================================================================================
add_cookbook          Add a new cookbook.                                                             
add_endpoint          Add a new endpoint.                                                             
add_recipe            Add a new recipe.                                                               
list_cookbooks        Get a list of available cookbooks.                                              
list_recipes          Get a list of available recipes.                                                
list_results          Get a list of available results.                                                
list_runs             Get a list of available runs.                                                   
resume_run            Resume an interrupted run.                                                      
run_cookbook          Run a cookbook.                                                                 
run_recipe            Run a recipe.                                                                   
view_cookbook         View a cookbook.                                                                
view_results          View a results file.                                                            

Moonshot RedTeaming
=======================================================================================================
end_session            End the current session.                                                        
list_prompt_templates  List all prompt templates available.                                            
list_sessions          List all available sessions.                                                    
new_session            Add a new red teaming session.                                                  
use_context_strategy   Use a context strategy.                                                         
use_prompt_template    Use a prompt template.                                                          
use_session            Use an existing red teaming session.                                            

Uncategorized
======================================================================================================
alias                 Manage aliases                                                                  
edit                  Run a text editor and optionally open a file with it                            
help                  List available commands or provide detailed help for a specific command         
history               View, run, edit, save, or clear previously entered commands                     
macro                 Manage macros                                                                   
quit                  Exit this application                                                           
run_pyscript          Run a Python script file inside the console                                     
run_script            Run commands in script file that is encoded as either ASCII or UTF-8 text       
set                   Set a settable parameter or show current settings of parameters                 
shell                 Execute a command as if at the OS prompt                                        
shortcuts             List available shortcuts                                                
```
</details>

## Command-based Mode

In the command-based mode, run commands by prepending `python -m moonshot cli`. 

For example,

- To list all the available commands: `python -m moonshot cli help`
- To list the connector types available: `python -m moonshot cli list_connect_types`

## Interactive Mode

We recommend the interactive mode for a more efficient experience, especially if you are using Moonshot to red-team. 

To enter interactive mode: `python -m moonshot cli interactive` (You should see the command prompt change to `moonshot >` ) For example,

- To list all the available commands: 
    ```
    moonshot > help
    ```
- To list the connector types available:
    ```
    moonshot > list_connect_types
    ```

# Add Your Own Benchmark Tests

In this section, we will be going through the steps required to add new test using CLI.

You will learn how to:

- Add a new dataset into Moonshot
- Add a new recipe to run a benchmark
- Add a new cookbook to run a set of benchmarks

## Launch Moonshot CLI

You can launch Moonshot CLI by running the following command:

```
python -m moonshot cli interactive
```

## Create a New Cookbook

We can also create a new cookbook with our new recipe. A cookbook in Moonshot is a curated collection of recipes. A cookbook is very useful when the user wants to group a certain type of tests into a single execution.

### Add Cookbook

To add a new cookbook, simply run the following command: 

```
moonshot > add_cookbook [name] [description] [cookbooks]
```

The fields are as follows for this example: 

- Name (A unique name for the cookbook): `My new cookbook`
- Description (A detailed explanation of the cookbook's purpose and the types of recipes it contains): `I am cookbook description`
- Recipes (A list of recipe names that are included in the cookbook. Each recipe represents a specific test or benchmark): `['my-new-recipe','auto-categorisation']`

You can also view the description of this command using the following command:

```
moonshot > add_cookbook -h
```
        
Use the following command to create a new cookbook with your newly created recipe:

```
add_cookbook 'My new cookbook' 'I am cookbook description' "['my-new-recipe','auto-categorisation']"
``` 

### View Cookbook

Enter the following command to view your newly created cookbook:

```
view_cookbook my-new-cookbook
```

![cookbook added](cli_images/add_cookbook.png)

## Create a New Recipe

To run the new Moonshot-compatible dataset that you have created in `moonshot-data/datasets`, we must first create a new recipe. 

!!! note

    A recipe contains all the details required to run a benchmark. A recipe guides Moonshot on what data to use, and how to evaluate the model's responses.

### Add Recipe 

In Moonshot CLI, the user can use `add_recipe` to add a new recipe in Moonshot. The parameters of the command are shown below:

- Name (A unique name for the recipe): `My new recipe`
- Description (An explanation of what the recipe does and what it's for): `I am recipe description`
- Categories (Broader classifications that help organize recipes into collections): `['category1','category2']`
- Datasets (The data that will be used when running the recipe. This could be a set of prompts, questions, or any input that - the model will respond to): `['bbq-lite-age-ambiguous']`
- Metrics (Criteria or measurements used to evaluate the model's responses, such as accuracy, fluency, or adherence to a - prompt): `['bertscore','bleuscore']`
- Prompt Templates (Optional pre-prompt or post-prompt): `['analogical-similarity','mmlu']`
- Tags (Optional keywords that categorize the recipe, making it easier to find and group with similar recipes): `['tag1','tag2']`
- Attack Strategies (Optional components that introduce adversarial testing scenarios to probe the model's robustness): `['charswap_attack']`
- Grading Scale (Optional set of thresholds or criteria used to grade or score the model's performance): `{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}`

You can also view the description of this command using the following command:

```
moonshot > add_recipe -h
```

Add a new recipe using the dataset that you have created in the previous section using the following command:

```
My new recipe' 'I am recipe description' "['category1','category2']" "['bbq-lite-age-ambiguous']" "['bertscore','bleuscore']" -p "['analogical-similarity','mmlu']" -t "['tag1','tag2']" -g "{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}" 
```

### View Recipe

Once created, you can view your recipe using `view_recipe`.

```
moonshot > view_recipe my-new-recipe
```
    
![recipe added](cli_images/add_recipe.png)

!!! note

    The ID of the recipe is created by slugifying the name. In this case, the ID of this recipe is `my-new-recipe`.


## Create a New Dataset

You can convert your raw dataset into Moonshot-compatible dataset using the following schema. Once you have created the new dataset, you can save the file in `moonshot-data/datasets` for Moonshot to access this dataset.

Use your favourite text editor and save the following json data in `moonshot-data/datasets/example-dataset.json`.

```python
{
    "name": "Fruits Dataset",
    "description":"Measures whether the model knows what is a fruit",
    "license": "MIT license",
    "reference": "",
    "examples": [
        {
            "input": "Is Lemon a Fruit? Answer Yes or No.",
            "target": "Yes."
        },
        {
            "input": "Is Apple a Fruit? Answer Yes or No.",
            "target": "Yes."
        },
        {
            "input": "Is Bak Choy a Fruit? Answer Yes or No.",
            "target": "No."
        },
        {
            "input": "Is Bak Kwa a Fruit? Answer Yes or No.",
            "target": "No."
        },
        {
            "input": "Is Dragonfruit a Fruit? Answer Yes or No.",
            "target": "Yes."
        },
        {
            "input": "Is Orange a Fruit? Answer Yes or No.",
            "target": "Yes."
        },
        {
            "input": "Is Coke Zero a Fruit? Answer Yes or No.",
            "target": "No."
        }
    ]
}
```

The name of the dataset is the unique identifier for the dataset. This will be used in the recipes.

!!! note

    You can also refer to [this Jupyter notebook example](https://github.com/aiverify-foundation/moonshot/blob/main/examples/jupyter-notebook/Tutorial%202%20-%20Basic%20Workflow%20-%20Add%20your%20own%20test.ipynb) for more details how a dataset can be created.



## Connecting Endpoints

In this section, we will be going through the steps required to create a connector endpoint.

Before we jump into executing tests and performing red teaming on LLMs, we have to first create a connector endpoint. This connector endpoint will help us to connect to a specific LLM.

For the following steps, they will be done in interactive mode in CLI. To activate interactive mode, enter:     
    
    python -m moonshot cli interactive

### Using an Existing Connector Endpoint

1. To view the connector endpoint available, enter:

        list_endpoints


You will see a list of available connector endpoints that we have created beforehand:
![list of endpoints](cli_images/endpoints.png)

2. If there is no connector endpoint for you here, you create your own connector endpoint [here](#creating-a-connector-endpoint). Otherwise, enter the following command to modify the connector endpoint you want to use (e.g., adding your own API key):

        update_endpoint -h

    You should see a help example:
    
        update_endpoint openai-gpt4 "[('name', 'my-special-openai-endpoint'), ('uri', 'my-uri-loc'), ('token', 'my-token-here'), ('params', {'hello': 'world'})]"

    Here, we are updating a connector endpoint with the ID `openai-gpt4`. The keys and values to be updated are tuples in a list (i.e. update the key `name` with the value`my-special-openai-endpoint`)

3. After you have used the `update_endpoint` command to update your connector endpoint. Enter the following command to view your updated connector endpoint:

        view_endpoint openai-gpt4

    ![endpoint updated](cli_images/update_endpoint.png)

### Creating a Connector Endpoint

1. Enter the following command to understand more on how to create a connector endpoint 

        add_endpoint -h

    You should see a help example:

        add_endpoint openai-connector 'OpenAI GPT3.5 Turbo 1106' MY_URI ADD_YOUR_TOKEN_HERE 1 2 'gpt-3.5-turbo-1106' "{'temperature': 0.5}"
        
    In this example, we are creating a connector endpoint for the `openai-connector` **connector type**:

    - Name of the Connector you want to use: `my-openai-connector`
    - Name of your new Connector Endpoint: `OpenAI GPT3.5 Turbo 1106`
    - Uri: `ADD_YOUR_TOKEN_HERE`
    - API token: `ADD_YOUR_TOKEN_HERE`
    - Max number of calls made to the endpoint per second: `1`
    - Max concurrency of the endpoint:`2`
    - Model of the endpoint you want to connect to `'gpt-3.5-turbo-1106'`
    - Other parameters that this endpoint may need:
        - Temperature: 0.5        


        To view the list of connector types, enter `list_connector_types`:
            ![list of connector types](cli_images/connector_types.png)


2. After you have used the `add_endpoint` command to create your endpoint, enter the following command to view your newly created connector endpoint:

        view_endpoint openai-gpt3-5-turbo-1106
    
    > **_NOTE:_** The ID (openai-gpt3-5-turbo-1106) of the connector endpoint is created by slugifying the name.

    ![endpoint connected](cli_images/endpoint_created.png)

# Run Red Teaming Sessions
In this section, we will be going through the steps required to run red teaming sessions.

To run a test, you will need:

- **Connector Endpoint** - a configuration file to connect to your desired LLM endpoint
- **Session** - a session allows users to perform manual and automated red teaming on the LLMs, and stores the prompts and responses to and fro.
- **Prompt** - a prompt that you will be sending to LLMs in manual red teaming/ a starting prompt to input in attack modules before sending to the LLMs

For the following steps, they will be done in interactive mode in CLI. To activate interactive mode, enter:
     
    python -m moonshot cli interactive

### Create a Connector Endpoint
If you have not already created a connector endpoint, check out the guide [here](connecting_endpoints.md).

### Create a Session
Once your connector endpoint is created, we can start creating our session for red teaming.

Every session must reside in a runner. Before we create a session, enter the following command to view a list of runners currently available by entering:

    list_runners

![list of runners](cli_images/runners.png)

There are two options to create a session: you can either use an existing runner, or create a new runner with a session. To better understand its usage, enter the following command:

    new_session -h

1. Use existing runner.
    - Example:

            new_session my-test-mrt -c add_previous_prompt -p mmlu

        - Runner ID: `my-test-mrt`
        - Context strategy: `add_previous_prompt`
        - Prompt template:  `mmlu`
    
    ![create session with existing runner](cli_images/create_session_existing_runner.png)

    > **_NOTE:_**  Context strategy and prompt template are optional and can be set later so you can omit the `-c -p` flags if you do not need them    


2. Create new runner.
    - Example: 
    
            new_session my-new-runner-test-mrt -e "['openai-gpt35-turbo','openai-gpt4']" -p phrase-relatedness

        
        - Runner ID: `my-new-runner-test-mrt`
        - Endpoint: `['openai-gpt35-turbo','openai-gpt4']`
        - Prompt template: `phrase-relatedness`

    ![create session with new runner](cli_images/create_session_new_runner.png)

Once you have a session created and activated, we can proceed with red teaming. There are two ways to perform red teaming:
manual red teaming and using attack modules to perform automated attacks. 

### Manual Red Teaming
From the previous section, you should have a session created and activated. For manual red teaming, you can start by typing something in the session and that prompt will be sent to all the LLMs in that session. 
    ![manual red teaming pt](cli_images/manual_red_teaming_pt.png)
> **_NOTE:_**  Anything entered in a session that is not a command will be considered a prompt and sent to the LLMs in that session! 

### Automated Red Teaming (Run Attack Modules)
We will use the same session from manual red teaming in this example. Enter the following command to find out more about running attack modules:

    run_attack_module -h

You should see a help example:

    run_attack_module charswap_attack "The grandpa and his son went to does not know how to use a phone?\na)Grandpa\nb)Son."

The fields are as follows for this example:

- Attack module ID:  `charswap_attack`
- Prompt: `The grandpa and his son went to does not know how to use a phone?\na)Grandpa\nb)Son.`
    
![automated red teaming](cli_images/automated_red_teaming.png)

Refer to this [section](#more-about-automated-red-teaming) for more information on automated red teaming

### Ending and Resuming a Session
End session - Once you are done with red teaming, you can close the session by entering: 

    end_session

View sessions -  You can view your sessions by entering: 

    list_sessions

Resume session - You can resume a session by entering:
    
    use_session <desired session id> 

where `<desired session id>` is an `id` in `list_sessions`. When you resume a session, the state of your previous red teaming attempts will be restored.

### Configurations in a Session

- These are the configurations you can set in a session:

    - Context strategy: a Python module that helps to add context to the current prompt (i.e. add in the previous five prompts sent.) 

        To use a context strategy:

            use_context_strategy <desired context strategy id> 

        You can use the following command to view the list of context strategies available:

            list_context_strategies

        The `<desired context strategy id>` should correspond to an `Id` in `list_context_strategies`.

        - It is also possible to set the number of previous prompts to use with a context strategy. For example, to add `8` previous prompts as context using the `add_previous_prompt`, use the command:

                use_context_strategy add_previous_prompt -n 8

        
        To clear a context strategy in a session, use:
        
            clear_context_strategy

    - Prompt template: a JSON file which contains static texts that is appended to every prompt before they are sent to the LLMs. 
        
        To use a prompt template:

            use_prompt_template <desired prompt template id>

        You can use the following command to view the list of prompt templates available:

            list_prompt_templates

        The `<desired prompt template id>` should correspond to an `Id` in `list_prompt_templates`.


        To clear a prompt template in a session, use:
        
            clear_prompt_template


### More About Automated Red Teaming
Currently, automated red teaming heavily relies on the attack module being used. We have created a class, AttackModule, which serves as the base class for creating custom attack modules within the Moonshot framework. This class provides a structure that red teamers can extend to implement their own adversarial attack strategies.

In the AttackModule class, we have simplified the process for red teamers by providing easy access to necessary components for red teaming, such as connector endpoints and a function to automatically wrap the prompt template and context strategy contents around the provided prompt.

The design is very free-form, thus it is entirely up to the attack module developers whether they want to use the functions we have prepared. For instance, they may choose not to use the context strategy and prompt template at all in the attack module, even though these may be set in the session.


# List of CLI Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| add_cookbook<br><sub>` add_cookbook 'My new cookbook' 'I am cookbook description' "['analogical-similarity','auto-categorisation']"`</sub> | Add a new cookbook. The 'name' argument will be slugified to create a unique identifier. | <table><tr><td>name (str)</td><td>Name of the new cookbook<br><sub>example:  `'My new cookbook'`</sub></td></tr><tr><td>description (str)</td><td>Description of the new cookbook<br><sub>example:  `I am cookbook description'`</sub></td></tr><tr><td>recipes (str)</td><td>List of recipes to be included in the new cookbook<br><sub>example:  `"['analogical-similarity','auto-categorisation']"`</sub></td></tr></table> |
| add_recipe<br><sub>` add_recipe 'My new recipe' 'I am recipe description' "['category1','category2']" "['bbq-lite-age-ambiguous']" "['bertscore','bleuscore']" -p "['analogical-similarity','mmlu']" -t "['tag1','tag2']" -g "{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}" `</sub> | Add a new recipe. The 'name' argument will be slugified to create a unique identifier. | <table><tr><td>name (str)</td><td>Name of the new recipe<br><sub>example:  `'My new recipe'` </sub></td></tr><tr><td>description (str)</td><td>Description of the new recipe<br><sub>example:  `'I am recipe description'`</sub></td></tr><tr><td>categories (str) </td><td>List of categories to be included in the new recipe (currently in string format). It will be converted into a list in the backend<br><sub>example:  `"['category1','category2']"`</sub></td></tr><tr><td>-t, --tags (str)</td><td>List of tags to be included in the new recipe<br><sub>example:  `"['tag1','tag2']"`</sub></td></tr><tr><td>datasets (str)</td><td>The dataset to be used<br><sub>example:  `"['bbq-lite-age-ambiguous']"`</sub></td></tr><tr><td>-p, --prompt_templates (str)</td><td>List of prompt templates to be included in the new recipe<br><sub>example:  `"['analogical-similarity','mmlu']"`</sub></td></tr><tr><td>metrics (str)</td><td>List of metrics to be included in the new recipe<br><sub>example:  `"['bertscore','bleuscore']"`</sub></td></tr><tr><td>-g, --grading_scale (str)</td><td>Dict of grading scale for the metric to be included in the new recipe<br><sub>example:  `"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}"`</sub></td></tr></table> |
| delete_cookbook<br><sub>` delete_cookbook my-new-cookbook`</sub> | Delete a cookbook. | <table><tr><td>cookbook (str)</td><td>Id of the cookbook<br><sub>example:  `my-new-cookbook`</sub></td></tr></table> |
| delete_dataset<br><sub>` delete_dataset bbq-lite-age-ambiguous`</sub> | Delete a dataset. | <table><tr><td>dataset (str)</td><td>Name of the dataset<br><sub>example:  `bbq-lite-age-ambiguous`</sub></td></tr></table> |
| delete_metric<br><sub>`delete_metric my-new-metric`</sub> | Delete a metric. | <table><tr><td>metric (str)</td><td>Name of the metric<br><sub>example: `my-new-metric`</sub></td></tr></table> |
| delete_recipe<br><sub>` delete_recipe my-new-recipe`</sub> | Delete a recipe. | <table><tr><td>recipe (str)</td><td>Id of the recipe<br><sub>example:  `my-new-recipe`</sub></td></tr></table> |
| delete_result<br><sub>` delete_result my-new-cookbook-runner`</sub> | Delete a result. | <table><tr><td>result (str)</td><td>Name of the result<br><sub>example:  `my-new-cookbook-runner`</sub></td></tr></table> |
| delete_runner<br><sub>` delete_runner my-new-cookbook-runner`</sub> | Delete a runner. | <table><tr><td>runner (str)</td><td>Name of the runner<br><sub>example:  `my-new-cookbook-runner`</sub></td></tr></table> |
| list_cookbooks<br><sub>` list_cookbooks -f "risk"`</sub> | List all cookbooks. | <table><tr><td>-f, --find (str)</td><td>Optional field to find cookbook(s) with keyword<br><sub>example:  `risk`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate cookbook(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_datasets<br><sub>` list_datasets -f "bbq"`</sub> | List all datasets. | <table><tr><td>-f, --find (str)</td><td>Optional field to find dataset(s) with keyword<br><sub>example:  `bbq`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate dataset(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_metrics<br><sub>` list_metrics -f "exact"`</sub> | List all metrics. | <table><tr><td>-f, --find (str)</td><td>Optional field to find metric(s) with keyword<br><sub>example:  `"exact"`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate metric(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_recipes<br><sub>` list_recipes -f "mmlu"`</sub> | List all recipes. | <table><tr><td>-f, --find (str)</td><td>Optional field to find recipe(s) with keyword<br><sub>example:  `mmlu`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate recipes(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_results<br><sub>` list_results -f "my-runner"`</sub> | List all results. | <table><tr><td>-f, --find (str)</td><td>Optional field to find result(s) with keyword<br><sub>example:  `my-runner`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate result(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_runners<br><sub>`list_runners`</sub> | List all runners. | - |
| list_runs<br><sub>` list_runs -f "my-run"`</sub> | List all runs. | <table><tr><td>-f, --find (str)</td><td>Optional field to find run(s) with keyword<br><sub>example:  `my-run` </sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate run(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| run_cookbook<br><sub>` run_cookbook "my new cookbook runner" "['chinese-safety-cookbook']" "['openai-gpt35-turbo']" -n 1 -r 1 -s "You are an intelligent AI" `</sub> | Run a cookbook. | <table><tr><td>name (str)</td><td>Name of cookbook runner<br><sub>example:  `"my new cookbook runner"`</sub></td></tr><tr><td>cookbooks (str)</td><td>List of cookbooks to run<br><sub>example:  `"['chinese-safety-cookbook']"`</sub></td></tr><tr><td>endpoints (str)</td><td>List of endpoints to run<br><sub>example:  `"['openai-gpt35-turbo']"`</sub></td></tr><tr><td>-n, --prompt_selection_percentage (int)</td><td>Percentage of prompts to run<br><sub>example:  `1`</sub></td></tr><tr><td>-r, --random_seed (int)</td><td>Random seed number<br><sub>example:  `1`</sub></td></tr><tr><td>-s, --system_prompt (str)</td><td>System Prompt to use<br><sub>example:  `"You are an intelligent AI"`</sub></td></tr><tr><td>-l, --runner_proc_module (str)</td><td>Runner processing module to use. Defaults to use the `benchmarking` module <br></td></tr><tr><td>-o, --result_proc_module (str)</td><td>Result processing module to use. Defaults to use the `benchmarking-result` module<br></td></tr></table> |
| run_recipe<br><sub>` run_recipe "my new recipe runner" "['bbq','mmlu']" "['openai-gpt35-turbo']" -n 1 -r 1 -s "You are an intelligent AI" `</sub> | Run a recipe. | <table><tr><td>name (str)</td><td>Name of recipe runner<br><sub>example:  `"my new recipe runner"`</sub></td></tr><tr><td>recipes (str)</td><td>List of recipes to run<br><sub>example:  `"['bbq','mmlu']"`</sub></td></tr><tr><td>endpoints (str)</td><td>List of endpoints to run<br><sub>example:  `"['openai-gpt35-turbo']"`</sub></td></tr><tr><td>-n, --prompt_selection_percentage (int)</td><td>Percentage of prompts to run<br><sub>example:  `1`</sub></td></tr><tr><td>-r, --random_seed (int)</td><td>Random seed number<br><sub>example:  `1`</sub></td></tr><tr><td>-s, --system_prompt (str)</td><td>System Prompt to use<br><sub>example:  `"You are an intelligent AI"`</sub></td></tr><tr><td>-l, --runner_proc_module (str)</td><td>Runner processing module to use. Defaults to use the `benchmarking` module <br></td></tr><tr><td>-o, --result_proc_module (str)</td><td>Result processing module to use. Defaults to use the `benchmarking-result` module<br></td></tr></table> |
| update_cookbook<br><sub>`update_cookbook my-new-cookbook "[('name', 'Updated Cookbook Name'), ('description', 'Updated description'), ('recipes', ['analogical-similarity'])]"`</sub> | Update a cookbook. | <table><tr><td>cookbook (str)</td><td>Id of the cookbook<br><sub>example:  ` my-new-cookbook`</sub></td></tr><tr><td>update_values (str)</td><td>Update cookbook key/value<br><sub>example:  ` "[('name', 'Updated Cookbook Name'), ('description', 'Updated description'), ('recipes', ['analogical-similarity'])]"`</sub></td></tr></table> |
| update_recipe<br><sub>`update_recipe my-new-recipe "[('name', 'Updated Recipe Name'), ('tags', ['fairness', 'bbq'])]"` </sub> | Update a recipe. | <table><tr><td>recipe (str)</td><td>Id of the recipe<br><sub>example:  `my-new-recipe`</sub></td></tr><tr><td>update_values (str)</td><td>Update recipe key/value<br><sub>example:  `"[('name', 'Updated Recipe Name'), ('tags', ['fairness', 'bbq'])]"`</sub></td></tr></table> |
| view_cookbook<br><sub>` view_cookbook my-new-cookbook`</sub> | View a cookbook. | <table><tr><td>cookbook (str)</td><td>Id of the cookbook<br><sub>example:  `my-new-cookbook`</sub></td></tr></table> |
| view_dataset<br><sub>` view_dataset bbq-lite-age-ambiguous`</sub> | View a dataset file. | <table><tr><td>dataset_filename (str)</td><td>Name of the dataset file<br><sub>example:  `bbq-lite-age-ambiguous`</sub></td></tr></table> |
| view_metric<br><sub>` view_metric my-new-metric`</sub> | View a metric file. | <table><tr><td>metric_filename (str)</td><td>Name of the metric file<br><sub>example:  `my-new-metric`</sub></td></tr></table> |
| view_recipe<br><sub>` view_recipe my-new-recipe`</sub> | View a recipe. | <table><tr><td>recipe (str)</td><td>Id of the recipe<br><sub>example:  `my-new-recipe`</sub></td></tr></table> |
| view_result<br><sub>` view_result my-new-cookbook-runner`</sub> | View a result file. | <table><tr><td>result_filename (str)</td><td>Name of the result file<br><sub>example:  `my-new-cookbook-runner`</sub></td></tr></table> |
| view_run<br><sub>` view_run my-new-cookbook-runner`</sub> | View a runner runs. | <table><tr><td>runner_id (str)</td><td>Name of the runner<br><sub>example:  `my-new-cookbook-runner`</sub></td></tr></table> |
| view_runner<br><sub>` view_runner my-new-cookbook-runner`</sub> | View a runner. | <table><tr><td>runner (str)</td><td>Name of the runner<br><sub>example:  `my-new-cookbook-runner`</sub></td></tr></table> |
| add_endpoint<br><sub>` add_endpoint openai-connector 'OpenAI GPT3.5 Turbo 1106' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "{'temperature': 0.5, 'model': 'gpt-3.5-turbo-1106'}"`</sub> | Add a new endpoint. The 'name' argument will be slugified to create a unique identifier. | <table><tr><td>connector_type (str)</td><td>Type of connection for the endpoint<br><sub>example:  `openai-connector`</sub></td></tr><tr><td>name (str)</td><td>Name of the new endpoint<br><sub>example:  `'OpenAI GPT3.5 Turbo 1106'`</sub></td></tr><tr><td>uri (str)</td><td>URI of the new endpoint<br><sub>example:  `MY_URI`</sub></td></tr><tr><td>token (str)</td><td>Token of the new endpoint<br><sub>example:  `ADD_YOUR_TOKEN_HERE`</sub></td></tr><tr><td>max_calls_per_second (int)</td><td>Max calls per second of the new endpoint<br><sub>example:  `1`</sub></td></tr><tr><td>max_concurrency (int)</td><td>Max concurrency of the new endpoint<br><sub>example:  `1`</sub></td></tr><tr><td>params (str)</td><td>Params of the new endpoint<br><sub>example:  `"{'temperature': 0.5, 'model': 'gpt-3.5-turbo-1106'}"`</sub></td></tr></table> |
| convert_dataset<br><sub>`  convert_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' '/path/to/your/file.csv'` </sub> | Convert your dataset. The 'name' argument will be slugified to create a unique identifier. | <table><tr><td>name (str)</td><td>Name of the new dataset</td></tr><tr><td>description (str)</td><td>Description of the new dataset</td></tr><tr><td>reference (str)</td><td>Reference of the new dataset</td></tr><tr><td>license (str)</td><td>License of the new dataset</td></tr><tr><td>csv_file_path (str)</td><td>Path to the your existing dataset</td></tr></table> |
| delete_endpoint<br><sub>` delete_endpoint openai-gpt4`</sub> | Delete an endpoint. | <table><tr><td>endpoint (str)</td><td>ID of the endpoint<br><sub>example:  `openai-gpt4`</sub></td></tr></table> |
| delete_prompt_template<br><sub>` delete_prompt_template squad-shifts`</sub> | Delete a prompt template. | <table><tr><td>prompt_template (str)</td><td>The ID of the prompt template to delete<br><sub>example:  `squad-shifts`</sub></td></tr></table> |
| download_dataset<br><sub>` download_dataset 'dataset-name' 'A brief description' 'http://reference.com' 'MIT' "{'dataset_name': 'cais/mmlu', 'dataset_config': 'college_biology', 'split': 'dev', 'input_col': ['question','choices'], 'target_col': 'answer'}"`</sub> | Download dataset from Hugging Face. The 'name' argument will be slugified to create a unique ID. | <table><tr><td>name (str)</td><td>Name of the new dataset</td></tr><tr><td>description (str)</td><td>Description of the new dataset</td></tr><tr><td>reference (str)</td><td>Reference of the new dataset</td></tr><tr><td>license (str)</td><td>License of the new dataset</td></tr><tr><td>params (str)</td><td>Params of the new dataset in dictionary format. For example:  `{'dataset_name': 'cais_mmlu', 'dataset_config': 'college_biology', 'split': 'test', 'input_col': ['questions','choices'], 'target_col': 'answer'}"`</td></tr></table> |
| delete_endpoint<br><sub>` delete_endpoint openai-gpt4`</sub> | Delete an endpoint. | <table><tr><td>endpoint (str)</td><td>ID of the endpoint<br><sub>example:  `openai-gpt4`</sub></td></tr></table>|
| list_connector_types<br><sub>` list_connector_types -f "openai"`</sub> | List all connector types. | <table><tr><td>-f, --find (str)</td><td>Optional field to find connector type(s) with keyword<br><sub>example:  `openai`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate connector type(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_endpoints<br><sub>` list_endpoints -f "gpt"`</sub> | List all endpoints. | <table><tr><td>-f, --find (str)</td><td>Optional field to find endpoint(s) with keyword<br><sub>example:  `gpt`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate endpoint(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_prompt_templates<br><sub>` list_prompt_templates -f "toxicity"`</sub> | List all prompt templates. | <table><tr><td>-f, --find (str)</td><td>Optional field to find prompt template(s) with keyword<br><sub>example:  `toxicity`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate prompt template(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| update_endpoint<br><sub>`  update_endpoint openai-gpt4 "[('name', 'my-special-openai-endpoint'), ('uri', 'my-uri-loc'), ('token', 'my-token-here')]"`</sub> | Update an endpoint. | <table><tr><td>endpoint (str)</td><td>ID of the endpoint. This field is not editable via CLI after creation.<br><sub>example:  `openai-gpt4`</sub></td></tr><tr><td>update_kwargs (str)</td><td>Update endpoint key/value<br><sub>example:  `"[('name', 'my-special-openai-endpoint'), ('uri', 'my-uri-loc'), ('token', 'my-token-here')]"`</sub></td></tr></table> |
| view_endpoint<br><sub>` view_endpoint openai-gpt4`</sub> | View an endpoint. | <table><tr><td>endpoint (str)</td><td>ID of the endpoint<br><sub>example:  `openai-gpt4`</sub></td></tr></table> |
| add_bookmark<br><sub>` add_bookmark openai-connector 2 my-bookmarked-prompt`</sub> | Bookmark a prompt. | <table><tr><td>endpoint (str)</td><td>Endpoint which the prompt was sent to.<br><sub>example:  `openai-connector`</sub></td></tr><tr><td>prompt_id (int)</td><td>ID of the prompt (the leftmost column)<br><sub>example:  `2`</sub></td></tr><tr><td>bookmark_name (str)</td><td>Name of the bookmark<br><sub>example:  `my-bookmarked-prompt`</sub></td></tr></table> |
| clear_context_strategy<br><sub>` clear_context_strategy`</sub> | Clear the context strategy set in a session.| - |
| clear_prompt_template<br><sub>` clear_prompt_template`</sub> | Clear the prompt_template set in a session.| - |
| delete_attack_module<br><sub>` delete_attack_module sample_attack_module`</sub> | Delete an attack module. | <table><tr><td>attack_module (str)</td><td>The ID of the attack module to delete<br><sub>example:  `sample_attack_module`</sub></td></tr></table> |
| delete_bookmark<br><sub>` delete_bookmark my_bookmarked_prompt`</sub> | Delete a bookmark. | <table><tr><td>bookmark_name (str)</td><td>Name of the bookmark<br><sub>example:  `my_bookmarked_prompt`</sub></td></tr></table> |
| delete_context_strategy<br><sub>` delete_context_strategy add_previous_prompt`</sub> | Delete a context strategy. | <table><tr><td>context_strategy (str)</td><td>The ID of the context strategy to delete<br><sub>example:  `add_previous_prompt`</sub></td></tr></table> |
| delete_session<br><sub>` delete_session my-test-runner`</sub> | Delete a session. | <table><tr><td>session (str)</td><td>The runner ID of the session to delete<br><sub>example:  `my-test-runner`</sub></td></tr></table> |
| end_session<br><sub>` end_session`</sub> | End the current red teaming session. | - |
| export_bookmarks<br><sub>` export_bookmarks "my_list_of_exported_bookmarks"`</sub> | Exports bookmarks as a JSON file | <table><tr><td>bookmark_list_name (str)</td><td>Name of the exported bookmarks JSON file you want to save as (without the .json extension)<br><sub>example:  `my_list_of_exported_bookmarks`</sub></td></tr></table> |
| list_attack_modules<br><sub>` list_attack_modules -f "text"`</sub> | List all attack modules. | <table><tr><td>-f, --find (str)</td><td>Optional field to find attack module(s) with keyword<br><sub>example:  `text`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate attack module(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_bookmarks<br><sub>` list_bookmarks -f my_bookmark`</sub> | List all bookmarks. | <table><tr><td>-f, --find (str)</td><td>Optional field to find bookmark(s) with keyword<br><sub>example:  `my_bookmark`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate bookmark(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_context_strategies<br><sub>` list_context_strategies -f "previous_prompt"`</sub> | List all context strategies. | <table><tr><td>-f, --find (str)</td><td>Optional field to find context strategies with keyword<br><sub>example:  `previous_prompt`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate context strategies(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| list_sessions<br><sub>` list_sessions -f "my-sessions"`</sub> | List all sessions. | <table><tr><td>-f, --find (str)</td><td>Optional field to find session(s) with keyword<br><sub>example:  `my-sessions`</sub></td></tr><tr><td>-p, --pagination (str)</td><td>Optional tuple to paginate session(s). E.g. (2,10) returns 2nd page with 10 items in each page.<br><sub>example:  `(2,10)`</sub></td></tr></table> |
| new_session<br><sub>`new_session my-runner -e "['openai-gpt4']" -c add_previous_prompt -p mmlu`</sub> | Creates a new red teaming session. | <table><tr><td>runner_id (str)</td><td>ID of the runner. Creates a new runner if runner does not exist.<br><sub>example:  `my-runner`</sub></td></tr><tr><td>-e, --endpoints (str)</td><td>List of endpoint(s) for the runner that is only compulsory for creating a new runner.<br><sub>example:  `"['openai-gpt4']"`</sub></td></tr><tr><td>-c, --context_strategy (str)</td><td>Name of the context_strategy to be used - indicate context strategy here if you wish to use with the selected attack.<br><sub>example:  `add_previous_prompt`</sub></td></tr><tr><td>-p, --prompt_template (str)</td><td>Name of the prompt template to be used - indicate prompt template here if you wish to use with the selected attack.<br><sub>example:  `mmlu`</sub></td></tr></table> |
| Automated red teaming<br><sub>` run_attack_module sample_attack_module "this is my prompt" -s "test system prompt" -m bleuscore`</sub> | Runs automated red teaming in the current session. | <table><tr><td>attack_module_id (str)</td><td>ID of the attack module.<br><sub>example:  `sample_attack_module`</sub></td></tr><tr><td>prompt (str)</td><td>Prompt to be used for the attack.<br><sub>example:  `"this is my prompt"`</sub></td></tr><tr><td>-s, --system_prompt (str)</td><td>System Prompt to be used for the attack. If not specified, the default system prompt will be used.<br><sub>example:  `"test system prompt"`</sub></td></tr><tr><td>-c, --context_strategy (str)</td><td>Name of the context strategy module to be used. If this is set, it will overwrite the context strategy set in the session while running this attack module.<br><sub>example:  `add_previous_prompt`</sub></td></tr><tr><td>-n, --cs_num_of_prev_prompts (str)</td><td>The number of previous prompts to use with the context strategy. If this is set, it will overwrite the number of previous prompts set in the session while running this attack module.<br><sub>example:  `5`</sub></td></tr><tr><td>-p, --prompt_template (str)</td><td>Name of the prompt template to be used. If this is set, it will overwrite the prompt template set in the session while running this attack module.<br><sub>example:  `mmlu`</sub></td></tr><tr><td>-m, --metric (str)</td><td>Name of the metric module to be used.<br><sub>example:  `bleuscore`</sub></td></tr><tr><td>-o, --optional_args (str)</td><td>Optional parameters to input into the red teaming module.<br><sub>example:  `"{'my_attack_module_custom_field': 1.0}"`</sub></td></tr></table> |
| show_prompts<br><sub>` show_prompts`</sub> | Show the prompts in the session. | - |
| use_bookmark<br><sub>` use_bookmark my_bookmark`</sub> | Use a bookmarked prompt. | <table><tr><td>bookmark_name (str)</td><td>Name of the bookmark<br><sub>example:  `my_bookmark`</sub></td></tr></table> |
| use_context_strategy<br><sub>` use_context_strategy my_strategy_one`</sub> | Use a context strategy. | <table><tr><td>context_strategy (str)</td><td>The ID of the context strategy to use<br><sub>example:  `my_strategy_one`</sub></td></tr><tr><td>-n, --num_of_prev_prompts (int)</td><td>The number of previous prompts to use with the context strategy<br><sub>example:  `6`</sub></td></tr></table> |
| use_prompt_template<br><sub>` use_prompt_template 'analogical-similarity'`</sub> | Use a prompt template. | <table><tr><td>prompt_template (str)</td><td>Name of the prompt template<br><sub>example:  `analogical-similarity`</sub></td></tr></table> |
| use_session<br><sub>` use_session 'my-runner'`</sub> | Use an existing red teaming session by specifying the runner ID. | <table><tr><td>runner_id (str)</td><td>The ID of the runner which contains the session you want to use.<br><sub>example:  `my-runner`</sub></td></tr></table> |
| view_bookmark<br><sub>` view_bookmark my_bookmarked_prompt`</sub> | View a bookmark. | <table><tr><td>bookmark_name (str)</td><td>Name of the bookmark you want to view<br><sub>example:  `my_bookmarked_prompt`</sub></td></tr></table> |




