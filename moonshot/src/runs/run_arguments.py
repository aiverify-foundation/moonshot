from __future__ import annotations

import ast
import json

from pydantic import BaseModel

from moonshot.src.runners.runner_type import RunnerType
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.db_interface import DBInterface


class RunArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    run_id: int = 0  # The id of the run

    runner_id: str  # The id of the runner

    runner_type: RunnerType  # Run type for the Run.

    runner_args: dict  # Dictionary containing arguments for the runner.

    database_instance: DBInterface | None  # Database instance for the Run.

    endpoints: list[str]  # List of endpoints for the Run.

    results_file: str  # The results file associated with the Run.

    start_time: float  # The start time of the Run.

    end_time: float  # The end time of the Run.

    duration: int  # The duration of the Run.

    error_messages: list[str]  # The error messages associated with the Run.

    raw_results: dict  # Results of the Run by runners-module.

    results: dict  # Generated Results of the Run by results-module.

    status: RunStatus  # Status of the Run.

    def to_dict(self) -> dict:
        """
        Converts the RunArguments object into a dictionary format.

        This method transforms the RunArguments instance into a dictionary, encapsulating all the critical attributes
        associated with the run. The resulting dictionary includes keys for runner_id, runner_type, runner_args,
        database_instance, endpoints, results_file, start_time, end_time, duration, error_messages, raw_results,
        results, and status offering a comprehensive snapshot of the run's parameters for straightforward access
        and further processing.

        Returns:
            dict: A dictionary containing all the significant attributes of the RunArguments instance.
        """
        return {
            "run_id": self.run_id,
            "runner_id": self.runner_id,
            "runner_type": self.runner_type,
            "runner_args": self.runner_args,
            "endpoints": self.endpoints,
            "results_file": self.results_file,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "error_messages": self.error_messages,
            "raw_results": self.raw_results,
            "results": self.results,
            "status": self.status,
        }

    def to_create_tuple(self) -> tuple:
        """
        Creates a tuple of run arguments for database insertion.

        This method prepares a tuple of run arguments that can be used to insert a new record into the run_table
        in the database. The tuple includes the runner_id, runner_type in lowercase, string representation of
        runner_args, string representation of endpoints, results_file, start_time, end_time, duration,
        string representation of error_messages, string representation of raw_results, string representation of results,
        and the run status in lowercase.

        Returns:
            tuple: A tuple containing the run arguments ready for database insertion.
        """
        return self._to_tuple(include_run_id=False)

    def to_tuple(self) -> tuple:
        """
        Serializes the RunArguments object to a tuple format.

        This method serializes the RunArguments instance to a tuple, encapsulating the primary attributes of the run.
        The resulting tuple contains the runner ID, runner type in lowercase, string representation of runner arguments,
        string representation of endpoints, results file path, start time, end time, run duration, string representation
        of error messages, string representation of raw results, string representation of results,
        and the run status in lowercase. This provides a complete summary of the run's parameters for easy storage
        or transmission.

        Returns:
            tuple: A tuple containing the serialized attributes of the RunArguments instance.
        """
        return self._to_tuple(include_run_id=True)

    def _to_tuple(self, include_run_id: bool) -> tuple:
        """
        Converts the RunArguments object to a tuple format.

        This method serializes the RunArguments instance into a tuple, including or excluding the run_id based on the
        include_run_id parameter. It ensures that all dictionary keys are converted to strings and JSON-encodes
        the raw_results and results attributes.

        Args:
            include_run_id (bool): A flag indicating whether to include the run_id in the resulting tuple.

        Returns:
            tuple: A tuple containing the serialized attributes of the RunArguments instance.
        """

        def convert_keys_to_str(d):
            """
            Recursively converts all keys in a dictionary to strings.

            Args:
                d (dict): The dictionary whose keys need to be converted.

            Returns:
                dict: A new dictionary with all keys converted to strings.
            """

            def convert_value(v):
                if isinstance(v, dict):
                    return {str(k): convert_value(val) for k, val in v.items()}
                return v

            return {str(k): convert_value(v) for k, v in d.items()}

        base_tuple = (
            self.runner_id,
            self.runner_type.name.lower(),
            str(self.runner_args),
            str(self.endpoints),
            self.results_file,
            self.start_time,
            self.end_time,
            self.duration,
            str(self.error_messages),
            json.dumps(convert_keys_to_str(self.raw_results)),
            json.dumps(self.results),
            self.status.name.lower(),
        )
        return base_tuple + (self.run_id,) if include_run_id else base_tuple

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
            run_id=run_record[0],
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
            raw_results=json.loads(run_record[10]),
            results=json.loads(run_record[11]),
            status=RunStatus(run_record[12]),
        )
