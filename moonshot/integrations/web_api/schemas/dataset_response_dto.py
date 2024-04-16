from pydantic import BaseModel, ConfigDict

class DatasetResponseDTO(BaseModel):
    id : str
    name: str
    description: str
    keywords: list[str]
    examples: list[str]