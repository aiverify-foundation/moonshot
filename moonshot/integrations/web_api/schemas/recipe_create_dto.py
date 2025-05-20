from typing import Optional

from pydantic import Field

from moonshot.src.recipes.recipe_arguments import RecipeArguments as RecipePydanticModel


class RecipeCreateDTO(RecipePydanticModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1)
    description: Optional[str] = Field(default="", min_length=1)
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    datasets: list[str] = Field(..., min_length=1)
    metrics: list[str] = Field(..., min_length=1)
    prompt_templates: Optional[list[str]] = None
    grading_scale: Optional[dict[str, list[int]]] = None
    stats: Optional[dict] = None


class RecipeUpdateDTO(RecipePydanticModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = Field(default="", min_length=1)
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    datasets: Optional[list[str]] = None
    prompt_templates: Optional[list[str]] = None
    metrics: Optional[list[str]] = None
    grading_scale: Optional[dict[str, list[int]]] = None
    stats: Optional[dict] = None
