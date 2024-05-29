1. Change directory to the root directory of Moonshot.

2. Enter `python -m moonshot cli interactive`.

3. Create a new session with a new runner:
    - Enter `new_session -h` to see the required fields to create a session:
        - To run the help example, enter `new_session my-runner -e "['openai-gpt4']" -c add_previous_prompt -p mmlu`. You should see that your session is created:

            ![new session](images/create_session.png)

### Manual Red Teaming

Continuing from Step 3, you can type a prompt and it will be sent to the LLM:

![manual prompt](images/manual_prompt.png)

### Automated Red Teaming

Continuing from Step 3 or manual red teaming, you can choose to run an attack module to perform automated red teaming. Enter `run_attack_module -h` to see the required fields to run attack modules:
    
- To run the help example, enter `run_attack_module sample_attack_module "this is my prompt" -s "test system prompt" -c "add_previous_prompt" -p "mmlu" -m "bleuscore"`. You should see your prompt and response:
    
![run attack module](images/run_attack_module.png)

You can view more information on running red teaming [here](../../cli/red_teaming.md).    

