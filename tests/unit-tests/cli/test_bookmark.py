from argparse import Namespace
from ast import literal_eval
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from moonshot.integrations.cli.redteam.session import (
    add_bookmark,
    use_bookmark,
    delete_bookmark,
    list_bookmarks,
    view_bookmark,
    export_bookmarks
)

class TestCollectionCliBookmark:

    list_of_endpoint_chats = {"test-endpoint-1": [{
                    "chat_record_id": 1,
                    "conn_id": "test-endpoint-1",
                    "context_strategy": "test-context-strategy",
                    "prompt_template": "test-prompt-template",
                    "attack_module": "test-attack-module",
                    "metric": "test-metric",
                    "prompt": "hello",
                    "prepared_prompt": "hello",
                    "system_prompt": "",
                    "predicted_result": "Hello! How can I assist you today?",
                    "duration": "1",
                    "prompt_time": "2024-08-27 00:00:00.0000"
                },
                {
                    "chat_record_id": 2,
                    "conn_id": "test-endpoint-1",
                    "context_strategy": "test-context-strategy",
                    "prompt_template": "test-prompt-template",
                    "attack_module": "test-attack-module",
                    "metric": "test-metric",
                    "prompt": "hello2",
                    "prepared_prompt": "hello2",
                    "system_prompt": "",
                    "predicted_result": "Hello2! How can I assist you today?",
                    "duration": "2",
                    "prompt_time": "2024-08-27 00:00:01.0000"
                }                
            ],
            "test-endpoint-2": [
                {
                    "chat_record_id": 1,
                    "conn_id": "test-endpoint-2",
                    "context_strategy": "test-context-strategy",
                    "prompt_template": "test-prompt-template",
                    "attack_module": "test-attack-module",
                    "metric": "test-metric",
                    "prompt": "hello",
                    "prepared_prompt": "hello",
                    "system_prompt": "",
                    "predicted_result": "Hello! How can I assist you today?",
                    "duration": "1",
                    "prompt_time": "2024-08-27 00:00:00.0000"
                },
                {
                    "chat_record_id": 2,
                    "conn_id": "test-endpoint-2",
                    "context_strategy": "test-context-strategy",
                    "prompt_template": "test-prompt-template",
                    "attack_module": "test-attack-module",
                    "metric": "test-metric",
                    "prompt": "hello2",
                    "prepared_prompt": "hello2",
                    "system_prompt": "",
                    "predicted_result": "Hello2! How can I assist you today?",
                    "duration": "2",
                    "prompt_time": "2024-08-27 00:00:01.0000"
                }         
            ]
        } 


    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Add Bookmark
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "endpoint, prompt_id, bookmark_name, endpoint_chats, expected_output",
        [
            # Valid case
            (
                "test-endpoint-1",
                1,
                "test-bookmark-name",
                list_of_endpoint_chats,
                "[bookmark_prompt]: [Bookmark] Bookmark added successfully."
            ),
            (
                "test-endpoint-2",
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: [Bookmark] Bookmark added successfully."
            ),
            (
                "test-endpoint-2",
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: [Bookmark] Bookmark added successfully."
            ),         
            # Invalid endpoint              
            (
                None,
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'endpoint' argument must be a non-empty string and not None."
            ),        
            (
                ["test-bookmark-name2"],
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'endpoint' argument must be a non-empty string and not None."
            ),                    
            (
                {"test-bookmark-name2"},
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'endpoint' argument must be a non-empty string and not None."
            ),                          
            (
                123,
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'endpoint' argument must be a non-empty string and not None."
            ),                                             
            (
                True,
                2,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'endpoint' argument must be a non-empty string and not None."
            ),           
            # Invalid prompt id         
            (
                "test-endpoint-2",
                None,
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'prompt_id' argument must be an integer."
            ),      
            (
                "test-endpoint-2",
                [2],
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'prompt_id' argument must be an integer."
            ),      
            (
                "test-endpoint-2",
                {2},
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'prompt_id' argument must be an integer."
            ),     
            (
                "test-endpoint-2",
                "2",
                "test-bookmark-name2",
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'prompt_id' argument must be an integer."
            ), 
            # Invalid bookmark name
            (
                "test-endpoint-2",
                2,
                None,
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),
            (
                "test-endpoint-2",
                2,
                ["test-bookmark-name2"],
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),                        
            (
                "test-endpoint-2",
                2,
                {"test-bookmark-name2"},
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),    
            (
                "test-endpoint-2",
                2,
                123,
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),     
            (
                "test-endpoint-2",
                2,
                True,
                list_of_endpoint_chats,
                "[bookmark_prompt]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),                              
            # check for oob index                                                                                                         
        ],
    )
    @patch('moonshot.integrations.cli.redteam.session.api_insert_bookmark')
    @patch('moonshot.integrations.cli.redteam.session.active_session', new_callable=dict)    
    def test_add_bookmark_type_check(self, mock_active_session, mock_api_insert_bookmark, endpoint, prompt_id, bookmark_name, endpoint_chats, expected_output, capsys):

        # Setup mock active session
        mock_active_session.update({
            "list_of_endpoint_chats": endpoint_chats            
        })

        args = Namespace(
            endpoint = endpoint,
            prompt_id = prompt_id,
            bookmark_name = bookmark_name
        )
        try:
            if not isinstance(args.endpoint, str) or not args.endpoint:
                raise TypeError("[bookmark_prompt]: The 'endpoint' argument must be a non-empty string and not None.")
            if not isinstance(args.prompt_id, int):
                raise TypeError("[bookmark_prompt]: The 'prompt_id' argument must be an integer.")
            if not isinstance(args.bookmark_name, str) or not args.bookmark_name:
                raise TypeError("[bookmark_prompt]: The 'bookmark_name' argument must be a non-empty string and not None.")
        except TypeError as e:
            captured = capsys.readouterr()
            assert str(e) == expected_output
            return

        target_chat = None
        for chat in mock_active_session["list_of_endpoint_chats"].get(endpoint, []):
            if chat["chat_record_id"] == prompt_id:
                target_chat = chat
                break

        # Ensure the chat was found
        assert target_chat is not None, f"Chat with prompt_id {prompt_id} not found for endpoint {endpoint}"
        
        # Setup mock api_insert_bookmark response
        mock_api_insert_bookmark.return_value = {'success': True, 'message': '[Bookmark] Bookmark added successfully.'}

        # Call the function
        bookmark_message = add_bookmark(args)

        captured = capsys.readouterr()
        assert expected_output == captured.out.strip()

        # Assertions
        mock_api_insert_bookmark.assert_called_once_with(bookmark_name, 
                                                         target_chat["prompt"],
                                                         target_chat["prepared_prompt"],
                                                         target_chat["predicted_result"],
                                                         target_chat["context_strategy"],
                                                         target_chat["prompt_template"],
                                                         target_chat["attack_module"],
                                                         target_chat["metric"])


    # ------------------------------------------------------------------------------
    # Use Bookmark
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_name, endpoint_chats, api_response, expected_log",
        [
            # Valid case: automated rt
            (
                "my-bookmark",
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "test_am",
                    "metric": "test_me",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "Copy this command and paste it below:\nrun_attack_module test_am \"test prepared prompt\""
            ),
            # Invalid bookmark_name automated rt
            (
                None,
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "test_am",
                    "metric": "test_me",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),            
            (
                ["my-bookmark"],
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "test_am",
                    "metric": "test_me",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),          
            (
                {"my-bookmark"},
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "test_am",
                    "metric": "test_me",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),      
            (
                123,
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "test_am",
                    "metric": "test_me",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),
            (
                False,
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "test_am",
                    "metric": "test_me",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),
            # Valid case: manual rt
            (
                "my-bookmark",
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "Copy this prompt and paste it below: \ntest prepared prompt"
            ),
            # Invalid bookmark_name automated rt
            (
                None,
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),            
            (
                ["my-bookmark"],
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),          
            (
                {"my-bookmark"},
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),      
            (
                123,
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),
            (
                False,
                list_of_endpoint_chats,
                {
                    "name": "my-bookmark",
                    "prompt": "test prompt",
                    "prepared_prompt": "test prepared prompt",
                    "response": "test response prompt",
                    "context_strategy": "test_cs",
                    "prompt_template": "test_pt",
                    "attack_module": "",
                    "metric": "",
                    "bookmark_time": "2024-08-27 00: 00: 00"
                },
                "[use_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None."
            ),            
        ],
    )
    @patch("moonshot.integrations.cli.redteam.session.api_get_bookmark")
    @patch('moonshot.integrations.cli.redteam.session.active_session', new_callable=dict)    
    def test_use_bookmark(
        self,
        mock_active_session,
        mock_api_get_bookmark,
        bookmark_name,
        endpoint_chats,
        api_response,
        expected_log,
        capsys,
    ):

        # Setup mock active session
        mock_active_session.update({
            "list_of_endpoint_chats": endpoint_chats            
        })

        if "error" in expected_log:
            mock_api_get_bookmark.side_effect = Exception(
                "An error has occurred while retrieving the bookmark."
            )
        else:
            mock_api_get_bookmark.return_value = api_response

        args = Namespace(
            bookmark_name = bookmark_name
        )

        use_bookmark(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()


    # ------------------------------------------------------------------------------
    # Delete Bookmark 
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_name, expected_log, to_be_called",
        [
            # Valid case
            (
                "my-bookmark", 
                "[delete_bookmark]: [Bookmark] Bookmark record deleted.",
                True
            ),
            # Invalid case - bookmark_name
            (
                "",
                "[delete_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                ["my-bookmark"],
                "[delete_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {"my-bookmark"},
                "[delete_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                False,
                "[delete_bookmark]: The 'bookmark_name' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.redteam.session.api_delete_bookmark")
    def test_delete_bookmark(
        self, mock_api_delete_bookmark, capsys, bookmark_name, expected_log, to_be_called
    ):
        args = Namespace(
            bookmark_name = bookmark_name
        )

        mock_api_delete_bookmark.return_value = {"success": True, "message": "[Bookmark] Bookmark record deleted."}

        with patch(
            "moonshot.integrations.cli.redteam.session.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.redteam.session.console.print"):
                delete_bookmark(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_bookmark.assert_called_once_with(args.bookmark_name)
        else:
            mock_api_delete_bookmark.assert_not_called()


    @patch(
        "moonshot.integrations.cli.redteam.session.console.input", return_value="y"
    )
    @patch("moonshot.integrations.cli.redteam.session.api_delete_bookmark")
    def test_delete_bookmark_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.bookmark_name = "test_bookmark_name"

        delete_bookmark(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the bookmark (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_bookmark_name")

    @patch(
        "moonshot.integrations.cli.redteam.session.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.redteam.session.api_delete_bookmark")
    def test_delete_cookbook_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.cookbook = "test_bookmark_name"

        delete_bookmark(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the bookmark (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch(
        "moonshot.integrations.cli.redteam.session.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.redteam.session.console.print")
    @patch("moonshot.integrations.cli.redteam.session.api_delete_bookmark")
    def test_delete_cookbook_cancelled_output(
        self, mock_delete, mock_print, mock_input
    ):
        args = MagicMock()
        args.cookbook = "test_bookmark_name"

        delete_bookmark(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the bookmark (y/N)? [/]"
        )
        mock_print.assert_called_once_with(
            "[bold yellow]Bookmark deletion cancelled.[/]"
        )
        mock_delete.assert_not_called()
