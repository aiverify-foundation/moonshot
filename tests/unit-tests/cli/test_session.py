from ast import literal_eval
import pytest
from unittest.mock import patch, MagicMock
from argparse import Namespace
from moonshot.integrations.cli.redteam.session import delete_session, list_sessions, new_session, use_session
from _pytest.assertion import truncate
truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999  

class TestCollectionCliSession:
    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # New session
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "argparse_value, expected_output",
        [
            # normal input 
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session] Using session: test_runner"
            ),
            # incorrect runner_id type
            (
                {
                "runner_id": {"x": "y"},
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: Invalid type for parameter: runner_id. Expecting type: str."
            ),     
            # incorrect context_strategy type
            (
                {
                "runner_id": "test_runner",
                "context_strategy": ["add_previous_prompt"],
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: Invalid type for parameter: context_strategy. Expecting type: str."
            ),                       
            # incorrect prompt_template type
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": 123,
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: Invalid type for parameter: prompt_template. Expecting type: str."
            ),         
            # incorrect endpoints type
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "123"
                },
                "[new_session]: Invalid type for parameter: endpoints. Expecting type list."
            ),
            # missing required argument: runner_id
            (
                {
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "123"
                },
                "[new_session]: Invalid or missing required parameter: runner_id"
            ),
            # missing optional argument: context_strategy
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session] Using session: test_runner"
            ),                            
            # missing optional argument: prompt_template
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session] Using session: test_runner"
            ),         
            # existing runner_name
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: [Runner] Unable to create runner because the runner file exists."
            ),
            # non-existent context_strategy
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "idontexist",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: [Session] Context Strategy idontexist does not exist."
            ),
            # non-existent prompt_template
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "idontexist",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: [Session] Prompt Template idontexist does not exist."
            ),
            # use non-existent endpoint
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"idontexist\"]"
                },
                "[new_session]: [Runner] Connector endpoint idontexist does not exist."
            ),
            # existing and non-existent endpoint respectively
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\", \"idontexist\"]"
                },
                "[new_session]: [Runner] Connector endpoint idontexist does not exist."
            ),         
            # multiple non-existent endpoints
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"idontexist\", \"idontexist2\"]"
                },
                "[new_session]: [Runner] Connector endpoint idontexist does not exist."
            ),                                                               
        ]
    )
    @patch('moonshot.integrations.cli.redteam.session.api_create_runner')
    @patch('moonshot.integrations.cli.redteam.session.api_create_session')
    @patch('moonshot.integrations.cli.redteam.session.api_load_session')
    def test_new_session_create_runner(self, mock_api_load_session, mock_api_create_runner, mock_api_create_session, argparse_value, expected_output, capsys):
        # mock the arguments
        args = Namespace(
            runner_id=argparse_value.get("runner_id"), 
            context_strategy=argparse_value.get("context_strategy"), 
            prompt_template=argparse_value.get("prompt_template"), 
            endpoints=argparse_value.get("endpoints")
        )
        endpoints = literal_eval(args.endpoints)

        # mock api_create_runner
        if "Unable to create runner" in expected_output:
            mock_api_create_runner.side_effect = Exception("[Runner] Unable to create runner because the runner file exists.")
        elif "[Session] Context Strategy" in expected_output:
            mock_api_create_runner.side_effect = Exception("[Session] Context Strategy idontexist does not exist.")
        elif "[Session] Prompt Template" in expected_output:
            mock_api_create_runner.side_effect = Exception("[Session] Prompt Template idontexist does not exist.")
        elif "[Runner] Connector endpoint" in expected_output:
            mock_api_create_runner.side_effect = Exception("[Runner] Connector endpoint idontexist does not exist.")                       
        else:
            mock_api_create_runner.return_value = MagicMock(database_instance=True, id=args.runner_id, endpoints=endpoints)

        # mock api_load_session
        mock_api_load_session.return_value = {'session_id': args.runner_id, 'context_strategy': args.context_strategy, 'prompt_template': args.prompt_template}

        new_session(args)
        captured = capsys.readouterr()
        assert expected_output in captured.out.strip()

    @pytest.mark.parametrize(
        "argparse_value, expected_output",
        [
            # normal input 
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                },
                "[new_session] Using session: test_runner"
            ),                
           # incorrect runner_id type
            (
                {
                "runner_id": {"x": "y"},
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                },
                "[new_session]: Invalid type for parameter: runner_id. Expecting type: str."
            ),  
            # incorrect context_strategy type
            (
                {
                "runner_id": "test_runner",
                "context_strategy": ["add_previous_prompt"],
                "prompt_template": "mmlu",
                },
                "[new_session]: Invalid type for parameter: context_strategy. Expecting type: str."
            ),                       
            # incorrect prompt_template type
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": 123,
                },
                "[new_session]: Invalid type for parameter: prompt_template. Expecting type: str."
            ),         
            # missing required argument: runner_id
            (
                {
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                },
                "[new_session]: Invalid or missing required parameter: runner_id"
            ),
            # missing optional argument: context_strategy
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                },
                "[new_session] Using session: test_runner"
            ),                            
            # missing optional argument: prompt_template
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                },
                "[new_session] Using session: test_runner"
            ),         
            # use non-existent runner
            (
                {
                "runner_id": "idonotexist",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: [Runner] Unable to load runner because the runner file does not exist."
            ),
            # use non-existent context_strategy
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "idontexist",
                "prompt_template": "mmlu",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: [Session] Context Strategy idontexist does not exist."
            ),
            # use non-existent prompt_template
            (
                {
                "runner_id": "test_runner",
                "context_strategy": "add_previous_prompt",
                "prompt_template": "idontexist",
                "endpoints": "[\"openai-gpt4\"]"
                },
                "[new_session]: [Session] Prompt Template idontexist does not exist."
            )                               
        ]
    )
    @patch('moonshot.integrations.cli.redteam.session.api_load_runner')
    @patch('moonshot.integrations.cli.redteam.session.api_create_session')
    @patch('moonshot.integrations.cli.redteam.session.api_load_session')
    def test_new_session_load_runner(self, mock_api_load_session, mock_api_load_runner, mock_api_create_session, argparse_value, expected_output, capsys):
        # mock the arguments
        args = Namespace(
            runner_id=argparse_value.get("runner_id"), 
            context_strategy=argparse_value.get("context_strategy"), 
            prompt_template=argparse_value.get("prompt_template"), 
        )

        # mock mock_api_load_runner
        if "Unable to load runner" in expected_output:
            mock_api_load_runner.side_effect = Exception("[Runner] Unable to load runner because the runner file does not exist.")
        elif "[Session] Context Strategy" in expected_output:
            mock_api_load_runner.side_effect = Exception("[Session] Context Strategy idontexist does not exist.")
        elif "[Session] Prompt Template" in expected_output:
            mock_api_load_runner.side_effect = Exception("[Session] Prompt Template idontexist does not exist.")
        elif "[Runner] Connector endpoint" in expected_output:
            mock_api_load_runner.side_effect = Exception("[Runner] Connector endpoint idontexist does not exist.")                       
        else:
            mock_api_load_runner.return_value = MagicMock(database_instance=True, id=args.runner_id)

        # mock api_load_session

        new_session(args)
        captured = capsys.readouterr()
        assert expected_output in captured.out.strip()


    # ------------------------------------------------------------------------------
    # Use session
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "argparse_value, expected_output",
        [
            # # existent runner
            # (
            #     {"runner_id": "test_runner"},
            #     "[use_session] Using session: test_runner"
            # ),      
            # non-existent runner 
            (
                {"runner_id": "test_runner"},
                "[use_session]: [Runner] Unable to load runner because the runner file does not exist."
            ),
            # incorrect runner_id type
            (
                {"runner_id": {"hello": "world"}},
                "[use_session]: Invalid type for parameter: runner_id. Expecting type str."
            ),
            #  missing required argument: runner_id
            (
                {"not_a_runner_id": "test_runner"},
                "[use_session]: Invalid or missing required parameter: runner_id"
            ),                                                
        ]
    )
    @patch('moonshot.integrations.cli.redteam.session.api_load_runner')
    @patch('moonshot.integrations.cli.redteam.session.api_load_session')
    def test_use_session(self, mock_api_load_session, mock_api_load_runner, argparse_value, expected_output, capsys):
        # mock the arguments
        args = Namespace(runner_id=argparse_value.get("runner_id"))

        valid_session_metadata = {
            'session_id': 'test_runner',
            'context_strategy': 'add_previous_prompt',
            'prompt_template': 'mmlu',
            'endpoints': ['openai-gpt4']
        }

        # mock api_load_runner
        if "Unable to load runner" in expected_output:
            mock_api_load_runner.side_effect = Exception("[Runner] Unable to load runner because the runner file does not exist.")
        mock_api_load_runner.return_value = MagicMock(database_instance=True, id=args.runner_id)

        # mock api_load_session
        mock_api_load_session.return_value = valid_session_metadata

        use_session(args)
        captured = capsys.readouterr()
        assert expected_output in captured.out.strip()

    # ------------------------------------------------------------------------------
    # Delete session
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "argparse_value, expected_output, to_be_called",
        [
            # normal input
            (
                {"session": "test_session"},
                "[delete_session]: Session deleted.",
                True
            ),
            # missing session 
            (
                {"not_a_session": "x"},
                "[delete_session]: Invalid or missing required parameter: session",
                False
            ),                                          
            # empty namespace
            (
                {},
                "[delete_session]: Invalid or missing required parameter: session",
                False
            ),            
            # incorrect session type: int
            (
                {"session": 123},
                "[delete_session]: Invalid type for parameter: session. Expecting type str.",
                False
            ),
            # incorrect session type: list
            (
                {"session": ["abc"]},
                "[delete_session]: Invalid type for parameter: session. Expecting type str.",
                False
            ),            
        ]
    
    )
    @patch('moonshot.integrations.cli.redteam.session.api_delete_session')
    def test_delete_session(self, mock_api_delete_session, argparse_value, expected_output, to_be_called, capsys):
        # mock the arguments
        args = Namespace(session=argparse_value.get("session", None))
    
        with patch("moonshot.integrations.cli.redteam.session.console.input", return_value="y"):
            with patch("moonshot.integrations.cli.redteam.session.console.print"):
                delete_session(args)

        captured = capsys.readouterr()
        assert expected_output == captured.out.strip()

        if to_be_called:
            mock_api_delete_session.assert_called_once_with(args.session)
        else:
            mock_api_delete_session.assert_not_called()

    @patch('moonshot.integrations.cli.redteam.session.console.input', return_value='y')
    @patch('moonshot.integrations.cli.redteam.session.api_delete_session')
    def test_delete_session_confirm_yes(self, mock_api_delete_session, mock_input):
        # mock the arguments
        args = Namespace(session="test_session")
    
        delete_session(args)

        mock_input.assert_called_once_with("[bold red]Are you sure you want to delete the session (y/N)? [/]")
        mock_api_delete_session.assert_called_once_with('test_session')

    @patch('moonshot.integrations.cli.redteam.session.console.input', return_value='n')
    @patch('moonshot.integrations.cli.redteam.session.api_delete_session')
    def test_delete_session_confirm_no(self, mock_api_delete_session, mock_input):
        # mock the arguments
        args = Namespace(session="test_session")
    
        delete_session(args)

        mock_input.assert_called_once_with("[bold red]Are you sure you want to delete the session (y/N)? [/]")
        mock_api_delete_session.assert_not_called()

    @patch('moonshot.integrations.cli.redteam.session.console.input', return_value='x')
    @patch('moonshot.integrations.cli.redteam.session.console.print')
    @patch('moonshot.integrations.cli.redteam.session.api_delete_session')
    def test_delete_session_confirm_cancelled(self, mock_api_delete_session, mock_print, mock_input):
        args = Namespace(session="test_session")
        
        delete_session(args)
        
        mock_input.assert_called_once_with("[bold red]Are you sure you want to delete the session (y/N)? [/]")
        mock_print.assert_called_once_with("[bold yellow]Session deletion cancelled.[/]")
        mock_api_delete_session.assert_not_called()


    # ------------------------------------------------------------------------------
    # List sessions
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "argparse_value, api_response, expected_output, expected_log",
        [
            # normal input 
            (
                {},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                ""
            ),
            # find and returned results
            (
                {"find": "my-runner"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                ""
            ),
            # find and no returned results
            (
                {"find": "my-runnerx"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None
                ,
                "There are no sessions found."
            ),
            # incorrect find type: int
            (
                {"find": 123},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None
                ,
                "[list_sessions]: Invalid type for parameter: find. Expecting type str."
            ),       
            # incorrect find type: dict
            (
                {"find": {"hello": "world"}},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None
                ,
                "[list_sessions]: Invalid type for parameter: find. Expecting type str."
            ),                             
            # paginate successfully
            (
                {"pagination": "(1, 1)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': '',
                        'idx':1
                    }
                ],
                ""
            ),
            # paginate with a larger page number than the total number of results
            (
                {"pagination": "(5, 1)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': '',
                        'idx':1
                    }
                ],
                ""
            ),            
            # incorrect pagination type: int
            (
                {"pagination": 123},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "[list_sessions]: Invalid type for parameter: pagination. Expecting type str."
            ),   
            # incorrect pagination type: list
            (
                {"pagination": ['123']},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "[list_sessions]: Invalid type for parameter: pagination. Expecting type str."
            ),     
            # incorrect pagination tuple values: negative page number
            (
                {"pagination": "(-1,1)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "[list_sessions]: Invalid page number or page size. Page number and page size should start from 1."
            ),             
            # incorrect pagination tuple values: negative page size
            (
                {"pagination": "(1,-1)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "[list_sessions]: Invalid page number or page size. Page number and page size should start from 1."
            ),   
            # incorrect pagination tuple values: 3 tuple values
            (
                {"pagination": "(1,2,3)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "[list_sessions]: The 'pagination' argument must be a tuple of two integers."
            ),    
            # incorrect pagination tuple value types: string
            (
                {"pagination": "(\"hello\", \"world\")"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "[list_sessions]: The 'pagination' argument must be a tuple of two integers."
            ),                                                                      
            # input with find and pagination
            (
                {"find": "my-runner", "pagination": "(1, 1)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': '',
                        'idx': 1
                    }
                ],
                ""
            ),
            # input with no find results and pagination
            (
                {"find": "my-runnerx", "pagination": "(1, 1)"},
                [
                    {
                        'session_id': 'my-runner', 
                        'endpoints': ['openai-gpt4'], 
                        'created_epoch': '1723878322.638593', 
                        'created_datetime': '20240817-150522', 
                        'prompt_template': '', 
                        'context_strategy': '', 
                        'cs_num_of_prev_prompts': 5, 
                        'attack_module': '', 
                        'metric': '', 
                        'system_prompt': ''
                    }
                ],
                None,
                "There are no sessions found."
            ),            
            # # error case
            # (
            #     {"find": "error"},
            #     [],
            #     [],
            #     "An error has occurred while listing sessions."
            # ),
        ]
    )
    @patch("moonshot.integrations.cli.redteam.session.api_get_all_session_metadata")
    @patch("moonshot.integrations.cli.redteam.session._display_sessions")
    def test_list_sessions(self, 
            mock_display_sessions, 
            mock_api_get_all_session_metadata, 
            argparse_value, 
            api_response, 
            expected_output, 
            expected_log,
            capsys):

        args = Namespace(find=argparse_value.get("find"), pagination=argparse_value.get("pagination") )

        if "error" in expected_log:
            mock_api_get_all_session_metadata.side_effect = Exception(
                "An error has occurred while listing sessions."
            )
        else:
            mock_api_get_all_session_metadata.return_value = api_response
        mock_api_get_all_session_metadata.return_value = api_response
        
        result = list_sessions(args)
        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if api_response and not expected_log:
            mock_display_sessions.assert_called_once_with(api_response)
        else:
            mock_display_sessions.assert_not_called()
