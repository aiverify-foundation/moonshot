from abc import abstractmethod
from typing import Any, Iterator


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
    def create_file_with_iterator(
        self, data: dict, iterator_keys: list[str], iterator_data: Iterator[dict]
    ) -> bool:
        """
        Creates a file using an iterator to provide the data for specified keys.

        Args:
            data (dict): The data to be serialized into JSON and written to the file.
            iterator_keys (list[str]): A list of keys for which the values will be written using iterators.
            iterator_data (Iterator[dict]): An iterator for the data to be written for the specified keys.

        Returns:
            bool: Always returns True to indicate the operation was executed without raising an exception.
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
