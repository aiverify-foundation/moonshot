from unittest.mock import MagicMock, patch

import pytest

from moonshot.integrations.cli.benchmark.datasets import (
    delete_dataset,
    list_datasets,
    view_dataset,
)


class TestCollectionCliDataset:
    api_response = [
        {
            "id": "squad-shifts-tnf",
            "name": "squad-shifts-tnf",
            "description": "Some description",
            "examples": None,
            "num_of_dataset_prompts": 48201,
            "created_date": "2024-05-27 16:48:35",
            "reference": "Some reference",
            "license": "",
        }
    ]
    api_response_pagination = [
        {
            "id": "squad-shifts-tnf",
            "name": "squad-shifts-tnf",
            "description": "Some description",
            "examples": None,
            "num_of_dataset_prompts": 48201,
            "created_date": "2024-05-27 16:48:35",
            "reference": "Some reference",
            "license": "",
            "idx": 1,
        }
    ]

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test list_datasets functionality with non-mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, expected_output, expected_log, to_be_called",
        [
            # Valid cases
            (
                None,
                None,
                api_response,
                api_response,
                "Listing datasets may take a while...",
                True,
            ),
            # No datasets
            (
                None,
                None,
                [],
                None,
                "Listing datasets may take a while...\nThere are no datasets found.",
                False,
            ),
            (
                "squad",
                None,
                api_response,
                api_response,
                "Listing datasets may take a while...",
                True,
            ),
            (
                None,
                "(1, 1)",
                api_response,
                api_response_pagination,
                "Listing datasets may take a while...",
                True,
            ),
            (
                "Dataset",
                "(1, 1)",
                api_response,
                None,
                "Listing datasets may take a while...\nThere are no datasets found.",
                False,
            ),
            # Invalid cases for find
            (
                "",
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                99,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                {},
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                [],
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                (),
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "(1, 'a')",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, 2, 3)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, )",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, 0)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(0, 0)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, -1)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, 1)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, -1)",
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            # Exception case
            (
                None,
                None,
                api_response,
                None,
                "Listing datasets may take a while...\n[list_datasets]: An error has occurred while listing datasets.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.api_get_all_datasets")
    @patch("moonshot.integrations.cli.benchmark.datasets._display_datasets")
    def test_list_datasets(
        self,
        mock_display_datasets,
        mock_api_get_all_datasets,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_datasets.side_effect = Exception(
                "An error has occurred while listing datasets."
            )
        else:
            mock_api_get_all_datasets.return_value = api_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_datasets(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_datasets.assert_called_once_with(api_response)
        else:
            mock_display_datasets.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_datasets functionality with mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, filtered_response, expected_output, expected_log, to_be_called",
        [
            (
                None,
                None,
                api_response,
                api_response_pagination,
                api_response_pagination,
                "Listing datasets may take a while...",
                True,
            ),
            (
                "squad",
                None,
                api_response,
                api_response_pagination,
                api_response_pagination,
                "Listing datasets may take a while...",
                True,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                api_response_pagination,
                api_response_pagination,
                "Listing datasets may take a while...",
                True,
            ),
            # Case where filtered_response is None
            (
                None,
                None,
                api_response,
                None,
                None,
                "Listing datasets may take a while...\nThere are no datasets found.",
                False,
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                api_response,
                [],
                None,
                "Listing datasets may take a while...\nThere are no datasets found.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.api_get_all_datasets")
    @patch("moonshot.integrations.cli.benchmark.datasets._display_datasets")
    @patch("moonshot.integrations.cli.benchmark.datasets.filter_data")
    def test_list_datasets_filtered(
        self,
        mock_filter_data,
        mock_display_datasets,
        mock_api_get_all_datasets,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        mock_api_get_all_datasets.return_value = api_response
        mock_filter_data.return_value = filtered_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_datasets(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_datasets.assert_called_once_with(filtered_response)
        else:
            mock_display_datasets.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test view_dataset functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "dataset_filename, api_response, api_name_response, expected_log, to_be_called",
        [
            # Valid case
            (
                "squad-shifts-tnf",
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...",
                True,
            ),
            # Invalid case: dataset_filename is None
            (
                None,
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case: dataset_filename is not a string
            (
                "",
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: The 'dataset_filename' argument must be a non-empty string and not None.",
                False,
            ),
            # Exception case: api_get_all_datasets raises an exception
            (
                "squad-shifts-tnf",
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: An error has occurred while reading the datasets.",
                False,
            ),
            # Exception case: api_get_all_datasets_name raises an exception
            (
                "squad-shifts-tnf",
                api_response,
                ["squad-shifts-tnf"],
                "Viewing datasets may take a while...\n[view_dataset]: An error has occurred while reading the dataset names.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.api_get_all_datasets")
    @patch("moonshot.integrations.cli.benchmark.datasets.api_get_all_datasets_name")
    @patch("moonshot.integrations.cli.benchmark.datasets._display_datasets")
    def test_view_dataset(
        self,
        mock_display_datasets,
        mock_api_get_all_datasets_name,
        mock_api_get_all_datasets,
        dataset_filename,
        api_response,
        api_name_response,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            if "reading the datasets." in expected_log:
                mock_api_get_all_datasets.side_effect = Exception(
                    "An error has occurred while reading the datasets."
                )
            if "reading the dataset names." in expected_log:
                mock_api_get_all_datasets_name.side_effect = Exception(
                    "An error has occurred while reading the dataset names."
                )
        else:
            mock_api_get_all_datasets.return_value = api_response
            mock_api_get_all_datasets_name.return_value = api_name_response

        class Args:
            pass

        args = Args()
        args.dataset_filename = dataset_filename

        view_dataset(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_display_datasets.assert_called_once_with(api_response)
        else:
            mock_display_datasets.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test delete_dataset functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "dataset, expected_log, to_be_called",
        [
            # Valid case
            ("Dataset 1", "[delete_dataset]: Dataset deleted.", True),
            # Invalid case - dataset
            (
                "",
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_dataset]: The 'dataset' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.api_delete_dataset")
    def test_delete_dataset(
        self, mock_api_delete_dataset, capsys, dataset, expected_log, to_be_called
    ):
        class Args:
            pass

        args = Args()
        args.dataset = dataset

        with patch(
            "moonshot.integrations.cli.benchmark.datasets.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.benchmark.datasets.console.print"):
                delete_dataset(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_dataset.assert_called_once_with(args.dataset)
        else:
            mock_api_delete_dataset.assert_not_called()

    @patch(
        "moonshot.integrations.cli.benchmark.datasets.console.input", return_value="y"
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.api_delete_dataset")
    def test_delete_dataset_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.dataset = "test_dataset_id"

        delete_dataset(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the dataset (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_dataset_id")

    @patch(
        "moonshot.integrations.cli.benchmark.datasets.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.api_delete_dataset")
    def test_delete_dataset_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.dataset = "test_dataset_id"

        delete_dataset(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the dataset (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch(
        "moonshot.integrations.cli.benchmark.datasets.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.benchmark.datasets.console.print")
    @patch("moonshot.integrations.cli.benchmark.datasets.api_delete_dataset")
    def test_delete_dataset_cancelled_output(self, mock_delete, mock_print, mock_input):
        args = MagicMock()
        args.dataset = "test_dataset_id"

        delete_dataset(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the dataset (y/N)? [/]"
        )
        mock_print.assert_called_once_with(
            "[bold yellow]Dataset deletion cancelled.[/]"
        )
        mock_delete.assert_not_called()
