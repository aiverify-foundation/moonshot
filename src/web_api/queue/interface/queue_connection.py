from typing import Any, Callable, Self
from abc import ABC, abstractmethod

class InterfaceQueueConnection(ABC):

    @abstractmethod
    def connect(self, queue_name: str | None = None) -> Self:
        pass
    
    @abstractmethod
    def subscribe(self, callback: Callable[[dict[str, Any]], None]) -> None:
        pass

    @abstractmethod
    def unsubscribe(self) -> None:
        pass
    
    @abstractmethod
    def publish(self, task: dict[str, Any]) -> bool | None:
        pass
    
    @abstractmethod
    def close(self):
        pass



