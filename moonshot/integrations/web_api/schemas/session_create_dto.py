from pydantic import BaseModel, ConfigDict, Field

class SessionCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=1000)
    endpoints: list[str] = Field(min_length=1)
    context_strategy: str = ""
    prompt_template: str = ""
