from abc import ABC
from ...types.types import CookbookTestRunProgress

class InterfaceBenchmarkCallbackHandler(ABC):
    def on_executor_update(self, progress_data: CookbookTestRunProgress) -> None:
        pass



