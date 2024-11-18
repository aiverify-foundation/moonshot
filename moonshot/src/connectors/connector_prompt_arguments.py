from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from moonshot.src.connectors.connector_response import ConnectorResponse


class ConnectorPromptArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    prompt_index: int  # The index of the prompt in the dataset

    prompt: str  # The actual prompt text

    target: Any  # The target response for the prompt

    predicted_results: ConnectorResponse | None = (
        None  # The predicted results, default is None
    )

    duration: float = 0.0  # The duration it took to get the results, default is 0.0
