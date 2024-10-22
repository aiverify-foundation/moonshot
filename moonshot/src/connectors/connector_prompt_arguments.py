from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, Field

from moonshot.src.connectors.connector_response import ConnectorResponse


class ConnectorPromptArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    prompt_index: Annotated[
        int, Field(strict=True, ge=0)
    ]  # The index of the prompt in the dataset

    prompt: str  # The actual prompt text

    target: Any  # The target response for the prompt

    predicted_results: ConnectorResponse | None = (
        None  # The predicted results, default is None
    )

    # The duration it took to get the results, must be a positive float
    duration: Annotated[float, Field(strict=True, ge=0.0)] = 0.0
