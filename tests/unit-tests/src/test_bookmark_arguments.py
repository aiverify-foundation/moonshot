import pytest
from pydantic import ValidationError

from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments


class TestCollectionBookmarkArguments:
    def test_create_bookmark_arguments(self):
        # Test creating a valid BookmarkArguments instance
        bookmark_args = BookmarkArguments(
            name="Bookmark A",
            prompt="Prompt A",
            prepared_prompt="Prepared Prompt A",
            response="Response A",
            context_strategy="Strategy A",
            prompt_template="Template A",
            attack_module="Module A",
            metric="Metric A",
            bookmark_time="Time A",
        )
        assert bookmark_args.name == "Bookmark A"
        assert bookmark_args.prompt == "Prompt A"
        assert bookmark_args.prepared_prompt == "Prepared Prompt A"
        assert bookmark_args.response == "Response A"
        assert bookmark_args.context_strategy == "Strategy A"
        assert bookmark_args.prompt_template == "Template A"
        assert bookmark_args.attack_module == "Module A"
        assert bookmark_args.metric == "Metric A"
        assert bookmark_args.bookmark_time == "Time A"

    @pytest.mark.parametrize(
        "name, prompt, prepared_prompt, response",
        [
            ("", "Prompt A", "Prepared Prompt A", "Response A"),  # Invalid name
            ("Bookmark A", "", "Prepared Prompt A", "Response A"),  # Invalid prompt
            ("Bookmark A", "Prompt A", "", "Response A"),  # Invalid prepared_prompt
            ("Bookmark A", "Prompt A", "Prepared Prompt A", ""),  # Invalid response
        ],
    )
    def test_create_bookmark_arguments_invalid(
        self, name, prompt, prepared_prompt, response
    ):
        with pytest.raises(ValidationError):
            BookmarkArguments(
                name=name,
                prompt=prompt,
                prepared_prompt=prepared_prompt,
                response=response,
                context_strategy="Strategy A",
                prompt_template="Template A",
                attack_module="Module A",
                metric="Metric A",
                bookmark_time="Time A",
            )

    def test_from_tuple_to_dict(self):
        # Test converting a tuple to a dictionary
        values = (
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
        )
        expected_dict = {
            "name": "Bookmark A",
            "prompt": "Prompt A",
            "prepared_prompt": "Prepared Prompt A",
            "response": "Response A",
            "context_strategy": "Strategy A",
            "prompt_template": "Template A",
            "attack_module": "Module A",
            "metric": "Metric A",
            "bookmark_time": "Time A",
        }
        result_dict = BookmarkArguments.from_tuple_to_dict(values)
        assert (
            result_dict == expected_dict
        ), "The dictionary representation should match the expected output."

    def test_from_tuple_to_dict_insufficient_values(self):
        # Test converting a tuple with insufficient values to a dictionary
        values = (
            "1",
            "Bookmark A",
            "Prompt A",
            "Prepared Prompt A",
            "Response A",
        )
        with pytest.raises(ValueError) as exc:
            BookmarkArguments.from_tuple_to_dict(values)
            assert (
                str(exc.value)
                == "[BookmarkArguments] Failed to convert to dictionary because of the insufficient number of values"
            ), "The error message should match the expected validation error message."
