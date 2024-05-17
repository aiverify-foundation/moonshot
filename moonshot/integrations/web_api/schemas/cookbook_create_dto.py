from typing import Optional

from moonshot.src.cookbooks.cookbook_arguments import (
    CookbookArguments as CookbookPydanticModel,
)


class CookbookCreateDTO(CookbookPydanticModel):
    id: Optional[str] = None


class CookbookUpdateDTO(CookbookPydanticModel):
    id: Optional[str] = None
    name: Optional[str] = None = Field(min_length=1)
    description: Optional[str] = None = Field(min_length=3, max_length=1000)
    recipes: Optional[list[str]] = None = Field(min_length=1)
