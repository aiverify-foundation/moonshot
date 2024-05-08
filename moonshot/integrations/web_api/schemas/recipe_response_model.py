from typing import Optional

from pydantic import BaseModel

from moonshot.src.recipes.recipe_arguments import RecipeArguments as Recipe


class RecipeResponseModel(BaseModel):
    recipe: Recipe
    total_prompt_in_recipe: Optional[int] = None
