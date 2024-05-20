from __future__ import annotations

from pydantic import BaseModel

from moonshot.src.runs.run_status import RunStatus


class ResultArguments(BaseModel):
    id: str  # The ID of the Runner.

    start_time: float  # The start time of the Run.

    end_time: float  # The end time of the Run.

    duration: int  # The duration of the Run.

    status: RunStatus  # Status of the Run.

    raw_results: dict = {}  # Raw Results of the Run from runners-modules.

    results: dict = {}  # Results of the Run from results-modules.

    params: dict = {}  # Other information required for results module

    def to_dict(self) -> dict:
        """
        Transforms the ResultArguments instance into a dictionary format.

        This method serializes the ResultArguments instance into a dictionary where attribute names become keys
        and their corresponding values are the dictionary values.

        Returns:
            A dictionary representation of the ResultArguments instance.
        """
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "status": self.status.name,
            "raw_results": self.raw_results,
            "results": self.results,
            "params": self.params,
        }
