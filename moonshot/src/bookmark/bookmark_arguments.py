from __future__ import annotations

from pydantic import BaseModel, Field


class BookmarkArguments(BaseModel):
    id: int = 0
    name: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
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
        """
        return {
            "id": values[0],
            "name": values[1],
            "prompt": values[2],
            "response": values[3],
            "context_strategy": values[4],
            "prompt_template": values[5],
            "attack_module": values[6],
            "metric": values[7],
            "bookmark_time": values[8],
        }
