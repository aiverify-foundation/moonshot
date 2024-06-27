
from __future__ import annotations

from pydantic import BaseModel


class BookmarkArguments(BaseModel):
    id: int = 0
    name: str
    prompt: str
    response: str
    context_strategy: str
    prompt_template: str
    attack_module: str
    bookmark_time: str = None
    @classmethod
    def from_tuple(cls, values: tuple) -> BookmarkArguments:
        """
        Creates a BookmarkArguments instance from a tuple of values.

        Args:
            values (tuple): A tuple containing the fields of BookmarkArguments in order.

        Returns:
            BookmarkArguments: An instance of BookmarkArguments.
        """
        return cls(
            id=values[0],
            name=values[1],
            prompt=values[2],
            response=values[3],
            context_strategy=values[4],
            prompt_template=values[5],
            attack_module=values[6],
            bookmark_time=values[7]
        )