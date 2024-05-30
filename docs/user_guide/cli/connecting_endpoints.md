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
    
        update_endpoint openai-gpt4 "[('name', 'my-special-openai-endpoint'), ('uri', 'my-uri-loc'), ('token', 'my-token-here')]"

    Here, we are updating a connector endpoint with the ID `openai-gpt4`. The keys and values to be updated are tuples in a list (i.e. update the key `name` with the value`my-special-openai-endpoint`)

3. After you have used the `update_endpoint` command to update your connector endpoint. Enter the following command to view your updated connector endpoint:

        view_endpoint openai-gpt4

    ![endpoint updated](cli_images/update_endpoint.png)

### Creating a Connector Endpoint

1. Enter the following command to understand more on how to create a connector endpoint 

        add_endpoint -h

    You should see a help example:

        add_endpoint openai-connector 'my-openai-connector' myendpointuri mythisismysecretapitoken 2 10 "{'temperature': 0.5}"
        
    In this example, we are creating a connector endpoint for the `openai-connector` **connector type**:

    - Name of your endpoint connenctor (unique identifier): `my-openai-connector`
    - URI: `myendpointuri` (set this to a random string like `none` if it is not required by your connector endpoint)
    - API token: `thisismysecretapitoken`
    - Max number of calls made to the endpoint per second: `2`
    - Max concurrency of the endpoint:`10`
    - Other parameters that this endpoint may need:
        - Temperature: 0.5        

        To view the list of connector types, enter `list_connector_types`:
            ![list of connector types](cli_images/connector_types.png)


        > **_NOTE:_** If you do not see the connector type you want to use, refer to our guide in contributor_guide/create_connector.md to learn how to create your own connector type. 


2. After you have used the `add_endpoint` command to create your endpoint. Enter the following command to view your newly created connector endpoint:

        view_endpoint my-openai-connector
    
    > **_NOTE:_** The ID (my-openai-connector)of the connector endpoint is created by slugifying the name.

    ![endpoint connected](cli_images/endpoint_created.png)
