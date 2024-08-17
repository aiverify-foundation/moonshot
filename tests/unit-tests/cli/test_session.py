from ast import literal_eval
import pytest
from unittest.mock import patch, MagicMock
from argparse import Namespace
from moonshot.integrations.cli.redteam.session import new_session, use_session


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
                "[new_session]: Invalid type for parameter: endpoint. Expecting type list."
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