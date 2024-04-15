from __future__ import annotations

import ast

from pydantic import BaseModel

from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_progress import RunProgress
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_accessor import DBAccessor


class RunArguments(BaseModel):
    runner_type: RunnerType  # Run type for the Run.

    runner_args: dict  # Dictionary containing arguments for the runner.

    database_instance: DBAccessor | None  # Database instance for the Run.

    endpoints: list[str]  # List of endpoints for the Run.

    results_file: str  # The results file associated with the Run.

    progress: RunProgress | None  # The progress for the Run.

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
        Converts the RunArguments object into a dictionary format.

        This method transforms the RunArguments instance into a dictionary, encapsulating all critical aspects of
        the run. The resulting dictionary includes keys for runner_type, runner_args, database_instance, endpoints,
        results_file, progress, start_time, end_time, duration, error_messages, results, and status, reflecting the
        comprehensive details of the run.

        Returns:
            dict: A dictionary representation of the RunArguments instance, detailing all essential run parameters.
        """
        if self.progress:
            progress_dict = self.progress.get_dict()
        else:
            progress_dict = {}

        return {
            "runner_type": self.runner_type,
            "runner_args": self.runner_args,
            "endpoints": self.endpoints,
            "results_file": self.results_file,
            "progress": progress_dict,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "error_messages": self.error_messages,
            "results": self.results,
            "status": self.status,
        }

    def to_tuple(self) -> tuple:
        """
        Converts the RunArguments object into a tuple representation.

        This method transforms the RunArguments instance into a tuple, encapsulating key aspects of the run.
        The returned tuple includes the runner type, runner arguments, endpoints, results file, start time, end time,
        duration, error messages, results, and status, providing a comprehensive overview of the run's parameters.

        Returns:
            tuple: A tuple representation of the RunArguments instance, detailing essential run parameters.
        """
        return (
            self.runner_type.name.lower(),
            str(self.runner_args),
            str(self.endpoints),
            self.results_file,
            self.start_time,
            self.end_time,
            self.duration,
            str(self.error_messages),
            str(self.results),
            self.status.name.lower(),
        )

    @classmethod
    def from_tuple(cls, run_record: tuple) -> RunArguments:
        """
        Reconstructs a RunArguments object from a tuple representation.

        This method reconstructs a RunArguments object from a tuple, which encapsulates all critical details of a run.
        The tuple should include information such as runner type, runner arguments, endpoints, results file, start time,
        end time, duration, error messages, results, and status, reflecting the comprehensive parameters of the run.

        Args:
            run_record (tuple): A tuple encapsulating all critical details of the run.

        Returns:
            RunArguments: A newly constructed RunArguments object populated with the data from the tuple.
        """
        return cls(
            runner_type=RunnerType(run_record[1]),
            runner_args=ast.literal_eval(run_record[2]),
            database_instance=None,
            endpoints=ast.literal_eval(run_record[3]),
            results_file=run_record[4],
            progress=None,
            start_time=float(run_record[5]),
            end_time=float(run_record[6]),
            duration=run_record[7],
            error_messages=ast.literal_eval(run_record[8]),
            results=ast.literal_eval(run_record[9]),
            status=RunStatus(run_record[10]),
        )
