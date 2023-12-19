<div align="center">

```
  _____           _           _     __  __                       _           _   
 |  __ \         (_)         | |   |  \/  |                     | |         | |  
 | |__) | __ ___  _  ___  ___| |_  | \  / | ___   ___  _ __  ___| |__   ___ | |_ 
 |  ___/ '__/ _ \| |/ _ \/ __| __| | |\/| |/ _ \ / _ \| '_ \/ __| '_ \ / _ \| __|
 | |   | | | (_) | |  __/ (__| |_  | |  | | (_) | (_) | | | \__ \ | | | (_) | |_ 
 |_|   |_|  \___/| |\___|\___|\__| |_|  |_|\___/ \___/|_| |_|___/_| |_|\___/ \__|
                _/ |                                                             
               |__/                                                              

```
**Version 0.1.0**

A simple and modular tool to evaluate and red-team any LLM application.

[![Python 3.11](https://img.shields.io/badge/python-3.11-green)](https://www.python.org/downloads/release/python-3111/)


</div>

Moonshot is a tool designed for AI developers and security experts to evaluate and red-team any LLM/ LLM application. In this initial version, Moonshot can be used through its interative Command Line Interface, within python notebooks [(example)](examples/test-openai-gpt35.ipynb), or even seamlessly integrated into your model development workflow to to run repeatable tests.



## Getting Started
### Prerequisites
1. Python (at least version 3.11)

2. Virtual Environment (optional) - Good to have different environments to separate Python dependencies

    - Create a virtual environment:
    ```
    python -m venv venv
    ```
    - Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
### Installation
1. Download the source files by cloning this repository. i.e. Git clone (via SSH): 
    
    ```
    git clone git@github.com:moonshot-admin/moonshot.git
    ```
2. Change directory to project's root directory: 

    ```
    cd moonshot
    ```

3. Install the required packages: 

    ```
    pip install -r requirements.txt
    ```
4. Verify Moonshot is installed: 

    ```
    cd src
    ```
    Then, run moonshot: 
    ```
    python -m moonshot
    ```


## Usage
Two modes are available on the Moonshot CLI: Command-Based Mode and Interactive Mode. 
<details>

<summary>Full list of commands in Moonshot</summary>

``````
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
``````
</details>

### Command-based Mode

In the command-based mode, run commands by prepending `python -m moonshot`. For example,
- To list all the available commands: `python -m moonshot help`
- To list the connector types available: `python -m moonshot list_connect_types`

### Interactive Mode

We recommend the interactive mode for a more efficient experience, especially if you are using Moonshot to red-team. 

To enter interactive mode: `python -m moonshot interactive` (You should see the command prompt change to `moonshot >` ) For example,
- To list all the available commands: 
    ```
    moonshot > help
    ```
- To list the connector types available:
    ```
    moonshot > list_connect_types
    ```

### Connecting LLMs

Establish and save connections to the endpoints of the LLMs that you wish to evaluate. Moonshot currently provides easy connection to: OpenAI's GPT4 & GPT3.5, GPT2 and Llama2-13b-gptq on Hugging Face, and Anthropic's Claude2.

> [!IMPORTANT]
> Please note that you will most likely need to supply your own API token/key to connect to the LLM endpoints.

To connect to these models, you simply need to create an endpoint configuration file under the directory `data/llm-endpoints` and define the following fields in that file:



- **type**: The python module name of LLM that you would like to connect to. (It should be any ONE of the Python modules available at `data/llm-connection-types`) 
- **name**: The name of this endpoint (It should also be the name of this file)
- **uri**: The URI of the LLM endpoint. 
- **token**: Your API token/key to connect to the LLM endpoint.
- **max_calls_per_second**: The maximum number of API calls made to the LLM endpoint per second.
- **max_concurrency**: The maximum number of open concurrent connections to the LLM endpoint.
- **params**: The parameter(s) required to be sent to the LLM endpoint. (optional)
 
For example, if you wish to create an endpoint configuration file to connect to Claude 2, you can create a file named `my-anthropic-claude2.json` in `data/llm-endpoints`. The contents of `my-anthropic-claude2.json` should look something like this:

    ```       
    {
        "type": "claude2",
        "name": "my-anthropic-claude2",
        "uri": "<your_endpoint_url>",
        "token": "<your_api_token>",
        "max_calls_per_second": 100,
        "max_concurrency": 100,
        "params": {}
    }
    ```
💡**Quick Start:** If you have an OpenAI API key, simply edit the pre-configured endpoint at `my-openai-gpt35.json`, and you'll be able to start evaluating or red-teaming GPT3.5. 

**Connecting LLMs - Commands**
```bash                                                          
list_connect_types    Get a list of available LLM connection types.
add_endpoint          Add a new endpoint.
list_endpoints        Get a list of configured LLM endpoints.
```
You can run `<command-name> --help` to better understand the useage of a command.

### Running Evaluation Benchmarks

#### 🧑‍🍳 Moonshot Cookbooks & Recipes

Through analysis of the myriad of open-source benchmarking tasks, we have identified a common structure that encapsulates the essence of these tasks. 

![Cookbooks & Recipes](misc/cookbook-recipe.png)

- Benchmark Datasets: Consists of the prompts to be sent to the model and the expected target. (if any)
- Scoring Mechanism: The method to score the model response.
- Pre & Post Prompts: The **Prompt Template** of additional content to be appended to the prompts in the benchmark dataset before sending to the LLM.
- Recipe: Consists minimally of a benchmark dataset and the scoring mechnism(s) to be used to score it. (Prompt template is optional)
- Cookbook: A curated set of recipes to run. 


**To run a cookbook**
1. Activate **Interactive Mode**: `python -m moonshot interactive`
2. Run the help command for run_cookbook to better understand its usage.
    ```
    run_cookbook --help
    ```
    To run one prompt from the cookbook 'bbq-lite-age-cookbook' on the LLM endpoint 'my-openai-gpt35', enter:
    ```
    run_cookbook -n 1 "['bbq-lite-age-cookbook']" "['my-openai-gpt35']"
    ```
3. Results will be displayed as a table and stored in `src/moonshot/data/results/`
    
    ![Benchmark results](misc/benchmark-results.png)

**Running Evaluation Benchmarks - Commands**
```bash
list_cookbooks        Get a list of available cookbooks.
view_cookbook         View contents of a cookbook.
add_cookbook          Add a new cookbook.
run_cookbook          Run a cookbook.
list_prompt_templates List all prompt templates available.
list_recipes          Get a list of available recipes.
add_recipe            Add a new recipe.
run_recipe            Run a recipe.    
view_results          View a specific results file.
list_results          Get a list of available results.
list_runs             Get a list of available runs.
resume_run            Resume an interrupted run.
```
You can run `<command-name> --help` to better understand the useage of a command.


### Red Teaming 

To send custom prompts to LLM endpoint(s), you need to first create a **session**. In a **session**, you can send prompts to multiple LLM endpoints (each endpoint will have its own chat), utilise prompt templates, and context strategies. 

- **Session**: A group of *Chat(s)*, depending on the number of endpoint(s) defined in the session. A Session can utilise one *Prompt Template* and *Context Strategy* at any one time. Every chat in a session will inherit the Prompt Template and Context Strategy set for the session.
- **Endpoint**: The URI of the LLM API, where your prompts will be sent to.
- **Chat**: The history of prompts and replies with a specific endpoint. Each endpoint in a session has a chat.
- **Prompt Template**: Additional static information that is appended to your prompt to form the final prompt. The final prompt will be sent to the endpoint.
- **Context Strategy**: Information to be sent with your current prompt to give a context or background to the LLM. Currently, the context strategy availabile are past prompt(s) and response(s) in the same chat. It is defined as an integer *n*, where *n* is the number of past prompts and responses to append to the current prompt.

  

**Sending a Prompt to LLM Endpoint(s)**

1. Create a session
            
    There are 3 parameters (**name**,**description** and **list of endpoint(s)**) required when creating a session. In this example, we are creating a session with 1 endpoint:  
    ```
    new_session my_test_sess "this is a session description" '["my-openai-gpt35"]'
    ```

2. Configure a prompt template for this session **(optional)**

    - Once you have created a session, you can specify a prompt template to use for all the chats in this session. 

        ```
        use_prompt_template <name of prompt template> 
        ```

        - To see the list of prompt templates availabile:
            ```
            list_prompt_templates
            ```

3. Configure a context strategy for this session **(optional)**
    - You can also specify the context strategy for the current session.
        
        ```
        use_context_strategy <number of previous prompts>
        ```


4. Send the prompt to the endpoint by typing into the terminal directly (the following example has a prompt template and context strategy set to prepend to the prompt):
    
    - prompt template: `auto-categorisation` with the following contents: `For the following statement, provide a short word or phrase as the completion of the sentence:`
    - context strategy: `1` (`1` previous prompt and response used as the context for the current prompt)
    - current prompt: `the capital of cambodia is` 
    - results:
        
        ![Redteaming prompt](misc/red-teaming-prompt.png)

> [!TIP]
> You can view the current prompt template and context strategy set by referring to `PT` and `CS` respectively in the CLI.


**Red Teaming - Commands**
```bash
new_session            Add a new red teaming session.
list_sessions          List all available sessions.
use_session            Use an existing red teaming session.
end_session            End the current session.
list_prompt_templates  List all prompt templates available.
use_prompt_template    Use a prompt template.
use_context_strategy   Use a context strategy.
```
You can run `<command-name> --help` to better understand the useage of a command.


## Examples
In [this Jupyter notebook](examples/test-openai-gpt35.ipynb), we demonstrate how you can leverage on the Moonshot library to:
- Connect to OpenAI's GPT-3.5
- Create your own recipes and cookbooks
- Run benchmarks

## Contact
The Moonshot Team <<our.moonshot.team@gmail.com>>

## Acknowledgements

### Datasets used in Moonshot recipes
| Dataset       | Source           | License           |
| :-------------:|:-------------:| :-------------:|
|AdvGLUE|https://adversarialglue.github.io/|Creative Commons Attribution 4.0 International|
|Analogical Similarity|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/analogical_similarity |Apache License Version 2.0, January 2004  |
|AI2 Reasoning Challenge |https://allenai.org/data/arc|Creative Commons Attribution-ShareAlike 4.0 International|
|Auto Categorization |https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/auto_categorization|Apache License Version 2.0, January 2004|
|BBQ|https://github.com/nyu-mll/BBQ|Creative Commons Attribution 4.0 International| 
|BBQ-Lite|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/bbq_lite|Apache License Version 2.0, January 2004|
|Cause and Effect|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/cause_and_effect|Apache License Version 2.0, January 2004|
|Challenging Toxicity Prompts|https://decodingtrust.github.io/|Creative Commons Attribution ShareAlike 4.0 International|
|Contextual Parametric Knowledge|https://github.com/google-research/language|Apache License Version 2.0, January 2004|
|CoQA|https://stanfordnlp.github.io/coqa/|Creative Commons Attribution 4.0 International; MSR-LA;     Apache License Version 2.0, January 2004|
|Enron Email|https://github.com/ParakweetLabs/EmailIntentDataSet|Apache License Version 2.0, January 2004| 
|GRE Reading Comprehension|https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/gre_reading_comprehension|Apache License Version 2.0, January 2004|
|GSM8K|https://github.com/openai/grade-school-math|MIT License|
|HellaSwag|https://github.com/rowanz/hellaswag|MIT License|
|MMLU|https://github.com/hendrycks/test|MIT License|
|TR9856|https://aclanthology.org/P15-2069.pdf|Creative Commons Attribution 3.0 International|
|Winogrande|https://github.com/allenai/winogrande|Apache-2.0 License|
|WORD|https://aclanthology.org/L18-1408/|Creative Commons Attribution 3.0 International|
|Real Toxicity Prompts|https://github.com/allenai/real-toxicity-prompts/|Apache License Version 2.0, January 2004|
|Stanford Question Answering Dataset (SQuAD)|https://modestyachts.github.io/squadshifts-website/|Creative Commons Attribution 4.0 International|
|TruthfulQA|https://github.com/sylinrl/TruthfulQA|Apache License Version 2.0, January 2004|
|UCI Adult|https://archive.ics.uci.edu/dataset/2/adult|Creative Commons Attribution 4.0 International|

## License
Licensed under Apache Software License 2.0.