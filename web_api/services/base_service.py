import logging
from typing import Any
import moonshot.api as moonshot_api

class BaseService:

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )


