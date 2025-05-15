from typing import Any, Optional

from pydantic import Field

from moonshot.src.datasets.dataset_arguments import (
    DatasetArguments as DatasetPydanticModel,
)


class CSV_Dataset_DTO(DatasetPydanticModel):
    id: Optional[str] = None  # Not required from user
    examples: Optional[Any] = None  # Not required from user
    name: str = Field(..., min_length=1)
    description: str = Field(default="", min_length=1)
    license: Optional[str] = ""
    reference: Optional[str] = ""
    file_path: str = Field(..., min_length=1)


class HF_Dataset_DTO(DatasetPydanticModel):
    id: Optional[str] = None  # Not a required from user
    examples: Optional[Any] = None  # Not a required from user
    name: str = Field(..., min_length=1)
    description: str = Field(default="", min_length=1)
    license: Optional[str] = ""
    reference: Optional[str] = ""
    params: dict = Field(..., min_length=1)
