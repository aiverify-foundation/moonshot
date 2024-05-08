from typing import Optional

from pydantic import BaseModel

from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments as Cookbook


class CookbookResponseModel(BaseModel):
    cookbook: Cookbook
    total_prompt_in_cookbook: Optional[int] = None
