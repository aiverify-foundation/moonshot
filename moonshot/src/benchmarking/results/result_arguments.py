from __future__ import annotations

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
        pass

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

    def to_file(self) -> dict:
        """
        Converts the ResultArguments object to a dictionary.

        This method takes the attributes of the ResultArguments object and converts them into a dictionary.
        This dictionary can then be used to write the result information to a JSON file.

        Returns:
            dict: A dictionary representation of the ResultArguments object.
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
