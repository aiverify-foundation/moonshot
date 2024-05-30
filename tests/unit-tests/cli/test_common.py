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
                "CONTEXT_STRATEGY": f"{ut_data_dir}/context-strategy/",
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
            f"{ut_sample_dir}/charswap_attack.py",
            f"{ut_data_dir}/attack-modules/charswap_attack.py",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/homoglyph_attack.py",
            f"{ut_data_dir}/attack-modules/homoglyph_attack.py",
        )        

        # Setup complete, proceed with tests
        yield

        common_files = [
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
        ]

        #files generated from unit tests
        common_files.extend([
            f"{ut_data_dir}/connectors-endpoints/another-connector-endpoint.json",
            f"{ut_data_dir}/connectors-endpoints/my-connector-endpoint.json",
        ])


        for common_file in common_files:
            if os.path.exists(common_file):
                os.remove(common_file)

    test_session_id = "my-unit-test-session"
    test_attack_module_id = "my-unit-test-attack_module"
    test_context_strategy_id = "add_previous_prompt"
    test_prompt_template_id = "mmlu"
    err_unrecognised_arg = "Error: unrecognized arguments"
    err_missing_required_arg = "Error: the following arguments are required"
    err_invalid_int_value = "invalid int value"


    # ------------------------------------------------------------------------------
    # Creation of files
    # ------------------------------------------------------------------------------
    
    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
                 "\"{'temperature': 0.5, 'model': 'gpt-3.5-turbo-1106'}\""],
                f"Endpoint (my-connector-endpoint) created.",
            ),
            # Success: Add with empty parameters
            (
                [f"add_endpoint openai-connector 'another-connector-endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
                 "\"{}\""],
                f"Endpoint (another-connector-endpoint) created.",
            ),     
            # Failure: Add with malformed params dict (list)
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
                 "\"{['this should not', 'be a list']}\""],
                f"unhashable type: 'list'",
            ),       
            # Failure: Add with malformed params dict (string)
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
                 "\"{'xo'}\""],
                "1 validation error for api_create_endpoint",
            ),                          
            # Failure: Add with wrong parameter type for max_calls_per_second
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE x 1 "
                 "\"{}\""],
                err_invalid_int_value,
            ),              

            # Failure: Add with wrong parameter type for max_concurrency
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 x "
                 "\"{}\""],
                err_invalid_int_value,
            ),

            # # Failure: Add with wrong parameter type for connector_type
            # # TODO Validate connector_type
            # (
            #     [f"add_endpoint ['openai-connector'] 'another-connector-endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
            #      "\"{}\""],
            #     "",
            # ),

            # Failure: Add with missing required argument
            (
                [f"add_endpoint 'openai-connector' 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "],
                "Error: the following arguments are required: params",
            ),

            # Failure: Add with two missing required arguments
            (
                [f"add_endpoint 'openai-connector' 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 "],
                "Error: the following arguments are required: max_concurrency, params",
            ),
        ]
    )    
    def test_add_endpoint(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)

    # # ------------------------------------------------------------------------------
    # # Listing and viewing data
    # # ------------------------------------------------------------------------------
    # def test_list_connector_types(self, cli, command_list, expected_output, capsys):
    #     perform_assertion(cli, command_list, expected_output, capsys)

    # def test_list_endpoints(self, cli, command_list, expected_output, capsys):
    #     perform_assertion(cli, command_list, expected_output, capsys)

    # def test_list_prompt_templates(self, cli, command_list, expected_output, capsys):
    #     perform_assertion(cli, command_list, expected_output, capsys)

    # def test_view_endpoint(self, cli, command_list, expected_output, capsys):
    #     perform_assertion(cli, command_list, expected_output, capsys)
    

    # ------------------------------------------------------------------------------
    # Updating of files
    # ------------------------------------------------------------------------------ 

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Example
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
                 "\"{'temperature': 0.5, 'model': 'gpt-3.5-turbo-1106'}\"",
                 "update_endpoint my-connector-endpoint \"[('name', 'My Connector Endpoint Updated'), "
                 "('uri', 'updated uri'), ('token', 'my updated token')]\""],
                f"Endpoint updated.",
            ),
            # Success: Update non-existent key. If key is non-existent, it will not be updated but will not error out
            # as well
            (
                [f"add_endpoint openai-connector 'My Connector Endpoint' MY_URI ADD_YOUR_TOKEN_HERE 1 1 "
                 "\"{'temperature': 0.5, 'model': 'gpt-3.5-turbo-1106'}\"",
                 "update_endpoint my-connector-endpoint \"[('namex', 'My Connector Endpoint Updated')]\""],
                f"Endpoint updated.",
            ),            
            # Failure: Update non-existent endpoint
            (
                ["update_endpoint nope-endpoint \"[('name', 'My Connector Endpoint Updated'), "
                 "('uri', 'updated uri'), ('token', 'my updated token')]\""],
                f"Endpoint with ID 'nope-endpoint' does not exist",
            ),          
            # Failure: Update with missing required argument
            (
                ["update_endpoint nope-endpoint"],
                err_missing_required_arg,
            ),                
            # Failure: Update with malformed update_kwargs
            (
                ["update_endpoint nope-endpoint \"[('name', 'My Connector Endpoint Updated'), "
                 "('uri', 'updated uri'), {'token': 'my updated token'}]\""],
                "dictionary update sequence element #2 has length 1; 2 is required",
            ),
            # Failure: Update with malformed update_kwargs
            (
                ["update_endpoint nope-endpoint \"[('name', 'My Connector Endpoint Updated'), "
                 "('uri', 'updated uri'), {'token': 'my updated token'}]\""],
                "dictionary update sequence element #2 has length 1; 2 is required",
            ),            
        ]
    )    

    def test_update_endpoint(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)


    # # # ------------------------------------------------------------------------------
    # # # Deletion of files
    # # # ------------------------------------------------------------------------------
    # def test_delete_endpoint(self, cli, command_list, expected_output, capsys):
    #     perform_assertion(cli, command_list, expected_output, capsys)

    # def test_delete_prompt_template(self, cli, command_list, expected_output, capsys):
    #     perform_assertion(cli, command_list, expected_output, capsys)
