from __future__ import annotations

from pydantic import BaseModel, Field

from moonshot.src.messages_constants import (
    BOOKMARK_ARGUMENTS_FROM_TUPLE_TO_DICT_VALIDATION_ERROR,
)


class BookmarkArguments(BaseModel):
    name: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    prepared_prompt: str = Field(min_length=1)
    response: str = Field(min_length=1)
    context_strategy: str
    prompt_template: str
    attack_module: str
    metric: str
    bookmark_time: str

    @classmethod
    def from_tuple_to_dict(cls, values: tuple) -> dict:
        """
        Creates a dictionary from a tuple of values representing BookmarkArguments fields.

        Args:
            values (tuple): A tuple containing the fields of BookmarkArguments in order.

        Returns:
            dict: A dictionary representing the BookmarkArguments.

        Raises:
            ValueError: If the number of values in the tuple is less than 10.
        """
        if len(values) < 10:
            raise ValueError(BOOKMARK_ARGUMENTS_FROM_TUPLE_TO_DICT_VALIDATION_ERROR)

        return {
            "name": values[1],
            "prompt": values[2],
            "prepared_prompt": values[3],
            "response": values[4],
            "context_strategy": values[5],
            "prompt_template": values[6],
            "attack_module": values[7],
            "metric": values[8],
            "bookmark_time": values[9],
        }
