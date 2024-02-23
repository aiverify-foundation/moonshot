from pydantic import BaseModel


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

    def to_dict(self) -> dict:
        """
        Converts the RecipeArguments instance into a dictionary.

        This method takes all the attributes of the RecipeArguments instance and constructs a dictionary
        with attribute names as keys and their corresponding values. This includes the id, name, description, tags,
        datasets, prompt_templates, and metrics. This dictionary can be used for serialization purposes,
        such as storing the recipe information in a JSON file or sending it over a network.

        Returns:
            dict: A dictionary representation of the RecipeArguments instance.
        """

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "datasets": self.datasets,
            "prompt_templates": self.prompt_templates,
            "metrics": self.metrics,
        }
