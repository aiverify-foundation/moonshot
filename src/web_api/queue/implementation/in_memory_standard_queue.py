import time
from typing import Any, Callable
from multiprocessing import Queue
from multiprocessing.queues import Empty
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process
from ..interface.queue_connection import InterfaceQueueConnection

def monitor_queue(queue: Queue, executor: ProcessPoolExecutor, worker: Callable[[dict[str, Any]], None]):
    print("monitor_queue started")  # Initial log
    try:
        while True:
            try:
                job = queue.get()  # do not use get_nowait, to avoid busy waiting
                executor.submit(worker, job)
            except Empty:
                time.sleep(1)  # Sleep for a bit to avoid busy waiting
            except Exception as e:
                print(f"[error] - monitor_queue: {e}")
                break
    except Exception as e:
        print(f"[error] - monitor_queue: {e}")

class InMemoryQueue(InterfaceQueueConnection):
    def __init__(self, name: str):
        self.name = name
        self.queue = Queue()
        self.futures = []
        self.executor = None

    def connect(self):
        # Since this is an in-memory queue, there's no external connection to establish.
        return self

    def subscribe(self, worker: Callable[[dict[str, Any]], None]) -> None:
        if not self.executor:
            self.executor = ProcessPoolExecutor()
        monitor_queue_process = Process(target=monitor_queue, args=(self.queue, self.executor, worker))
        monitor_queue_process.daemon = False
        monitor_queue_process.start()

    def unsubscribe(self) -> None:
        self.executor.shutdown()

    def publish(self, job: dict[str, Any]) -> bool:
        # Since this implementation does not support channels, ignore the channel_name.
        try:
            self.queue.put_nowait(job)
            return True
        except:
            return False

    def close(self):
        # Clearing the queue to mimic closing the connection.
        while not self.queue.empty():
            self.queue.get_nowait()
