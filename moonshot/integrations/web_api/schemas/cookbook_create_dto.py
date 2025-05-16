from typing import Optional

from pydantic import Field

from moonshot.src.cookbooks.cookbook_arguments import (
    CookbookArguments as CookbookPydanticModel,
)


class CookbookCreateDTO(CookbookPydanticModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1)
    description: Optional[str] = Field(default="", min_length=1)
    tags: Optional[list[str]] = []
    categories: Optional[list[str]] = []
    recipes: list[str] = Field(..., min_length=1)


class CookbookUpdateDTO(CookbookPydanticModel):
    id: Optional[str] = None
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    recipes: Optional[list[str]] = Field(default=None, min_length=1)
