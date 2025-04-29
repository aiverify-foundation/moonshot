# Connecting to LLMs

1. This page shows you the connector endpoints available for testing. Moonshot comes with pre-configured connector endpoints of some popular model providers, you will need to provide your respective API key

    - Click on ‘Edit’ to add in the API key for any of these models you may wish to test. 

    - If you wish to test other LLMs or your own hosted LLM application, click on ‘Create New Endpoint’. 

    ![List of Endpoints](./imgs/benchmarking(8).png)

2. Provide the following information and click ‘Save’ to create/update the endpoint. 

    ![Creating New Endpoints](./imgs/benchmarking(9).png)

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `My GPT4`                                   |
    | **Connection Type** (Required) | Type of API to use. If you do not see the type that you need, see [How to build a custom connector](../../tutorial/contributor/create_connector.md)                           | `openai-connector`                          |
    | **URI**                 | URI to the endpoint to be tested                                                                                                    | `<left blank>`                              |
    | **Token**               | Your private API token                                                                                                              | `123myopenaicontoken456`                    |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | Certain connector types require extra parameters. e.g., for OpenAI connectors, you will need to specify the `model`. See [OpenAI docs](https://platform.openai.com/docs/models) | ```{ "timeout": 300, "allow_retries": true, "num_of_retries": 3, "temperature": 0.5, "model": "gpt-4" }``` |



3. Select the endpoints to the AI models by checking their checkboxes. and click the next button to move onto the next step. 

    ![Selection of Endpoints](./imgs/selecting_endpoints(10).png)
