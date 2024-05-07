from typing import Optional

from pydantic import BaseModel


class CookbookResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    recipes: list[str]
    total_prompt_in_cookbook: Optional[int] = None
