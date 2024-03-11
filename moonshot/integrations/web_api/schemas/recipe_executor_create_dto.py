from pydantic import BaseModel, ConfigDict

class RecipeExecutorCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    recipes: list[str]
    endpoints: list[str]
    num_of_prompts: int