from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Any

class SessionMetadataModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    session_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    created_epoch: float
    created_datetime: str = Field(min_length=1)
    chat_ids: list[str]
    endpoints: list[str] = Field(min_length=1)
    prompt_template: str | None = None 
    context_strategy: str | None = None
    chat_history: dict[str, list[Any]] | None = None

    @validator('context_strategy', pre=True)
    def empty_string_to_default_context_strategy(cls, val: str) -> str | None:
        if val == '':
            return None
        return val
    
    @validator('prompt_template', pre=True)
    def empty_string_to_default_prompt_template(cls, val: str) -> str | None:
        if val == '':
            return None
        return val

class SessionResponseModel(BaseModel):
    session: SessionMetadataModel
