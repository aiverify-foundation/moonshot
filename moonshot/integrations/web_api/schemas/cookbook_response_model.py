from typing import Optional

from moonshot.src.cookbooks.cookbook_arguments import (
    CookbookArguments as CookbookPydanticModel,
)


class CookbookResponseModel(CookbookPydanticModel):
    total_prompt_in_cookbook: Optional[int] = None
