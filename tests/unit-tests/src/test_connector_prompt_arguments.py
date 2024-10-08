import pytest
from pydantic import ValidationError

from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors.connector_response import ConnectorResponse


class TestCollectionConnectorPromptArguments:
    # ------------------------------------------------------------------------------
    # Test ConnectorPromptArguments functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "prompt_index, prompt, target, predicted_results, duration",
        [
            (0, "Prompt 0", "Target 0", None, 0.0),
            (1, "Prompt 1", "Target 1", None, 0.0),
            (2, "Prompt 2", "Target 2", None, 0.255),
            (
                3,
                "Prompt 3",
                "Target 3",
                ConnectorResponse(response="Response 3"),
                0.255,
            ),
        ],
    )
    def test_create_connector_prompt_arguments(
        self, prompt_index, prompt, target, predicted_results, duration
    ):
        # Test creating a valid connector prompt arguments instance
        connector_prompt_arguments = ConnectorPromptArguments(
            prompt_index=prompt_index,
            prompt=prompt,
            target=target,
            predicted_results=predicted_results,
            duration=duration,
        )
        assert connector_prompt_arguments.prompt_index == prompt_index
        assert connector_prompt_arguments.prompt == prompt
        assert connector_prompt_arguments.target == target
        assert connector_prompt_arguments.predicted_results == predicted_results
        assert connector_prompt_arguments.duration == duration

    @pytest.mark.parametrize(
        "prompt_index, prompt, target",
        [
            (1, "Prompt 1", "Target 1"),
            (2, "Prompt 2", "Target 2"),
        ],
    )
    def test_create_connector_prompt_arguments_1(self, prompt_index, prompt, target):
        # Test creating a valid connector prompt arguments instance
        connector_prompt_arguments = ConnectorPromptArguments(
            prompt_index=prompt_index, prompt=prompt, target=target
        )
        assert connector_prompt_arguments.prompt_index == prompt_index
        assert connector_prompt_arguments.prompt == prompt
        assert connector_prompt_arguments.target == target
        assert connector_prompt_arguments.predicted_results is None
        assert connector_prompt_arguments.duration == 0.0

    @pytest.mark.parametrize(
        "prompt_index, prompt, target",
        [
            (-1, "Prompt C", "Target C"),  # Invalid prompt_index
            ("", "Prompt B", "Target B"),  # Invalid prompt_index
            (None, "Prompt C", "Target C"),  # Invalid prompt_index
            ({}, "Prompt D", "Target D"),  # Invalid prompt_index
            ([], "Prompt E", "Target E"),  # Invalid prompt_index
            ((), "Prompt F", "Target F"),  # Invalid prompt_index
            (2, 123, "Target B"),  # Invalid prompt
            (3, {}, "Target C"),  # Invalid prompt
            (4, None, "Target D"),  # Invalid prompt
            (5, [], "Target E"),  # Invalid prompt
            (6, (), "Target F"),  # Invalid prompt
        ],
    )
    def test_create_connector_prompt_arguments_invalid(
        self, prompt_index, prompt, target
    ):
        # Ensure that invalid inputs raise a ValidationError
        with pytest.raises(ValidationError):
            ConnectorPromptArguments(
                prompt_index=prompt_index, prompt=prompt, target=target
            )

    @pytest.mark.parametrize(
        "predicted_results, duration",
        [
            ("InvalidType", 0.0),  # Invalid predicted_results
            (123, 0.0),  # Invalid predicted_results
            ([], 0.0),  # Invalid predicted_results
            ((), 0.0),  # Invalid predicted_results
            (None, "InvalidDuration"),  # Invalid duration
            (None, -1),  # Invalid duration
            (None, []),  # Invalid duration
            (None, {}),  # Invalid duration
            (None, ()),  # Invalid duration
        ],
    )
    def test_create_connector_prompt_arguments_invalid_1(
        self, predicted_results, duration
    ):
        # Ensure that invalid inputs raise a ValidationError
        with pytest.raises(ValidationError):
            ConnectorPromptArguments(
                prompt_index=1,
                prompt="Prompt 1",
                target="Target 1",
                predicted_results=predicted_results,
                duration=duration,
            )
