from pydantic import BaseModel, ConfigDict, Field


class SessionPromptDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    history_length: int | None = 10
    user_prompt: str = Field(min_length=1)
