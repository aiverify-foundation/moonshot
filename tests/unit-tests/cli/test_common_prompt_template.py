from unittest.mock import MagicMock, patch
from argparse import Namespace
import pytest

from moonshot.integrations.cli.common.prompt_template import (
    list_prompt_templates,
    delete_prompt_template
)


class TestCollectionCliPromptTemplate:
    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # List Prompt Templates with non-mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, expected_output, expected_log",
        [
            # Valid cases with no filter
            (
                None,
                None,
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }
                ],
                "",
            ),
            # No prompt templates
            (
                None,
                None,
                [],
                None,
                "There are no prompt templates found.",
            ),
            # Valid case with find
            (
                "prompt-template",
                None,
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }
                ],
                "",
            ),
            # Valid case with find but no results
            (
                "nothingvalid",
                None,
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }                    
                ],
                None,
                "There are no prompt templates found.",
            ),
            # Valid case with pagination                        
            (
                None,
                "(1,1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }        
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 1
                    },
                ],
                "",
            ),
            # Valid case with pagination but no results
            (
                None,
                "(1, 1)",
                [],
                None,
                "There are no prompt templates found.",
            ),
            # Invalid cases for find
            (
                "",
                None,
                None,
                None,
                "[list_prompt_templates]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                99,
                None,
                None,
                None,
                "[list_prompt_templates]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                {},
                None,
                None,
                None,
                "[list_prompt_templates]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                [],
                None,
                None,
                None,
                "[list_prompt_templates]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                (),
                None,
                None,
                None,
                "[list_prompt_templates]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                True,
                None,
                None,
                None,
                "[list_prompt_templates]: The 'find' argument must be a non-empty string and not None.",
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                99,
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                {},
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                [],
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                (),
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                True,
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                True,
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                "(1, 'a')",
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(1, 2, 3)",
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(1, )",
                None,
                None,
                "[list_prompt_templates]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(0, 1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }      
                ],
                None,
                "[list_prompt_templates]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(1, 0)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }      
                ],
                None,
                "[list_prompt_templates]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(0, 0)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }      
                ],
                None,
                "[list_prompt_templates]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(1, -1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }      
                ],
                None,
                "[list_prompt_templates]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(-1, 1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }      
                ],
                None,
                "[list_prompt_templates]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(-1, -1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }      
                ],
                None,
                "[list_prompt_templates]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            # Exception case
            (
                None,
                None,
                None,
                None,
                "[list_prompt_templates]: An error has occurred while listing prompt templates.",
            ),
        ],
    )    
    @patch("moonshot.integrations.cli.common.prompt_template.api_get_all_prompt_template_detail")
    @patch("moonshot.integrations.cli.common.prompt_template._display_prompt_templates")
    def test_list_prompt_templates(
        self,
        mock_display_prompt_templates,
        mock_api_get_all_prompt_template,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_prompt_template.side_effect = Exception(
                "An error has occurred while listing prompt templates."
            )
        else:
            mock_api_get_all_prompt_template.return_value = api_response

        args = Namespace(
            find = find, 
            pagination = pagination
        )

        result = list_prompt_templates(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if api_response and not expected_log:
            mock_display_prompt_templates.assert_called_once_with(api_response)
        else:
            mock_display_prompt_templates.assert_not_called()

    # ------------------------------------------------------------------------------
    # List Prompt Templates with mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, filtered_response, expected_output, expected_log",
        
        [
            # valid case no find and pagination
            (
                None,
                None,
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },         
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }                 
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }
                ],
                "",
            ),
            # valid find with results
            (
                "prompt-template",
                None,
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },
                    {
                        "id": 2,
                        "name": "another-pt",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }                    
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },
                ],
                "",
            ),
            (
                " test description",
                None,
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },
                    {
                        "id": 2,
                        "name": "another-pt",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    }                    
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },
                ],
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },
                ],
                "",
            ),            
            # valid pagination with results
            (
                None,
                "(2, 1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },   
                    {
                        "id": 2,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },                       
                ],
                [
                    {
                        "id": 2,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 2
                    },       
                ],
                [
                    {
                        "id": 2,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 2
                    },       
                ],
                "",
            ),
            # valid pagination and find no results
            (
                "non-existent-prompt-template",
                "(1,1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },   
                    {
                        "id": 2,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },                    

                ],
                None,
                None,
                "There are no prompt templates found.",
            ),
            # valid pagination and find with results
            (
                "test description",
                "(2, 1)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "other description",
                        "template": "This is a sample {{prompt}}."
                    },   
                    {
                        "id": 2,
                        "name": "test-prompt-template2",
                        "description": "other description",
                        "template": "This is a sample {{prompt}}."
                    },    
                    {
                        "id": 3,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },    
                    {
                        "id": 4,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },                                                               
                ],
                [
                    {
                        "id": 4,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 2
                    },                                                               
                ],
                [
                    {
                        "id": 4,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 2
                    },        
                ],
                "",
            ),        
            (
                "test description",
                "(2, 2)",
                [
                    {
                        "id": 1,
                        "name": "test-prompt-template",
                        "description": "other description",
                        "template": "This is a sample {{prompt}}."
                    },   
                    {
                        "id": 2,
                        "name": "test-prompt-template2",
                        "description": "other description",
                        "template": "This is a sample {{prompt}}."
                    },    
                    {
                        "id": 3,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },    
                    {
                        "id": 4,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}."
                    },                                                               
                ],
                [
                    {
                        "id": 3,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 1
                    },    
                    {
                        "id": 4,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 2
                    },                                                                
                ],
                [
                    {
                        "id": 3,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 1
                    },    
                    {
                        "id": 4,
                        "name": "test-prompt-template2",
                        "description": "test description",
                        "template": "This is a sample {{prompt}}.",
                        "idx": 2
                    },             
                ],
                "",
            ),                        
        ],
    )
    @patch("moonshot.integrations.cli.common.prompt_template.api_get_all_prompt_template_detail")
    @patch("moonshot.integrations.cli.common.prompt_template._display_prompt_templates")
    @patch("moonshot.integrations.cli.common.prompt_template.filter_data")
    def test_list_prompt_templates_filtered(
        self,
        mock_filter_data,
        mock_display_prompt_templates,
        mock_api_get_all_prompt_template,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        capsys,
    ):
        mock_api_get_all_prompt_template.return_value = api_response
        mock_filter_data.return_value = filtered_response

        args = Namespace(
            find = find,
            pagination = pagination
        )

        result = list_prompt_templates(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if filtered_response and not expected_log:
            mock_display_prompt_templates.assert_called_once_with(filtered_response)
        else:
            mock_display_prompt_templates.assert_not_called()

    # ------------------------------------------------------------------------------
    # Delete Prompt Templates
    # ------------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "prompt_template, expected_log, to_be_called",
        [
            # Valid case
            (
                "Prompt Template 1",
                "[delete_prompt_template]: Prompt template deleted.",
                True
            ),
            # Invalid case - prompt template
            (
                "",
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
            (
                None,
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
            (
                123,
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
            (
                {},
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
            (
                [],
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
            (
                (),
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
            (
                True,
                "[delete_prompt_template]: The 'prompt_template' argument must be a non-empty string and not None.",
                False
            ),
        ]
    )
    @patch("moonshot.integrations.cli.common.prompt_template.api_delete_prompt_template")
    def test_delete_prompt_template(self, mock_api_delete_prompt_template, capsys, prompt_template, expected_log, to_be_called):
        args = Namespace(
            prompt_template = prompt_template
        )

        with patch("moonshot.integrations.cli.common.prompt_template.console.input", return_value="y"):
            with patch("moonshot.integrations.cli.common.prompt_template.console.print") as mock_console_print:
                delete_prompt_template(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_prompt_template.assert_called_once_with(args.prompt_template)
        else:
            mock_api_delete_prompt_template.assert_not_called()

    @patch("moonshot.integrations.cli.common.prompt_template.console.input", return_value='y')
    @patch("moonshot.integrations.cli.common.prompt_template.api_delete_prompt_template")
    def test_delete_prompt_template_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.prompt_template = 'test_prompt_template'
        
        delete_prompt_template(args)
        
        mock_input.assert_called_once_with("[bold red]Are you sure you want to delete the prompt template (y/N)? [/]")
        mock_delete.assert_called_once_with('test_prompt_template')

    @patch("moonshot.integrations.cli.common.prompt_template.console.input", return_value='n')
    @patch("moonshot.integrations.cli.common.prompt_template.api_delete_prompt_template")
    def test_delete_prompt_template_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.prompt_template = 'test_prompt_template'
        
        delete_prompt_template(args)
        
        mock_input.assert_called_once_with("[bold red]Are you sure you want to delete the prompt template (y/N)? [/]")
        mock_delete.assert_not_called()
    
    @patch("moonshot.integrations.cli.common.prompt_template.console.input", return_value='n')
    @patch('moonshot.integrations.cli.common.prompt_template.console.print')
    @patch("moonshot.integrations.cli.common.prompt_template.api_delete_prompt_template")
    def test_delete_prompt_template_cancelled_output(self, mock_delete, mock_print, mock_input):
        args = MagicMock()
        args.prompt_template = 'test_prompt_template'
        
        delete_prompt_template(args)
        
        mock_input.assert_called_once_with("[bold red]Are you sure you want to delete the prompt template (y/N)? [/]")
        mock_print.assert_called_once_with("[bold yellow]Prompt template deletion cancelled.[/]")
        mock_delete.assert_not_called()
