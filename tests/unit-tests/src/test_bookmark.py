import textwrap
from unittest.mock import patch

import pytest

from moonshot.src.bookmark.bookmark import Bookmark
from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments


class TestCollectionBookmark:
    # ------------------------------------------------------------------------------
    # Test add_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, mock_return_value, expected_dict",
        [
            # Valid case for bookmark insertion
            (
                {
                    "name": "Bookmark A",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                    "bookmark_time": "Time A",
                },
                True,
                {
                    "expected_output": True,
                    "expected_message": "[Bookmark] Bookmark added successfully.",
                },
            ),
            # Case where insertion fails
            (
                {
                    "name": "Bookmark B",
                    "prompt": "Prompt B",
                    "prepared_prompt": "Prepared Prompt",
                    "response": "Response B",
                    "context_strategy": "Strategy B",
                    "prompt_template": "Template B",
                    "attack_module": "Module B",
                    "metric": "Metric B",
                    "bookmark_time": "Time B",
                },
                None,
                {
                    "expected_output": False,
                    "expected_message": "[Bookmark] Failed to add bookmark record: Error "
                    "inserting record into database.",
                },
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.create_database_record")
    def test_add_bookmark(
        self, mock_create_database_record, input_args, mock_return_value, expected_dict
    ):
        bookmark_instance = Bookmark()

        # Convert input_args to BookmarkArguments
        bookmark_args = BookmarkArguments(**input_args)

        # Set up the mock return value for create_database_record
        mock_create_database_record.return_value = mock_return_value

        # Call the API function to insert a bookmark
        result = bookmark_instance.add_bookmark(bookmark_args)

        # Assert the result
        assert (
            result["success"] == expected_dict["expected_output"]
        ), "Bookmark insertion success status should match."
        assert (
            result["message"] == expected_dict["expected_message"]
        ), "Bookmark insertion message should match."

        # Close the instance
        bookmark_instance.close()

    # ------------------------------------------------------------------------------
    # Test get_all_bookmarks functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_return_value, expected_output",
        [
            # Case with multiple bookmarks
            (
                [
                    (
                        "1",
                        "Bookmark A",
                        "Prompt A",
                        "Prepared Prompt A",
                        "Response A",
                        "Strategy A",
                        "Template A",
                        "Module A",
                        "Metric A",
                        "Time A",
                    ),
                    (
                        "2",
                        "Bookmark B",
                        "Prompt B",
                        "Prepared Prompt B",
                        "Response B",
                        "Strategy B",
                        "Template B",
                        "Module B",
                        "Metric B",
                        "Time B",
                    ),
                ],
                [
                    {
                        "name": "Bookmark A",
                        "prompt": "Prompt A",
                        "prepared_prompt": "Prepared Prompt A",
                        "response": "Response A",
                        "context_strategy": "Strategy A",
                        "prompt_template": "Template A",
                        "attack_module": "Module A",
                        "metric": "Metric A",
                        "bookmark_time": "Time A",
                    },
                    {
                        "name": "Bookmark B",
                        "prompt": "Prompt B",
                        "prepared_prompt": "Prepared Prompt B",
                        "response": "Response B",
                        "context_strategy": "Strategy B",
                        "prompt_template": "Template B",
                        "attack_module": "Module B",
                        "metric": "Metric B",
                        "bookmark_time": "Time B",
                    },
                ],
            ),
            # Case with no bookmarks
            (
                [],
                [],
            ),
            # Case where read_database_records returns None
            (
                None,
                [],
            ),
            # Case where read_database_records returns an empty string
            (
                "",
                [],
            ),
            # Case where read_database_records returns a dictionary
            (
                {"key": "value"},
                [],
            ),
            # Case where read_database_records returns a list of strings
            (
                ["string1", "string2"],
                [],
            ),
            # Case where read_database_records returns an integer
            (
                123,
                [],
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.read_database_records")
    def test_get_all_bookmarks(
        self, mock_read_database_records, mock_return_value, expected_output
    ):
        bookmark_instance = Bookmark()

        # Set up the mock return value for read_database_records
        mock_read_database_records.return_value = mock_return_value

        # Call the API function to retrieve all bookmarks
        result = bookmark_instance.get_all_bookmarks()

        # Assert the result
        assert (
            result == expected_output
        ), "The list of bookmarks should match the expected output."

        # Assert read_database_records was called once
        mock_read_database_records.assert_called_once_with(
            bookmark_instance.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )

        # Close the instance
        bookmark_instance.close()

    # ------------------------------------------------------------------------------
    # Test get_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "bookmark_name, mock_return_value, expected_output, expected_exception, expected_call",
        [
            # Case where the bookmark is found
            (
                "Bookmark A",
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                {
                    "name": "Bookmark A",
                    "prompt": "Prompt A",
                    "prepared_prompt": "Prepared Prompt A",
                    "response": "Response A",
                    "context_strategy": "Strategy A",
                    "prompt_template": "Template A",
                    "attack_module": "Module A",
                    "metric": "Metric A",
                    "bookmark_time": "Time A",
                },
                None,
                True,
            ),
            # Case where the bookmark_name is invalid
            (
                None,
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                "[Bookmark] Invalid bookmark name: None",
                RuntimeError,
                False,
            ),
            (
                "",
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                "[Bookmark] Invalid bookmark name: ",
                RuntimeError,
                False,
            ),
            (
                (),
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                "[Bookmark] Invalid bookmark name: ()",
                RuntimeError,
                False,
            ),
            (
                [],
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                "[Bookmark] Invalid bookmark name: []",
                RuntimeError,
                False,
            ),
            (
                {},
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                "[Bookmark] Invalid bookmark name: {}",
                RuntimeError,
                False,
            ),
            (
                123,
                (
                    "1",
                    "Bookmark A",
                    "Prompt A",
                    "Prepared Prompt A",
                    "Response A",
                    "Strategy A",
                    "Template A",
                    "Module A",
                    "Metric A",
                    "Time A",
                ),
                "[Bookmark] Invalid bookmark name: 123",
                RuntimeError,
                False,
            ),
            # Case where read_database_record returns an unexpected type (e.g., a dictionary)
            (
                "Bookmark C",
                None,
                "[Bookmark] No record found for bookmark name: Bookmark C",
                RuntimeError,
                True,
            ),
            (
                "Bookmark C",
                "",
                "[Bookmark] No record found for bookmark name: Bookmark C",
                RuntimeError,
                True,
            ),
            (
                "Bookmark C",
                [],
                "[Bookmark] No record found for bookmark name: Bookmark C",
                RuntimeError,
                True,
            ),
            (
                "Bookmark C",
                {},
                "[Bookmark] No record found for bookmark name: Bookmark C",
                RuntimeError,
                True,
            ),
            (
                "Bookmark C",
                123,
                "[Bookmark] No record found for bookmark name: Bookmark C",
                RuntimeError,
                True,
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.read_database_record")
    def test_get_bookmark(
        self,
        mock_read_database_record,
        bookmark_name,
        mock_return_value,
        expected_output,
        expected_exception,
        expected_call,
    ):
        bookmark_instance = Bookmark()

        # Set up the mock return value for read_database_record
        mock_read_database_record.return_value = mock_return_value

        # Call the API function to retrieve the bookmark
        if expected_exception:
            with pytest.raises(expected_exception):
                bookmark_instance.get_bookmark(bookmark_name)
        else:
            result = bookmark_instance.get_bookmark(bookmark_name)
            # Assert the result
            assert (
                result == expected_output
            ), "The bookmark information should match the expected output."

        # Assert read_database_record was called with the correct arguments
        if expected_call:
            mock_read_database_record.assert_called_once_with(
                bookmark_instance.db_instance,
                (bookmark_name,),
                Bookmark.sql_select_bookmark_record,
            )
        else:
            mock_read_database_record.assert_not_called()

        # Close the instance
        bookmark_instance.close()

    # ------------------------------------------------------------------------------
    # Test delete_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_read_database_side_effect, mock_delete_database_side_effect, bookmark_name, expected_output, expected_call",
        [
            # Case where the bookmark is deleted successfully
            (
                ("database_record","result"),
                None,
                "Bookmark A",
                {"success": True, "message": "[Bookmark] Bookmark record deleted."},
                True,
            ),
            # Case where the bookmark_name is invalid (None)
            (
                ("database_record","result"),
                None,
                None,
                {"success": False, "message": "[Bookmark] Invalid bookmark name: None"},
                False,
            ),
            # Case where the bookmark_name is invalid (empty string)
            (
                ("database_record","result"),
                None,
                "",
                {"success": False, "message": "[Bookmark] Invalid bookmark name: "},
                False,
            ),
            # Case where the bookmark_name is invalid (tuple)
            (
                ("database_record","result"),
                None,
                (),
                {"success": False, "message": "[Bookmark] Invalid bookmark name: ()"},
                False,
            ),
            # Case where the bookmark_name is invalid (list)
            (
                ("database_record","result"),
                None,
                [],
                {"success": False, "message": "[Bookmark] Invalid bookmark name: []"},
                False,
            ),
            # Case where the bookmark_name is invalid (dictionary)
            (
                ("database_record","result"),
                None,
                {},
                {"success": False, "message": "[Bookmark] Invalid bookmark name: {}"},
                False,
            ),
            # Case where the bookmark_name is invalid (integer)
            (
                ("database_record","result"),
                None,
                123,
                {"success": False, "message": "[Bookmark] Invalid bookmark name: 123"},
                False,
            ),
            # Case where deletion fails
            (
                ("database_record","result"),
                Exception("Deletion error"),
                "Bookmark A",
                {
                    "success": False,
                    "message": "[Bookmark] Failed to delete bookmark record: Deletion error",
                },
                True,
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.delete_database_record_in_table")
    @patch("moonshot.src.storage.storage.Storage.read_database_record")
    def test_delete_bookmark(
        self,
        mock_read_database_record_in_table,
        mock_delete_database_record_in_table,
        mock_read_database_side_effect,
        mock_delete_database_side_effect,
        bookmark_name,
        expected_output,
        expected_call,
    ):
        bookmark_instance = Bookmark()

        # Set up the mock side effect for read_database_record_in_table
        mock_read_database_record_in_table.side_effect = mock_read_database_side_effect

        # Set up the mock side effect for delete_database_record_in_table
        mock_delete_database_record_in_table.side_effect = mock_delete_database_side_effect

        # Call the API function to delete the bookmark
        result = bookmark_instance.delete_bookmark(bookmark_name)

        # Assert the result
        assert (
            result == expected_output
        ), "The result of deleting the bookmark should match the expected output."

        # Assert delete_database_record_in_table was called with the correct arguments
        if expected_call:
            sql_delete_bookmark_record = textwrap.dedent(
                f"""
                DELETE FROM bookmark WHERE name = '{bookmark_name}';
            """
            )
            mock_delete_database_record_in_table.assert_called_once_with(
                bookmark_instance.db_instance,
                sql_delete_bookmark_record,
            )
        else:
            mock_delete_database_record_in_table.assert_not_called()

        # Close the instance
        bookmark_instance.close()

    # ------------------------------------------------------------------------------
    # Test delete_all_bookmark functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_side_effect, expected_output",
        [
            # Case where deletion is successful
            (
                None,
                {
                    "success": True,
                    "message": "[Bookmark] All bookmark records deleted.",
                },
            ),
            # Case where deletion fails
            (
                Exception("Deletion error"),
                {
                    "success": False,
                    "message": "[Bookmark] Failed to delete all bookmark records: Deletion error",
                },
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.delete_database_record_in_table")
    def test_delete_all_bookmark(
        self, mock_delete_database_record_in_table, mock_side_effect, expected_output
    ):
        bookmark_instance = Bookmark()

        # Set up the mock side effect for delete_database_record_in_table
        mock_delete_database_record_in_table.side_effect = mock_side_effect

        # Call the API function to delete all bookmarks
        result = bookmark_instance.delete_all_bookmark()

        # Assert the result
        assert (
            result == expected_output
        ), "The result of deleting all bookmarks should match the expected output."

        # Assert delete_database_record_in_table was called once with the correct arguments
        mock_delete_database_record_in_table.assert_called_once_with(
            bookmark_instance.db_instance,
            Bookmark.sql_delete_bookmark_records,
        )

        # Close the instance
        bookmark_instance.close()

    # ------------------------------------------------------------------------------
    # Test export_bookmarks functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_read_return_value, mock_create_return_value, expected_bookmarks_json, expected_output",
        [
            # Case where export is successful with multiple bookmarks
            (
                [
                    (
                        "1",
                        "Bookmark A",
                        "Prompt A",
                        "Prepared Prompt A",
                        "Response A",
                        "Strategy A",
                        "Template A",
                        "Module A",
                        "Metric A",
                        "Time A",
                    ),
                    (
                        "2",
                        "Bookmark B",
                        "Prompt B",
                        "Prepared Prompt B",
                        "Response B",
                        "Strategy B",
                        "Template B",
                        "Module B",
                        "Metric B",
                        "Time B",
                    ),
                ],
                "moonshot-data/bookmark/bookmarks.json",
                [
                    {
                        "name": "Bookmark A",
                        "prompt": "Prompt A",
                        "prepared_prompt": "Prepared Prompt A",
                        "response": "Response A",
                        "context_strategy": "Strategy A",
                        "prompt_template": "Template A",
                        "attack_module": "Module A",
                        "metric": "Metric A",
                        "bookmark_time": "Time A",
                    },
                    {
                        "name": "Bookmark B",
                        "prompt": "Prompt B",
                        "prepared_prompt": "Prepared Prompt B",
                        "response": "Response B",
                        "context_strategy": "Strategy B",
                        "prompt_template": "Template B",
                        "attack_module": "Module B",
                        "metric": "Metric B",
                        "bookmark_time": "Time B",
                    },
                ],
                "moonshot-data/bookmark/bookmarks.json",
            ),
            # Case where export is successful with no bookmarks
            (
                [],
                "moonshot-data/bookmark/bookmarks.json",
                [],
                "moonshot-data/bookmark/bookmarks.json",
            ),
            # Case where read_database_records returns None
            (
                None,
                "moonshot-data/bookmark/bookmarks.json",
                [],
                "moonshot-data/bookmark/bookmarks.json",
            ),
            # Case where read_database_records returns an empty string
            (
                "",
                "moonshot-data/bookmark/bookmarks.json",
                [],
                "moonshot-data/bookmark/bookmarks.json",
            ),
            # Case where read_database_records returns a dictionary
            (
                {"key": "value"},
                "moonshot-data/bookmark/bookmarks.json",
                [],
                "moonshot-data/bookmark/bookmarks.json",
            ),
            # Case where read_database_records returns a list of strings
            (
                ["string1", "string2"],
                "moonshot-data/bookmark/bookmarks.json",
                [],
                "moonshot-data/bookmark/bookmarks.json",
            ),
            # Case where read_database_records returns an integer
            (
                123,
                "moonshot-data/bookmark/bookmarks.json",
                [],
                "moonshot-data/bookmark/bookmarks.json",
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.read_database_records")
    @patch("moonshot.src.storage.storage.Storage.create_object")
    def test_export_bookmarks(
        self,
        mock_create_object,
        mock_read_database_records,
        mock_read_return_value,
        mock_create_return_value,
        expected_bookmarks_json,
        expected_output,
    ):
        bookmark_instance = Bookmark()

        # Set up the mock return values
        mock_read_database_records.return_value = mock_read_return_value
        mock_create_object.return_value = mock_create_return_value

        # Call the API function to export bookmarks
        result = bookmark_instance.export_bookmarks()

        # Assert the result
        assert (
            result == expected_output
        ), "The path to the exported JSON file should match the expected output."

        # Assert read_database_records was called once with the correct arguments
        mock_read_database_records.assert_called_once_with(
            bookmark_instance.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )

        # Assert create_object was called once with the correct arguments
        mock_create_object.assert_called_once_with(
            "BOOKMARKS",
            "bookmarks",
            {"bookmarks": expected_bookmarks_json},
            "json",
        )

        # Close the instance
        bookmark_instance.close()

    @pytest.mark.parametrize(
        "export_file_name, expected_exception, expected_message",
        [
            # Case where export_file_name is None
            (
                None,
                Exception,
                "[Bookmark] Failed to export bookmarks: Export filename must be a non-empty string.",
            ),
            # Case where export_file_name is an empty string
            (
                "",
                Exception,
                "[Bookmark] Failed to export bookmarks: Export filename must be a non-empty string.",
            ),
            # Case where export_file_name is a tuple
            (
                (),
                Exception,
                "[Bookmark] Failed to export bookmarks: Export filename must be a non-empty string.",
            ),
            # Case where export_file_name is a list
            (
                [],
                Exception,
                "[Bookmark] Failed to export bookmarks: Export filename must be a non-empty string.",
            ),
            # Case where export_file_name is a dictionary
            (
                {},
                Exception,
                "[Bookmark] Failed to export bookmarks: Export filename must be a non-empty string.",
            ),
            # Case where export_file_name is an integer
            (
                123,
                Exception,
                "[Bookmark] Failed to export bookmarks: Export filename must be a non-empty string.",
            ),
        ],
    )
    def test_export_bookmarks_invalid_filename(
        self, export_file_name, expected_exception, expected_message
    ):
        bookmark_instance = Bookmark()

        # Call the API function to export bookmarks and assert the exception
        with pytest.raises(expected_exception) as exc_info:
            bookmark_instance.export_bookmarks(export_file_name)

        # Assert the exception message
        assert (
            str(exc_info.value) == expected_message
        ), "The exception message should match the expected message."

    @pytest.mark.parametrize(
        "mock_read_return_value, mock_create_side_effect, expected_exception, expected_message",
        [
            # Case where create_object raises an exception
            (
                [
                    (
                        "1",
                        "Bookmark A",
                        "Prompt A",
                        "Prepared Prompt A",
                        "Response A",
                        "Strategy A",
                        "Template A",
                        "Module A",
                        "Metric A",
                        "Time A",
                    ),
                ],
                Exception("Export error"),
                Exception,
                "[Bookmark] Failed to export bookmarks: Export error",
            ),
        ],
    )
    @patch("moonshot.src.storage.storage.Storage.read_database_records")
    @patch("moonshot.src.storage.storage.Storage.create_object")
    def test_export_bookmarks_exception(
        self,
        mock_create_object,
        mock_read_database_records,
        mock_read_return_value,
        mock_create_side_effect,
        expected_exception,
        expected_message,
    ):
        bookmark_instance = Bookmark()

        # Set up the mock return values and side effects
        mock_read_database_records.return_value = mock_read_return_value
        mock_create_object.side_effect = mock_create_side_effect

        # Call the API function to export bookmarks and assert the exception
        with pytest.raises(expected_exception) as exc_info:
            bookmark_instance.export_bookmarks()

        # Assert the exception message
        assert (
            str(exc_info.value) == expected_message
        ), "The exception message should match the expected message."

        # Assert read_database_records was called once with the correct arguments
        mock_read_database_records.assert_called_once_with(
            bookmark_instance.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )

        # Close the instance
        bookmark_instance.close()

    # ------------------------------------------------------------------------------
    # Test close functionality
    # ------------------------------------------------------------------------------
    @patch("moonshot.src.storage.storage.Storage.close_database_connection")
    def test_close(self, mock_close_database_connection):
        # Create an instance of Bookmark
        bookmark_instance = Bookmark()

        # Call the close method
        bookmark_instance.close()

        # Assert close_database_connection was called once with the correct arguments
        mock_close_database_connection.assert_called_once_with(
            bookmark_instance.db_instance
        )

        # Assert the singleton instance is set to None
        assert (
            Bookmark._instance is None
        ), "The singleton instance should be set to None after closing."

    @patch("moonshot.src.storage.storage.Storage.close_database_connection")
    def test_close_no_db_instance(self, mock_close_database_connection):
        # Create an instance of Bookmark
        bookmark_instance = Bookmark()
        bookmark_instance.db_instance = None  # Simulate no database instance

        # Call the close method
        bookmark_instance.close()

        # Assert close_database_connection was not called
        mock_close_database_connection.assert_not_called()

        # Assert the singleton instance is set to None
        assert (
            Bookmark._instance is None
        ), "The singleton instance should be set to None after closing."

    @patch("moonshot.src.storage.storage.Storage.close_database_connection")
    def test_close_multiple_times(self, mock_close_database_connection):
        # Create an instance of Bookmark
        bookmark_instance = Bookmark()

        # Call the close method multiple times
        bookmark_instance.close()
        bookmark_instance.close()
        bookmark_instance.close()

        # Assert close_database_connection was called three times with the correct arguments
        assert (
            mock_close_database_connection.call_count == 3
        ), "close_database_connection should be called three times."
        mock_close_database_connection.assert_called_with(bookmark_instance.db_instance)

        # Assert the singleton instance is set to None
        assert (
            Bookmark._instance is None
        ), "The singleton instance should be set to None after closing."

    # ------------------------------------------------------------------------------
    # Test bookmark instance is singleton
    # ------------------------------------------------------------------------------
    def test_bookmark_singleton(self):
        # Retrieve two instances of the Bookmark class
        bookmark_instance_1 = Bookmark()
        bookmark_instance_2 = Bookmark()

        # Assert that both instances are the same (singleton behavior)
        assert (
            bookmark_instance_1 is bookmark_instance_2
        ), "Bookmark instances should be the same (singleton pattern)."

        # Terminate the bookmark_instance
        bookmark_instance_1.close()
