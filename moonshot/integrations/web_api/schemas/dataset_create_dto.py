from typing import Optional

from pydantic import Field
from pyparsing import Iterator

from moonshot.src.datasets.dataset_arguments import (
    DatasetArguments as DatasetPydanticModel,
)


class DatasetCreateDTO(DatasetPydanticModel):
    id: Optional[str] = None
    examples: Iterator[dict] = None
    name: str = Field(..., min_length=1)
    description: str = Field(default="", min_length=1)
    license: Optional[str] = ""
    reference: Optional[str] = ""
    params: dict
