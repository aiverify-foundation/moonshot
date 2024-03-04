from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Any

class SessionMetadataModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    session_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    created_epoch: float
    created_datetime: str = Field(min_length=1)
    chats: list[str]
    endpoints: list[str] = Field(min_length=1)
    metadata_file: str = Field(min_length=1)
    prompt_template: str | None = None 
    context_strategy: int | None = None
    filename: str | None = None
    chat_history: dict[str, list[Any]] | None = None

    @validator('context_strategy', pre=True)
    def empty_string_to_default(cls, val):
        if val == '':
            return None
        return val

class SessionResponseModel(BaseModel):
    session: SessionMetadataModel
