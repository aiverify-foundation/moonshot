from multiprocessing import Queue
from multiprocessing.queues import Empty
from concurrent.futures import ProcessPoolExecutor, Future
from ..interface.queue_connection import InterfaceQueueConnection
from typing import Any

class InMemoryQueue(InterfaceQueueConnection):
    def __init__(self, name: str):
        self.name = name
        self.queue = Queue()
        self.futures = []

    def connect(self):
        # Since this is an in-memory queue, there's no external connection to establish.
        return self

    def subscribe(self, callback) -> None:
        self.executor = ProcessPoolExecutor()
        self.futures = []

        def monitor_queue(self):
            while True:
                try:
                    message = self.queue.get()
                    future = self.executor.submit(callback, message)
                    self.futures.append(future)
                except Empty:
                    # The queue is empty. In this case, we just catch the exception and continue.
                    # This exception handling is more explicit and safer than a bare except.
                    continue
                except Exception as e:
                    # Handle or log other exceptions as needed
                    print(f"Unexpected error: {e}")
                    break

        self.executor.submit(monitor_queue)

    def unsubscribe(self) -> None:
        self.executor.shutdown()

    def publish(self, task: dict[str, Any]) -> bool:
        # Since this implementation does not support channels, ignore the channel_name.
        try:
            self.queue.put_nowait(task)
            return True
        except:
            return False

    def close(self):
        # Clearing the queue to mimic closing the connection.
        while not self.queue.empty():
            self.queue.get_nowait()
