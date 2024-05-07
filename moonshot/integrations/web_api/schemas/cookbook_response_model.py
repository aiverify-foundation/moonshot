from typing import Optional

from pydantic import BaseModel

from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments


class CookbookResponseModel(BaseModel):
    cookbook: CookbookArguments
    total_prompt_in_cookbook: Optional[int] = None
