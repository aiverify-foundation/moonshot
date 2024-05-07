from typing import Optional

from pydantic import BaseModel


class RecipeResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    tags: list[str]
    categories: list[str]
    datasets: list[str]
    prompt_templates: list[str]
    metrics: list[str]
    attack_modules: list[str]
    grading_scale: dict[str, list[int]]
    stats: dict
    total_prompt_in_recipe: Optional[int] = None
