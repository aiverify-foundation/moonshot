# Walkthrough

Users can use this tool to run benchmark tests and perform red teaming on LLMs. Before doing these, we need to configure a LLM endpoint to connect to. Currently, these are the connectors we support out of the box for connectiong to LLMs:
    
| Connector Types | LLM Connector Name |
| --- | ----------- |
| OpenAI GPT4 |  `openai-gpt4`|
| OpenAI GPT3.5 Turbo 16k | `openai-gpt35-turbo-16k` |
| OpenAI GPT3.5 |`openai-gpt35` |
| Hugging Face Llama2 13B GPTQ | `hf-llama2-13b-gptq` |
| Anthropic Claude2    | `claude2` |
| OpenAI GPT2 (Hugging Face)    | `hf-gpt2` |

## Configuring Your Endpoints

If you see the Connector Types you wish to connect to in our list of supported connectors, good for you! You can simply configure the connector by referring to [sample-my-gpt4-config.json](#) by doing the following:
    
1. Make a copy of the sample JSON file in the same directory and rename the file to your liking. Let's say I want to connect to GPT4, and I have renamed the file to  ```my-gpt4-config.json ```.

2. Modify the contents of ```my-gpt4-config.json ```:
    ```
    {
        "id": "my-gpt4-config",
        "name": "my-gpt4-config",
        "connector_type": "openai-gpt4", 
        "uri": "", 
        "token": "my-api-token",
        "max_calls_per_second": 100,
        "max_concurrency": 100,
        "params": {
            "timeout": 234,
            "allow_retries": true,
            "num_of_retries": 3
        }
    }
    ```

If you do not see the connector for the LLM you want to connect to, fret not. You can refer to how we define our connectors [here](https://github.com/moonshot-admin/moonshot/tree/new_dev_main/moonshot/data/connectors) and create your own. You can simply make a copy of the Python in the same directory, modify the name of the class and the logic inside the file. 

When you have configured your connector, you can start doing your benchmark tests and red teaming!

## Running Benchmark Tests
To start running a benchmark, you will have to first select your Recipe or Cookbook. So what is a <b>Recipe</b> and a <b>Cookbook</b>? [Click on the links to find out more](/understanding_moonshot/introduction/).

<b>Recipe</b>: A file which contains the dataset(s), prompt template(s) and metric(s) to run for a benchmark. 

<b>Cookbook</b>: A file which contains a collection of <b>Recipes</b>

1. Select a Recipe/Cookbook to run 

2. Execute the Recipe/Cookbook

3. View results of the run


## Performing Red Teaming

To start red teaming, you will first have to create a <b>Session</b>. 

<b>Session</b>: A Session helps users to send prompts to multiple LLM endpoints. Each LLM endpoint will have a <b>Chat</b>, which stores the conversation between users and the LLM. 

1. Create/Resume a Session

2. Send a prompt

3. View the responses from the LLM

## Quick Start Guides
For more elaborate instruction, you can view our quick start guide.

[Getting Started with Library](/getting_started/quick_start_library)

[Getting Started with Web API](/getting_started/quick_start_web_api)
