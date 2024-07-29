from typing import Any

from pydantic import BaseModel, Field


class RecipeArguments(BaseModel):
    # id (str): The ID of the recipe.
    id: str

    name: str = Field(min_length=1)  # name (str): The name for the endpoint.

    # description (str): The description of the recipe.
    description: str

    # tags (list): The list of tags in the recipe.
    tags: list[str]

    # categories (list): The list of categories in the recipe.
    categories: list[str]

    # datasets (list): The list of datasets used in the recipe.
    datasets: list[str] = Field(min_length=1)

    # prompt_templates (list): The list of prompt templates in the recipe.
    prompt_templates: list[str]

    # metrics (list): The list of metrics in the recipe.
    metrics: list[str] = Field(min_length=1)

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
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "categories": self.categories,
            "datasets": self.datasets,
            "prompt_templates": self.prompt_templates,
            "metrics": self.metrics,
            "grading_scale": self.grading_scale,
            "stats": self.stats,
        }
