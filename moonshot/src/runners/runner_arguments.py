from __future__ import annotations

from typing import Any, Callable

from pydantic import BaseModel, Field


class RunnerArguments(BaseModel):
    id: str  # The ID of the Runner.

    name: str = Field(min_length=1)  # The name of the Runner.

    database_file: str = ""  # The database file associated with the Runner.

    endpoints: list[str] = Field(min_length=1)  # List of endpoints for the Runner.

    description: str = ""  # A brief description of the Runner.

    # ------------------------------------------------------------------------------
    # These attributes are not exported to dict
    # ------------------------------------------------------------------------------
    database_instance: Any | None = (
        None  # The database instance associated with the Runner.
    )

    progress_callback_func: Callable | None = (
        None  # The progress callback function for the Runner.
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
            "description": self.description,
        }
