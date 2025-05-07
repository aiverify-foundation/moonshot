# Connecting to LLMs

This page will guide you through setting up the connector endpoints. These endpoints will become available for testing. Moonshot comes with pre-configured connector endpoints of some popular model providers, you will need to provide your respective API key.

1. To set up your LLMs, click on the *model endpoints* icon on the sidebar, which will display the list of endpoints available for configuration

    ![List of Endpoints](./imgs/endpoint_1.png)

2. Provide the following information 
    - Select the endpoints and click ‘Edit Endpoint’ to add in the API key for any of these models you may wish to test. 

    - Click ‘Save’ to create/update the endpoint.

    ![Creating New Endpoints](./imgs/endpoint_2.png)

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `My GPT4`                                   |
    | **Connection Type** (Required) | Type of API to use. If you do not see the type that you need, see [How to build a custom connector](../../tutorial/contributor/create_connector.md)                           | `openai-connector`                          |
    | **URI**                 | URI to the endpoint to be tested                                                                                                    | `<left blank>`                              |
    | **Token**               | Your private API token                                                                                                              | `123myopenaicontoken456`                    |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | Certain connector types require extra parameters. e.g., for OpenAI connectors, you will need to specify the `model`. See [OpenAI docs](https://platform.openai.com/docs/models) | ```{ "timeout": 300, "allow_retries": true, "num_of_retries": 3, "temperature": 0.5, "model": "gpt-4" }``` |

    !!!note
        If you wish to test other LLMs or your own hosted LLM application, click on ‘Create New Endpoint’. You will be prompted for the endpoint information

        ![Selection of Endpoints](./imgs/endpoint_3.png)


3. Once the endpoints have been configured, you can do the following
    1. [Look through the relevant test cases](./choosing_relevant_tests.md)
    2. [Run a benchmark test run](./running_benchmarks.md)
    3. [Run a red teaming session](./running_red_teaming.md)


