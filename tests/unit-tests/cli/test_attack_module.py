import pytest
from unittest.mock import patch
from argparse import Namespace
from moonshot.integrations.cli.redteam.attack_module import list_attack_modules
from _pytest.assertion import truncate
truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999  
import textwrap

class TestCollectionCliAttackModule:
    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # List attack modules
    # ------------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "argparse_value, api_response, expected_output, expected_log, expected_to_call",
        [
            # normal input 
            (
                {},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                "Listing attack modules may take a while...",
                True
            ),
            # find and returned results
            (
                {"find": "charswap_attack"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                "Listing attack modules may take a while...",
                True
            ),
            # find and no returned results
            (
                {"find": "charswap_attackx"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                # "Listing attack modules may take a while...",
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    There are no attack modules found."""),                
                False
            ),
            # incorrect find type: int
            (
                {"find": 123},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None
                ,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: Invalid type for parameter: find. Expecting type str."""),                       
                # "[list_attack_modules]: Invalid type for parameter: find. Expecting type str.",
                False
            ),       
            # incorrect find type: dict
            (
                {"find": {"hello": "world"}},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None
                ,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: Invalid type for parameter: find. Expecting type str."""),                     
                # "[list_attack_modules]: Invalid type for parameter: find. Expecting type str.",
                False
            ),                             
            # paginate successfully
            (
                {"pagination": "(1, 1)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        },
                        "idx": 1
                    }
                ],
                "Listing attack modules may take a while...",
                True
            ),
            # paginate with a larger page number than the total number of results
            (
                {"pagination": "(5, 1)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        },
                        "idx": 1
                    }
                ],
                "Listing attack modules may take a while...",
                True
            ),            
            # incorrect pagination type: int
            (
                {"pagination": 123},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: Invalid type for parameter: pagination. Expecting type str."""),                                  
                False
            ),   
            # incorrect pagination type: list
            (
                {"pagination": ['123']},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: Invalid type for parameter: pagination. Expecting type str."""),                                  
                False
            ),     
            # incorrect pagination tuple values: negative page number
            (
                {"pagination": "(-1,1)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: Invalid page number or page size. Page number and page size should start from 1."""),                 
                False
            ),             
            # incorrect pagination tuple values: negative page size
            (
                {"pagination": "(1,-1)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: Invalid page number or page size. Page number and page size should start from 1."""),                
                False
            ),   
            # incorrect pagination tuple values: 3 tuple values
            (
                {"pagination": "(1,2,3)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: The 'pagination' argument must be a tuple of two integers."""),
                False
            ),    
            # incorrect pagination tuple value types: string
            (
                {"pagination": "(\"hello\", \"world\")"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    [list_attack_modules]: The 'pagination' argument must be a tuple of two integers."""),
                False
            ),                                                                      
            # input with find and pagination
            (
                {"find": "charswap_attack", "pagination": "(1, 1)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        },
                        "idx": 1
                    }
                ],
                "Listing attack modules may take a while...",
                True
            ),
            # input with no find results and pagination
            (
                {"find": "homoglyph_attack", "pagination": "(1, 1)"},
                [
                    {
                        "id": "charswap_attack",
                        "name": "Character Swap Attack",
                        "description": "This module tests for adversarial textual robustness. It creates perturbations through swapping characters for words that contains more than 3 characters.\nParameters:\n1. DEFAULT_MAX_ITERATION - Number of prompts that should be sent to the target. [Default: 10]",
                        "endpoints": [],
                        "configurations": {
                            "max_iteration": 10,
                            "word_swap_ratio": 0.2
                        }
                    }
                ],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    There are no attack modules found."""),
                False
            ),            
            # error case
            (
                {"find": "error"},
                [],
                None,
                textwrap.dedent("""\
                    Listing attack modules may take a while...
                    There are no attack modules found."""),                
                # "An error has occurred while listing attack modules.",
                False
            ),
        ]
    )
    @patch("moonshot.integrations.cli.redteam.attack_module.api_get_all_attack_module_metadata")
    @patch("moonshot.integrations.cli.redteam.attack_module._display_attack_modules")
    def test_list_attack_modules(self, 
            mock_display_attack_modules, 
            mock_api_get_all_attack_module_metadata, 
            argparse_value, 
            api_response, 
            expected_output, 
            expected_log,
            expected_to_call,
            capsys):

        args = Namespace(find=argparse_value.get("find"), pagination=argparse_value.get("pagination") )

        if "error" in expected_log:
            mock_api_get_all_attack_module_metadata.side_effect = Exception(
                "An error has occurred while listing attack modules."
            )
        else:
            mock_api_get_all_attack_module_metadata.return_value = api_response
        mock_api_get_all_attack_module_metadata.return_value = api_response
        
        result = list_attack_modules(args)
        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if expected_to_call:
            mock_display_attack_modules.assert_called_once_with(api_response)
        else:
            mock_display_attack_modules.assert_not_called()