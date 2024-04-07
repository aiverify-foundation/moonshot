from pydantic import BaseModel, ConfigDict

class CookbookResponeDTO(BaseModel):
    id: str
    name: str
    description: str
    recipes: list[str] 