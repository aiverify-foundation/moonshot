from moonshot.integrations.cli.benchmark.datasets import list_datasets
from moonshot.integrations.cli.benchmark.metrics import list_metrics
from moonshot.integrations.cli.benchmark.result import list_results
from moonshot.integrations.cli.benchmark.run import list_runs
import pytest
from io import StringIO 
from unittest.mock import patch
from moonshot.integrations.cli.cli import CommandLineInterface
from moonshot.api import api_set_environment_variables
import shutil
import os
import argparse

from moonshot.integrations.cli.benchmark.recipe import list_recipes
from moonshot.integrations.cli.benchmark.cookbook import list_cookbooks

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
        assert captured.out.rstrip() == expected_output or expected_output in captured.out.rstrip()
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

class TestBenchmarkingCLI:
    @pytest.fixture(autouse=True)
    def init(self):
        # Set environment variables for result paths
        api_set_environment_variables(
            {
                "RUNNERS": f"{ut_data_dir}/runners/",
                "DATABASES": f"{ut_data_dir}/databases/",
                "DATABASES_MODULES": f"{ut_data_dir}/databases-modules/",
                "DATASETS": f"{ut_data_dir}/datasets/",
                "CONNECTORS": f"{ut_data_dir}/connectors/",
                "CONNECTORS_ENDPOINTS": f"{ut_data_dir}/connectors-endpoints/",
                "IO_MODULES": f"{ut_data_dir}/io-modules/",
                "ATTACK_MODULES": f"{ut_data_dir}/attack-modules/",
                "CONTEXT_STRATEGY": f"{ut_data_dir}/context-strategy/",
                "COOKBOOKS": f"{ut_data_dir}/cookbooks/",
                "METRICS": f"{ut_data_dir}/metrics/",
                "PROMPT_TEMPLATES": f"{ut_data_dir}/prompt-templates/",
                "RECIPES": f"{ut_data_dir}/recipes/",
                "RUNNERS": f"{ut_data_dir}/runners/",
                "RUNNERS_MODULES": f"{ut_data_dir}/runner-modules/",          
                "RESULTS_MODULES": f"{ut_data_dir}/results-modules/",
                "RESULTS": f"{ut_data_dir}/results/",
            }
        )

        # Copy cookbooks
        shutil.copyfile(
            f"{ut_sample_dir}/chinese-safety-cookbook.json",
            f"{ut_data_dir}/cookbooks/chinese-safety-cookbook.json",
        )

        shutil.copyfile(
            f"{ut_sample_dir}/tamil-language-cookbook.json",
            f"{ut_data_dir}/cookbooks/tamil-language-cookbook.json",
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
            f"{ut_sample_dir}/bbq-lite-age-disamb.json",
            f"{ut_data_dir}/datasets/bbq-lite-age-disamb.json",
        )
        shutil.copyfile(
            f"{ut_sample_dir}/bbq-lite-age-ambiguous.json",
            f"{ut_data_dir}/datasets/bbq-lite-age-ambiguous.json",
        )        
        shutil.copyfile(
            f"{ut_sample_dir}/arc-easy.json",
            f"{ut_data_dir}/datasets/arc-easy.json",
        )        
        shutil.copyfile(
            f"{ut_sample_dir}/arc-challenge.json",
            f"{ut_data_dir}/datasets/arc-challenge.json",    
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
        shutil.copyfile(
            f"{ut_sample_dir}/exactstrmatch.py",
            f"{ut_data_dir}/metrics/exactstrmatch.py",
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
        shutil.copyfile(
            f"{ut_sample_dir}/mcq-template.json",
            f"{ut_data_dir}/prompt-templates/mcq-template.json",
        )        

        # Copy attack modules
        shutil.copyfile(
            f"{ut_sample_dir}/charswap_attack.py",
            f"{ut_data_dir}/attack-modules/charswap_attack.py",
        )

        # Copy connector
        shutil.copyfile(
            f"{ut_sample_dir}/openai-connector.py",
            f"{ut_data_dir}/connectors/openai-connector.py",
        )    

        # # Copy connector endpoint
        # shutil.copyfile(
        #     f"{ut_sample_dir}/openai-gpt4.json",
        #     f"{ut_data_dir}/connectors-endpoints/openai-gpt4.json",
        # )        

        shutil.copyfile(
            f"{ut_sample_dir}/openai-gpt35-turbo.json",
            f"{ut_data_dir}/connectors-endpoints/openai-gpt35-turbo.json",
        )        

        # Copy runner module
        shutil.copyfile(
            f"{ut_sample_dir}/benchmarking.py",
            f"{ut_data_dir}/runner-modules/benchmarking.py",
        )

        # Copy results module
        shutil.copyfile(
            f"{ut_sample_dir}/benchmarking-result.py",
            f"{ut_data_dir}/results-modules/benchmarking-result.py",
        )        

        # Copy first sample runner
        shutil.copyfile(
            f"{ut_sample_dir}/my-new-recipe-runner.json",
            f"{ut_data_dir}/runners/my-new-recipe-runner.json",
        )
        
        shutil.copyfile(
            f"{ut_sample_dir}/my-new-recipe-runner.db",
            f"{ut_data_dir}/databases/my-new-recipe-runner.db",
        )

        # Copy first sample result
        shutil.copyfile(
            f"{ut_sample_dir}/my-new-recipe-runner-result.json",
            f"{ut_data_dir}/results/my-new-recipe-runner-result.json",
        )

        # Copy second sample result
        shutil.copyfile(
            f"{ut_sample_dir}/sample-result.json",
            f"{ut_data_dir}/results/sample-result.json",
        )

        # Setup complete, proceed with tests
        yield

        benchmarking_files = [
            f"{ut_data_dir}/cookbooks/chinese-safety-cookbook.json",
            f"{ut_data_dir}/recipes/bbq.json",
            f"{ut_data_dir}/recipes/arc.json",
            f"{ut_data_dir}/datasets/bbq-lite-age-disamb.json",
            f"{ut_data_dir}/datasets/bbq-lite-age-ambiguous.json",
            f"{ut_data_dir}/metrics/bertscore.py",
            f"{ut_data_dir}/metrics/bleuscore.py",
            f"{ut_data_dir}/prompt-templates/analogical-similarity.json",
            f"{ut_data_dir}/prompt-templates/mmlu.json",
            f"{ut_data_dir}/attack-modules/charswap_attack.py",
            f"{ut_data_dir}/connectors/openai-connector.py",
            # f"{ut_data_dir}/connectors-endpoints/openai-gpt4.json",
            f"{ut_data_dir}/connectors-endpoints/openai-gpt35-turbo.json",
            f"{ut_data_dir}/runner-modules/benchmarking.py",
            f"{ut_data_dir}/results-modules/benchmarking-result.py",
            f"{ut_data_dir}/datasets/arc-easy.json",
            f"{ut_data_dir}/metrics/exactstrmatch.py",
            f"{ut_data_dir}/prompt-templates/mcq-template.json",
            f"{ut_data_dir}/datasets/arc-challenge.json",
            f"{ut_data_dir}/runners/my-new-recipe-runner.json",
            f"{ut_data_dir}/databases/my-new-recipe-runner.db",
            f"{ut_data_dir}/runners/my-runner.json",
            f"{ut_data_dir}/databases/my-runner.db",
            f"{ut_data_dir}/results/my-new-recipe-runner-result.json",
            f"{ut_data_dir}/results/sample-result.json",
            f"{ut_data_dir}/cookbooks/tamil-language-cookbook.json",
        ]

        #files generated from unit tests
        benchmarking_files.extend([
            f"{ut_data_dir}/cookbooks/my-unit-test-cookbook.json",
            f"{ut_data_dir}/databases/my-new-cookbook.db",
            f"{ut_data_dir}/databases/my-new-recipe.db",
            f"{ut_data_dir}/databases/my-unit-test-cookbook.db",
            f"{ut_data_dir}/results/my-new-cookbook.json",
            f"{ut_data_dir}/results/my-unit-test-cookbook.json",
            f"{ut_data_dir}/results/my-unit-test-recipe.json",
            f"{ut_data_dir}/runners/my-new-cookbook.json",
            f"{ut_data_dir}/runners/my-unit-test-cookbook.json",
            f"{ut_data_dir}/runners/my-unit-test-recipe.json",
            f"{ut_data_dir}/recipes/my-unit-test-recipe.json",
        ])
        for benchmarking_file in benchmarking_files:
            if os.path.exists(benchmarking_file):
                os.remove(benchmarking_file)


    test_recipe_id = "my-unit-test-recipe"
    test_cookbook_id = "my-unit-test-cookbook"
    err_unrecognised_arg = "Error: unrecognized arguments"
    err_missing_required_arg = "Error: the following arguments are required"

    # ------------------------------------------------------------------------------
    # Running of recipes and cookbooks, and viewing the files generated (Commented out to not run the benchmarks. 
    # Uncomment to run tests. Add in your token in the connector endpoints to run the tests)
    # ------------------------------------------------------------------------------
    
    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Help example. 
            # Uncomment this to run the actual benchmarking test with your own token
            # Add in your own token also
            ([f"run_recipe {test_recipe_id} \"['arc']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\""],
             "Time taken to run"
            ),       
        ]
    )
    def test_run_recipe(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)

    @pytest.mark.parametrize(
        "command_list, expected_output",
        [
            # Success: Help example
            ([f"run_cookbook {test_cookbook_id} \"['chinese-safety-cookbook']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\""],
             "Time taken to run"
            ),

        ]
        )
    def test_run_cookbook(self, cli, command_list, expected_output, capsys):
        perform_assertion(cli, command_list, expected_output, capsys)