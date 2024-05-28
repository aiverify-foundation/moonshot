# User Guide for Moonshot Web UI

## <b>Getting Started with Moonshot Web UI</b>

In this step-by-step tutorial, we will walk you through the key functionalities of Project Moonshot’s user-friendly web UI. 

Before starting on this tutorial, you should [Install and Set Up Moonshot Web UI](../getting_started/installation_ui.md) and have an understanding of [Moonshot’s key features](../../README.md#key-features). 

This tutorial will walk you through the UI’s guided workflow to: 

1. Choose tests relevant to your AI system 
2. Set up connection to your AI systems 
3. Run Benchmarks 
4. Conduct Red-Teaming 
  
After you have completed this tutorial, you can learn some of these more advanced functions: 

5. How to create custom cookbooks 

## <b>1. Choosing Relevant Tests</b>

1. Click on ‘Get Started’ 
    ![alt text](./imgs/get_started(1).png)

2. This page lists the cookbooks that Project Moonshot provides. Each cookbook contains tests of the same theme. Select the areas that are relevant to your use case. This is not final as you will be able to further curate the scope and scale of the tests in following steps.   
    [View full list of cookbook details]() 

    !!! note 
        Some of these cookbooks contain scoring metrics that require connection to specific models. 

        MLCommons AI Safety Benchmarks v0.5 (Requires an API key for accessing Llama Guard via Together AI) 

        Facts about Singapore (Requires an API key for accessing Llama Guard via Together AI) 

    [How to set up alternative connections]() 

3. When done, click on the next button. 
    ![alt text](./imgs/list_cookbooks(2).png) 

4. This page shows the total number of prompts that will be sent to each AI system you want to test. Click on ‘these cookbooks’ to see in greater detail what tests will be run. 
    ![alt text](./imgs/cookbook_recommendations(3).png) 

5. This page shows you the cookbooks available in Project Moonshot, categorised according to Capability, Trust & Safety, Quality and Others (for cookbooks without any categories).   

    You can click on ‘About’ for each cookbook to see what recipes it contains. 

    ![alt text](./imgs/benchmarking(4).png) 

    Check the ‘Run this cookbook’ checkbox if you wish to run any of the cookbooks. Click on ‘X’ to close the pop-up. 

    ![alt text](./imgs/benchmarking(5).png) 

    You can also unselect cookbooks if you do not wish to run them. 

    Click on ‘OK’ once you are satisfied with the cookbooks to be run. The total number of prompts to be sent should be updated. (There will be a step later on in the workflow for you to run a smaller number of prompts) 

    ![alt text](./imgs/benchmarking(6).png) 

    Click on the next button. 

    ![alt text](./imgs/benchmarking(7).png) 


## <b>2. Connecting AI Systems</b>

1. This page shows you the connector endpoints available to be tested. Project Moonshot comes with pre-configured connector endpoints to some popular model providers, you will just need to provide your API key.  

    - Click on ‘Edit’ to add in the API key for any of these models you may wish to test. 

    - If you wish to test other LLMs or your own hosted LLM application, click on ‘Create New Endpoint’. 

    ![alt text](./imgs/benchmarking(8).png)

2. Provide the following info as necessary, and click ‘Save’ to create/ update the endpoint. 

    ![alt text](./imgs/benchmarking(9).png)

    | Name                    | Description                                                                                                                         | Example                                     |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this new endpoint by                                                                              | `My GPT4`                                   |
    | **Connection Type** (Required) | Type of API to use. If you do not see the type that you need, see [How to build a custom connector](URL)                            | `openai-connector`                          |
    | **URI**                 | URI to the endpoint to be tested                                                                                                    | `<left blank>`                              |
    | **Token**               | Your private API token                                                                                                              | `123myopenaicontoken456`                    |
    | **Max Calls Per Second**| The maximum number of calls to be made to the endpoint per second                                                                   | `10`                                        |
    | **Max Concurrency**     | The maximum number of calls that can be made to the endpoint at any one time                                                        | `1`                                         |
    | **Other Parameters**    | Certain connector types require extra parameters. E.g., for OpenAI connectors, you will need to specify the `model`. See [OpenAI docs](https://platform.openai.com/docs/models) | `{ "timeout": 300, "allow_retries": true, "num_of_retries": 3, "temperature": 0.5, "model": "gpt-4" }` |



3. Select the endpoints to the AI systems that you wish to run benchmarks on, and click the next button when done. 

    !!! NOTE 
        If you wish to run any of these cookbooks, you will need to provide additional API keys: <br>
            1. MLCommons AI Safety Benchmarks v0.5, Facts about Singapore 




    Click on ‘Edit’ for Together Llama Guard 7B Assistant, provide your API token, and click ‘Save’.(You don’t need to select Together Llama Guard 7B Assistant for testing) 
    ![alt text](./imgs/selecting_endpoints(10).png)

## <b>3. Running Benchmarks</b>

1. Before you can start running benchmarks, provide the following info. These will be included in the report generated at the end of the run. 


    | Name        |Description   | Example          |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this benchmark run by| `GPT4 vs Claude on safety benchmarks`  |
    | **Description** | Describe the purpose and scopte of this benchmark run. | Comparing GPT4 and Claude to determine which model is safer as a chatbot |
    | **Run a smaller set** | The number of prompts per recipe to be run. Indicating 0 will run the full set. <br> <span style="font-size: 12px"><i>* Before running the full recommended set, you may want to run a smaller number of prompts from each recipe to do a sanity check.</i><span> | 5 |

2. Click ‘Run’ to start running the benchmarks. 

    ![alt text](./imgs/run_benchmark(11).png)

3. You can click on ‘See Details’ to recap on what is currently being run. 

    ![alt text](./imgs/view_run_details(12).png)

4. A report will be generated once the run is completed. Meanwhile, you can:

    - Start Red Teaming to discover new vulnerabilities   
    - Create a custom cookbook by curating your own set of recipes   
    - Go back to home  

5. To view the progress of the run, click on the bell icon, then select the specific benchmark run.

    ![alt text](./imgs/run_progress(13).png)

6. Once run is completed, you can click on ‘View Report’ 

    ![alt text](./imgs/view_report(14).png)

7. One report will be generated for each endpoint tested. Click on the dropdown to toggle the report displayed. You can also download the HTML report and the detailed results as a JSON file. 

    ![alt text](./imgs/download_report(15).png)

8. You can also view the details of previous runs through: 
    1. Click on ‘history’ icon, then ‘View Past Runs’ 
    2. Click on ‘benchmarking’ icon, then ‘View Past Runs’ 

## <b>4. Red-Teaming</b>

1. Click on ‘Discover new vulnerabilities, Start Red Teaming’ to start a new Red-Teaming session. 

    ![alt text](./imgs/red_teaming_discover(16).png)

2. Select the endpoints to the AI systems that you wish to Red-Team simultaneously in this session, and click the next button when done. <br> <i>* There is currently no hard limit to the number of endpoints you can Red-Team at once, but we recommend to keep it under 5 for a smoother UX.</i>

    ![alt text](./imgs/red_teaming_endpoints_selection(17).png)

3. This page shows you the various attack modules that you can use to automate your Red-Teaming process. Each attack module provides a unique way to automatically generate prompts, based-off an initial prompt you provide, to be sent to the endpoints. Some of these attack modules require the connection to a helper model E.g. GPT4. 

    Select one attack module you would like to try out as a start and click the next button, or click on ‘Skip for now’:
    ![alt text](./imgs/choose_attack_modules(18).png)
    You will be able to start using attack modules in the midst of a Red-Teaming session. 

4. Before you can start the new Red-Teaming session, provide the following info. 

    |    Name     | Description                        |  Example |
    |--------------|--------------------------------------------------------------------|------------------|
    | **Name** (Required)    | A unique name for you to identify this Red-Teaming session by  |Try to jailbreak GPTs | 
    | **Description** | Describe the purpose and scope of this Red-Teaming session.   | Comparing GPT versions on resistance to various attack techniques  |

    ![alt text](./imgs/start_red_teaming(19).png)

5. Click ‘Start’ to create the new Red-Teaming session. 

6. This page shows Project Moonshot’s Red-Teaming interface.  

    ![alt text](./imgs/red_teaming_interface(20).png)


**Chat boxes and Layout**

Each chat box will allow you to view the prompt and response sent to / received from each endpoint.   

There are two layout options:   
1. Carousel (Default if you have >3 endpoints) and    
2. Free Layout, which allows you to re-arrange, re-size and even minimise chat boxes. 

**Sending Prompts**

Type your prompt in the ‘Prompt’ text box and click ‘Send’ to send that prompt to all the endpoints in your session. 
    ![alt text](./imgs/red_teaming_chatbot_layout(21).png)


**Red-Teaming Tools** 

You can use some of these tools to enhance your Red-Teaming process: 

1. **Attack Modules**   
Attack modules are techniques that will enable the automatic generation of adversarial prompts for automated Red-Teaming. Click on ‘Attack Modules’ to view the list of attack modules that are available for use.
    ![alt text](./imgs/red_teaming_attack_module(22).png)
    Click on ‘Use’ to select an attack module.
    ![alt text](./imgs/select_attack_module(23).png)
    
    !!! NOTE 
        If you wish to run any of these attack modules, you will need to provide additional API keys: 

            1. Malicious Question Generator (Requires OpenAI’s GPT4) 

            2. Violent Durian (Requires OpenAI’s GPT4) 

        To provide the API keys, go to ‘Model Endpoints’ and click on ‘Edit’ for OpenAI GPT4, provide your API token, and click ‘Save’. (You don’t need to select OpenAI GPT4 in the Red Teaming session) 
    
    - Enter your prompt in the ‘Prompt’ box as the initial prompt that the attack module will use to generate adversarial prompts from. 
    - Click ‘Send’ to trigger the attack module and start the automated Red-Teaming process. Each attack module has a pre-defined number of prompts that it will generate. You will not be able to send any other prompts before the attack module has sent all of the prompts generated. 

    ![alt text](./imgs/send_prompt(24).png)

    Click on 'X' to remove the attack module set.
    ![alt text](./imgs/remove_attack_module(25).png)

    

2. **Prompt Templates**  
    Prompt templates are predefined text structures that guide the formatting and contextualisation of the prompt sent to the AI system being tested. Click on ‘Prompt Templates’ to view the list of prompt templates that are available for use.  
    ![alt text](./imgs/prompt_template(26).png)

    Click on 'Use' to select a prompt template.
    ![alt text](./imgs/select_prompt_template(27).png)

    Enter your prompt in the ‘Prompt’ box. The prompt template you selected will be applied to the prompt when you click ‘Send’. 
    ![alt text](./imgs/prompt_template(28).png)

    Hover your mouse over each prompt to view its details. 
    ![alt text](./imgs/prompt_details(29).png)

    Click on ‘X’ to remove the prompt template set. 
    ![alt text](./imgs/remove_prompt_template_set(30).png)

3. **Context Strategies**  
    Context Strategies are predefined approaches to append the Red-Teaming session's context to each prompt. Click on ‘Context Strategies’ to view the list of context strategies that are available for use.  
    ![alt text](./imgs/available_context_strategies(31).png)
    

    Click on ‘Use’ to select a context strategy. 
    ![alt text](./imgs/use_context_strategy(32).png)

    Enter your prompt in the ‘Prompt’ box. Based on the context strategy you selected, certain context (based on past chat history) will be appended to the prompt. 

    Click on ‘X’ to remove the context strategy set. 
    ![alt text](./imgs/remove_context_strategy_set(33).png)


**Ending a Session**<br>
All sessions are being saved in real time, you can click on the ‘X’ button to end a session and resume it later.   
![alt text](./imgs/ending_a_session(34).png)

Click on 'Exit'.  
![alt text](./imgs/exit_session(35).png)

**Resuming a Session**

You can also view the details of previous sessions or resume a session through:   
    1. Click on ‘history’ icon, then ‘View Past Sessions’   
    2. Click on ‘red teaming’ icon, then ‘View Past Sessions’   


## <b>5. Creating Custom Cookbooks</b>

Using the recipes available on Project Moonshot, you can easily curate custom cookbooks to suit your testing needs. 

1. Click on ‘Create cookbooks, Select Recipes &rarr;’  
    ![alt text](./imgs/create_custom_cookbook(36).png)

2. Provide the following information.

    |    Name     | Description                        |  Example |
    |--------------|--------------------------------------------------------------------|------------------|
    | **Name (Required)** | A unique name to identify this cookbook by. | My Custom Cookbook |
    | **Description** | Describe what the tests in this cookbook will cover. | This cookbook is designed to evaluate chatbots in capabilities that we expect it to excel in. |

    ![alt text](./imgs/select_recipe_for_cookbook(37).png)

3. Click on ‘Select Recipes’. 

4. Here you can view the list of recipes available in Moonshot. Select the recipes that you would like to include in your custom cookbook and click on ‘Add to Cookbook’. 

    ![alt text](./imgs/add_to_cookbook(38).png)

5. Click on ‘Create Cookbook’, then ‘View Cookbooks’ to view all the cookbooks that you now have in the tool. 

    ![alt text](./imgs/create_cookbook(39).png)

6. To run this cookbook, click on ‘Get Started’ 

    ![alt text](./imgs/get_started(1).png)