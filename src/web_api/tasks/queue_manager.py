from typing import Any, Callable
from .interface.queue_connection import InterfaceQueueConnection

class QueueManager:
    def __init__(self, connection: InterfaceQueueConnection) -> None:
        self.connection = connection

    def connect(self):
        self.connection.connect()
        return self.connection

    def subscribe(self, callback: Callable[[dict[str, Any]], None]) -> None:
        return self.connection.subscribe(callback)

    def publish(self, task: dict[str, Any]):
        self.connection.publish(task)

    def close(self):
        self.connection.close()