from typing import Any

from pydantic import BaseModel


class RecipeArguments(BaseModel):
    # id (str): The ID of the recipe.
    id: str

    # name (str): The name of the recipe.
    name: str

    # description (str): The description of the recipe.
    description: str

    # tags (list): The list of tags in the recipe.
    tags: list[str]

    # categories (list): The list of categories in the recipe.
    categories: list[str]

    # datasets (list): The list of datasets used in the recipe.
    datasets: list[str]

    # prompt_templates (list): The list of prompt templates in the recipe.
    prompt_templates: list[str]

    # metrics (list): The list of metrics in the recipe.
    metrics: list[str]

    # attack_modules (list): The list of attack modules in the recipe.
    attack_modules: list[str]

    # grading_scale (dict): A dictionary where keys are grading categories and values are lists of grading scale.
    grading_scale: dict[str, list[int]]

    # stats (dict): A dictionary containing statistics about the recipe.
    stats: dict = {}

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.validate_grading_scale()

    def get_start_of_grading_scale(self, item: tuple[str, list[int]]) -> int:
        """
        Retrieve the starting value of a grading scale for a given grade.

        Args:
            item (tuple[str, list[int]]): A tuple containing the grade as a string and the associated grading scale
            as a list of ints.

        Returns:
            int: The first value in the grading scale list, representing the start of the grading range.
        """
        _, grading_scale = item
        return grading_scale[0]

    def validate_grading_scale(self) -> None:
        """
        Validate the grading scale to ensure that it covers a continuous range from 0 to 100.

        This method checks that each grading range starts where the previous one ended and that
        the final grading range ends at 100. If any grading range does not start as expected or
        if the end of the last grading range is not 100, it raises a ValueError.

        Raises:
            ValueError: If any grading range does not start as expected or if the grading ranges
            do not cover the full range from 0 to 100.
        """
        if not self.grading_scale:  # Check if grading_scale is empty
            return  # If empty, it's considered valid and the method returns early

        expected_start = 0
        for grade, grading_range in sorted(
            self.grading_scale.items(), key=self.get_start_of_grading_scale
        ):
            start, end = grading_range
            if start != expected_start:
                raise ValueError(
                    f"Invalid grading range for '{grade}'. Expected start: {expected_start}, got {start}."
                )
            if end < start:
                raise ValueError(
                    f"Invalid grading range for '{grade}'. The end value {end} is less than "
                    f"the start value {start}."
                )
            expected_start = end + 1

        if expected_start - 1 != 100:
            raise ValueError("Grading ranges do not cover 0 to 100.")

    def to_dict(self) -> dict:
        """
        Convert the RecipeArguments object to a dictionary.

        Returns:
            dict: A dictionary representation of the RecipeArguments object.
            The keys are the attribute names and the values are the attribute values.
        """
        return {
            "id": self.check_type("id", str),
            "name": self.check_type("name", str),
            "description": self.check_type("description", str),
            "tags": self.check_type("tags", list),
            "categories": self.check_type("categories", list),
            "datasets": self.check_type("datasets", list),
            "prompt_templates": self.check_type("prompt_templates", list),
            "metrics": self.check_type("metrics", list),
            "attack_modules": self.check_type("attack_modules", list),
            "grading_scale": self.check_type("grading_scale", dict),
            "stats": self.check_type("stats", dict),
        }

    def check_type(self, attribute: str, expected_type: type) -> Any:
        """
        Checks the type of a given attribute of the RecipeArguments instance.

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
