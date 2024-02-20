from pydantic import BaseModel, ConfigDict
from typing import Any, Optional

class SessionMetadataModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    session_id: str
    name: str
    description: str
    created_epoch: float
    created_datetime: str
    chats: list[str]
    endpoints: list[str]
    metadata_file: str
    prompt_template: str
    context_strategy: int
    filename: str
    chat_history: Optional[dict[str, list[Any]]] = None

class SessionResponseModel(BaseModel):
    session: SessionMetadataModel
