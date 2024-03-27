from __future__ import annotations

from typing import Any, Callable, Union

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
    database_instance: Union[
        Any, None
    ] = None  # The database instance associated with the Run.

    progress_callback_func: Union[
        Callable, None
    ] = None  # The progress callback function for the Run.

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "run_type": self.run_type,
            "database_file": self.database_file,
            "recipes": self.recipes,
            "cookbooks": self.cookbooks,
            "endpoints": self.endpoints,
            "num_of_prompts": self.num_of_prompts,
        }
