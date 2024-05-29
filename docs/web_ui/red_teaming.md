# Red Teaming

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