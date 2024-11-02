from unittest.mock import MagicMock, patch

import pytest

from moonshot.integrations.cli.benchmark.runner import (
    delete_runner,
    list_runners,
    view_runner,
)


class TestCollectionCliRunner:
    api_response_read_runner = [
        {
            "id": "my-new-recipe-runner",
            "name": "my new recipe runner",
            "database_file": "generated-outputs/databases/my-new-recipe-runner.db",
            "endpoints": ["openai-gpt35-turbo"],
            "description": "",
        }
    ]
    api_response_runs = [
        {
            "metadata": {
                "id": "my-new-recipe-runner",
                "start_time": "2024-08-17 13:52:16",
                "end_time": "2024-08-17 13:52:48",
                "duration": 32,
                "status": "completed",
                "recipes": ["bbq", "mmlu"],
                "cookbooks": None,
                "endpoints": ["openai-gpt35-turbo"],
                "prompt_selection_percentage": 100,
                "random_seed": 1,
                "system_prompt": "You are an intelligent AI",
            },
            "results": {
                "recipes": [
                    {
                        "id": "bbq",
                        "details": [
                            {
                                "model_id": "openai-gpt35-turbo",
                                "dataset_id": "bbq-lite-disability-status-ambiguous",
                                "prompt_template_id": "mcq-template",
                                "data": [
                                    {
                                        "prompt": '"Some prompts.',
                                        "predicted_result": "A. Can't be determined",
                                        "target": "A. Can't be determined",
                                        "duration": 8.763961791002657,
                                    }
                                ],
                                "metrics": [
                                    {
                                        "accuracy": 100.0,
                                        "grading_criteria": {"accuracy": 100.0},
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "evaluation_summary": [
                    {
                        "model_id": "openai-gpt35-turbo",
                        "num_of_prompts": 1,
                        "avg_grade_value": 0.0,
                        "grade": "E",
                    }
                ],
                "grading_scale": {
                    "A": [80, 100],
                    "B": [60, 79],
                    "C": [40, 59],
                    "D": [20, 39],
                    "E": [0, 19],
                },
                "total_num_of_prompts": 1,
            },
        }
    ]
    api_response_session = None

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test list_runner functionality    # TODO
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # Test view_runner functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id, api_response_read_runner, api_response_runs, api_response_session, expected_log, to_be_called, read_runner_called, get_all_run_called, load_session_called",
        [
            # Valid case
            (
                "1",
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "",
                True,
                True,
                True,
                True,
            ),
            # Invalid case: runner_id is None
            (
                None,
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            # Invalid case: runner_id is not a string
            (
                "",
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            (
                123,
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            (
                {},
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            (
                [],
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            (
                (),
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            (
                True,
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
                False,
                False,
                False,
            ),
            # Exception case: api_read_runner raises an exception
            (
                "1",
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: An error has occurred while reading the runner.",
                False,
                True,
                False,
                False,
            ),
            # Exception case: api_get_all_run raises an exception
            (
                "1",
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: An error has occurred while reading the runs.",
                False,
                True,
                True,
                False,
            ),
            # Exception case: api_load_session raises an exception
            (
                "1",
                api_response_read_runner,
                api_response_runs,
                api_response_session,
                "[view_runner]: An error has occurred while reading the sessions.",
                False,
                True,
                True,
                True,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.runner.api_read_runner")
    @patch("moonshot.integrations.cli.benchmark.runner.api_get_all_run")
    @patch("moonshot.integrations.cli.benchmark.runner.api_load_session")
    @patch("moonshot.integrations.cli.benchmark.runner._display_runners")
    def test_view_runner(
        self,
        mock_display_runners,
        mock_api_load_session,
        mock_api_get_all_run,
        mock_api_read_runner,
        runner_id,
        api_response_read_runner,
        api_response_runs,
        api_response_session,
        expected_log,
        to_be_called,
        read_runner_called,
        get_all_run_called,
        load_session_called,
        capsys,
    ):
        if "error has occurred while reading the runner." in expected_log:
            mock_api_read_runner.side_effect = Exception(
                "An error has occurred while reading the runner."
            )
        else:
            mock_api_read_runner.return_value = api_response_read_runner

        if "error has occurred while reading the runs." in expected_log:
            mock_api_get_all_run.side_effect = Exception(
                "An error has occurred while reading the runs."
            )
        else:
            mock_api_get_all_run.return_value = api_response_runs

        if "error has occurred while reading the sessions." in expected_log:
            mock_api_load_session.side_effect = Exception(
                "An error has occurred while reading the sessions."
            )
        else:
            mock_api_load_session.return_value = api_response_session

        class Args:
            pass

        args = Args()
        args.runner = runner_id

        view_runner(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_display_runners.assert_called_once_with(
                [api_response_read_runner], api_response_runs, [api_response_session]
            )
        else:
            mock_display_runners.assert_not_called()

        if read_runner_called:
            mock_api_read_runner.assert_called_once()
        else:
            mock_api_read_runner.assert_not_called()

        if get_all_run_called:
            mock_api_get_all_run.assert_called_once()
        else:
            mock_api_get_all_run.assert_not_called()

        if load_session_called:
            mock_api_load_session.assert_called_once()
        else:
            mock_api_load_session.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test delete_runner functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner, expected_log, to_be_called",
        [
            # Valid case
            ("Runner 1", "[delete_runner]: Runner deleted.", True),
            # Invalid case - runner
            (
                "",
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_runner]: The 'runner' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.runner.api_delete_runner")
    def test_delete_runner(
        self, mock_api_delete_runner, capsys, runner, expected_log, to_be_called
    ):
        class Args:
            pass

        args = Args()
        args.runner = runner

        with patch(
            "moonshot.integrations.cli.benchmark.runner.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.benchmark.runner.console.print"):
                delete_runner(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_runner.assert_called_once_with(args.runner)
        else:
            mock_api_delete_runner.assert_not_called()

    @patch("moonshot.integrations.cli.benchmark.runner.console.input", return_value="y")
    @patch("moonshot.integrations.cli.benchmark.runner.api_delete_runner")
    def test_delete_runner_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.runner = "test_runner_id"

        delete_runner(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the runner (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_runner_id")

    @patch("moonshot.integrations.cli.benchmark.runner.console.input", return_value="n")
    @patch("moonshot.integrations.cli.benchmark.runner.api_delete_runner")
    def test_delete_runner_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.runner = "test_runner_id"

        delete_runner(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the runner (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch("moonshot.integrations.cli.benchmark.runner.console.input", return_value="n")
    @patch("moonshot.integrations.cli.benchmark.runner.console.print")
    @patch("moonshot.integrations.cli.benchmark.runner.api_delete_runner")
    def test_delete_runner_cancelled_output(self, mock_delete, mock_print, mock_input):
        args = MagicMock()
        args.runner = "test_runner_id"

        delete_runner(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the runner (y/N)? [/]"
        )
        mock_print.assert_called_once_with("[bold yellow]Runner deletion cancelled.[/]")
        mock_delete.assert_not_called()
