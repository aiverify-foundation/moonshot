from typing import Optional

from pydantic import BaseModel, ConfigDict
from typing import Optional


class CookbookResponeDTO(BaseModel):
    id: str
    name: str
    description: str
    recipes: list[str] 
    total_prompt_in_cookbook: Optional[int] = None
