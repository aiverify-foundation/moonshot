from typing import Optional

from moonshot.src.recipes.recipe_arguments import RecipeArguments as RecipePydanticModel


class RecipeResponseModel(RecipePydanticModel):
    total_prompt_in_recipe: Optional[int] = None
    endpoint_required: Optional[list[str]] = None
