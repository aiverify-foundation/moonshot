from pydantic import BaseModel, ConfigDict

class RecipeResponseDTO(BaseModel):
    id : str
    name: str
    description: str
    tags: list[str]
    datasets: list[str]
    prompt_templates: list[str]
    metrics: list[str]
    type: str
    attack_strategies: list[dict]
