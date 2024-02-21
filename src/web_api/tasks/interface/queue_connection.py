from queue import Queue
from typing import Any
from abc import ABC, abstractmethod

class I_QueueConnection(ABC):

    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def get_channels(self) -> dict[str, Queue]:
        pass

    @abstractmethod
    def create_channel(self, channel_name) -> bool:
        pass

    def consume(self, channel_name) -> dict[str, Any] | None:
        pass

    def publish(self, channel_name, task) -> bool | None:
        pass

    def close(self):
        pass