import os
import shutil

import pytest

from moonshot.api import api_get_all_run, api_set_environment_variables
from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_status import RunStatus


class TestCollectionApiRun:
    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        api_set_environment_variables(
            {
                "DATABASES": "tests/unit-tests/src/data/databases/",
                "DATABASES_MODULES": "tests/unit-tests/src/data/databases-modules/",
                "RUNNERS": "tests/unit-tests/src/data/runners/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy run data
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/runners/my-new-recipe-runner.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner.db",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner.db",
        )

        # Perform tests
        yield

        # Delete the run data using os.remove
        run_data_files = [
            "tests/unit-tests/src/data/runners/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner.db",
            "tests/unit-tests/src/data/runners/my-new-recipe-runner-no-db.json",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner-no-db.db",
        ]
        for run_data_file in run_data_files:
            if os.path.exists(run_data_file):
                os.remove(run_data_file)

    # ------------------------------------------------------------------------------
    # Test api_get_all_run functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_run(self):
        """
        Test the api_get_all_run function to ensure it returns the correct list of runs.

        This test compares the output of the api_get_all_run function with a predefined list
        of expected runs. It checks that the number of runs and the content of each run match
        the expected values.
        """
        detected_runs = [
            {
                "run_id": 1,
                "runner_id": "my-new-recipe-runner",
                "runner_type": RunnerType.BENCHMARK,
                "runner_args": {
                    "recipes": ["bbq", "auto-categorisation"],
                    "prompt_selection_percentage": 1,
                    "random_seed": 1,
                    "system_prompt": "You are an intelligent AI",
                    "runner_processing_module": "benchmarking",
                    "result_processing_module": "benchmarking-result",
                },
                "endpoints": ["openai-gpt35-turbo"],
                "results_file": "my-new-recipe-runner.json",
                "start_time": 1716171596.8328981,
                "end_time": 1716171597.730658,
                "duration": 0,
                "error_messages": [],
                "raw_results": {},
                "results": {},
                "status": RunStatus.RUNNING,
            }
        ]

        runs = api_get_all_run()
        assert len(runs) == len(
            detected_runs
        ), "The number of runs returned by api_get_all_run does not match the expected count."

        for run in runs:
            assert (
                run in detected_runs
            ), f"The run with details '{run}' was not found in the list of expected runs."

    # ------------------------------------------------------------------------------
    # Test api_get_all_run functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,expected_dict",
        [
            (
                "invalid_runner",
                {"expected_output": []},
            ),
            (
                "",
                {
                    "expected_output": [
                        {
                            "run_id": 1,
                            "runner_id": "my-new-recipe-runner",
                            "runner_type": RunnerType.BENCHMARK,
                            "runner_args": {
                                "recipes": ["bbq", "auto-categorisation"],
                                "prompt_selection_percentage": 1,
                                "random_seed": 1,
                                "system_prompt": "You are an intelligent AI",
                                "runner_processing_module": "benchmarking",
                                "result_processing_module": "benchmarking-result",
                            },
                            "endpoints": ["openai-gpt35-turbo"],
                            "results_file": "my-new-recipe-runner.json",
                            "start_time": 1716171596.8328981,
                            "end_time": 1716171597.730658,
                            "duration": 0,
                            "error_messages": [],
                            "raw_results": {},
                            "results": {},
                            "status": RunStatus.RUNNING,
                        }
                    ]
                },
            ),
            (
                None,
                {
                    "expected_output": [
                        {
                            "run_id": 1,
                            "runner_id": "my-new-recipe-runner",
                            "runner_type": RunnerType.BENCHMARK,
                            "runner_args": {
                                "recipes": ["bbq", "auto-categorisation"],
                                "prompt_selection_percentage": 1,
                                "random_seed": 1,
                                "system_prompt": "You are an intelligent AI",
                                "runner_processing_module": "benchmarking",
                                "result_processing_module": "benchmarking-result",
                            },
                            "endpoints": ["openai-gpt35-turbo"],
                            "results_file": "my-new-recipe-runner.json",
                            "start_time": 1716171596.8328981,
                            "end_time": 1716171597.730658,
                            "duration": 0,
                            "error_messages": [],
                            "raw_results": {},
                            "results": {},
                            "status": RunStatus.RUNNING,
                        }
                    ]
                },
            ),
            (
                "None",
                {"expected_output": []},
            ),
            (
                {},
                {
                    "expected_output": [
                        {
                            "run_id": 1,
                            "runner_id": "my-new-recipe-runner",
                            "runner_type": RunnerType.BENCHMARK,
                            "runner_args": {
                                "recipes": ["bbq", "auto-categorisation"],
                                "prompt_selection_percentage": 1,
                                "random_seed": 1,
                                "system_prompt": "You are an intelligent AI",
                                "runner_processing_module": "benchmarking",
                                "result_processing_module": "benchmarking-result",
                            },
                            "endpoints": ["openai-gpt35-turbo"],
                            "results_file": "my-new-recipe-runner.json",
                            "start_time": 1716171596.8328981,
                            "end_time": 1716171597.730658,
                            "duration": 0,
                            "error_messages": [],
                            "raw_results": {},
                            "results": {},
                            "status": RunStatus.RUNNING,
                        }
                    ]
                },
            ),
            (
                [],
                {
                    "expected_output": [
                        {
                            "run_id": 1,
                            "runner_id": "my-new-recipe-runner",
                            "runner_type": RunnerType.BENCHMARK,
                            "runner_args": {
                                "recipes": ["bbq", "auto-categorisation"],
                                "prompt_selection_percentage": 1,
                                "random_seed": 1,
                                "system_prompt": "You are an intelligent AI",
                                "runner_processing_module": "benchmarking",
                                "result_processing_module": "benchmarking-result",
                            },
                            "endpoints": ["openai-gpt35-turbo"],
                            "results_file": "my-new-recipe-runner.json",
                            "start_time": 1716171596.8328981,
                            "end_time": 1716171597.730658,
                            "duration": 0,
                            "error_messages": [],
                            "raw_results": {},
                            "results": {},
                            "status": RunStatus.RUNNING,
                        }
                    ]
                },
            ),
            (
                123,
                {"expected_output": []},
            ),
        ],
    )
    def test_api_get_all_run_with_id(self, runner_id, expected_dict):
        """Verify that the api_get_all_run function returns the correct list of runs for a given runner ID.

        Args:
            runner_id (str): The ID of the runner to retrieve runs for.
            expected_dict (dict): A dictionary containing the expected output.

        This test compares the actual list of runs returned by the api_get_all_run function
        against the expected list provided in the expected_dict. It checks both the count
        and the presence of each run in the expected output.
        """
        runs = api_get_all_run(runner_id)
        assert len(runs) == len(
            expected_dict["expected_output"]
        ), "The number of runs returned does not match the expected count."

        for run in runs:
            assert (
                run in expected_dict["expected_output"]
            ), f"The run {run} was not found in the expected list of runs."

    def test_api_get_all_run_no_db(self):
        """
        Test the api_get_all_run function without a database.

        This test checks if the api_get_all_run function correctly returns an empty list
        when there is no database file for the specified runner.
        """
        # Copy a sample runner file to the runners directory to simulate a runner without a database
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner-no-db.json",
            "tests/unit-tests/src/data/runners/my-new-recipe-runner-no-db.json",
        )

        # Call the function with the runner ID and verify that it returns an empty list
        runs = api_get_all_run("my-new-recipe-runner-no-db")
        assert (
            len(runs) == 0
        ), "The number of runners does not match the expected count."
