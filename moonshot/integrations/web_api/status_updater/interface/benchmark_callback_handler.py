from abc import ABC
from ...types.types import CookbookTestRunProgress

class InterfaceBenchmarkCallbackHandler(ABC):
    @staticmethod
    def on_executor_update(progress_data: CookbookTestRunProgress) -> None:
       pass



