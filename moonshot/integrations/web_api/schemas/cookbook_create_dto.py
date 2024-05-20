from typing import Optional

from moonshot.src.cookbooks.cookbook_arguments import (
    CookbookArguments as CookbookPydanticModel,
)


class CookbookCreateDTO(CookbookPydanticModel):
    id: Optional[str] = None


class CookbookUpdateDTO(CookbookPydanticModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    recipes: Optional[list[str]] = None
