from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SessionCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=3)
    description: Optional[str] = Field(default="", max_length=1000)
    endpoints: list[str] = Field(min_length=1)
    context_strategy: str = ""
    prompt_template: str = ""
    attack_module: str = ""
    metric: str = ""
    system_prompt: str = ""
    cs_num_of_prev_prompts: int = 5
