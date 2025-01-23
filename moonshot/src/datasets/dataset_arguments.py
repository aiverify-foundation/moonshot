from typing import Iterator

from pydantic import BaseModel


class DatasetArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # id (str): Unique identifier for the dataset
    id: str

    # name (str): Name of the dataset
    name: str

    # description (str): Description of the dataset's contents and purpose
    description: str

    # examples (Iterator[dict] | None): Generator of examples from the dataset, where each example is a dictionary.
    examples: Iterator[dict] | None

    # num_of_dataset_prompts (int): The number of dataset prompts, automatically calculated
    num_of_dataset_prompts: int = 0

    # created_date (str): The creation date and time of the dataset in ISO format without 'T'. Automatically generated.
    created_date: str = ""

    # reference (str): An optional string to store a reference link or identifier for the dataset
    reference: str = ""

    # license (str): License information for the dataset. Defaults to an empty string if not provided.
    license: str = ""

    def to_dict(self) -> dict:
        """
        Converts the DatasetArguments object to a dictionary.

        Returns:
            dict: A dictionary representation of the DatasetArguments object, including the id, name, description,
                  examples, number of dataset prompts, created date, reference, and license.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "examples": self.examples,
            "num_of_dataset_prompts": self.num_of_dataset_prompts,
            "created_date": self.created_date,
            "reference": self.reference,
            "license": self.license,
        }
