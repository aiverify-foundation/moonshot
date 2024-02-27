import logging
from typing import Any
from moonshot.src.common.prompt_template import get_prompt_templates #TODO - call new interface

class BaseService:

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def get_prompt_templates(self) -> list[Any | None]:
        return get_prompt_templates()

