from __future__ import annotations

import ast
from typing import Any

from pydantic import BaseModel


class PromptArguments(BaseModel):
    conn_id: str = ""  # The ID of the connection, default is an empty string

    rec_id: str  # The ID of the recipe

    ds_id: str  # The ID of the dataset

    pt_id: str  # The ID of the prompt template

    prompt_index: int  # The index of the prompt in the dataset

    prompt: str  # The actual prompt text

    target: Any  # The target response for the prompt

    predicted_results: Any = ""  # The predicted results, default is an empty string

    duration: float = 0.0  # The duration it took to get the results, default is 0.0

    def to_tuple(self) -> tuple:
        """
        Converts the PromptArguments instance into a tuple.

        This method takes all the attributes of the PromptArguments instance and constructs a tuple
        with the attribute values in the following order: conn_id, rec_id, ds_id, pt_id, prompt,
        target, predicted_results, duration.
        This tuple can be used for serialization purposes, such as storing the prompt arguments information
        in a database or sending it over a network.

        Returns:
            tuple: A tuple representation of the PromptArguments instance.
        """
        return (
            self.conn_id,
            self.rec_id,
            self.ds_id,
            self.pt_id,
            self.prompt_index,
            self.prompt,
            str(self.target),
            str(self.predicted_results),
            str(self.duration),
        )

    @classmethod
    def from_tuple(cls, cache_record: tuple) -> PromptArguments:
        """
        Converts a tuple into a PromptArguments instance.

        This method takes a tuple with the attribute values in the following order: conn_id, rec_id, ds_id, pt_id,
        prompt_index, prompt, target, predicted_results, duration.
        It constructs a PromptArguments instance using these values. This method can be used for deserialization
        purposes, such as retrieving the prompt arguments information from a database or receiving it over a network.

        Args:
            cache_record (tuple): A tuple containing the attribute values for a PromptArguments instance.

        Returns:
            PromptArguments: A PromptArguments instance constructed from the tuple.
        """
        return cls(
            conn_id=cache_record[1],
            rec_id=cache_record[2],
            ds_id=cache_record[3],
            pt_id=cache_record[4],
            prompt_index=cache_record[5],
            prompt=cache_record[6],
            target=ast.literal_eval(cache_record[7]),
            predicted_results=ast.literal_eval(cache_record[8]),
            duration=float(cache_record[9]),
        )
