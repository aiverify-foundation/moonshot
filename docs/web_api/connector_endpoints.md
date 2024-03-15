# Moonshot Connector API Endpoints

<details>
<summary> [GET] /v1/connectors</summary>
This endpoint is use to get all connectors.
<br/>
<b> Parameters (body)</b> : None
<br/>
<b>Success Response: </b>
```json
[
    "hf-llama2-13b-gptq",
    "openai-gpt4",
    "claude2",
    "openai-gpt35",
    "openai-gpt35-turbo-16k",
    "hf-gpt2"
]
```
</details>

<details>
<summary> [GET] /v1/llm_endpoints</summary>
This endpoint is use to get all endpoints.
<br/>
<b> Parameters (body)</b> : None
<br/>
<b>Success Response: </b>
```json
[
    {
        "id": "openaigpt35turbotest2",
        "connector_type": "openai-gpt35-turbo-16k",
        "name": "openaigpt35TurboTest2",
        "uri": "https://api.openai.com/v1/chat/completions",
        "token": "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",
        "max_calls_per_second": 10,
        "max_concurrency": 1,
        "params": {
            "temperature": 4
        }
    }
]
```
</details>

<details>
<summary>[POST] /v1/llm_endpoints</summary>
This endpoint is use to create new endpoints.
<br/>
<b> Parameters (body): </b>
```json
{
    "name": "string",
    "connector_type": "string",
    "uri": "string",
    "token": "string",
    "max_calls_per_second": "int",
    "max_concurrency": "int",
    "params": "dict"
}
``` 
<b>Example</b> 
<br/>
```json
{
  "name": "openaigpt35TurboTest2",
  "connector_type": "openai-gpt35-turbo-16k",
  "uri": "https://api.openai.com/v1/chat/completions",
  "token": "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",
  "max_calls_per_second": 10,
  "max_concurrency": 1,
  "params": {
    "temperature": 4
  }
}
```
<b>Success Response: </b>
```json
{
    "message": "Endpoint added successfully"
}
```
</details>


<details>
<summary>[DELETE] /v1/llm_endpoints/{llm_endpoint_id}</summary>
This endpoint is use to delete an existing endpoint.
<br/>
<b> Parameters (path)</b> :<code>llm_endpoint_id</code>: The ID of the LLM endpoint to delete.
<br/>
<b>Example: </b>  <code>/v1/llm_endpoints/openaigpt35TurboTest2</code>
<br/>
<b>Success Response: </b>
```json
{
    "message": "Endpoint deleted successfully"
}
```
</details>
