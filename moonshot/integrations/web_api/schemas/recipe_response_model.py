from typing import Optional

from pydantic import BaseModel

from moonshot.src.recipes.recipe_arguments import RecipeArguments


class RecipeResponseModel(BaseModel):
    recipe: RecipeArguments
    total_prompt_in_recipe: Optional[int] = None
