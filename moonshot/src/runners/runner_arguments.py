from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel


class RunnerArguments(BaseModel):
    id: str  # The ID of the Run.

    name: str  # The name of the Run.

    database_file: str = ""  # The database file associated with the Run.

    endpoints: list[str] = []  # List of endpoints for the Run.

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
        Transforms the RunnerArguments instance into a dictionary format.

        This method serializes the RunnerArguments instance, excluding 'database_instance' and 'progress_callback_func',
        into a dictionary where attribute names become keys and their corresponding values are the dictionary values.

        Returns:
            A dictionary representation of the RunnerArguments instance, excluding non-serializable attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "database_file": self.database_file,
            "endpoints": self.endpoints,
        }
