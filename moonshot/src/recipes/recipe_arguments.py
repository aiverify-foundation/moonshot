import math
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

    # datasets (list): The list of datasets used in the recipe.
    datasets: list[str]

    # prompt_templates (list): The list of prompt templates in the recipe.
    prompt_templates: list[str]

    # metrics (list): The list of metrics in the recipe.
    metrics: list[str]

    # attack_modules (list): The list of attack modules in the recipe.
    attack_modules: list[str]

    # grading_scale (dict): A dictionary where keys are grading categories and values are lists of grading scale.
    grading_scale: dict[str, list[float]] = {}

    # stats (dict): A dictionary containing statistics about the recipe.
    stats: dict = {}

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.validate_grading_scale()

    def get_start_of_grading_scale(self, item: tuple[str, list[float]]) -> float:
        """
        Retrieve the starting value of a grading scale for a given grade.

        Args:
            item (tuple[str, list[float]]): A tuple containing the grade as a string and the associated grading scale
            as a list of floats.

        Returns:
            float: The first value in the grading scale list, representing the start of the grading range.
        """
        _, grading_scale = item
        return grading_scale[0]

    def validate_grading_scale(self) -> None:
        """
        Validates the grading scale for the recipe.

        This method checks if the grading scale is contiguous and covers the range from 0.0 to 1.0 inclusively.
        It sorts the grading scale by their start values using the get_start_of_grading_scale method and ensures that
        each range starts where the previous one ended, within a tolerance level to account for floating-point
        imprecision.

        If a range does not start as expected within the tolerance, if the end of a range is less than its start,
        or if any value is outside the range of 0.0 to 1.0, a ValueError is raised.
        Additionally, it checks if the last grading range ends at 1.0, ensuring complete coverage.

        Raises:
            ValueError: If a grading range does not start as expected within the tolerance, ends before it starts,
            if the scale does not cover the full range from 0.0 to 1.0, or if any value is outside the range
            of 0.0 to 1.0.
        """
        expected_start = 0.0
        tolerance = 1e-5  # Define a tolerance level for floating-point comparison
        for grade, grading_range in sorted(
            self.grading_scale.items(), key=self.get_start_of_grading_scale
        ):
            start, end = grading_range
            if not (0.0 <= start < end <= 1.0):
                raise ValueError(
                    f"Grading scale for '{grade}' must start before it ends and be within 0.0 to 1.0."
                )
            if not math.isclose(start, expected_start, rel_tol=tolerance):
                raise ValueError(
                    f"Invalid grading scale for '{grade}'. Expected start: {expected_start}, got {start}."
                )
            expected_start = end

        if not math.isclose(expected_start, 1.0, rel_tol=tolerance):
            raise ValueError("Grading scale does not cover 0.0 to 1.0.")

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
            "attack_modules": self.attack_modules,
            "grading_scale": self.grading_scale,
            "stats": self.stats,
        }
