import pytest
from io import StringIO 
from unittest.mock import patch
import sys
import os
from moonshot.integrations.cli.cli import CommandLineInterface

@pytest.fixture
def cli():
    return CommandLineInterface()

def run_command(cli: CommandLineInterface, command: str):
    cli.onecmd_plus_hooks(command)

def run_command_table(cli, command):
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli.onecmd_plus_hooks(command)
        return mock_stdout.getvalue()

def perform_assertion(cli, command, expected_output, capsys, additional_command = ""):
    run_command(cli, command)
    if additional_command:
        print("additional commandz:", additional_command)
        run_command(cli, command)
    captured = capsys.readouterr()
    if captured.out:
        assert captured.out.rstrip() == expected_output or expected_output in captured.out.rstrip()
    else:
        assert expected_output in captured.err.rstrip()    


class TestBenchmarkingCLI:
    test_recipe_id = "my-unit-test-recipe"
    test_cookbook_id = "my-unit-test-cookbook"
    err_unrecognised_arg = "Error: unrecognized arguments"
    err_missing_required_arg = "Error: the following arguments are required"

    # ------------------------------------------------------------------------------
    # Creation of files
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: Add with missing optional args
            (
                "add_recipe 'My unit test recipe' "
                "'hello world description?!' "
                "\"['category1','category2']\" "
                "\"['bbq-lite-age-ambiguous']\" "
                "\"['bertscore','bleuscore']\" " 
                "-p \"['analogical-similarity','auto-categorisation']\" "
                "-t \"['tag1','tag2']\" ",
                f"[add_recipe]: Recipe ({test_recipe_id}) created."
            ),

            # Failure: Add with 1 missing required argument
            (
                "add_recipe 'My unit test recipe' "
                "'hello world description?!' "
                "\"['category1','category2']\" "
                "\"['bbq-lite-age-ambiguous']\" "
                "-p \"['analogical-similarity','auto-categorisation']\" "
                "-t \"['tag1','tag2']\" "
                "-a \"['charswap_attack_module']\" "
                "-g \"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}\" ",
                err_missing_required_arg
            ),

            # Failure: Add with missing required arguments
            (
                "add_recipe 'My unit test recipe' "
                "'hello world description?!' "
                "\"['category1','category2']\" "
                "-p \"['analogical-similarity','auto-categorisation']\" "
                "-t \"['tag1','tag2']\" "
                "-a \"['charswap_attack_module']\" "
                "-g \"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}\" ",
                err_missing_required_arg
            ),

            # Success: Help example
            (
                "add_recipe 'My unit test recipe' "
                "'hello world description?!' "
                "\"['category1','category2']\" "
                "\"['bbq-lite-age-ambiguous']\" "
                "\"['bertscore','bleuscore']\" " 
                "-p \"['analogical-similarity','auto-categorisation']\" "
                "-t \"['tag1','tag2']\" "
                "-a \"['charswap_attack_module']\" "
                "-g \"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}\" ",
                f"[add_recipe]: Recipe ({test_recipe_id}) created."
            ),

            # Failure: Add with incorrect parameter type for lists
            (
                "add_recipe 'My unit test recipe' "
                "'hello world description?!' "
                "\"['category1','category2']\" "
                "\"['bbq-lite-age-ambiguous']\" "
                "\"['bertscore','bleuscore']\" " 
                "-p \"['analogical-similarity','auto-categorisation']\" "
                "-t \"['tag1','tag2']\" "
                "-a \"'charswap_attack_module'\" "
                "-g \"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}\" ",
                "[add_recipe]: 1 validation error for RecipeArguments"              
            ),
            # Failure: Add with unknown flag           
            (
                "add_recipe 'My unit test recipe' "
                "'hello world description?!' "
                "\"['category1','category2']\" "
                "\"['bbq-lite-age-ambiguous']\" "
                "\"['bertscore','bleuscore']\" " 
                "-p \"['analogical-similarity','auto-categorisation']\" "
                "-t \"['tag1','tag2']\" "
                "-a \"['charswap_attack_module']\" "
                "-g \"{'A':[80,100],'B':[60,79],'C':[40,59],'D':[20,39],'E':[0,19]}\" "
                "-x o",
                err_unrecognised_arg
            ),
        ]
    )    
    def test_add_recipe(self, cli, command, expected_output,capsys):
        perform_assertion(cli, command, expected_output, capsys)

    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: Help example
            (
                "add_cookbook 'My unit test cookbook' 'hello world description?!' "
                "\"['analogical-similarity','auto-categorisation']\"",
                "[add_cookbook]: Cookbook (my-unit-test-cookbook) created."
            ),

            # Failure: Add with 1 missing required argument
            (
                "add_cookbook 'hello world description?!' \"['analogical-similarity','auto-categorisation']\"",
                err_missing_required_arg
            ),

            # Failure: Add with missing required arguments
            (
                "add_cookbook \"['analogical-similarity','auto-categorisation']\"",
                err_missing_required_arg
            ), 

            # Failure: Add with incorrect parameter type for list
            (
                "add_cookbook 'My unit test cookbook' 'hello world description?!' "
                "\"'this is not a list!!'\"",
                "[add_cookbook]: 1 validation error for CookbookArguments"
            ),   
            # Failure: Add with non-existent recipe
            (
                "add_cookbook 'My unit test cookbook' 'hello world description?!' "
                "\"['analogical-similarity','auto-categorisatison']\"",
                "recipe does not exist."
            ),

            # Failure: Add with unknown flag
            (
                "add_cookbook 'My unit test cookbook' 'hello world description?!' "
                "\"['analogical-similarity','auto-categorisation']\" -n 1",
                err_unrecognised_arg
            ),                                               
        ],
    )    
    def test_add_cookbook(self, cli, command, expected_output, capsys):
        perform_assertion(cli, command, expected_output, capsys)
 
    # ------------------------------------------------------------------------------
    # Listing and viewing data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: ID
            (f"view_recipe {test_recipe_id}", "id: my-unit-test-recipe"),

            # Success: description
            (f"view_recipe {test_recipe_id}", "hello world description?!"),

            # Success: tags
            (f"view_recipe {test_recipe_id}", "1. tag1"),
            (f"view_recipe {test_recipe_id}", "2. tag2"),

            # Success: categories
            (f"view_recipe {test_recipe_id}", "1. category1"),
            (f"view_recipe {test_recipe_id}", "2. category2"),

            # Success: grading scale
            (f"view_recipe {test_recipe_id}", "A [80 - 100]"),
            (f"view_recipe {test_recipe_id}", "B [60 - 79]"),
            (f"view_recipe {test_recipe_id}", "C [40 - 59]"),
            (f"view_recipe {test_recipe_id}", "D [20 - 39]"),
            (f"view_recipe {test_recipe_id}", "E [0 - 19]"),

            # Success: dataset
            (f"view_recipe {test_recipe_id}", "bbq-lite-age-ambiguous"),

            # # Success: prompt template
            # ("analogical-similarity"),
            # ("auto-categorisation"),

            # # Success: metric
            # ("bertscore"),
            # ("bleuscore"),

            # # Success: attack strategies
            # ("charswap_attack_module")

            # Failure: Test with unrecognised flag
            (f"view_recipe {test_recipe_id} -x o" , err_unrecognised_arg),

            # Failure: Test with non-existment recipe
            (f"view_recipe nope", "[view_recipe]: No recipes found with ID")
        ]
    )
    def test_view_recipe(self, cli, command, expected_output, capsys):
        perform_assertion(cli, command, expected_output, capsys)
    
    # def test_list_recipes(self, cli, command):
    # pass

    # def test_view_cookbook(self, cli):
    # pass

    # def test_list_cookbooks(self, cli):
    # pass

    # def test_view_dataset(self, cli):
    # pass

    # def test_list_datasets(self, cli):
    # pass

    # def test_view_metric(self, cli):
    # pass

    # def test_list_metrics(self, cli):
    # pass

    # ------------------------------------------------------------------------------
    # Updating of files
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: Help example update with missing optional arguments
            (f"update_recipe {test_recipe_id} \"[('name', 'My Updated Recipe'), ('tags', ['fairness', 'bbq'])]\"",
             "[update_recipe]: Recipe updated."
            ),

            # Success: Update every available key
            (f"update_recipe {test_recipe_id} \"[('name', 'My Updated Recipe2'), ('tags', ['updated tag']), "
             "('description', 'updated description'), ('categories', ['updated cat 1', 'updated cat 2']), "
             " ('dataset', 'updated dataset'), ('prompt_templates', ['updated pt 1', 'updated pt 2']), "
             " ('metrics', ['updated metric']), ('attack_modules', ['updated am 1', 'updated am 2']), "
             " ('grading_scale', {'New A':[75,100],'New B':[50,74],'New C':[25,49],'New D':[0,24]}) "
             "]\"",
             "[update_recipe]: Recipe updated."
            ),

            # Failure: Update with some wrong parameter types
            (f"update_recipe {test_recipe_id} \"[('name', ['Name should not be a list']), ('tags', ['updated tag']), "
             " ('description', 'updated description'), ('categories', ['updated cat 1', 'updated cat 2']), "
             " ('dataset', 'updated dataset'), ('prompt_templates', ['updated pt 1', 'updated pt 2']), "
             " ('metrics', ['updated metric']), ('attack_modules', ['updated am 1', 'updated am 2']), "
             " ('grading_scale', [{'New A':[75,100],'New B':[50,74],'New C':[25,49],'New D':[0,24]}]) "
             "]\"",
             "Failed to update recipe: Expected type for name is"
            ),

            # Failure: Update with missing required argument
            (f"update_recipe \"[('name', ['Name should not be a list']), ('tags', ['updated tag']), "
             " ('description', 'updated description'), ('categories', ['updated cat 1', 'updated cat 2']), "
             " ('dataset', 'updated dataset'), ('prompt_templates', ['updated pt 1', 'updated pt 2']), "
             " ('metrics', ['updated metric']), ('attack_modules', ['updated am 1', 'updated am 2']), "
             " ('grading_scale', [{'New A':[75,100],'New B':[50,74],'New C':[25,49],'New D':[0,24]}]) "
             "]\"",
             err_missing_required_arg
            ),             

            # Failure: Update with unknown flag
            (f"update_recipe {test_recipe_id} \"[('name', 'My Updated Recipe2'), ('tags', ['updated tag']), "
             "('description', 'updated description'), ('categories', ['updated cat 1', 'updated cat 2']), "
             " ('dataset', 'updated dataset'), ('prompt_templates', ['updated pt 1', 'updated pt 2']), "
             " ('metrics', ['updated metric']), ('attack_modules', ['updated am 1', 'updated am 2']), "
             " ('grading_scale', {'New A':[75,100],'New B':[50,74],'New C':[25,49],'New D':[0,24]}) "
             "]\" -x o",
             err_unrecognised_arg
            ),         

        ]
    )
    def test_update_recipe(self, cli, command, expected_output, capsys):
        perform_assertion(cli, command, expected_output, capsys)

    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: Help example
            (f"update_cookbook {test_cookbook_id} \"[('name', 'Updated cookbook name'), "
             "('description', 'Updated description'), ('recipes', ['analogical-similarity'])]\"",
             "[update_cookbook]: Cookbook updated."
            ),

            # Success: Update some keys
            (f"update_cookbook {test_cookbook_id} \"[('description', 'Updated cookbook description. again.')]\"",
             "[update_cookbook]: Cookbook updated."
            ),

            # Failure: Update with some wrong parameter types
            (f"update_cookbook {test_cookbook_id} \"[('name', ['Updated cookbook name']), "
             "('description', 'Updated description'), ('recipes', ['analogical-similarity'])]\"",
             "Failed to update cookbook: Expected type for name is"
            ),

            # Failure: Update with missing required argument
            (f"update_cookbook \"\"",
             err_missing_required_arg
            ),

            # # Failure: Update with unknown flag
            (f"update_cookbook {test_cookbook_id} \"[('name', 'Updated cookbook name'), "
             "('description', 'Updated description'), ('recipes', ['analogical-similarity'])]\" -x o",
             err_unrecognised_arg
            ),
        ]
    )
    def test_update_cookbook(self, cli, command, expected_output, capsys):
        perform_assertion(cli, command, expected_output, capsys)
    
    
    # ------------------------------------------------------------------------------
    # Running of recipes and cookbooks, and viewing the files generated
    # ------------------------------------------------------------------------------
    
    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: Help example
            (f"run_recipe {test_recipe_id} \"['bbq','auto-categorisation']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\"",
             "Time taken to run"
            ),

            # Failure: Run with non-existent recipes with new runner
            (f"run_recipe my_new_recipe \"['bbqx','auto-categorisationx']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\"",
             "No recipes found with ID"
            ),

            # Failure: Run with non-existent connector endpoint with new runner
            (f"run_recipe my_new_recipe_two \"['bbq','auto-categorisation']\" \"['openai-gpt35-turbox']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\"",
             "Connector endpoint openai-gpt35-turbox does not exist."
            ),

            # Failure: Run with wrong type for optional arguments (input string instead of int)
            (f"run_recipe my_new_recipe \"['bbqx','auto-categorisationx']\" \"['openai-gpt35-turbox']\" -n x -r s "
             "-s \"You are an intelligent AI\"",
             "invalid int value"
            ),

            # Failure: Run with unknown flag
            (f"run_recipe my_new_recipe \"['bbqx','auto-categorisationx']\" \"['openai-gpt35-turbox']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\" -x o",
             err_unrecognised_arg
            ),            
        ]
    )
    def test_run_recipe(self, cli, command, expected_output, capsys):
        perform_assertion(cli, command, expected_output, capsys)


    @pytest.mark.parametrize(
        "command, expected_output",
        [
            # Success: Help example
            (f"run_cookbook {test_cookbook_id} \"['chinese-safety-cookbook']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\"",
             "Time taken to run"
            ),

            # Failure: Run with non-existent cookbook
            (f"run_cookbook my_new_cookbook \"['chinese-safety-cookbookx']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\"",
             "No cookbooks found with ID"
            ),

            # Failure: Run with non-existent connector endpoint with new runner
            (f"run_cookbook my_new_cookbook_two \"['chinese-safety-cookbook']\" \"['openai-gpt35-turbox']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\"",
             "Connector endpoint openai-gpt35-turbox does not exist."
            ),


            # Failure: Run with wrong type for optional arguments (input string instead of int)
            (f"run_cookbook my_new_cookbook \"['chinese-safety-cookbook']\" \"['openai-gpt35-turbo']\" -n x -r s "
             "-s \"You are an intelligent AI\"",
             "invalid int value"
            ),

            # Failure: Run with unknown flag
            (f"run_cookbook my_new_cookbook\"['chinese-safety-cookbook']\" \"['openai-gpt35-turbo']\" -n 1 -r 1 "
             "-s \"You are an intelligent AI\" -x o",
             err_unrecognised_arg
            ),            
        ]
        )
    def test_run_cookbook(self, cli, command, expected_output, capsys):
        perform_assertion(cli, command, expected_output, capsys)

    #     def test_view_result(self, cli):
    #         pass

    #     def test_list_results(self, cli):
    #         pass

    #     def test_view_run(self, cli):
    #         pass

    #     def test_list_runs(self, cli):
    #         pass

    #     def test_view_runner(self, cli):
    #         pass
        
    #     def test_list_runners(self, cli):
    #         pass


    # ------------------------------------------------------------------------------
    # Deleting of files
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "command, additional_command, expected_output", 
        [   
            # # Success: Delete existing recipe TOFIX
            # (f"delete_recipe {test_recipe_id}", "y", "[delete_recipe]: Recipe deleted."),

            # Failure: Delete with missing argument
            (f"delete_recipe", "", err_missing_required_arg),

            # Failure: Delete with unknown flag
            (f"delete_recipe {test_recipe_id} -x o", "", err_unrecognised_arg),
        ]
    )
    def test_delete_recipe(self, cli, command, expected_output, capsys, additional_command):
        perform_assertion(cli, command, expected_output, capsys, additional_command)

    @pytest.mark.parametrize(
        "command, additional_command, expected_output", 
        [   
            # # Success: Delete existing cookbook TOFIX
            # (f"delete_cookbook {test_cookbook_id}", "y", "[delete_cookbook]: Cookbook deleted."),

            # Failure: Delete with missing argument
            (f"delete_cookbook", "", err_missing_required_arg),

            # Failure: Delete with unknown flag
            (f"delete_cookbook {test_cookbook_id} -x o", "", err_unrecognised_arg),
        ]
    )
    def test_delete_cookbook(self, cli, command, expected_output, capsys, additional_command):
        perform_assertion(cli, command, expected_output, capsys, additional_command)

    # def test_delete_dataset(self, cli):
    #     pass

    # def test_delete_metrics(self, cli):
    #     pass    

    # def test_delete_result(self, cli):
    # pass

    # def test_delete_runner(self, cli):
    # pass
