# Red Teaming

1. Click on ‘Discover new vulnerabilities’ to start a new red teaming session. 

    ![Homepage](./imgs/red_teaming_discover(16).png)

2. Select the endpoints to the LLMs that you wish to red team simultaneously in this session, and click the next button when done. <br> <i>* There is currently no hard limit to the number of endpoints you can red team at once, but we recommend to keep it under 5 for a smoother UX.</i>

    ![Choose Endpoints](./imgs/red_teaming_endpoints_selection(17).png)

3. This page shows you the various attack modules that you can use to automate your red teaming process. Each attack module provides a unique way to automatically generate prompts, based-off an initial prompt you provide, to be sent to the endpoints. Some of these attack modules require the connection to a helper model e.g., GPT4. 

    !!! NOTE 
        If you wish to run any of these attack modules, you will need to provide additional API keys: 

            1. Malicious Question Generator (Requires OpenAI’s GPT4) 

            2. Violent Durian (Requires OpenAI’s GPT4) 

        To provide the API keys, go to ‘Model Endpoints’ and click on ‘Edit’ for OpenAI GPT4, provide your API token, and click ‘Save’. (You don’t need to select OpenAI GPT4 in the red teaming session) 

    Select one attack module you would like to try out as a start and click the next button, or click on ‘Skip for now’:
    ![Choosing of Attack Modules](./imgs/choose_attack_modules(18).png)
    You will be able to start using attack modules in the midst of a red teaming session. 

4. Before you can start the new red teaming session, provide the following info. 

    |    Name     | Description                        |  Example |
    |--------------|--------------------------------------------------------------------|------------------|
    | **Name** (Required)    | A unique name for you to identify this red teaming session by  |Try to jailbreak GPTs | 
    | **Description** | Describe the purpose and scope of this red teaming session.   | Comparing GPT versions on resistance to various attack techniques  |

    ![Start New Red Teaming Session](./imgs/start_red_teaming(19).png)

5. Click ‘Start’ to create the new red teaming session. 

6.  This page shows Moonshot’s red teaming interface.  

    ![Red teaming Interface](./imgs/red_teaming_interface(20).png)


**Chat boxes and Layout**

Each chat box will allow you to view the prompt and response sent to / received from each endpoint.   

There are two layout options:   
1. Carousel (Default if you have >3 endpoints) and    
2. Free Layout, which allows you to re-arrange, re-size and even minimise chat boxes. 

**Sending Prompts**

Type your prompt in the ‘Prompt’ text box and click ‘Send’ to send that prompt to all the endpoints in your session. 
    ![Sending Prompts during red teaming](./imgs/red_teaming_chatbot_layout(21).png)


**Red Teaming Tools** 

You can use some of these tools to enhance your red teaming process: 

1. **Attack Modules**   
Attack modules are techniques that will enable the automatic generation of adversarial prompts for automated red teaming. Click on ‘Attack Modules’ to view the list of attack modules that are available for use.

    ![View Attack Modules](./imgs/red_teaming_attack_module(22).png)
    
    Click on ‘Use’ to select an attack module.

    ![Select Attack Modules](./imgs/select_attack_module(23).png)
    

    
    - Enter your prompt in the ‘Prompt’ box as the initial prompt that the attack module will use to generate adversarial prompts from. 
    
    - Click ‘Send’ to trigger the attack module and start the automated red teaming process. Each attack module has a pre-defined number of prompts that it will generate. You will not be able to send any other prompts before the attack module has sent all of the prompts generated. 

    ![Start Automated Red Teaming Process](./imgs/send_prompt(24).png)

    Click on 'X' to remove the attack module set.
    ![Remove Attack Module](./imgs/remove_attack_module(25).png)

    
1. **Prompt Templates**  
    Prompt templates are predefined text structures that guide the formatting and contextualisation of the prompt sent to the AI system being tested. Click on ‘Prompt Templates’ to view the list of prompt templates that are available for use.  
    ![List of Prompt Templates](./imgs/prompt_template(26).png)

    Click on 'Use' to select a prompt template.
    ![Select Prompt Templates](./imgs/select_prompt_template(27).png)

    Enter your prompt in the ‘Prompt’ box. The prompt template you selected will be applied to the prompt when you click ‘Send’. 
    ![Send Prompt](./imgs/prompt_template(28).png)

    Hover your mouse over each prompt to view its details. 
    ![View Prompt Details](./imgs/prompt_details(29).png)

    Click on ‘X’ to remove the prompt template set. 
    ![Remove Prompt Template](./imgs/remove_prompt_template_set(30).png)

2. **Context Strategies**  

    Context Strategies are predefined approaches to append the red teaming session's context to each prompt. Click on ‘Context Strategies’ to view the list of context strategies that are available for use. 
     
    ![List Context Strategies](./imgs/available_context_strategies(31).png)
    

    Click on ‘Use’ to select a context strategy. 
    ![Pick Context Strategy](./imgs/use_context_strategy(32).png)

    Enter your prompt in the ‘Prompt’ box. Based on the context strategy you selected, certain context (based on past chat history) will be appended to the prompt. 

    Click on ‘X’ to remove the context strategy set. 
    ![Remove Context Strategy](./imgs/remove_context_strategy_set(33).png)


**Ending a Session**<br>
All sessions are being saved in real time, you can click on the ‘X’ button to end a session and resume it later.   
![End Session](./imgs/ending_a_session(34).png)

Click on 'Exit'.  
![Exit Session](./imgs/exit_session(35).png)

**Resuming a Session**

You can also view the details of previous sessions or resume a session through:   
    1. Click on ‘history’ icon, then ‘View Past Sessions’   
    2. Click on ‘red teaming’ icon, then ‘View Past Sessions’  