from typing import Optional

from pydantic import BaseModel, ConfigDict


class DatasetResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    num_of_dataset_prompts: int
    created_date: str
