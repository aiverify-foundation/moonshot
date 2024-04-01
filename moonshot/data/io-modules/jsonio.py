import json
from io import TextIOWrapper

from moonshot.src.storage.object_accessor import ObjectAccessor


class JSONIO(ObjectAccessor):
    def __init__(self, json_path: str):
        self.json_path = json_path

    def create_file(self, data: dict) -> bool:
        """
        This method creates a JSON file at the path specified during the class instantiation with the provided data.

        Args:
            data (dict): The dictionary to be serialized and written to the JSON file.

        Returns:
            bool: Returns True if the file was successfully created, otherwise False.
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
        This method reads a JSON file at the path specified during the class instantiation.

        Returns:
            dict | None: Returns the dictionary deserialized from the JSON file if the file was successfully read,
            otherwise None.
        """
        try:
            with open(self.json_path, "r", encoding="utf-8") as json_file:
                obj_info = json.load(json_file)
            return obj_info
        except FileNotFoundError:
            print(f"No file found at {self.json_path}")
            return None

    def read_file_raw(self) -> TextIOWrapper | None:
        """
        This method opens a JSON file at the path specified during the class instantiation for reading.

        Returns:
            TextIOWrapper | None: Returns a TextIOWrapper object if the file was successfully opened, otherwise None.
        """
        try:
            return open(self.json_path, "r", encoding="utf-8")

        except FileNotFoundError:
            print(f"No file found at {self.json_path}")
            return None
