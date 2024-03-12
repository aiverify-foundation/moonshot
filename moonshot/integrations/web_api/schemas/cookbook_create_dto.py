from pydantic import BaseModel, ConfigDict

class CookbookCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    recipes: list[str] 