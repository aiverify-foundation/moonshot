import pytest
from io import StringIO 
from unittest.mock import patch
from moonshot.integrations.cli.cli import CommandLineInterface
from moonshot.api import api_set_environment_variables
import shutil
import os


@pytest.fixture
def cli():
    return CommandLineInterface()

def run_command(cli: CommandLineInterface, command_list: list = []):
    for command in command_list:
        cli.onecmd_plus_hooks(command)

def run_command_table(cli, command):
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli.onecmd_plus_hooks(command)
        return mock_stdout.getvalue()

def perform_assertion(cli, command_list, expected_output, capsys):
    run_command(cli, command_list)
    captured = capsys.readouterr()
    if captured.out:   
        assert expected_output in captured.out.rstrip()
    else:
        assert expected_output in captured.err.rstrip()

ut_data_dir = "tests/unit-tests/src/data"
ut_sample_dir = "tests/unit-tests/common/samples"    

class TestRedTeamingCLI:
    @pytest.fixture(autouse=True)
    def init(self):
        list_of_directories = ["attack-modules", "connectors-endpoints", "context-strategies", "cookbooks", 
                               "databases", "databases-modules", "datasets", "io-modules", "metrics",
                               "prompt-templates", "recipes", "runners"]
        
        for dir_name in list_of_directories:
            os.makedirs(f"{ut_data_dir}/{dir_name}/", exist_ok=True)

        # Set environment variables for result paths
        api_set_environment_variables(
            {
                "RUNNERS": f"{ut_data_dir}/runners/",
                "DATABASES": f"{ut_data_dir}/databases/",
                "DATABASES_MODULES": f"{ut_data_dir}/databases-modules/",
                "CONNECTORS_ENDPOINTS": f"{ut_data_dir}/connectors-endpoints/",
                "IO_MODULES": f"{ut_data_dir}/io-modules/",
                "ATTACK_MODULES": f"{ut_data_dir}/attack-modules/",
                "CONTEXT_STRATEGY": f"{ut_data_dir}/context-strategies/",
                "COOKBOOKS": f"{ut_data_dir}/cookbooks/",
                "METRICS": f"{ut_data_dir}/metrics/",
                "PROMPT_TEMPLATES": f"{ut_data_dir}/prompt-templates/",
                "RECIPES": f"{ut_data_dir}/recipes/",
            }
        )

        # Copy cookbooks
        shutil.copyfile(
            f"{ut_sample_dir}/chinese-safety-cookbook.json",
            f"{ut_data_dir}/cookbooks/chinese-safety-cookbook.json",
        )

        # Copy recipes
        shutil.copyfile(
            f"{ut_sample_dir}/bbq.json",
            f"{ut_data_dir}/recipes/bbq.json",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/arc.json",
            f"{ut_data_dir}/recipes/arc.json",
        )        

        # Copy dataset
        shutil.copyfile(
            f"{ut_sample_dir}/bbq-lite-age-ambiguous.json",
            f"{ut_data_dir}/datasets/bbq-lite-age-ambiguous.json",
        )

        # Copy metrics
        shutil.copyfile(
            f"{ut_sample_dir}/bertscore.py",
            f"{ut_data_dir}/metrics/bertscore.py",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/bleuscore.py",
            f"{ut_data_dir}/metrics/bleuscore.py",
        )

        # Copy prompt templates
        shutil.copyfile(
            f"{ut_sample_dir}/analogical-similarity.json",
            f"{ut_data_dir}/prompt-templates/analogical-similarity.json",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/mmlu.json",
            f"{ut_data_dir}/prompt-templates/mmlu.json",
        )

        # Copy attack modules
        shutil.copyfile(
            f"{ut_sample_dir}/charswap_attack_module.py",
            f"{ut_data_dir}/attack-modules/charswap_attack_module.py",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/homoglyph_attack_module.py",
            f"{ut_data_dir}/attack-modules/homoglyph_attack_module.py",
        )        

        # Setup complete, proceed with tests
        yield

        for dir_name in list_of_directories:
            if os.path.exists(f"{ut_data_dir}/{dir_name}"):
                shutil.rmtree(f"{ut_data_dir}/{dir_name}/")

    test_session_id = "my-unit-test-session"
    test_attack_module_id = "my-unit-test-attack_module"
    test_context_strategy_id = "add_previous_prompt"
    test_prompt_template_id = "mmlu"
    err_unrecognised_arg = "Error: unrecognized arguments"
    err_missing_required_arg = "Error: the following arguments are required"
    err_invalid_int_value = "invalid int value"


    # ------------------------------------------------------------------------------
    # Creation of session and configurations
    # ------------------------------------------------------------------------------
    
    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example (create new runner and session)
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu"],
                f"Using session: {test_session_id}",
            ),

            # # Success: Example (create new session with existing runner) TODO when runner is copied in
            # (
            #     f"new_session new-session -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
            #     f"Using session: {test_session_id}",
            # ),

            # Success: New session with missing optional arguments
            (
                ["end_session", f"new_session my-second-session -e \"['openai-gpt4']\""],
                f"Using session: my-second-session",
            ),

            # Failure: New session with missing requirements
            (
                ["end_session",f"new_session"],
                err_missing_required_arg,
            ),

            # Failure: New session and runner with non-existent connector
            (
                [f"new_session my-new-runner -e ['non-existent-connector'] -c add_previous_prompt -p mmlu"],
                "Connector endpoint non-existent-connector does not exist.",
            ),

            # Failure: New session and with non-existent runner
            (
                [f"new_session my-non-existent-runner -c add_previous_prompt -p mmlu"],
                "[Runner] Unable to create runner because the runner file does not exist.",
            ),

            # # Failure: New session and runner with non-existent prompt template
            ## test cases passes if establish connection to database is removed
            # (
            #     [f"new_session my-runner-two -e ['openai-gpt4'] -c add_previous_prompt -p nope-prompt-template"],
            #     "does not exist.",
            # ),
        ]
    )    
    def test_new_session(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
                 "end_session",
                 f"use_session {test_session_id}"],
                f"Using session: {test_session_id}",
            ),
            # Failure: Use existing runner with no session in the runner
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
                 "end_session",
                 f"use_session {test_session_id}"],
                f"Using session: {test_session_id}",
            ),            

            # Failure: Use non-existent runner
            (
                [ f"use_session my-non-existent-runner"],
                "[Runner] Unable to create runner because the runner file does not exist.",
            ),                        
            # Failure: Use session with unknown flags
            (
                 [f"use_session {test_session_id} -x o"],
                err_unrecognised_arg
            ), 

        ]
    )    
    def test_use_session(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
                 "end_session",
                 f"use_session {test_session_id}", f"use_context_strategy {test_context_strategy_id}"],
                 f"Updated session: {test_session_id}. Context Strategy: {test_context_strategy_id}.",
            ),
            # Success: Use context strategy with number of prompts
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 f"use_context_strategy {test_context_strategy_id} -n 10"],
                f"Updated session: {test_session_id}. Context Strategy: {test_context_strategy_id}.",
            ),            
            # Failure: Use non-existent context strategy TOFIX
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                f"use_context_strategy nope"],
                f"Context Strategy nope does not exist.",
            ),          
            # Failure: Use right context strategy with wrong type for number of prompts
            (
                [f"use_context_strategy {test_context_strategy_id} -n helloworld"],
                err_invalid_int_value,
            ),
            # Failure: Use context strategy with missing requirement argument
            (
                ["use_context_strategy"],
                err_missing_required_arg,
            ),                 
        ]
    )    
    def test_set_context_strategy(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)        

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 f"use_prompt_template {test_prompt_template_id}"],
                f"Updated session: {test_session_id}. Prompt Template: {test_prompt_template_id}.",
            ),
          
            # Failure: Use non-existent prompt template
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 f"use_prompt_template nope"],
                f"Prompt Template nope does not exist.",
            ),             
            # Failure: Use prompt template with missing requirement argument
            (
                ["use_prompt_template"],
                err_missing_required_arg,
            ),                 
        ]
    )    
    def test_set_prompt_template(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)        

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Default
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                "clear_context_strategy"],
                "Cleared context strategy.",
            ),
            # Success: With additional flags but they're expected to be ignored
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                "clear_context_strategy hello world"],
                "Cleared context strategy.",
            ),
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                "clear_context_strategy -x o"],
                "Cleared context strategy.",
            ),            
        ]
    )    
    def test_clear_context_strategy(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)    

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Default
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 f"clear_prompt_template"],
                "Cleared prompt template.",
            ),
          
            # Success: With additional flags but they're expected to be ignored
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "clear_prompt_template hello world"],
                "Cleared prompt template.",
            ),            
            # Failure: Use prompt template with missing requirement argument
            (
                ["use_prompt_template"],
                err_missing_required_arg,
            ),                 
        ]
    )    
    def test_clear_prompt_template(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)        

    # # ------------------------------------------------------------------------------
    # # Listing of files
    # # ------------------------------------------------------------------------------

    # #     def test_list_attack_modules(self, cli, command_list, expected_output, capsys):
    # #         pass

    # #     def list_context_strategies(self, cli, command_list, expected_output, capsys)::
    # #         pass

    # #     def list_sessions(self, cli, command_list, expected_output, capsys)::
    # #         pass


    
    # ------------------------------------------------------------------------------
    # Running of manual and automated red teaming (Commented out to not send the prompts. Uncomment to run tests.)
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Create session and do manual red teaming
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
                 "hello"
                 ],
                "[Prompt 0] took",
            ),

            # Success: Create session and recognise that it is a command instead of sending the prompt
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
                 f"clear_prompt_template"
                 ],
                "Cleared prompt template.",
            ),

        ]
    )    
    def test_manual_red_teaming(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "run_attack_module sample_attack_module \"this is my prompt\" "
                 "-s \"test system prompt\" -c \"add_previous_prompt\" -p \"mmlu\" -m \"bleuscore\""
                 ],
                "[Prompt 1] took",
            ),

            # Success: Run with missing optional arguments
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "run_attack_module sample_attack_module \"this is my prompt\" "
                 ],
                "[Prompt 1] took",
            ),

            # Failure: Run with missing required argument
            (
                 ["run_attack_module \"this is my prompt\" "],
                "the following arguments",
            ),       

            # Failure: Run with missing required argument
            (
                 ["run_attack_module"],
                err_missing_required_arg,
            ),       


            # Failure: Run with non-existent attack module
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "run_attack_module sample_attack_modulex \"this is my prompt\" "
                 "-s \"test system prompt\" -c \"add_previous_prompt\" -p \"mmlu\" -m \"bleuscore\""
                 ],
                "Unable to get defined attack module instance - sample_attack_modulex",
            ),       


            # Failure: Run with non-existent context strategy
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "run_attack_module sample_attack_module \"this is my prompt\" "
                 "-s \"test system prompt\" -c \"add_previous_promptx\" -p \"mmlu\" -m \"bleuscore\""
                 ],
                "Unable to get defined context strategy instance - add_previous_promptx",
            ),       

            # Failure: Run with non-existent prompt template
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "run_attack_module sample_attack_module \"this is my prompt\" "
                 "-s \"test system prompt\" -c \"add_previous_prompt\" -p \"mmlux\" -m \"bleuscore\""
                 ],
                "No prompt_templates found with ID: mmlux",
            ),       

            # Failure: Run with non-existent metric
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\"",
                 "run_attack_module sample_attack_module \"this is my prompt\" "
                 "-s \"test system prompt\" -c \"add_previous_prompt\" -p \"mmlu\" -m \"bleuscorex\""
                 ],
                "Unable to get defined metric instance - bleuscorex",
            ),       
        ]
    )    
    def test_automated_red_teaming(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)


    # # ------------------------------------------------------------------------------
    # # Deleting of files
    # # ------------------------------------------------------------------------------


    # #     def delete_attack_module(self, cli, command_list, expected_output, capsys):
    # #         pass

    # #     def delete_context_strategy(self, cli, command_list, expected_output, capsys)::
    # #         pass

    # #     def delete_session(self, cli, command_list, expected_output, capsys)::
    # #         pass