# Connecting to LLMs

Using Moonshot, you can directly test some of the popular models [using the preconfigured endpoints](#using-a-pre-configured-endpoint) provided. If you don't see one for the model you want to test, you can easily [create your own endpoints](#creating-a-new-endpoint) using the connectors available. Moonshot currently provides connectors to these model providers:

| Connector | Description |  
|---|---|
| [amazon-bedrock-connector](connectors/amazon-bedrock-connector.py) | For models consumed through [AWS' Bedrock service](https://aws.amazon.com/bedrock/) |
| [azure-openai-connector](connectors/azure-openai-connector.py) | For models consumed through [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service) |
| [anthropic-connector](connectors/anthropic-connector.py) | For [Anthropic API](https://www.anthropic.com/api) |
| [huggingface-connector](connectors/huggingface-connector.py) | For [Hugging Face Inference Endpoints](https://huggingface.co/docs/inference-endpoints/index) |  
| [openai-connector](connectors/openai-connector.py) | For [OpenAI API](https://openai.com/api/) *Can also be used for [Ollama](https://ollama.com/) connections |  
| [together-connector](connectors/together-connector.py) | For [TogetherAI Severless API](https://www.together.ai/products#inference) |
| [google-gemini-connector](connectors/google-gemini-connector.py) | For [Google Gemini API](https://ai.google.dev/gemini-api/docs) |  

</br>

If you want to test custom models or applications not supported by the above connectors, you will need to create a new connector type. [Read: How to create a custom connector](https://aiverify-foundation.github.io/moonshot/tutorial/contributor/create_connector/)

</br>

> [!NOTE]
> Some benchmarking cookbooks and red teaming attack modules also require connection to a secondary model for llm-assisted evaluation. You will need to set up connections to these models on Moonshot by providing your API key to its preconfigured endpoint.
> </br></br> <i> E.g. If you intend to run the MLCommons AI Safety Benchmarks v0.5 cookbook, you’ll need to add your API key for the pre-configured Together Llama Guard 7B Assistant endpoint. </i>
> </br></br> For benchmarking, Moonshot will identify the additional endpoints you need to set up after you have selected the cookbooks you want to run.

[TODO: INSERT SCREENSHOT OF COOKBOOK PRECONDITION]


</br>

## Using a Pre-configured Endpoint

1. Find the pre-configured model endpoint that you want to set up. The full list of available endpoints can also be found [here](https://github.com/aiverify-foundation/moonshot-data/tree/main/connectors-endpoints). 

    - Click on ‘Edit’

    [TODO: INSERT SCREENSHOT OF MODEL ENDPOINT SELECTION PAGE WITH EDIT BUTTON HIGHLIGHTED]

    If you have not started any workflows, go to the Model Endpoints page and find the pre-configured model endpoint that you want to set up.

    -  Click on ‘Edit Endpoint’

    [TODO: INSERT SCREENSHOT OF MODEL ENDPOINTS PAGE WITH EDIT BUTTON HIGHLIGHTED]


2. Refer to the table below and provide the URI and/or Token as required.

    | Pre-configured Endpoint Name | URI | Token |
    |---|---|---|
    | Amazon Bedrock Endpoints <details><summary>View List</summary>  <ul> <li>Amazon Bedrock - AI21 Labs Jurassic-2 Mid `amazon-bedrock-ai21-labs-j2-mid-connector`</li> <li>Amazon Bedrock - AI21 Labs Jurassic-2 Ultra `amazon-bedrock-ai21-labs-j2-ultra-connector`</li> <li>Amazon Bedrock - AI21 Labs Jamba Instruct `amazon-bedrock-ai21-labs-jamba-instruct-connector`</li> <li>Amazon Bedrock - Titan Text G1 - Express `amazon-bedrock-amazon-titan-text-g1-express-connector`</li> <li>Amazon Bedrock - Titan Text G1 - Lite `amazon-bedrock-amazon-titan-text-g1-lite-connector`</li> <li>Amazon Bedrock - Anthropic Claude 3.5 Sonnet `amazon-bedrock-anthropic-claude-3-5-sonnet-connector`</li> <li>Amazon Bedrock - Anthropic Claude 3 Haiku `amazon-bedrock-anthropic-claude-3-haiku-connector`</li> <li>Amazon Bedrock - Anthropic Claude 3 Opus `amazon-bedrock-anthropic-claude-3-opus-connector`</li> <li>Amazon Bedrock - Anthropic Claude 3 Sonnet `amazon-bedrock-anthropic-claude-3-sonnet-connector`</li> <li>Amazon Bedrock - Cohere Command `amazon-bedrock-cohere-command-connector`</li> <li>Amazon Bedrock - Cohere Command Light `amazon-bedrock-cohere-command-light-connector`</li> <li>Amazon Bedrock - Cohere Command R+ `amazon-bedrock-cohere-command-r-connector`</li> <li>Amazon Bedrock - Llama 3.1 405B Instruct `amazon-bedrock-meta-llama-3-1-405b-instruct-connector`</li> <li>Amazon Bedrock - Llama 3.1 70B Instruct `amazon-bedrock-meta-llama-3-1-70b-instruct-connector`</li> <li>Amazon Bedrock - Llama 3.1 8B Instruct `amazon-bedrock-meta-llama-3-1-8b-instruct-connector`</li> <li>Amazon Bedrock - Llama 3 70B Instruct `amazon-bedrock-meta-llama-3-70b-instruct-connector`</li> <li>Amazon Bedrock - Llama 3 8B Instruct `amazon-bedrock-meta-llama-3-8b-instruct-connector`</li> <li>Amazon Bedrock - Mistral 7B Instruct `amazon-bedrock-mistral-ai-mistral-7b-instruct-connector`</li> <li>Amazon Bedrock - Mistral Large 2 `amazon-bedrock-mistral-ai-mistral-large-2-connector`</li> <li>Amazon Bedrock - Mistral Large `amazon-bedrock-mistral-ai-mistral-large-connector`</li> <li>Amazon Bedrock - Mixtral 8x7B Instruct `amazon-bedrock-mistral-ai-mixtral-8x7b-instruct-connector`</li> </ul> </details> | Leave this as the placeholder value `DEFAULT` for the URI to be automatically inferred based on your AWS environment setup. If you provide a `uri` of 8 characters or more, it'll be treated like specifying a boto3 `client.endpoint_url`. | It is recommended to enter a short placeholder e.g. 'NONE' and instead configure your AWS credentials via the environment - as standard for boto3 and AWS CLI. Else, you can also use your AWS Session token.  |
    | Azure OpenAI Endpoints <ul><li>Azure OpenAI Dall-E `azure-openai-dalle`</li><li>Azure OpenAI GPT4 Turbo Preview `azure-openai-gpt4-turbo-preview`</li><li>Azure OpenAI GPT4o `azure-openai-gpt4o`</li></ul> | Edit to replace with the model's Azure OpenAI Service endpoint. You can find the URL in the Azure model admin interface or [create a new resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal). </br> E.g. `https://abc123.openai.azure.com` | Edit to include your API key. You can find it in your Azure portal's API Management instance. |
    | Anthropic Endpoints <ul><li>Claude 2 `claude2-connector`</li></ul> | Leave as blank. | Enter your API key. You can find it in your [Anthropic account settings](https://console.anthropic.com/account/keys). |
    | FlagEval FlagJudge `flageval-flagjudge` | No edits needed. Use default URI provided. | No edits needed. Use default token provided. |
    | Google Gemini Endpoints <ul><li>`google-gemini-flash-15`</li><li>`google-gemini-pro-15`</li></ul> | Leave as blank | Your [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key). |
    | Hugging Face Endpoints <ul><li>HuggingFace GPT-2 `huggingface-gpt2`</li><li>HuggingFace Llama2 13B GPTQ `huggingface-llama2-13b-gptq`</li></ul> | Enter the model's [Hugging Face inference endpoint](https://huggingface.co/docs/inference-endpoints/index) URL. | Enter your Hugging Face user token. You can find it in your [Hugging Face account settings](https://huggingface.co/settings/tokens) |
    | OpenAI Endpoints <ul><li>LLM Judge - OpenAI GPT4 `llm-judge-openai-gpt4-annotator`</li><li>OpenAI Dall-E-2 `openai-dalle2`</li><li>OpenAI GPT35 Turbo 16k `openai-gpt35-turbo-16k`</li><li>OpenAI GPT35 Turbo `openai-gpt35-turbo`</li><li>OpenAI GPT4 `openai-gpt4`</li></ul> | Leave as blank. | Enter your API key. You can find it on the [OpenAI API key page](https://platform.openai.com/api-keys) |
    | Ollama Endpoints <ul><li>Ollama Llama3 `ollama-llama3`</li><li>Ollama Llama3.1 `ollama-llama31`</li></ul> | No edits needed if your Ollama is running on the default port 11434. | No edits needed. This is just a placeholder value. |
    | Together AI Endpoints <ul><li>Together Llama Guard 7B Assistant `together-llama-guard-7b-assistant`</li><li>Ollama Together Llama3 8B Chat HF `together-llama3-8b-chat-hf`</li></ul> | Leave as blank. | Enter your API key. You can find it in [Together AI settings page](https://api.together.ai/settings/api-keys) |


3. Click ‘Save’ to update the endpoint. 

[TODO: INSERT SCREENSHOT OF FILLED ENDPOINT PAGE WITH SAVE BUTTON HIGHLIGHTED]

4. If you have started a workflow, select the endpoints to the AI systems that you wish to run benchmarks on, and click the next button to proceed to the next step. 

> [!NOTE]
> You do not have to select connections to secondary models needed to run benchmarking cookbooks/ red teaming attack modules at this stage. Just ensure that their endpoints have been set up with the required URI and Token and let Moonshot handle the rest.


</br>

## Creating a New Endpoint

1. Click on 'Create New Endpoint'.

[TODO: INSERT SCREENSHOT OF MODEL ENDPOINT SELECTION PAGE WITH CREATE BUTTON HIGHLIGHTED]

If you have not started any workflows, go to the Model Endpoints page and then 'Create New Endpoint'

[TODO: INSERT SCREENSHOT OF MODEL ENDPOINTS PAGE WITH CREATE BUTTON HIGHLIGHTED]

2. Give this new endpoint a unique name for you to identify this new endpoint by. This name will be reflected in the report generated.

3. Select the connection type and refer to its respective section below for more info on its usage.

    <details>
    <summary>Amazon Bedrock</summary>

    The `amazon-bedrock-connector` in Moonshot allows you to create endpoints to models consumed through [Amazon Bedrock](https://aws.amazon.com/bedrock/), such as AI21 Labs, Cohere and Mistral. Before creating an endpoint on Moonshot, ensure that you have obtained access and the required AWS credentials to use the model on Bedrock.

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `Mistral Large on Bedrock`                                   |
    | **Connection Type** (Required) | Type of API to use. By selecting the Amazon Bedrock Connector, Moonshot will use the Bedrock Converse API. [More Details](https://github.com/aiverify-foundation/moonshot-data/blob/main/connectors/amazon-bedrock-connector.py)                            | `amazon-bedrock-connector`                          |
    | **URI**  (Required)               | URI to the endpoint to be tested. Give this a short placeholder value like `DEFAULT` for the URI to be automatically inferred based on your AWS environment setup. If you provide a URI of 8 characters or more, it'll be treated like specifying a boto3 `client.endpoint_url`.                                                                                                    | `DEFAULT` or `bedrock.ap-southeast-1.amazonaws.com`                              |
    | **Token** (Required)              | Your AWS Session token. It's recommended to leave this field as a short placeholder e.g. 'NONE' and instead configure your AWS credentials via the environment - as standard for boto3 and AWS CLI.  | `NONE` or `123myToken456`                    |
    | **Model** (Required)    | The Amazon Bedrock model ID. [Read: How to find the model ID](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html)| `mistral.mistral-large-2407-v1:0`                                         |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | The Amazon Bedrock connector allows the configuration of the following parameters. </br> - timeout: The number of seconds before a connection timeout. </br> - max_attempts: The number of times Moonshot should retry an interaction with the endpoint. </br> - temperature: The amount of randomness. | ``` "params": { "timeout": 300, "max_attempts": 3, "temperature": 0.5 } ``` |

    </details>


    <details>
    <summary>Azure OpenAI</summary>
    
    The `azure-openai-connector` in Moonshot allows you to create endpoints to models consumed through [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service), such as GPT-4, GPT-3.5-Turbo, and DALL-E, among others. Before creating an endpoint on Moonshot, ensure that you have obtained model access and the required API key for the model on Azure.

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `GPT4o on Azure`                                   |
    | **Connection Type** (Required) |                     | `azure-openai-connector`                          |
    | **URI**  (Required)               | The model's Azure OpenAI Service endpoint. You can find the URL in the Azure model admin interface or [create a new resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal). | `https://abc123.openai.azure.com`                              |
    | **Token** (Required)              | Your API key. You can find it in your Azure portal's API Management instance.              | `123myToken456`                    |
    | **Model** (Required)    | The model deployment name you defined in Azure. [See: Deploy a model on Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model)| `gpt-4o-12345`                                         |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | The Azure OpenAI connector allows the configuration of the following parameters. </br> - timeout: The number of seconds before a connection timeout. </br> - max_attempts: The number of times Moonshot should retry an interaction with the endpoint. </br> - temperature: The amount of randomness. | ``` "params": { "timeout": 300, "max_attempts": 3, "temperature": 0.5 } ``` |

    </details>


    <details>
    <summary>Anthropic</summary>
    
    The `anthropic-connector` in Moonshot allows you to create endpoints to models via the Anthropic API, such as their Claude series (Sonnet, Haiku, Opus). Before creating an endpoint on Moonshot, ensure that you have set up an Anthropic console account with API key to the model.

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `Claude 3.5 Sonnet`                                   |
    | **Connection Type** (Required) | Type of API to use. By selecting the Anthropic Connector, Moonshot will make the Anthropic API request.                            | `anthropic-connector`                          |
    | **URI**               | This field is not required for endpoints using Anthropic Connector. | `<leave as blank>`                              |
    | **Token** (Required)              | Your API key. You can find it in your [Anthropic account settings](https://console.anthropic.com/account/keys).              | `123myToken456`                    |
    | **Model** (Required)    | The Anthropic API model name. [Anthropic Models](https://docs.anthropic.com/en/docs/about-claude/models)| `claude-3-5-sonnet-20240620`                                         |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | The Azure OpenAI connector allows the configuration of the following parameters. </br> - timeout: The number of seconds before a connection timeout. </br> - max_attempts: The number of times Moonshot should retry an interaction with the endpoint. </br> - temperature: The amount of randomness. </br> - max_tokens_to_sample: The maximum number of tokens to generate before stopping. | ``` "params": { "timeout": 300, "max_attempts": 3, "temperature": 0.5, "max_tokens_to_sample": 300 } ``` |

    </details>


    <details>
    <summary>Hugging Face</summary>
    
    The `huggingface-connector` in Moonshot allows you to create endpoints to models hosted on [Hugging Face Inference Endpoints](https://huggingface.co/docs/inference-endpoints/index). Before creating an endpoint on Moonshot, ensure that you have built a Hugging Face Inference Endpoint for the model and a valid user token. <i>If you are deploying Hugging Face models locally, this connector will not work and you will need to create a new connector type. [Read: How to create a custom connector](https://aiverify-foundation.github.io/moonshot/tutorial/contributor/create_connector/)</i>

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `Hugging Face GPT2`                                   |
    | **Connection Type** (Required) | Type of API to use. By selecting the Hugging Face Connector, Moonshot will form the appropriate API to your inference endpoint based on the information you provide in the below fields.                            | `huggingface-connector`                          |
    | **URI** (Required)              | Enter the model's [Hugging Face inference endpoint](https://huggingface.co/docs/inference-endpoints/index) URL. | `NEED A SAMPLE`                              |
    | **Token** (Required)              |  Enter your Hugging Face user token. You can find it in your [Hugging Face account settings](https://huggingface.co/settings/tokens).              | `123myToken456`                    |
    | **Model**    | This field is not required for endpoints using the Hugging Face connector | `<leave as blank>`                                         |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | The Hugging Face connector allows the configuration of the following parameters. </br> - timeout: The number of seconds before a connection timeout. </br> - max_attempts: The number of times Moonshot should retry an interaction with the endpoint. </br> - temperature: The amount of randomness. </br> - max_tokens_to_sample: The maximum number of tokens to generate before stopping. | ``` "params": { "timeout": 300, "max_attempts": 3, "temperature": 0.5, "max_tokens_to_sample": 300 } ``` |

    </details>


    <details>
    <summary>OpenAI, OpenAI t2i, Ollama</summary>

    The `openai-connector` in Moonshot allows you to create endpoints to text generation models via the [OpenAI API](https://openai.com/api/) asynchronously. For text-to-image models like Dall-E, use `openai-t2i-connector` instead. As the API format needed to reach models deployed locally via [Ollama](https://ollama.com/) is the same, you can use the `openai-connector` to create endpoints to models on Ollama as well, even if they are not OpenAI models. Before creating an endpoint on Moonshot, ensure that you have a valid OpenAI API key, or a model running locally via Ollama.

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `GPT3.5 Turbo Turbo`                                   |
    | **Connection Type** (Required) | Type of API to use. By selecting the OpenAI Connector, Moonshot will form the appropriate API to OpenAI, or a local Ollama deployment.                          | `openai-connector` or  `openai-t2i-connector`                      |
    | **URI**              | This field is not needed for endpoints on OpenAI. If you are creating an endpoint for a model deployed via Ollama, enter the URI to the port Ollama is running on. | OpenAI: `<>` ; Ollama: `http://localhost:11434/v1/`                              |
    | **Token** (Required)              |  Enter your API key. You can find it on the [OpenAI API key page](https://platform.openai.com/api-keys).     OLLAMA NEED TOKEN?         | `123myToken456`                     |
    | **Model**    |  | `<leave as blank>`                                         |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | The OpenAI connector allows the configuration of the following parameters. </br> - timeout: The number of seconds before a connection timeout. </br> - max_attempts: The number of times Moonshot should retry an interaction with the endpoint. </br> - temperature: The amount of randomness. </br> - max_tokens_to_sample: The maximum number of tokens to generate before stopping. | ``` "params": { "timeout": 300, "max_attempts": 3, "temperature": 0.5, "max_tokens_to_sample": 300 } ``` |

    </details>


    ![TODO: TogetherAI, Google Gemini]


4. Click ‘Save’ to update the endpoint. 

![Creating New Endpoints](./imgs/benchmarking(9).png)

5. If you have started a workflow, select the endpoints to the AI systems that you wish to run benchmarks on, and click the next button to proceed to the next step. 

> [!NOTE]
> You do not have to select connections to secondary models needed to run benchmarking cookbooks/ red teaming attack modules at this stage. Just ensure that their endpoints have been set up with the required URI and Token and let Moonshot handle the rest.

