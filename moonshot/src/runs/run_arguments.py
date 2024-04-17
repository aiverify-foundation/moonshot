from __future__ import annotations

import ast

from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_accessor import DBAccessor


class RunArguments:
    def __init__(
        self,
        runner_id: str,  # Runner id for the runner
        runner_type: RunnerType,  # Run type for the Run.
        runner_args: dict,  # Dictionary containing arguments for the runner.
        database_instance: DBAccessor | None,  # Database instance for the Run.
        endpoints: list[str],  # List of endpoints for the Run.
        results_file: str,  # The results file associated with the Run.
        start_time: float,  # The start time of the Run.
        end_time: float,  # The end time of the Run.
        duration: int,  # The duration of the Run.
        error_messages: list[str],  # The error messages associated with the Run.
        results: dict,  # Results of the Run.
        status: RunStatus,  # Status of the Run.
    ) -> None:
        self.runner_id = runner_id
        self.runner_type = runner_type
        self.runner_args = runner_args
        self.database_instance = database_instance
        self.endpoints = endpoints
        self.results_file = results_file
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.error_messages = error_messages
        self.results = results
        self.status = status

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        """
        Converts the RunArguments object into a dictionary format.

        This method transforms the RunArguments instance into a dictionary, encapsulating all the critical attributes
        associated with the run. The resulting dictionary includes keys for runner_id, runner_type, runner_args,
        database_instance, endpoints, results_file, start_time, end_time, duration, error_messages, results, and status,
        offering a comprehensive snapshot of the run's parameters for straightforward access and further processing.

        Returns:
            dict: A dictionary containing all the significant attributes of the RunArguments instance.
        """
        return {
            "runner_id": self.runner_id,
            "runner_type": self.runner_type,
            "runner_args": self.runner_args,
            "endpoints": self.endpoints,
            "results_file": self.results_file,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "error_messages": self.error_messages,
            "results": self.results,
            "status": self.status,
        }

    def to_tuple(self) -> tuple:
        """
        Serializes the RunArguments object to a tuple format.

        This method serializes the RunArguments instance to a tuple, encapsulating the primary attributes of the run.
        The resulting tuple contains the runner ID, runner type in lowercase, string representation of runner arguments,
        string representation of endpoints, results file path, start time, end time, run duration, string representation
        of error messages, string representation of results, and the run status in lowercase. This provides a complete
        summary of the run's parameters for easy storage or transmission.

        Returns:
            tuple: A tuple containing the serialized attributes of the RunArguments instance.
        """
        return (
            self.runner_id,
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
        Reconstructs a RunArguments object from a serialized tuple.

        This class method takes a tuple that contains the serialized form of a RunArguments object and reconstructs it
        into a new RunArguments instance. The tuple is expected to contain the following elements in order: runner ID,
        runner type, runner arguments, endpoints, results file, start time, end time, duration, error messages, results,
        and status. These elements collectively represent the state of a run at a specific point in time.

        Args:
            run_record (tuple): A tuple containing the serialized state of a RunArguments object.

        Returns:
            RunArguments: An instance of RunArguments initialized with the data extracted from the tuple.
        """
        return cls(
            runner_id=run_record[1],
            runner_type=RunnerType(run_record[2]),
            runner_args=ast.literal_eval(run_record[3]),
            database_instance=None,
            endpoints=ast.literal_eval(run_record[4]),
            results_file=run_record[5],
            start_time=float(run_record[6]),
            end_time=float(run_record[7]),
            duration=run_record[8],
            error_messages=ast.literal_eval(run_record[9]),
            results=ast.literal_eval(run_record[10]),
            status=RunStatus(run_record[11]),
        )
