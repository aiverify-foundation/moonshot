import json
from io import TextIOWrapper

import ijson

from moonshot.src.storage.io_interface import IOInterface


class JsonIO(IOInterface):
    def __init__(self, json_path: str):
        """
        Initializes the JsonIO object with a path to a JSON file.

        Args:
            json_path (str): The file path to the JSON file that will be read from or written to.
        """
        self.json_path = json_path

    def create_file(self, data: dict) -> bool:
        """
        Creates a JSON file at the specified path with the provided data.

        Args:
            data (dict): The data to serialize into JSON format and write to the file.

        Returns:
            bool: True if the file creation was successful, False otherwise.
        """
        try:
            with open(self.json_path, "w") as json_file:
                json.dump(data, json_file, indent=2)
            return True
        except Exception as e:
            print(f"Error creating JSON file ({self.json_path}) - {str(e)}")
            return False

    def read_file(self) -> dict | None:
        """
        Reads the JSON file and returns its content as a dictionary.

        Returns:
            dict | None: The content of the JSON file as a dictionary if successful, None if the file is not found.
        """
        try:
            with open(self.json_path, "r", encoding="utf-8") as json_file:
                obj_info = json.load(json_file)
            return obj_info

        except FileNotFoundError:
            print(f"No file found at {self.json_path}")
            return None

    def read_file_iterator(
        self, json_keys: list[str] | None = None, iterator_keys: list[str] | None = None
    ) -> dict | None:
        """
        Reads specified keys from a JSON file using an iterator to minimize memory usage.

        Args:
            json_keys (list[str] | None): A list of keys to retrieve values for. If provided, only these keys will be
            included in the returned dictionary.

            iterator_keys (list[str] | None): A list of keys to create iterators for. This allows for streaming access
            to large or nested structures within the JSON file.

        Returns:
            dict | None: A dictionary with values for `json_keys` and iterators for `iterator_keys`,
            or None if the file is not found.
        """
        try:
            obj_info = {}
            # Retrieve direct values for specified keys
            if json_keys:
                with open(self.json_path, "r", encoding="utf-8") as json_file:
                    for prefix, _, value in ijson.parse(json_file):
                        if prefix in json_keys:
                            obj_info[prefix] = value

            # Create iterators for specified keys
            if iterator_keys:
                for iterator_key in iterator_keys:
                    raw_file = self.read_file_raw()
                    if raw_file:
                        obj_info[iterator_key.split(".")[0]] = self.GeneratorIO(
                            raw_file, iterator_key
                        )

            return obj_info

        except FileNotFoundError:
            print(f"No file found at {self.json_path}")
            return None

    def read_file_raw(self) -> TextIOWrapper | None:
        """
        Opens the JSON file for reading and returns the file object.

        Returns:
            TextIOWrapper | None: The file object if the file was successfully opened, None if the file is not found.
        """
        try:
            return open(self.json_path, "r", encoding="utf-8")

        except FileNotFoundError:
            print(f"No file found at {self.json_path}")
            return None

    class GeneratorIO:
        """
        A class that wraps a file object and an ijson generator to allow iteration over JSON items.

        Attributes:
            file (TextIOWrapper): The file object from which to read the JSON data.
            generator (ijson.items): The ijson generator used to iterate over items in the JSON file.
        """

        def __init__(self, file: TextIOWrapper, item_path: str):
            """
            Initializes the GeneratorIO with a file and a specific item path for the ijson generator.

            Args:
                file (TextIOWrapper): The file object from which to read the JSON data.
                item_path (str): The JSON path to the item to iterate over.
            """
            self.file = file
            self.generator = ijson.items(self.file, item_path)

        def __iter__(self):
            """
            Returns the iterator object itself.

            Returns:
                GeneratorIO: The instance itself as an iterator.
            """
            return self

        def __next__(self):
            """
            Returns the next item from the generator or closes the file and stops iteration.

            Returns:
                The next item from the JSON generator.

            Raises:
                StopIteration: If there are no further items, closes the file and raises StopIteration.
            """
            try:
                return next(self.generator)
            except StopIteration:
                self.file.close()
                raise StopIteration
