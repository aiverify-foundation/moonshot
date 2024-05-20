from typing import Optional

from moonshot.src.recipes.recipe_arguments import RecipeArguments as RecipePydanticModel


class RecipeCreateDTO(RecipePydanticModel):
    id: Optional[str] = None


class RecipeUpdateDTO(RecipePydanticModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    datasets: Optional[list[str]] = None
    prompt_templates: Optional[list[str]] = None
    metrics: Optional[list[str]] = None
    attack_modules: Optional[list[str]] = None
    grading_scale: Optional[dict[str, list[int]]] = None
    stats: Optional[dict] = None
