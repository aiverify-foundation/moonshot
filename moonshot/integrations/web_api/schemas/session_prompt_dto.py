from pydantic import BaseModel, ConfigDict, Field

class SessionPromptDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    history_length: int | None = 10
    prompt: str = Field(min_length=1)
