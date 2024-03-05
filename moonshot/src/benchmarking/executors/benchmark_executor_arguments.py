from __future__ import annotations

import ast
import time
from typing import Any, Callable, Union

from pydantic import BaseModel

from moonshot.src.benchmarking.executors.benchmark_executor_status import (
    BenchmarkExecutorStatus,
)
from moonshot.src.benchmarking.executors.benchmark_executor_types import (
    BenchmarkExecutorTypes,
)


class BenchmarkExecutorArguments(BaseModel):
    id: str  # The ID of the BenchmarkExecutor.

    name: str  # The name of the BenchmarkExecutor.

    type: BenchmarkExecutorTypes  # The type of the BenchmarkExecutor.

    start_time: float = time.time()  # The start time of the BenchmarkExecutor.

    end_time: float = time.time()  # The end time of the BenchmarkExecutor.

    duration: int = 0  # The duration of the BenchmarkExecutor.

    database_instance: Union[
        Any, None
    ] = None  # The database instance associated with the BenchmarkExecutor.

    database_file: str = ""  # The database file associated with the BenchmarkExecutor.

    error_messages: list[
        str
    ] = []  # The error messages associated with the BenchmarkExecutor.

    results_file: str = ""  # The results file associated with the BenchmarkExecutor.

    recipes: list[str] = []  # List of recipes for the BenchmarkExecutor.

    cookbooks: list[str] = []  # List of cookbooks for the BenchmarkExecutor.

    endpoints: list[str] = []  # List of endpoints for the BenchmarkExecutor.

    num_of_prompts: int = 0  # Number of prompts for the BenchmarkExecutor.

    results: dict = {}  # Results of the BenchmarkExecutor.

    status: BenchmarkExecutorStatus = (
        BenchmarkExecutorStatus.PENDING
    )  # Status of the BenchmarkExecutor

    progress_callback_func: Union[
        Callable, None
    ] = None  # The progress callback function for the BenchmarkExecutor.

    def to_dict(self) -> dict:
        """
        Converts the BenchmarkExecutorArguments instance into a dictionary.

        This method takes all the attributes of the BenchmarkExecutorArguments instance and constructs a dictionary
        with attribute names as keys and their corresponding values. This includes the id, name, type, start_time,
        end_time, duration, database_instance, database_file, error_messages, results_file, recipes, cookbooks,
        endpoints, num_of_prompts, results, status, and progress_callback_func.

        This dictionary can be used for serialization purposes, such as storing the benchmark executor arguments
        information in a JSON file or sending it over a network.

        Returns:
            dict: A dictionary representation of the BenchmarkExecutorArguments instance.
        """
        return {
            "id": self.id,
            "type": self.type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "database_file": self.database_file,
            "error_messages": self.error_messages,
            "results_file": self.results_file,
            "recipes": self.recipes,
            "cookbooks": self.cookbooks,
            "endpoints": self.endpoints,
            "num_of_prompts": self.num_of_prompts,
            "results": self.results,
            "status": self.status,
            "progress_callback_func": self.progress_callback_func,
        }

    def to_tuple(self) -> tuple:
        """
        Converts the BenchmarkExecutorArguments instance into a tuple.

        This method takes all the attributes of the BenchmarkExecutorArguments instance and constructs a tuple
        with attribute values in the following order: name, type, start_time, end_time, duration, database_file,
        error_messages, results_file, recipes, cookbooks, endpoints, num_of_prompts, results, status, id.

        This tuple can be used for serialization purposes, such as storing the benchmark executor arguments
        information in a database or sending it over a network.

        Returns:
            tuple: A tuple representation of the BenchmarkExecutorArguments instance.
        """
        return (
            self.name,
            self.type.name.lower(),
            self.start_time,
            self.end_time,
            self.duration,
            self.database_file,
            str(self.error_messages),
            self.results_file,
            str(self.recipes),
            str(self.cookbooks),
            str(self.endpoints),
            self.num_of_prompts,
            str(self.results),
            self.status.name.lower(),
            self.id,
        )

    @classmethod
    def from_tuple(cls, bm_record: tuple) -> BenchmarkExecutorArguments:
        """
        Converts a tuple into a BenchmarkExecutorArguments instance.

        This method takes a tuple with attribute values in the following order: id, name, type, start_time,
        end_time, duration, database_file, error_messages, results_file, recipes, cookbooks, endpoints,
        num_of_prompts, results, status. It then constructs a BenchmarkExecutorArguments instance using these values.

        This method is useful for deserialization purposes, such as retrieving the benchmark executor arguments
        information from a database or receiving it over a network.

        Args:
            bm_record (tuple): A tuple representation of the BenchmarkExecutorArguments instance.

        Returns:
            BenchmarkExecutorArguments: An instance of the BenchmarkExecutorArguments class with the loaded
            benchmark executor arguments information.
        """
        return cls(
            id=bm_record[0],
            name=bm_record[1],
            type=BenchmarkExecutorTypes(bm_record[2].lower()),
            start_time=float(bm_record[3]),
            end_time=float(bm_record[4]),
            duration=bm_record[5],
            database_file=bm_record[6],
            error_messages=ast.literal_eval(bm_record[7]),
            results_file=bm_record[8],
            recipes=ast.literal_eval(bm_record[9]),
            cookbooks=ast.literal_eval(bm_record[10]),
            endpoints=ast.literal_eval(bm_record[11]),
            num_of_prompts=bm_record[12],
            results=ast.literal_eval(bm_record[13]),
            status=BenchmarkExecutorStatus(bm_record[14].lower()),
        )
