from __future__ import annotations

import ast
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from moonshot.src.benchmarking.executors.benchmark_executor_status import (
    BenchmarkExecutorStatus,
)


class ResultArguments(BaseModel):
    id: str  # The ID of the BenchmarkExecutor.

    name: str  # The name of the BenchmarkExecutor.

    start_time: float  # The start time of the BenchmarkExecutor.

    end_time: float  # The end time of the BenchmarkExecutor.

    duration: int  # The duration of the BenchmarkExecutor.

    recipes: list[str]  # List of recipes for the BenchmarkExecutor.

    cookbooks: list[str]  # List of cookbooks for the BenchmarkExecutor.

    endpoints: list[str]  # List of endpoints for the BenchmarkExecutor.

    num_of_prompts: int  # Number of prompts for the BenchmarkExecutor.

    results: dict  # Results of the BenchmarkExecutor.

    status: BenchmarkExecutorStatus  # Status of the BenchmarkExecutor

    @classmethod
    def from_file(cls, results: dict) -> ResultArguments:
        """
        Creates a ResultArguments instance from a dictionary.

        This method extracts metadata from the input dictionary, converts the start and end times from string format
        to timestamp, and converts the status to a BenchmarkExecutorStatus enum. It also converts any stringified
        tuples in the results back to tuples.

        Args:
            results (dict): The input dictionary containing the results and metadata.

        Returns:
            ResultArguments: An instance of ResultArguments initialized with the data from the input dictionary.
        """
        metadata = results.pop("metadata")
        start_time = datetime.strptime(
            metadata["start_time"], "%Y%m%d-%H%M%S"
        ).timestamp()
        end_time = datetime.strptime(metadata["end_time"], "%Y%m%d-%H%M%S").timestamp()
        status = BenchmarkExecutorStatus[metadata["status"].upper()]

        # Convert stringified tuples back to tuples
        results = cls.convert_str_tuples_to_tuples(results)

        return cls(
            id=metadata["id"],
            name=metadata["name"],
            start_time=start_time,
            end_time=end_time,
            duration=metadata["duration"],
            recipes=metadata["recipes"],
            cookbooks=metadata["cookbooks"],
            endpoints=metadata["endpoints"],
            num_of_prompts=metadata["num_of_prompts"],
            results=results,
            status=status,
        )

    @classmethod
    def convert_str_tuples_to_tuples(cls, data: Any) -> Any:
        """
        Converts stringified tuples back to tuples.

        This method takes a dictionary as input and converts all its keys to tuples if they represent a tuple.
        If the value associated with a key is a dictionary, it recursively converts the keys of that dictionary
        to tuples as well.
        If the value is a list, it recursively applies the conversion to each element in the list.
        If the value is neither a dictionary nor a list, it returns the value as is.

        Args:
            data (Any): The input data. This could be a dictionary, a list, or any other data type.

        Returns:
            Any: The input data with all stringified tuples converted back to tuples.
        """
        if isinstance(data, dict):
            return {
                ast.literal_eval(key)
                if cls.is_tuple_str(key)
                else key: cls.convert_str_tuples_to_tuples(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [cls.convert_str_tuples_to_tuples(item) for item in data]
        else:
            return data

    @staticmethod
    def is_tuple_str(s: str) -> bool:
        """
        Checks if a string represents a tuple.

        Args:
            s (str): The input string.

        Returns:
            bool: True if the string represents a tuple, False otherwise.
        """
        return s.startswith("(") and s.endswith(")")

    def convert_dict_keys_to_str(self, data: Any) -> Any:
        """
        Converts the keys of a dictionary to strings.

        This method takes a dictionary as input and converts all its keys to strings.
        If the value associated with a key is a dictionary, it recursively converts the keys of that dictionary
        to strings as well.
        If the value is a list, it recursively applies the conversion to each element in the list.
        If the value is neither a dictionary nor a list, it returns the value as is.

        Args:
            data (Any): The input data. This could be a dictionary, a list, or any other data type.

        Returns:
            Any: The input data with all dictionary keys converted to strings.
        """
        if isinstance(data, dict):
            return {
                str(key): self.convert_dict_keys_to_str(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.convert_dict_keys_to_str(item) for item in data]
        else:
            return data

    def to_dict(self) -> dict:
        """
        Converts the instance variables of the class to a dictionary.

        This method takes the instance variables of the class and converts them into a dictionary.
        The keys of the dictionary are the names of the instance variables and the values are the values of the
        instance variables.
        The dictionary is then returned.

        Returns:
            dict: A dictionary representation of the instance variables of the class.
        """
        results = {
            "metadata": {
                "id": self.id,
                "name": self.name,
                "start_time": datetime.fromtimestamp(self.start_time).strftime(
                    "%Y%m%d-%H%M%S"
                ),
                "end_time": datetime.fromtimestamp(self.end_time).strftime(
                    "%Y%m%d-%H%M%S"
                ),
                "duration": self.duration,
                "recipes": self.recipes,
                "cookbooks": self.cookbooks,
                "endpoints": self.endpoints,
                "num_of_prompts": self.num_of_prompts,
                "status": self.status.name.lower(),
            },
        }
        results.update(self.convert_dict_keys_to_str(self.results))
        return results
