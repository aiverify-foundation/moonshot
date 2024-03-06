import time
import logging
import os

from typing import Any, Callable
from multiprocessing import Queue
from multiprocessing.queues import Empty
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process
from ..interface.queue_connection import InterfaceQueueConnection


def monitor_queue(queue: Queue, queue_name: str, executor: ProcessPoolExecutor, job_worker: Callable[[dict[str, Any]], None]):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(" queue module")
    logger.info(f" {queue_name} - monitor loop started")
    logger.debug(f" Process ID: {os.getpid()}")
    try:
        while True:
            try:
                job = queue.get()  # do not use get_nowait, to avoid busy waiting
                executor.submit(job_worker, job)
            except Empty:
                time.sleep(1)  # Sleep for a bit to avoid busy waiting
            except Exception as e:
                logger.error(f"[error] - monitor_queue: {e}")
                break
    except Exception as e:
        logger.error(f"[error] - monitor_queue: {e}")

class InMemoryQueue(InterfaceQueueConnection):
    def __init__(self, queue_name: str):
        self.name = queue_name
        self.queue = Queue()
        self.futures = []
        self.executor = None
        self.queue_monitor: Process | None

    def connect(self):
        # this is an in-memory queue, there's no external connection to establish.
        return self

    def subscribe(self, worker: Callable[[dict[str, Any]], None]) -> None:
        if not self.executor:
            self.executor = ProcessPoolExecutor()
        monitor_queue_process = Process(target=monitor_queue, args=(self.queue, self.name, self.executor, worker))
        monitor_queue_process.daemon = False
        monitor_queue_process.start()

    def unsubscribe(self) -> None:
        if self.queue_monitor.is_alive():
            self.queue_monitor.terminate()
            self.queue_monitor.join()
        if self.executor:
            self.executor.shutdown(wait=True)

    def publish(self, job: dict[str, Any]) -> bool:
        try:
            self.queue.put_nowait(job)
            return True
        except:
            return False

    def close(self):
        # just clear the queue to mimic closing connection.
        while not self.queue.empty():
            self.queue.get_nowait()
