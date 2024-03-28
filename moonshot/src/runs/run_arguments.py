from __future__ import annotations

from typing import Union

from pydantic import BaseModel

from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db.db_accessor import DBAccessor


class RunArguments(BaseModel):
    run_type: RunnerType  # Run type for the Run.

    recipes: list[str]  # List of recipes for the Run.

    cookbooks: list[str]  # List of cookbooks for the Run.

    endpoints: list[str]  # List of endpoints for the Run.

    num_of_prompts: int  # Number of prompts for the Run.

    database_instance: Union[DBAccessor, None]  # Database instance for the Run.

    results_file: str  # The results file associated with the Run.

    progress: RunProgress  # The progress for the Run.

    start_time: float  # The start time of the Run.

    end_time: float  # The end time of the Run.

    duration: int  # The duration of the Run.

    error_messages: list[str]  # The error messages associated with the Run.

    results: dict  # Results of the Run.

    status: RunStatus  # Status of the Run.

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        """
        Converts the RunArguments object to a dictionary.

        This method is used to convert the RunArguments object to a dictionary. It returns a dictionary that
        contains all the necessary details of the run such as run_type, recipes, cookbooks, endpoints, num_of_prompts,
        database_instance, results_file, progress, start_time, end_time, duration, error_messages, results, and status.

        Returns:
            dict: A dictionary that contains all the necessary details of the run.
        """
        return {
            "run_type": self.run_type,
            "recipes": self.recipes,
            "cookbooks": self.cookbooks,
            "endpoints": self.endpoints,
            "num_of_prompts": self.num_of_prompts,
            "results_file": self.results_file,
            "progress": self.progress.get_dict(),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "error_messages": self.error_messages,
            "results": self.results,
            "status": self.status,
        }

    def to_tuple(self) -> tuple:
        """
        Converts the RunArguments object to a tuple.

        This method is used to convert the RunArguments object to a tuple. It returns a tuple that
        contains all the necessary details of the run such as run_type, recipes, cookbooks, endpoints, num_of_prompts,
        database_instance, results_file, progress, start_time, end_time, duration, error_messages, results, and status.

        Returns:
            tuple: A tuple that contains all the necessary details of the run.
        """
        return (
            self.run_type.name.lower(),
            str(self.recipes),
            str(self.cookbooks),
            str(self.endpoints),
            self.num_of_prompts,
            self.results_file,
            self.start_time,
            self.end_time,
            self.duration,
            str(self.error_messages),
            str(self.results),
            self.status.name.lower(),
        )
