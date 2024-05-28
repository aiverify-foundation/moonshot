from typing import Optional

from moonshot.src.cookbooks.cookbook_arguments import (
    CookbookArguments as CookbookPydanticModel,
)
from pydantic import Field

class CookbookCreateDTO(CookbookPydanticModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1)
    description: Optional[str] = Field(default="", min_length=1)
    recipes: list[str] = Field(..., min_length=1)


class CookbookUpdateDTO(CookbookPydanticModel):
    id: Optional[str] = None
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    recipes: Optional[list[str]] = Field(default=None, min_length=1)