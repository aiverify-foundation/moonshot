from pydantic import BaseModel

from moonshot.src.recipes.recipe_type import RecipeType


class RecipeArguments(BaseModel):
    id: str  # id (str): The ID of the recipe.

    name: str  # name (str): The name of the recipe.

    description: str  # description (str): The description of the recipe.

    tags: list[str]  # tags (list): The list of tags in the recipe.

    datasets: list[str]  # datasets (list): The list of datasets used in the recipe.

    prompt_templates: list[
        str
    ]  # prompt_templates (list): The list of prompt templates in the recipe.

    metrics: list[str]  # metrics (list): The list of metrics in the recipe.

    type: RecipeType  # type (RecipeType): The type of recipe.

    attack_strategies: list[
        dict
    ]  # attack_strategies (list): The list of attack strategies in the recipe.

    def to_dict(self) -> dict:
        """
        Convert the RecipeArguments object to a dictionary.

        Returns:
            dict: A dictionary representation of the RecipeArguments object.
            The keys are the attribute names and the values are the attribute values.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "datasets": self.datasets,
            "prompt_templates": self.prompt_templates,
            "metrics": self.metrics,
            "type": self.type.name.lower(),
            "attack_strategies": self.attack_strategies,
        }
