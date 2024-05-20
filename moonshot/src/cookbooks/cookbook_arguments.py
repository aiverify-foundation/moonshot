from pydantic import BaseModel


class CookbookArguments(BaseModel):
    id: str  # id (str): The unique identifier for the Cookbook.

    name: str  # name (str): The name of the Cookbook.

    description: str  # description (str): A brief description of the Cookbook.

    recipes: list[str]  # recipes (list): A list of recipes included in the Cookbook.

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
            "description": self.description,
            "recipes": self.recipes,
        }
