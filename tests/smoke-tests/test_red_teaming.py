import argparse
from moonshot.integrations.cli.redteam.attack_module import list_attack_modules
from moonshot.integrations.cli.redteam.context_strategy import list_context_strategies
from moonshot.integrations.cli.redteam.session import list_sessions
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

def perform_assertion_function_output(expected_output, returned_results, capsys):
    if returned_results:
        assert any(expected_output in returned_result.values() for returned_result in returned_results)
    else:
        captured = capsys.readouterr()
        if captured.out:
            assert captured.out.rstrip() == expected_output or expected_output in captured.out.rstrip()


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
                "CONNECTORS": f"{ut_data_dir}/connectors/",
                "IO_MODULES": f"{ut_data_dir}/io-modules/",
                "ATTACK_MODULES": f"{ut_data_dir}/attack-modules/",
                "CONTEXT_STRATEGY": f"{ut_data_dir}/context-strategy/",
                "COOKBOOKS": f"{ut_data_dir}/cookbooks/",
                "METRICS": f"{ut_data_dir}/metrics/",
                "PROMPT_TEMPLATES": f"{ut_data_dir}/prompt-templates/",
                "RECIPES": f"{ut_data_dir}/recipes/",
                "RESULTS": f"{ut_data_dir}/results/",
                "RUNNERS_MODULES": f"{ut_data_dir}/runner-modules/",
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
            f"{ut_sample_dir}/charswap_attack.py",
            f"{ut_data_dir}/attack-modules/charswap_attack.py",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/homoglyph_attack.py",
            f"{ut_data_dir}/attack-modules/homoglyph_attack.py",
        )        
        shutil.copyfile(
            f"{ut_sample_dir}/sample_attack_module.py",
            f"{ut_data_dir}/attack-modules/sample_attack_module.py",
        )        

        # Copy connector
        shutil.copyfile(
            f"{ut_sample_dir}/openai-connector.py",
            f"{ut_data_dir}/connectors/openai-connector.py",
        )        

        # Copy connector endpoint
        shutil.copyfile(
            f"{ut_sample_dir}/openai-gpt4.json",
            f"{ut_data_dir}/connectors-endpoints/openai-gpt4.json",
        )        
        shutil.copyfile(
            f"{ut_sample_dir}/openai-gpt35-turbo.json",
            f"{ut_data_dir}/connectors-endpoints/openai-gpt35-turbo.json",
        )        

        # Copy context strategy
        shutil.copyfile(
            f"{ut_sample_dir}/add_previous_prompt.py",
            f"{ut_data_dir}/context-strategy/add_previous_prompt.py",
        )        

        # Copy runner module
        shutil.copyfile(
            f"{ut_sample_dir}/redteaming.py",
            f"{ut_data_dir}/runner-modules/redteaming.py",
        )

        # Setup complete, proceed with tests
        yield

        redteaming_files = [
            f"{ut_data_dir}/cookbooks/chinese-safety-cookbook.json",
            f"{ut_data_dir}/recipes/bbq.json",
            f"{ut_data_dir}/recipes/arc.json",
            f"{ut_data_dir}/datasets/bbq-lite-age-ambiguous.json",
            f"{ut_data_dir}/metrics/bertscore.py",
            f"{ut_data_dir}/metrics/bleuscore.py",
            f"{ut_data_dir}/prompt-templates/analogical-similarity.json",
            f"{ut_data_dir}/prompt-templates/mmlu.json",
            f"{ut_data_dir}/attack-modules/charswap_attack.py",
            f"{ut_data_dir}/attack-modules/homoglyph_attack.py",
            f"{ut_data_dir}/attack-modules/sample_attack_module.py",
            f"{ut_data_dir}/connectors-endpoints/openai-gpt35-turbo.json",
            f"{ut_data_dir}/connectors-endpoints/openai-gpt4.json",
            f"{ut_data_dir}/connectors/openai-connector.py",
            f"{ut_data_dir}/runner-modules/redteaming.py",
        ]

        #files generated from unit tests
        redteaming_files.extend([
            f"{ut_data_dir}/databases/my-second-session.db",
            f"{ut_data_dir}/databases/my-unit-test-session.db",
            f"{ut_data_dir}/runners/my-second-session.json",
            f"{ut_data_dir}/runners/my-unit-test-session.json",
        ])

        for redteaming_file in redteaming_files:
            if os.path.exists(redteaming_file):
                os.remove(redteaming_file)

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
                "[Runner] Unable to load runner because the runner file does not exist.",
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
    
    # ------------------------------------------------------------------------------
    # Running of manual and automated red teaming (Commented out to not send the prompts. Uncomment to run tests.)
    # Add in your token in the connector endpoints to run the tests
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Create session and do manual red teaming
            (
                [f"new_session {test_session_id} -e \"['openai-gpt4']\" -c add_previous_prompt -p mmlu",
                 "hello"
                 ],
                "[Prompt 0]",
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

        ]
    )    
    def test_automated_red_teaming(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)