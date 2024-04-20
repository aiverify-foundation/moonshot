from abc import abstractmethod
from typing import Any


class IOInterface:
    @abstractmethod
    def create_file(self, data: dict) -> Any | None:
        """
        Creates a file with the given data.

        Args:
            data (dict): The data to be written to the file.

        Returns:
            Any | None: The result of the file creation operation, or None if the operation was unsuccessful.
        """
        pass

    @abstractmethod
    def read_file(self, filepath: str) -> dict | None:
        """
        Reads the file at the given filepath.

        Args:
            filepath (str): The path to the file to be read.

        Returns:
            dict | None: The data from the file if the file was successfully read, or None if the operation was
            unsuccessful.
        """
        pass
