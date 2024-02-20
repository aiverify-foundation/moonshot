from pydantic import BaseModel, ConfigDict, Field
from typing import Any

class SessionMetadataModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    session_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    created_epoch: float
    created_datetime: str = Field(min_length=1)
    chats: list[str] = Field(min_length=1)
    endpoints: list[str] = Field(min_length=1)
    metadata_file: str = Field(min_length=1)
    prompt_template: str = Field(min_length=1)
    context_strategy: int
    filename: str = Field(min_length=1)
    chat_history: dict[str, list[Any]] | None = None

class SessionResponseModel(BaseModel):
    session: SessionMetadataModel
