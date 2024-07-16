from typing import Optional

from moonshot.src.bookmark.bookmark_arguments import (
    BookmarkArguments as BookmarkPydanticModel,
)


class BookmarkCreateDTO(BookmarkPydanticModel):
    prompt_template: Optional[str] = ""
    context_strategy: Optional[str] = ""
    attack_module: Optional[str] = ""
    metric: Optional[str] = ""
    bookmark_time: Optional[str] = None
