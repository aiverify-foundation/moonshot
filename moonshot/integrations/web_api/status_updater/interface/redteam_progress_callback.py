from abc import ABC, abstractmethod

from ...types.types import TestRunProgress


class InterfaceRedTeamProgressCallback(ABC):
    """
    The interface to implement for handling of redteam progress updates from moonshot library

    """

    @abstractmethod
    def on_art_progress_update(self, progress_data: TestRunProgress) -> None:
        pass
