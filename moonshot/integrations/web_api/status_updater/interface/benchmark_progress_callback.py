from abc import ABC, abstractmethod

from ...types.types import TestRunProgress


class InterfaceBenchmarkProgressCallback(ABC):
    """
    The interface to implement for handling of benchmark progress updates from moonshot library

    """

    @abstractmethod
    def on_progress_update(self, progress_data: TestRunProgress) -> None:
        pass
