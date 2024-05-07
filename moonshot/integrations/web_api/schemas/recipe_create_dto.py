from pydantic import BaseModel, ConfigDict


class RecipeCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    tags: list[str]
    categories: list[str]
    datasets: list[str]
    prompt_templates: list[str]
    metrics: list[str]
    attack_modules: list[str]
