from abc import ABC
from ...types.types import ExecutionInfo

class InterfaceBenchmarkCallbackHandler(ABC):

    @staticmethod
    def on_executor_update(progress_data: ExecutionInfo) -> None:
       pass



