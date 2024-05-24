from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ConnectorPromptArguments(BaseModel):
    prompt_index: int  # The index of the prompt in the dataset

    prompt: str  # The actual prompt text

    target: Any  # The target response for the prompt

    predicted_results: Any = ""  # The predicted results, default is an empty string

    duration: float = 0.0  # The duration it took to get the results, default is 0.0
