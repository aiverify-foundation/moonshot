from typing import Optional
from pydantic import BaseModel

class SessionPromptDTO(BaseModel):
    history_length: Optional[int] = 10
    prompt: str
