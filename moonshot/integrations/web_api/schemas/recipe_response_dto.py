from pydantic import BaseModel, ConfigDict
from typing import Optional
class RecipeResponseDTO(BaseModel):
    id : str
    name: str
    description: str
    tags: list[str]
    datasets: list[str]
    prompt_templates: list[str]
    metrics: list[str]
    attack_modules: list[str]
    stats: dict
    total_prompt_in_recipe: Optional[int] = None