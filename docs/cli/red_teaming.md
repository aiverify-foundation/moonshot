# Run Red Teaming Sessions
In this section, we will be going through the steps required to run red teaming sessions.

To run a test, you will need:

- **Endpoint Connector** - a configuration file to connect to your desired LLM endpoint
- **Session** - a session allows users to perform manual and automated red teaming on the LLMs, and stores the prompts and responses to and fro.
- **Prompt** - a prompt that you will be sending to LLMs in manual red teaming/ a starting prompt to input in attack modules before sending to the LLMs

For the following steps, they will be done in interactive mode in CLI. To activate interactive mode, enter `python -m moonshot cli interactive`

### Create an Endpoint Connector
If you have not already created an endpoint connector, check out the guide [here](connecting_endpoints.md).

### Create a Session
Once your endpoint connector is created, we can start creating our session for red teaming.

Every session must reside in a runner. Before we create a session, we can view a list of runners currently available by entering `list_runners`:
    ![list of runners](cli_images/runners.png)

There are two options to create a session, we can either use an existing runner, or create a new runner with a session. You can enter `new_session -h` to better understand its usage.


1. Use existing runner. For example, to create a session with an existing runner with the following configurations:

    - Runner ID (`id` in `list_runners`):  `my-test-mrt`
    - Context strategy (`id` in `list_context_strategies`): `add_previous_prompt`
    - Prompt template (`id` in `list_prompt_templates`): `mmlu`
    
    The command would be `new_session my-test-mrt -c add_previous_prompt -p mmlu`.  You should see that your session is created:
    ![create session with existing runner](cli_images/create_session_existing_runner.png)


    > **_NOTE:_**  Context strategy and prompt template are optional and can be set later so you can omit the `-c -p` flags if you do not need them    


2. Create new runner. For example, to create a session with a new runner with the following configurations: 

    - Runner ID: `my-new-runner-test-mrt`
    - Endpoint: `openai-gpt35-turbo and openai-gpt4` (endpoint(s) is required when you create a new session)
    - Prompt template (`id` in `list_prompt_templates`): `phrase-relatedness`

    The command would be `new_session my-new-runner-test-mrt -e "['openai-gpt35-turbo','openai-gpt4']" -p phrase-relatedness`.

    ![create session with new runner](cli_images/create_session_new_runner.png)

Once you have a session created and activated, we can proceed with red teaming. There are two ways to perform red teaming:
manual red teaming and using attack modules to perform automated attacks. 

### Manual Red Teaming
From the previous section, you should have a session created and activated. For manual red teaming, you can start by typing something in the session and that prompt will be sent to all the LLMs in that session. 
    ![manual red teaming pt](cli_images/manual_red_teaming_pt.png)
    > **_NOTE:_**  Anything entered in a session that is not a command will be considered a prompt and sent to the LLMs in that session! 

### Run Attack Modules
We will use the same session from manual red teaming. Enter `run_attack_module -h` to better understand its usage. For example, to run an attack module with the following configuration:
    - Attack module ID (`Id` in `list_runners`):  `sample_attack_module`
    - Prompt: `Hello world`
    
    
