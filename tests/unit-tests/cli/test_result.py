from unittest.mock import MagicMock, patch

import pytest

from moonshot.integrations.cli.benchmark.result import (
    delete_result,
    list_results,
    view_result,
)


class TestCollectionCliResult:
    api_response = [
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
    api_response_pagination = [
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
            "idx": 1,
        }
    ]
    api_read_response_recipe = {
        "metadata": {
            "id": "my-new-recipe-runner",
            "start_time": "2024-08-17 13:52:16",
            "end_time": "2024-08-17 13:52:48",
            "duration": 32,
            "status": "completed",
            "recipes": ["mmlu"],
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
    api_read_response_cookbook = {
        "metadata": {
            "id": "my-new-recipe-runner",
            "start_time": "2024-08-17 13:52:16",
            "end_time": "2024-08-17 13:52:48",
            "duration": 32,
            "status": "completed",
            "recipes": None,
            "cookbooks": ["bbq_cookbook"],
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

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test list_results functionality with non-mocked filter-data
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
            # No results
            (
                None,
                None,
                [],
                None,
                "There are no results found.",
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
                "Results",
                "(1, 1)",
                api_response,
                None,
                "There are no results found.",
                False,
            ),
            # Invalid cases for find
            (
                "",
                None,
                api_response,
                None,
                "[list_results]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                None,
                api_response,
                None,
                "[list_results]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                None,
                api_response,
                None,
                "[list_results]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                None,
                api_response,
                None,
                "[list_results]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                None,
                api_response,
                None,
                "[list_results]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                None,
                api_response,
                None,
                "[list_results]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                99,
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                {},
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                [],
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                (),
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "(1, 'a')",
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, 2, 3)",
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, )",
                api_response,
                None,
                "[list_results]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                None,
                "[list_results]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, 0)",
                api_response,
                None,
                "[list_results]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(0, 0)",
                api_response,
                None,
                "[list_results]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, -1)",
                api_response,
                None,
                "[list_results]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, 1)",
                api_response,
                None,
                "[list_results]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, -1)",
                api_response,
                None,
                "[list_results]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            # Exception case
            (
                None,
                None,
                api_response,
                None,
                "[list_results]: An error has occurred while listing results.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.result.api_get_all_result")
    @patch("moonshot.integrations.cli.benchmark.result._display_results")
    def test_list_results(
        self,
        mock_display_results,
        mock_api_get_all_results,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_results.side_effect = Exception(
                "An error has occurred while listing results."
            )
        else:
            mock_api_get_all_results.return_value = api_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_results(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_results.assert_called_once_with(api_response)
        else:
            mock_display_results.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_results functionality with mocked filter-data
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
                "squad",
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
                "There are no results found.",
                False,
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                api_response,
                [],
                None,
                "There are no results found.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.result.api_get_all_result")
    @patch("moonshot.integrations.cli.benchmark.result._display_results")
    @patch("moonshot.integrations.cli.benchmark.result.filter_data")
    def test_list_results_filtered(
        self,
        mock_filter_data,
        mock_display_results,
        mock_api_get_all_results,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        mock_api_get_all_results.return_value = api_response
        mock_filter_data.return_value = filtered_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_results(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_results.assert_called_once_with(filtered_response)
        else:
            mock_display_results.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test view_result functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "result_filename, api_response, expected_log, expected_cookbook_call, expected_recipe_call",
        [
            # Test for Cookbook Result
            (
                "cookbook_result",
                api_read_response_cookbook,
                None,
                True,
                False,
            ),
            # Test for Recipe Result
            (
                "recipe_result",
                api_read_response_recipe,
                None,
                False,
                True,
            ),
            # Invalid case: result_filename is None
            (
                None,
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            # Invalid case: result_filename is not a string
            (
                "",
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            (
                123,
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            (
                {},
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            (
                [],
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            (
                (),
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            (
                True,
                api_read_response_recipe,
                "[view_result]: The 'result_filename' argument must be a non-empty string and not None.",
                False,
                False,
            ),
            # Invalid case: read result is not correct
            (
                "recipe_result",
                "",
                "[view_result]: The 'metadata' argument not found.",
                False,
                False,
            ),
            (
                "recipe_result",
                123,
                "[view_result]: The 'metadata' argument not found.",
                False,
                False,
            ),
            (
                "recipe_result",
                {},
                "[view_result]: The 'metadata' argument not found.",
                False,
                False,
            ),
            (
                "recipe_result",
                [],
                "[view_result]: The 'metadata' argument not found.",
                False,
                False,
            ),
            (
                "recipe_result",
                (),
                "[view_result]: The 'metadata' argument not found.",
                False,
                False,
            ),
            (
                "recipe_result",
                True,
                "[view_result]: The 'metadata' argument not found.",
                False,
                False,
            ),
            # No recipe or cookbooks
            (
                "no_metadata_result",
                {"metadata": {}},
                "[view_result]: Unable to determine cookbook or recipe",
                False,
                False,
            ),
            # Exception case: api_read_result raises an exception
            (
                "exception_result",
                Exception("Test Exception"),
                "[view_result]: Test Exception",
                False,
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.result.api_read_result")
    @patch("moonshot.integrations.cli.benchmark.result._display_view_recipe_result")
    @patch("moonshot.integrations.cli.benchmark.result._display_view_cookbook_result")
    def test_view_result(
        self,
        mock_display_cookbook,
        mock_display_recipe,
        mock_api_read,
        result_filename,
        api_response,
        expected_log,
        expected_cookbook_call,
        expected_recipe_call,
        capsys,
    ):
        if isinstance(api_response, Exception):
            mock_api_read.side_effect = api_response
        else:
            mock_api_read.return_value = api_response

        class Args:
            pass

        args = Args()
        args.result_filename = result_filename

        view_result(args)

        captured = capsys.readouterr()
        if expected_log:
            assert expected_log in captured.out.strip()
        else:
            assert captured.out.strip() == ""

        if expected_cookbook_call:
            mock_display_cookbook.assert_called_once()
        else:
            mock_display_cookbook.assert_not_called()

        if expected_recipe_call:
            mock_display_recipe.assert_called_once()
        else:
            mock_display_recipe.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test delete_result functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "result, expected_log, to_be_called",
        [
            # Valid case
            ("Result 1", "[delete_result]: Result deleted.", True),
            # Invalid case - result
            (
                "",
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_result]: The 'result' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.result.api_delete_result")
    def test_delete_result(
        self, mock_api_delete_result, capsys, result, expected_log, to_be_called
    ):
        class Args:
            pass

        args = Args()
        args.result = result

        with patch(
            "moonshot.integrations.cli.benchmark.result.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.benchmark.result.console.print"):
                delete_result(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_result.assert_called_once_with(args.result)
        else:
            mock_api_delete_result.assert_not_called()

    @patch("moonshot.integrations.cli.benchmark.result.console.input", return_value="y")
    @patch("moonshot.integrations.cli.benchmark.result.api_delete_result")
    def test_delete_result_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.result = "test_result_id"

        delete_result(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the result (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_result_id")

    @patch("moonshot.integrations.cli.benchmark.result.console.input", return_value="n")
    @patch("moonshot.integrations.cli.benchmark.result.api_delete_result")
    def test_delete_result_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.result = "test_result_id"

        delete_result(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the result (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch("moonshot.integrations.cli.benchmark.result.console.input", return_value="n")
    @patch("moonshot.integrations.cli.benchmark.result.console.print")
    @patch("moonshot.integrations.cli.benchmark.result.api_delete_result")
    def test_delete_result_cancelled_output(self, mock_delete, mock_print, mock_input):
        args = MagicMock()
        args.result = "test_result_id"

        delete_result(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the result (y/N)? [/]"
        )
        mock_print.assert_called_once_with("[bold yellow]Result deletion cancelled.[/]")
        mock_delete.assert_not_called()
