from typing import Any

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
            "name": self.check_type("name", str),
            "description": self.check_type("description", str),
            "recipes": self.check_type("recipes", list),
        }

    def check_type(self, attribute: str, expected_type: type) -> Any:
        """
        Checks the type of a given attribute of the CookbookArguments instance.

        This method retrieves the value of the specified attribute and checks if its type matches the expected type.
        If the types do not match, it raises a TypeError with a message indicating the attribute name, the expected type
        , and the actual type of the value.

        Args:
            attribute (str): The name of the attribute to check.
            expected_type (type): The expected type of the attribute.

        Returns:
            Any: The value of the attribute if its type matches the expected type.

        Raises:
            TypeError: If the type of the attribute does not match the expected type.
        """
        value = getattr(self, attribute)
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Expected type for {attribute} is {expected_type}, but got {type(value)}"
            )
        return value
