from pydantic import BaseModel, Field


class CookbookArguments(BaseModel):
    id: str  # id (str): The unique identifier for the Cookbook.

    name: str = Field(min_length=1)  # name (str): The name of the Cookbook.

    description: str  # description (str): A brief description of the Cookbook.

    tags: list[str]  # tags (list): The list of tags in the Cookbook.

    categories: list[str]  # categories (list): The list of categories in the Cookbook.

    recipes: list[str] = Field(
        min_length=1
    )  # recipes (list): A list of recipes included in the Cookbook.

    def to_dict(self) -> dict:
        """
        Converts the CookbookArguments instance into a dictionary.

        This method takes all the attributes of the CookbookArguments instance and constructs a dictionary
        with attribute names as keys and their corresponding values. This includes the id, name, description,
        and recipes.

        This dictionary can be used for serialization purposes, such as storing the cookbook information in a JSON file
        or sending it over a network.

        Returns:
            dict: A dictionary representation of the CookbookArguments instance.
        """
        return {
            "id": self.id,
            "name": self.name,
            "tags": self.tags,
            "categories": self.categories,
            "description": self.description,
            "recipes": self.recipes,
        }
