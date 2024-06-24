from moonshot.src.datasets.dataset_arguments import (
    DatasetArguments as DatasetPydanticModel,
)
from typing import Optional
from pydantic import Field
from pyparsing import Iterator

class DatasetCreateDTO(DatasetPydanticModel):
    # not needed fields
    id: Optional[str] = None
    examples: Iterator[dict] = None  
    #end
    name: str = Field(..., min_length=1)
    description: str = Field(default="", min_length=1)
    license: str
    reference: str
    params: dict
