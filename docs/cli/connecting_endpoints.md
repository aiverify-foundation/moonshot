In this section, we will be going through the steps required to create an endpoint connector.

Before we jump into executing tests and performing red teaming on LLMs, we have to first create an endpoint connector. This endpoint connector will help us to connect to a specific LLM.

For the following steps, they will be done in interactive mode in CLI. To activate interactive mode, enter `python -m moonshot cli interactive`

### Using an Existing Endpoint Connector

1. To view the endpoint connectors available, enter `list_endpoints`. You will see a list of available endpoints that we have created beforehand:

    ![list of endpoints](cli_images/endpoints.png)

2. If there is no endpoint connector for you here, you create your own endpoint connector [here](#creating-an-endpoint-connector). Otherwise, enter `update_endpoint -h` to understand how to modify the endpoint connector you want to use (like adding your own API key):

    - Example: `update_endpoint openai-gpt4 "[('name', 'my-special-openai-endpoint'), ('uri', 'my-uri-loc'), ('token', 'my-token-here')]"`

        Here, we are updating an endpoint connector with the ID `open-gpt-4`. The keys and values to be updated are tuples in a list (i.e. update the `name` field to `my-special-openai-endpoint`)

3. Use the `update_endpoint` command to update your endpoint, then use the `view_endpoint` command to view your updated endpoint connector:

    ![endpoint updated](cli_images/update_endpoint.png)

### Creating an Endpoint Connector

1. To understand more about creating an endpoint connector, enter `add_endpoint -h`:
    - Example: `add_endpoint openai-connector 'my-openai-connector' myendpointuri mythisismysecretapitoken 2 10 "{'temperature': 0.5}"`. 
    
        To view the list of connector types, enter `list_connector_types`:
    ![list of connector types](cli_images/connector_types.png)
        
        In this example, we are creating an endpoint connector for the `openai-connector` **connector type**:

        - Name of your endpoint connenctor (unique identifier): `my-openai-connector`
        - URI: `myendpointuri` (can set this to a random string like `none` if it is not required by your endpoint connector)
        - API token: `thisismysecretapitoken`
        - Max number of calls made to the endpoint per second: `2`
        - Max concurrency of the endpoint:`10`
        - Other parameters that this endpoint may need:
            - Temperature: 0.5        

        > **_NOTE:_** If you do not see the connector type you want to use, refer to this TODO guide to learn how to create your own connector type. 


2. Use the `create_endpoint` command to create your endpoint, then use the `view_endpoint <YOUR ENDPOINT CONNECTOR ID>` command to view your newly created endpoint connector:
        > **_NOTE:_** The ID of the connector endpoint is created by slugifying the name.
    ![endpoint connected](cli_images/endpoint_created.png)
