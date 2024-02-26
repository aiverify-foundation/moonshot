import multiprocessing
from multiprocessing.managers import DictProxy, SyncManager
from queue import Queue
from typing import Any
from ..interface.queue_connection import InterfaceQueueConnection

# TODO - this probably has to be a Singleton because it's a shared resource

class InMemorySharedQueue(InterfaceQueueConnection):
    def __init__(self):
        self.manager: SyncManager = multiprocessing.Manager()
        self.channels: DictProxy[str, Queue] = self.manager.dict()

    def connect(self):
        return self
    
    
    def get_channels(self):
        return self.channels
    
    # TODO
    # Shared queue (to be shared between processes) do not need below methods. 
    # connect returns the shared queue object and that's it.
    # figure how to make below optional in Interface

    def create_channel(self, channel_name: str) -> bool:
        if channel_name not in self.channels:
            self.channels[channel_name] = self.manager.Queue()
            return True
        return False

    def consume(self, channel_name: str) -> dict[str, Any] | None:
        if channel_name in self.channels:
            return self.channels[channel_name].get()
        return None

    def publish(self, channel_name: str, task: dict[str, Any]) -> bool:
        if channel_name in self.channels:
            self.channels[channel_name].put(task)
            return True
        return False

    def close(self):
        self.channels.clear()
        self.manager.shutdown()

