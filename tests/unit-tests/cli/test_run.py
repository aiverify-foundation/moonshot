from unittest.mock import patch

import pytest

from moonshot.integrations.cli.benchmark.run import list_runs, view_run
from moonshot.src.runners.runner_type import RunnerType


class TestCollectionCliRun:
    api_response = [
        {
            "run_id": 1,
            "runner_id": "my-new-recipe-runner",
            "runner_type": RunnerType.BENCHMARK,
            "runner_args": {
                "recipes": ["bbq"],
                "prompt_selection_percentage": 100,
                "random_seed": 1,
                "system_prompt": "You are an intelligent AI",
                "runner_processing_module": "benchmarking",
                "run_processing_module": "benchmarking-run",
            },
            "endpoints": ["openai-gpt35-turbo"],
            "runs_file": "/generated-outputs/runs/my-new-recipe-runner.json",
            "start_time": 1723873936.436674,
            "end_time": 1723873968.6472352,
            "duration": 32,
            "error_messages": [],
            "raw_runs": {"bbq": "some run"},
        }
    ]

    api_response_pagination = [
        {
            "run_id": 1,
            "runner_id": "my-new-recipe-runner",
            "runner_type": RunnerType.BENCHMARK,
            "runner_args": {
                "recipes": ["bbq"],
                "prompt_selection_percentage": 100,
                "random_seed": 1,
                "system_prompt": "You are an intelligent AI",
                "runner_processing_module": "benchmarking",
                "run_processing_module": "benchmarking-run",
            },
            "endpoints": ["openai-gpt35-turbo"],
            "runs_file": "/generated-outputs/runs/my-new-recipe-runner.json",
            "start_time": 1723873936.436674,
            "end_time": 1723873968.6472352,
            "duration": 32,
            "error_messages": [],
            "raw_runs": {"bbq": "some run"},
            "idx": 1,
        }
    ]

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test list_runs functionality with non-mocked filter-data
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
                "",
                True,
            ),
            # No runs
            (
                None,
                None,
                [],
                None,
                "There are no runs found.",
                False,
            ),
            (
                "my-new-recipe-runner",
                None,
                api_response,
                api_response,
                "",
                True,
            ),
            (
                None,
                "(1, 1)",
                api_response,
                api_response_pagination,
                "",
                True,
            ),
            (
                "Squad",
                "(1, 1)",
                api_response,
                None,
                "There are no runs found.",
                False,
            ),
            # Invalid cases for find
            (
                "",
                None,
                api_response,
                None,
                "[list_runs]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                None,
                api_response,
                None,
                "[list_runs]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                None,
                api_response,
                None,
                "[list_runs]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                None,
                api_response,
                None,
                "[list_runs]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                None,
                api_response,
                None,
                "[list_runs]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                None,
                api_response,
                None,
                "[list_runs]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                99,
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                {},
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                [],
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                (),
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "(1, 'a')",
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, 2, 3)",
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, )",
                api_response,
                None,
                "[list_runs]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                None,
                "[list_runs]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, 0)",
                api_response,
                None,
                "[list_runs]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(0, 0)",
                api_response,
                None,
                "[list_runs]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, -1)",
                api_response,
                None,
                "[list_runs]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, 1)",
                api_response,
                None,
                "[list_runs]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, -1)",
                api_response,
                None,
                "[list_runs]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            # Exception case
            (
                None,
                None,
                api_response,
                None,
                "[list_runs]: An error has occurred while listing runs.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.run.api_get_all_run")
    @patch("moonshot.integrations.cli.benchmark.run._display_runs")
    def test_list_runs(
        self,
        mock_display_runs,
        mock_api_get_all_runs,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_runs.side_effect = Exception(
                "An error has occurred while listing runs."
            )
        else:
            mock_api_get_all_runs.return_value = api_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        run = list_runs(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert run == expected_output

        if to_be_called:
            mock_display_runs.assert_called_once_with(api_response)
        else:
            mock_display_runs.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_runs functionality with mocked filter-data
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
                "",
                True,
            ),
            (
                "my-new-recipe",
                None,
                api_response,
                api_response_pagination,
                api_response_pagination,
                "",
                True,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                api_response_pagination,
                api_response_pagination,
                "",
                True,
            ),
            # Case where filtered_response is None
            (
                None,
                None,
                api_response,
                None,
                None,
                "There are no runs found.",
                False,
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                api_response,
                [],
                None,
                "There are no runs found.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.run.api_get_all_run")
    @patch("moonshot.integrations.cli.benchmark.run._display_runs")
    @patch("moonshot.integrations.cli.benchmark.run.filter_data")
    def test_list_runs_filtered(
        self,
        mock_filter_data,
        mock_display_runs,
        mock_api_get_all_runs,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        mock_api_get_all_runs.return_value = api_response
        mock_filter_data.return_value = filtered_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        run = list_runs(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert run == expected_output

        if to_be_called:
            mock_display_runs.assert_called_once_with(filtered_response)
        else:
            mock_display_runs.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test view_run functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id, api_response, expected_log, expected_call",
        [
            # Test for Cookbook Run
            (
                "runner_id",
                api_response,
                None,
                True,
            ),
            # Invalid case: runner_id is None
            (
                None,
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case: runner_id is not a string
            (
                "",
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                api_response,
                "[view_run]: The 'runner_id' argument must be a non-empty string and not None.",
                False,
            ),
            # Exception case: api_get_all_run raises an exception
            (
                "exception_run",
                Exception("Test Exception"),
                "[view_run]: Test Exception",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.run.api_get_all_run")
    @patch("moonshot.integrations.cli.benchmark.run._display_runs")
    def test_view_run(
        self,
        mock_display_runs,
        mock_api_get_all_run,
        runner_id,
        api_response,
        expected_log,
        expected_call,
        capsys,
    ):
        if isinstance(api_response, Exception):
            mock_api_get_all_run.side_effect = api_response
        else:
            mock_api_get_all_run.return_value = api_response

        class Args:
            pass

        args = Args()
        args.runner_id = runner_id

        view_run(args)

        captured = capsys.readouterr()
        if expected_log:
            assert expected_log in captured.out.strip()
        else:
            assert captured.out.strip() == ""

        if expected_call:
            mock_display_runs.assert_called_once()
        else:
            mock_display_runs.assert_not_called()
