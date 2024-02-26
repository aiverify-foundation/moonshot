from multiprocessing.managers import DictProxy
from queue import Queue
from typing import Any
from .tasks.implementation.in_memory_standard_queue import InMemoryQueue
import uvicorn
import time
import os
from multiprocessing import Pool
from threading import Thread

from web_api.tasks.queue_task_processor import QueueTaskProcessor
from .tasks.implementation.in_memory_shared_queue import InMemorySharedQueue
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue
from .tasks.queue_manager import QueueManager
from .app import init_api
from . import globals

# Choose the queue implementation
# QUEUE_TYPE = InMemorySharedQueue()
QUEUE_TYPE = InMemoryQueue("benchmark_test_queue")
# BENCHMARK_TEST_CHANNEL = "benchmark_test"

def run_uvicorn():
    app = init_api()
    # uvicorn (ASGI server) uses an event loop for handling async tasks associated with FastAPI app.
    uvicorn.run(app, host="0.0.0.0", port=5000)

def consumer_benchmark_test_queue(channel_name: str, channels):
    channel = channels[channel_name]
    while True:
        task = channel.get()
        if task is None:
            break
        # Simulate processing task
        print(f"Worker process ID: {os.getpid()}")
        print(f"Processing task in channel {channel_name}: {task}")
        QueueTaskProcessor.run_benchmark_test(task)
        time.sleep(1)

def process_task(task_data: dict[str, Any]) -> None:
    # Example processing of task_data
    print("Processing task with data:", task_data)

def main():
    # global SHARED_CHANNELS
    globals.BENCHMARK_TEST_QUEUE_MANAGER = QueueManager(QUEUE_TYPE)
    globals.BENCHMARK_TEST_QUEUE_MANAGER.subscribe(QueueTaskProcessor.run_benchmark_test)
    # connection = queue_manager.connect(); #TODO - this needs to be a Singleton - Explore using IOC container for better management
    # globals.SHARED_CHANNELS = connection.get_channels()


    # TODO
    # A separate channel for test workers to produce feedback messages to the app
    # Explore if uvicorn's event loop can be used to handle feedback from the channel using async.io
    # benchmark_updates_channel = "benchmark_update" 

    # Start Uvicorn in a separate thread
    uvicorn_thread = Thread(target=run_uvicorn) #automatically be killed when all non-daemon threads (including the main thread) have exited
    uvicorn_thread.start()

    # Create a pool of 4 worker processes
    # pool = None
    # try:
    #     pool = Pool(4)
    #     result = pool.starmap_async(consumer_benchmark_test_queue, [(BENCHMARK_TEST_CHANNEL,globals.SHARED_CHANNELS)] * 4)
    #     # result.wait()
    # except KeyboardInterrupt:
    #     print("KeyboardInterrupt. Terminating workers.")
    #     if pool is not None:
    #         pool.terminate()  # Immediately stop the worker processes
    #         pool.close()  # Necesary before join(). Clean up the pool resources
    #         pool.join()  # Necessary to wait for the worker processes to exit
    #         connection.close();
    #         print("Cleaned up resources.")
            

if __name__ == "__main__":
    main()