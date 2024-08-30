from unittest.mock import MagicMock, patch

import pytest

from moonshot.integrations.cli.benchmark.metrics import (
    delete_metric,
    list_metrics,
    view_metric,
)


class TestCollectionCliMetrics:
    api_response = [
        {
            "id": "bertscore",
            "name": "BertScore",
            "description": "Some description",
        }
    ]
    api_response_pagination = [
        {
            "id": "bertscore",
            "name": "BertScore",
            "description": "Some description",
            "idx": 1,
        }
    ]

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test list_metrics functionality with non-mocked filter-data
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
                "Listing metrics may take a while...",
                True,
            ),
            # No metrics
            (
                None,
                None,
                [],
                None,
                "Listing metrics may take a while...\nThere are no metrics found.",
                False,
            ),
            (
                "bert",
                None,
                api_response,
                api_response,
                "Listing metrics may take a while...",
                True,
            ),
            (
                None,
                "(1, 1)",
                api_response,
                api_response_pagination,
                "Listing metrics may take a while...",
                True,
            ),
            (
                "Metrics",
                "(1, 1)",
                api_response,
                None,
                "Listing metrics may take a while...\nThere are no metrics found.",
                False,
            ),
            # Invalid cases for find
            (
                "",
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                99,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                {},
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                [],
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                (),
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "(1, 'a')",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, 2, 3)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, )",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, 0)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(0, 0)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, -1)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, 1)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, -1)",
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            # Exception case
            (
                None,
                None,
                api_response,
                None,
                "Listing metrics may take a while...\n[list_metrics]: An error has occurred while listing metrics.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.api_get_all_metric")
    @patch("moonshot.integrations.cli.benchmark.metrics._display_metrics")
    def test_list_metrics(
        self,
        mock_display_metrics,
        mock_api_get_all_metrics,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_metrics.side_effect = Exception(
                "An error has occurred while listing metrics."
            )
        else:
            mock_api_get_all_metrics.return_value = api_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_metrics(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_metrics.assert_called_once_with(api_response)
        else:
            mock_display_metrics.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_metrics functionality with mocked filter-data
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
                "Listing metrics may take a while...",
                True,
            ),
            (
                "squad",
                None,
                api_response,
                api_response_pagination,
                api_response_pagination,
                "Listing metrics may take a while...",
                True,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                api_response_pagination,
                api_response_pagination,
                "Listing metrics may take a while...",
                True,
            ),
            # Case where filtered_response is None
            (
                None,
                None,
                api_response,
                None,
                None,
                "Listing metrics may take a while...\nThere are no metrics found.",
                False,
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                api_response,
                [],
                None,
                "Listing metrics may take a while...\nThere are no metrics found.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.api_get_all_metric")
    @patch("moonshot.integrations.cli.benchmark.metrics._display_metrics")
    @patch("moonshot.integrations.cli.benchmark.metrics.filter_data")
    def test_list_metrics_filtered(
        self,
        mock_filter_data,
        mock_display_metrics,
        mock_api_get_all_metrics,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        mock_api_get_all_metrics.return_value = api_response
        mock_filter_data.return_value = filtered_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_metrics(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_metrics.assert_called_once_with(filtered_response)
        else:
            mock_display_metrics.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test view_metric functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "metric_filename, api_response, api_name_response, expected_log, to_be_called",
        [
            # Valid case
            (
                "bertscore",
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...",
                True,
            ),
            # Invalid case: metric_filename is None
            (
                None,
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case: metric_filename is not a string
            (
                "",
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: The 'metric_filename' argument must be a non-empty string and not None.",
                False,
            ),
            # Exception case: api_get_all_metrics raises an exception
            (
                "bertscore",
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: An error has occurred while reading the metrics.",
                False,
            ),
            # Exception case: api_get_all_metric_name raises an exception
            (
                "bertscore",
                api_response,
                ["bertscore"],
                "Viewing metrics may take a while...\n[view_metric]: An error has occurred while reading the metric names.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.api_get_all_metric")
    @patch("moonshot.integrations.cli.benchmark.metrics.api_get_all_metric_name")
    @patch("moonshot.integrations.cli.benchmark.metrics._display_metrics")
    def test_view_metric(
        self,
        mock_display_metrics,
        mock_api_get_all_metric_name,
        mock_api_get_all_metrics,
        metric_filename,
        api_response,
        api_name_response,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            if "reading the metrics." in expected_log:
                mock_api_get_all_metrics.side_effect = Exception(
                    "An error has occurred while reading the metrics."
                )
            if "reading the metric names." in expected_log:
                mock_api_get_all_metric_name.side_effect = Exception(
                    "An error has occurred while reading the metric names."
                )
        else:
            mock_api_get_all_metrics.return_value = api_response
            mock_api_get_all_metric_name.return_value = api_name_response

        class Args:
            pass

        args = Args()
        args.metric_filename = metric_filename

        view_metric(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_display_metrics.assert_called_once_with(api_response)
        else:
            mock_display_metrics.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test delete_metric functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "metric, expected_log, to_be_called",
        [
            # Valid case
            ("Metric 1", "[delete_metric]: Metric deleted.", True),
            # Invalid case - metric
            (
                "",
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_metric]: The 'metric' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.api_delete_metric")
    def test_delete_metric(
        self, mock_api_delete_metric, capsys, metric, expected_log, to_be_called
    ):
        class Args:
            pass

        args = Args()
        args.metric = metric

        with patch(
            "moonshot.integrations.cli.benchmark.metrics.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.benchmark.metrics.console.print"):
                delete_metric(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_metric.assert_called_once_with(args.metric)
        else:
            mock_api_delete_metric.assert_not_called()

    @patch(
        "moonshot.integrations.cli.benchmark.metrics.console.input", return_value="y"
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.api_delete_metric")
    def test_delete_metric_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.metric = "test_metric_id"

        delete_metric(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the metric (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_metric_id")

    @patch(
        "moonshot.integrations.cli.benchmark.metrics.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.api_delete_metric")
    def test_delete_metric_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.metric = "test_metric_id"

        delete_metric(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the metric (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch(
        "moonshot.integrations.cli.benchmark.metrics.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.benchmark.metrics.console.print")
    @patch("moonshot.integrations.cli.benchmark.metrics.api_delete_metric")
    def test_delete_metric_cancelled_output(self, mock_delete, mock_print, mock_input):
        args = MagicMock()
        args.metric = "test_metric_id"

        delete_metric(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the metric (y/N)? [/]"
        )
        mock_print.assert_called_once_with("[bold yellow]Metric deletion cancelled.[/]")
        mock_delete.assert_not_called()
