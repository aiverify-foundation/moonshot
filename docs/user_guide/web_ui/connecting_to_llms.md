# Connecting to LLMs

1. This page shows you the connector endpoints available to be tested. Moonshot comes with pre-configured connector endpoints to some popular model providers, you will just need to provide your API key.  

    - Click on ‘Edit’ to add in the API key for any of these models you may wish to test. 

    - If you wish to test other LLMs or your own hosted LLM application, click on ‘Create New Endpoint’. 

    ![List of Endpoints](./imgs/benchmarking(8).png)

2. Provide the following info as necessary, and click ‘Save’ to create/ update the endpoint. 

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



3. Select the endpoints to the AI systems that you wish to run benchmarks on, and click the next button when done. 


    Click on ‘Edit’ for Together Llama Guard 7B Assistant, provide your API token, and click ‘Save’. (You don’t need to select Together Llama Guard 7B Assistant for testing. This is necessary to run some of the cookbooks like MLCommon's AI Safety Benchmark.) 
    ![Selection of Endpoints](./imgs/selecting_endpoints(10).png)
