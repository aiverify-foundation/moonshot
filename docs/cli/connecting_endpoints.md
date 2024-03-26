## Connecting Endpoints

Establish and save connections to the endpoints of the LLMs that you wish to evaluate. 

Moonshot currently provides easy connection to: OpenAI's GPT4 & GPT3.5, GPT2 and Llama2-13b-gptq on Hugging Face, and Anthropic's Claude2.

!!! important "Important"
    Please note that you will most likely need to supply your own API token/key to connect to the LLM endpoints.


To connect to these models, you simply need to create an endpoint configuration file under the directory `data/connectors-endpoints` and define the following fields in that file:



- **type**: The python module name of LLM that you would like to connect to. (It should be any ONE of the Python modules available at `data/connectors`) 
- **name**: The name of this endpoint (It should also be the name of this file)
- **uri**: The URI of the LLM endpoint. 
- **token**: Your API token/key to connect to the LLM endpoint.
- **max_calls_per_second**: The maximum number of API calls made to the LLM endpoint per second.
- **max_concurrency**: The maximum number of open concurrent connections to the LLM endpoint.
- **params**: The parameter(s) required to be sent to the LLM endpoint. (optional)
 
For example, if you wish to create an endpoint configuration file to connect to Claude 2, you can create a file named `my-anthropic-claude2.json` in `data/connectors-endpoints`. The contents of `my-anthropic-claude2.json` should look something like this:

    {
        "type": "claude2",
        "name": "my-anthropic-claude2",
        "uri": "<your_endpoint_url>",
        "token": "<your_api_token>",
        "max_calls_per_second": 100,
        "max_concurrency": 100,
        "params": {}
    }
💡**Quick Start:** If you have an OpenAI API key, simply edit the pre-configured endpoint at `my-openai-gpt35.json`, and you'll be able to start evaluating or red-teaming GPT3.5. 

**Connecting LLMs - CLI Commands**
```bash                                                          
list_connect_types    Get a list of available LLM connection types.
add_endpoint          Add a new endpoint.
list_endpoints        Get a list of configured LLM endpoints.
```
You can run `<command-name> --help` to better understand the usage of a command or view cli guide [here](../cli/cli_guide.md).
