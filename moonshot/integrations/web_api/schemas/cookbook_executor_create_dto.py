from pydantic import BaseModel, ConfigDict

class CookbookExecutorCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    cookbooks: list[str]
    endpoints: list[str]
    num_of_prompts: int