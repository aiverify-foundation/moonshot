import pytest
from io import StringIO 
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from moonshot.interfaces.cli.cli import CommandLineInterface 

@pytest.fixture
def cli():
    return CommandLineInterface()


def run_command(cli, command):
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli.onecmd_plus_hooks(command)
        return mock_stdout.getvalue()


def test_version(cli):
    # Test the "version" command
    result = run_command(cli, "version")
    assert "moonshot v" in result


def test_list_recipes(cli):
    # Test the "list_recipes" command
    result = run_command(cli, "list_recipes")
    assert "cbbq-lite-SES-disamb" in result


def test_list_cookbooks(cli):
    # Test the "list_cookbooks" command
    result = run_command(cli, "list_cookbooks")
    assert "cbbq-disamb-cookbook" in result


def test_list_runs(cli):
    # Test the "list_runs" command
    result = run_command(cli, "list_runs")
    assert "cookbook-testing-db" in result


def test_list_connection_type(cli):
    # Test the "list_connection_type" command
    result = run_command(cli, "list_connect_types")
    assert "hf-llama2-13b-gptq" in result


def test_add_cookbook(cli):
    # Test the "add_cookbook" command
    run_command(cli, "add_cookbook 'Cookbook Test' 'I am cookbook description created by PyTest' "
                +"\"['analogical-similarity','auto-categorisation']\""
                )
    result = run_command(cli, "list_cookbooks")
    assert "Cookbook Test" in result # Check if the cookbook name is in the result


def test_add_recipe(cli):
    # Test the "add_recipe" command
    result = run_command(cli, "add_recipe 'Recipe Test' 'I am recipe description created by PyTest' " 
                         + "\"['tag1','tag2']\""
                         + " bbq-lite-age-ambiguous "
                         + "\"['analogical-similarity','auto-categorisation'] \""
                         + "\"['bertscore','bleuscore']\""
                         )
    result = run_command(cli, "list_recipes")
    assert "Recipe Test" in result # Check if the recipe name is in the result


# TODO has an issue where the test cant pass as the table is hiding the connection name
def test_add_endpoint(cli):
    # Test the "add_endpoint" command
    result = run_command(cli, "add_endpoint pytest pytest https://www.api.com/myapi 1234 10 1 " "\"{'temperature': 0}\"")
    result = run_command(cli, "list_endpoints")
    assert "pytest" in result # Check if the endpoint name is in the result


def test_view_cookbook(cli):
    #Test the "view_cookbook" command
    result = run_command(cli, "view_cookbook bbq-lite-age-cookbook")
    assert "id: bbq-lite-age-ambiguous" in result # Check if the recipe id is in the result


#INFO commented out to save prompts
def test_run_cookbook(cli):
    #Test the "run_cookbook" command
    result = run_command(cli, "run_cookbook -n 1 ['bbq-lite-age-cookbook'] ['my-openai-gpt35']")
    assert "Results saved in moonshot/data/results/cookbook-" in result 


#INFO commented out to save prompts
def test_run_recipe(cli):
    #Test the "run_recipe" command
    result = run_command(cli, "run_recipe -n 1 ['bbq-lite-age-ambiguous','bbq-lite-age-disamb'] ['my-openai-gpt35']")
    assert "Results saved in moonshot/data/results/recipe-" in result 

def test_resume_run(cli):
    #Test the "resume_run" command
    result = run_command(cli, "resume_run cookbook-testing-db")
    assert "Results saved in moonshot/data/results/cookbook-testing-results.json" in result


def test_list_results(cli):
    # Test the "list_results" command
    result = run_command(cli, "list_results")
    assert "cookbook-testing-results" in result


def test_view_results(cli):
    #Test the "view_results" command
    result = run_command(cli, "view_results cookbook-testing-results")
    assert "bbq-lite-age-cookbook" in result ## Fixed result to match the test run


##commands in redteam category
def test_list_prompt_templates(cli):
    # Test the "list_prompt_templates" command
    result = run_command(cli, "list_prompt_templates")
    assert "analogical-similarity" in result #Randomly selected 1 prompt template from the list


def test_new_session(cli):
    # Test the "new_session" command
    result = run_command(cli, "new_session 'my_new_test_session' 'My new test session description' \"['my-openai-gpt35']\"")
    assert "Prepared Prompts" in result #This is to check that the table is created. 


def test_use_session(cli):
    # Test the "use_session" command
    #using the created session
    result = run_command(cli, "use_session my-new-test-session")
    assert "Prepared Prompts" in result #This is to check that the table is created. 


def test_list_session(cli):
    # Test the "list_session" command
    #using the created session
    result = run_command(cli, "list_sessions")
    assert "my-new-test-session" in result #Check if our previously created session is in. 


def test_use_prompt_template(cli):
    #Test the "use_prompt_template" command
    #Enter a created session
    run_command(cli, "use_session my-new-test-session")
    result = run_command(cli, "use_prompt_template 'analogical-similarity'")
    assert "Updated session: my-new-test-session. Prompt Template: analogical-similarity."


def test_use_context_strategy(cli):
    #Test the "use_context_strategy" command
    #Enter a created session
    run_command(cli, "use_session my-new-test-session")
    result = run_command(cli, "use_context_strategy context-example")
    assert "Updated session: my-new-test-session. Context Strategy: context-example."


def test_clear_prompt_template(cli):
    #Test the "clear_prompt_template" command
    #Enter a created session
    run_command(cli, "use_session my-new-test-session")
    result = run_command(cli, "clear_prompt_template")
    assert "Updated session: my-new-test-session. Prompt Template: ."


def test_clear_context_strategy(cli):
    #Test the "clear_context_strategy" command
    #Enter a created session
    run_command(cli, "use_session my-new-test-session")
    result = run_command(cli, "clear_context_strategy")
    assert "Updated session: my-new-test-session. Context Strategy: 0."


#End session has nothing to assert with :) 
#no list context strategy?


if __name__ == "__main__":
    # Run all the test cases using pytest
    pytest.main()
