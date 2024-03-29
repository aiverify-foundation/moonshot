from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel

from moonshot.src.runners.runner_type import RunnerType


class RunnerArguments(BaseModel):
    id: str  # The ID of the Run.

    name: str  # The name of the Run.

    run_type: RunnerType  # The type of the Run.

    database_file: str = ""  # The database file associated with the Run.

    recipes: list[str] = []  # List of recipes for the Run.

    cookbooks: list[str] = []  # List of cookbooks for the Run.

    endpoints: list[str] = []  # List of endpoints for the Run.

    num_of_prompts: int = 0  # Number of prompts for the Run.

    # ------------------------------------------------------------------------------
    # These attributes are not exported to dict
    # ------------------------------------------------------------------------------
    database_instance: Any | None = (
        None  # The database instance associated with the Run.
    )

    progress_callback_func: Callable | None = (
        None  # The progress callback function for the Run.
    )

    def to_dict(self) -> dict:
        """
        Convert the RunnerArguments object to a dictionary.

        This method converts the attributes of the RunnerArguments object into a dictionary. The keys of the dictionary
        are the attribute names and the values are the attribute values. The attributes that are not exported to the
        dictionary are 'database_instance' and 'progress_callback_func'.

        Returns:
            dict: A dictionary representation of the RunnerArguments object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "run_type": self.run_type.name.lower(),
            "database_file": self.database_file,
            "recipes": self.recipes,
            "cookbooks": self.cookbooks,
            "endpoints": self.endpoints,
            "num_of_prompts": self.num_of_prompts,
        }
