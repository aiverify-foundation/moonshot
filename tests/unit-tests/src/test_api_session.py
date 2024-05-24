import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_create_session,
    api_delete_session,
    api_get_all_chats_from_session,
    api_get_all_session_metadata,
    api_get_all_session_names,
    api_get_available_session_info,
    api_load_runner,
    api_load_session,
    api_set_environment_variables,
    api_update_attack_module,
    api_update_context_strategy,
    api_update_cs_num_of_prev_prompts,
    api_update_metric,
    api_update_prompt_template,
    api_update_system_prompt,
)
from moonshot.src.redteaming.session.session import Session


class TestCollectionApiSession:
    @pytest.fixture(autouse=True)
    def init(self):
        # Set environment variables for session paths
        api_set_environment_variables(
            {
                "ATTACK_MODULES": "tests/unit-tests/src/data/attack-modules/",
                "METRICS": "tests/unit-tests/src/data/metrics/",
                "CONTEXT_STRATEGY": "tests/unit-tests/src/data/context-strategy/",
                "SESSIONS": "tests/unit-tests/src/data/sessions/",
                "RUNNERS": "tests/unit-tests/src/data/runners/",
                "DATABASES": "tests/unit-tests/src/data/databases/",
                "DATABASES_MODULES": "tests/unit-tests/src/data/databases-modules/",
                "CONNECTORS_ENDPOINTS": "tests/unit-tests/src/data/connectors-endpoints/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
                "PROMPT_TEMPLATES": "tests/unit-tests/src/data/prompt-templates/",
            }
        )

        # Copy data
        shutil.copyfile(
            "tests/unit-tests/common/samples/sample_attack_module.py",
            "tests/unit-tests/src/data/attack-modules/sample_attack_module.py",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/advglue.py",
            "tests/unit-tests/src/data/metrics/advglue.py",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/answer-template.json",
            "tests/unit-tests/src/data/prompt-templates/answer-template.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/add_previous_prompt.py",
            "tests/unit-tests/src/data/context-strategy/add_previous_prompt.py",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/runners/my-new-recipe-runner.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-runner.json",
            "tests/unit-tests/src/data/runners/my-runner.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/openai-gpt4.json",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-new-recipe-runner.db",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner.db",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/my-runner.db",
            "tests/unit-tests/src/data/databases/my-runner.db",
        )

        # Setup complete, proceed with tests
        yield

        # Delete the session data using os.remove
        session_data_files = [
            "tests/unit-tests/src/data/runners/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/connectors-endpoints/openai-gpt4.json",
            "tests/unit-tests/src/data/databases/my-new-recipe-runner.db",
            "tests/unit-tests/src/data/sessions/my-new-recipe-runner.json",
            "tests/unit-tests/src/data/runners/my-runner.json",
            "tests/unit-tests/src/data/databases/my-runner.db",
            "tests/unit-tests/src/data/context-strategy/add_previous_prompt.py",
            "tests/unit-tests/src/data/prompt-templates/answer-template.json",
            "tests/unit-tests/src/data/metrics/advglue.py",
            "tests/unit-tests/src/data/metrics/cache.json",
            "tests/unit-tests/src/data/metrics/metrics_config.json",
            "tests/unit-tests/src/data/attack-modules/sample_attack_module.py",
            "tests/unit-tests/src/data/attack-modules/cache.json",
        ]
        for session_data_file in session_data_files:
            if os.path.exists(session_data_file):
                os.remove(session_data_file)

    # ------------------------------------------------------------------------------
    # Test api_create_session functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, expected_dict",
        [
            # Valid case
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {"expected_output": True, "expected_id": "my-new-session"},
            ),
            (
                {
                    "runner_id": "none",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": True,
                    "expected_id": "none",
                },
            ),
            # Invalid cases for runner_id
            (
                {
                    "runner_id": "my new session 1",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session-1",
                    "expected_error_message": "[Session] Failed to initialise Session. Invalid Runner ID.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {
                    "runner_id": "my_new-ses sion 1@.!23",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-ses-sion-1-23",
                    "expected_error_message": "[Session] Failed to initialise Session. Invalid Runner ID.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {
                    "runner_id": "",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "",
                    "expected_error_message": "[Session] Failed to initialise Session. String should have at least 1 character.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {
                    "runner_id": None,
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": [],
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": {},
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": 123,
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for database instance
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": None,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "[Session] Failed to initialise Session. No database instance provided.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": [],
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "[Session] Failed to initialise Session. No database instance provided.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": {},
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "[Session] Failed to initialise Session. No database instance provided.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": 123,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "[Session] Failed to initialise Session. No database instance provided.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Invalid cases for endpoints
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": "",
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": None,
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4", 123],
                    "runner_args": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for runner_args
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": "",
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": None,
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "runner_id": "my-new-session",
                    "database_instance": True,
                    "endpoints": ["openai-gpt4"],
                    "runner_args": 123,
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-session",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_create_session(self, input_args, expected_dict):
        """
        Test the api_create_session function with various input arguments and expected outcomes.

        This test uses parametrized input arguments and expected dictionaries to validate both successful
        session creation and proper handling of invalid inputs through exceptions.

        Args:
            input_args (dict): A dictionary containing the input parameters to the api_create_session function.
            expected_dict (dict): A dictionary containing the expected result of the test case. This includes
                                  the expected output, expected ID, expected error message, and expected exception.

        The test cases include:
        - Valid cases with proper input arguments that should result in successful session creation.
        - Invalid cases with improper input arguments that should raise specific exceptions with appropriate error messages.
        """
        if input_args["database_instance"] is True:
            runner_instance = api_load_runner("my-new-recipe-runner", None)
            input_args["database_instance"] = runner_instance.database_instance

        if expected_dict["expected_output"]:
            # Test valid cases where session creation should succeed.
            session_instance = api_create_session(
                input_args["runner_id"],
                input_args["database_instance"],
                input_args["endpoints"],
                input_args["runner_args"],
            )
            assert isinstance(session_instance, Session)
            assert session_instance.runner_id == expected_dict["expected_id"]
            assert session_instance.database_instance == input_args["database_instance"]
            assert session_instance.runner_args == input_args["runner_args"]
        else:
            # Test invalid cases where session creation should fail and raise an exception.
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_session(
                        input_args["runner_id"],
                        input_args["database_instance"],
                        input_args["endpoints"],
                        input_args["runner_args"],
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_session(
                        input_args["runner_id"],
                        input_args["database_instance"],
                        input_args["endpoints"],
                        input_args["runner_args"],
                    )
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                # If an unexpected exception is specified, fail the test.
                assert False

    # ------------------------------------------------------------------------------
    # Test api_load_session functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,expected_dict",
        [
            # Valid case - No session in db
            (
                "my-new-recipe-runner",
                {
                    "expected_output": "NoSession",
                },
            ),
            # Valid case - Session in db
            (
                "my-runner",
                {
                    "expected_output": True,
                    "id": "my-runner",
                    "endpoints": ["openai-gpt4"],
                },
            ),
            # Invalid cases
            # Runner Id
            (
                "vanilla-cake",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_load_session(self, runner_id, expected_dict):
        if expected_dict["expected_output"] is True:
            session_details = api_load_session(runner_id)
            assert isinstance(session_details, dict)
            assert session_details["session_id"] == expected_dict["id"]
            assert session_details["endpoints"] == expected_dict["endpoints"]
        elif expected_dict["expected_output"] == "NoSession":
            session_details = api_load_session(runner_id)
            assert session_details is None
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_load_session(runner_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_load_session(runner_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_get_all_session_names functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_session_names(self):
        """
        Test the api_get_all_session_names function.

        This test ensures that the api_get_all_session_names function returns a list containing the correct session names.
        """
        expected_session_names = ["my-runner"]

        session_names_response = api_get_all_session_names()
        assert len(session_names_response) == len(
            expected_session_names
        ), "The number of session names returned does not match the expected count."
        for session_name in session_names_response:
            assert (
                session_name in expected_session_names
            ), f"Session name '{session_name}' is not in the list of expected session names."

    # ------------------------------------------------------------------------------
    # Test api_get_all_session_info functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_session_info(self):
        """
        Test the api_get_all_session_info function.

        This test ensures that the api_get_all_session_info function returns a list of session information that matches the expected sessions list.
        Each session in the returned list is checked against the expected sessions to ensure that all details are correct.
        """
        expected_sessions = [
            ["my-runner"],
            [
                {
                    "session_id": "my-runner",
                    "endpoints": ["openai-gpt4"],
                    "created_epoch": "1716384698.5068061",
                    "created_datetime": "20240522-213138",
                    "prompt_template": "mmlu",
                    "context_strategy": "add_previous_prompt",
                    "cs_num_of_prev_prompts": 5,
                    "attack_module": "",
                    "metric": "",
                    "system_prompt": "",
                }
            ],
        ]

        actual_sessions = api_get_available_session_info()
        assert len(actual_sessions) == len(
            expected_sessions
        ), "The number of sessions returned does not match the expected count."

        for session in actual_sessions:
            assert (
                session in expected_sessions
            ), f"The session data {session} does not match any expected session."

    # ------------------------------------------------------------------------------
    # Test api_get_all_session_metadata functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_session_metadata(self):
        """
        Test the api_get_all_session_metadata function.

        This test ensures that the api_get_all_session_metadata function returns a list of session metadata that matches the expected metadata list.
        Each session metadata in the returned list is checked against the expected metadata to ensure that all details are correct.
        """
        expected_session_metadata = [
            {
                "session_id": "my-runner",
                "endpoints": ["openai-gpt4"],
                "created_epoch": "1716384698.5068061",
                "created_datetime": "20240522-213138",
                "prompt_template": "mmlu",
                "context_strategy": "add_previous_prompt",
                "cs_num_of_prev_prompts": 5,
                "attack_module": "",
                "metric": "",
                "system_prompt": "",
            }
        ]

        actual_session_metadata = api_get_all_session_metadata()
        assert len(actual_session_metadata) == len(
            expected_session_metadata
        ), "The number of session metadata entries returned does not match the expected count."

        for metadata in actual_session_metadata:
            assert (
                metadata in expected_session_metadata
            ), f"The session metadata {metadata} does not match any expected metadata."

    # ------------------------------------------------------------------------------
    # Test api_update_context_strategy functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,context_strategy,expected_dict",
        [
            # Valid case
            (
                "my-runner",
                "add_previous_prompt",
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-runner",
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                "add_previous_prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid context strategy
            (
                "my-runner",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_context_strategy(
        self, runner_id: str, context_strategy: str, expected_dict: dict
    ):
        """
        Test the API update context strategy functionality.

        This test checks if the API update context strategy behaves as expected when provided with
        different runner IDs and context strategies. It tests for both successful updates and
        various error scenarios.

        Args:
            runner_id (str): The runner ID to update.
            context_strategy (str): The context strategy to be updated.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_context_strategy(runner_id, context_strategy)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_context_strategy(runner_id, context_strategy)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_context_strategy(runner_id, context_strategy)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_update_cs_num_of_prev_prompts functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,num_of_prev_prompts,expected_dict",
        [
            # Valid case
            (
                "my-runner",
                5,
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-runner",
                3,
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                2,
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                1,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                0,
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                4,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                3,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                2,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid number of previous prompts
            (
                "my-runner",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid integer",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid integer",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid integer",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_cs_num_of_prev_prompts(
        self, runner_id: str, num_of_prev_prompts: int, expected_dict: dict
    ):
        """
        Test the API update number of previous prompts functionality.

        This test checks if the API update number of previous prompts behaves as expected when provided with
        different runner IDs and numbers of previous prompts. It tests for both successful updates and
        various error scenarios.

        Args:
            runner_id (str): The runner ID to update.
            num_of_prev_prompts (int): The number of previous prompts to be updated.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_cs_num_of_prev_prompts(runner_id, num_of_prev_prompts)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_cs_num_of_prev_prompts(runner_id, num_of_prev_prompts)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_cs_num_of_prev_prompts(runner_id, num_of_prev_prompts)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_update_prompt_template functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,prompt_template,expected_dict",
        [
            # Valid case
            (
                "my-runner",
                "answer-template",
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-runner",
                "Some prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                "Another prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                "Invalid prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                "Yet another prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                "Empty prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                "No prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                "123 prompt template",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid prompt template
            (
                "my-runner",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_prompt_template(
        self, runner_id: str, prompt_template: str, expected_dict: dict
    ):
        """
        Test the API update prompt template functionality.

        This test checks if the API update prompt template behaves as expected when provided with
        different runner IDs and prompt templates. It tests for both successful updates and
        various error scenarios.

        Args:
            runner_id (str): The runner ID to update.
            prompt_template (str): The new prompt template to be updated.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_prompt_template(runner_id, prompt_template)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_prompt_template(runner_id, prompt_template)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_prompt_template(runner_id, prompt_template)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_update_metric functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,metric_id,expected_dict",
        [
            # Valid case
            (
                "my-runner",
                "advglue",
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-runner",
                "metric-100",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                "metric-0",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                "invalid-metric",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                "metric-123.456",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                "metric-0",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                "metric-1",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                "metric-2",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid metric id
            (
                "my-runner",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_metric(
        self, runner_id: str, metric_id: str, expected_dict: dict
    ):
        """
        Test the API update metric functionality.

        This test checks if the API update metric behaves as expected when provided with
        different runner IDs and metric IDs. It tests for both successful updates and
        various error scenarios.

        Args:
            runner_id (str): The runner ID to update.
            metric_id (str): The new metric ID to be updated.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_metric(runner_id, metric_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_metric(runner_id, metric_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_metric(runner_id, metric_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_update_system_prompt functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,system_prompt,expected_dict",
        [
            # Valid case
            (
                "my-runner",
                "new-system-prompt",
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-runner",
                "prompt-100",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                "prompt-0",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                "invalid-prompt",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                "prompt-123.456",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                "prompt-0",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                "prompt-1",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                "prompt-2",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid system prompt
            (
                "my-runner",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_system_prompt(
        self, runner_id: str, system_prompt: str, expected_dict: dict
    ):
        """
        Test the API update system prompt functionality.

        This test checks if the API update system prompt behaves as expected when provided with
        different runner IDs and system prompts. It tests for both successful updates and
        various error scenarios.

        Args:
            runner_id (str): The runner ID to update.
            system_prompt (str): The new system prompt to be updated.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_system_prompt(runner_id, system_prompt)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_system_prompt(runner_id, system_prompt)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_system_prompt(runner_id, system_prompt)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_update_attack_module functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "runner_id,attack_module_id,expected_dict",
        [
            # Valid case
            (
                "my-runner",
                "sample_attack_module",
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "nonexistent-runner",
                "module-100",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                "module-0",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                "invalid-module",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                "module-123.456",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                "module-0",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                "module-1",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                "module-2",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid attack module
            (
                "my-runner",
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "my-runner",
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_attack_module(
        self, runner_id: str, attack_module_id: str, expected_dict: dict
    ):
        """
        Test the API update attack module functionality.

        This test checks if the API update attack module behaves as expected when provided with
        different runner IDs and attack modules. It tests for both successful updates and
        various error scenarios.

        Args:
            runner_id (str): The runner ID to update.
            attack_module_id (str): The new attack module to be updated.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_attack_module(runner_id, attack_module_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_attack_module(runner_id, attack_module_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_attack_module(runner_id, attack_module_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_delete_session functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "session_id,expected_dict",
        [
            # Valid case
            ("my-runner", {"expected_output": True}),
            # Invalid cases
            (
                "nonexistent_session",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_delete_session(self, session_id, expected_dict):
        """
        Test the api_delete_session function.

        This test checks if the function either returns the expected output or raises the expected exception with the correct error message.

        Args:
            session_id: The session ID to delete.
            expected_dict: A dictionary containing the 'expected_output', 'expected_error_message', and 'expected_exception' keys.
        """
        if expected_dict["expected_output"]:
            response = api_delete_session(session_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_session does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_session(session_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_session(session_id)
                assert (
                    len(e.value.errors()) == 1
                ), "The number of validation errors does not match the expected count."
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                ), "The validation error message does not contain the expected text."

            else:
                assert (
                    False
                ), "An unexpected exception type was specified in the test parameters."

    # ------------------------------------------------------------------------------
    # Test api_get_all_chats_from_session functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "session_id,expected_dict",
        [
            # Valid case
            ("my-runner", {"expected_output": {"openai-gpt4": []}}),
            # Invalid cases
            (
                "nonexistent_session",
                {
                    "expected_output": None,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": None,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "expected_output": None,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": None,
                    "expected_error_message": "[Runner] Unable to load runner because the runner file does not exist.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "expected_output": None,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "expected_output": None,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": None,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_get_all_chats_from_session(self, session_id, expected_dict):
        """
        Test the api_get_all_chats_from_session function.

        This test checks if the function either returns the expected output or raises the expected exception with the correct error message.

        Args:
            session_id: The session ID from which to retrieve all chats.
            expected_dict: A dictionary containing the 'expected_output', 'expected_error_message', and 'expected_exception' keys.
        """
        if expected_dict["expected_output"] is not None:
            response = api_get_all_chats_from_session(session_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_get_all_chats_from_session does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_get_all_chats_from_session(session_id)
                assert (
                    str(e.value) == expected_dict["expected_error_message"]
                ), "The error message does not match the expected error message."

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_get_all_chats_from_session(session_id)
                assert (
                    len(e.value.errors()) == 1
                ), "The number of validation errors does not match the expected count."
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                ), "The validation error message does not contain the expected text."

            else:
                assert (
                    False
                ), "An unexpected exception type was specified in the test parameters."
