from queue import Queue
import uvicorn
import time
import os
from multiprocessing import Pool
from threading import Thread

from web_api.tasks.task_processor import TaskProcessor
from .tasks.implementation.in_memory_shared_queue import InMemorySharedQueue
from .tasks.queue_manager import QueueManager
from .app import init_api

# Choose the queue implementation
QUEUE_TYPE = InMemorySharedQueue()
BENCHMARK_TEST_CHANNEL = "benchmark_test"
SHARED_CHANNELS: dict[str, Queue] = {}

def run_uvicorn():
    app = init_api()
    # uvicorn (ASGI server) uses an event loop for handling async tasks associated with FastAPI app.
    # This event loop runs on the main thread
    uvicorn.run(app, host="0.0.0.0", port=5000)

def benchmark_test_worker_process(channel_name: str):
    channel = SHARED_CHANNELS[channel_name]
    while True:
        task = channel.get()
        if task is None:
            break
        # Simulate processing task
        print(f"Worker process ID: {os.getpid()}")
        print(f"Processing task in channel {channel_name}: {task}")
        TaskProcessor.run_benchmark_test(task)
        time.sleep(1)

def main():
    global SHARED_CHANNELS
    queue_manager = QueueManager(QUEUE_TYPE)
    connection = queue_manager.connect();
    connection.create_channel(BENCHMARK_TEST_CHANNEL)
    SHARED_CHANNELS = connection.get_channels()


    # TODO
    # A separate channel for test workers to produce feedback messages to the app
    # Explore if uvicorn's event loop can be used to handle feedback from the channel using async.io
    # benchmark_updates_channel = "benchmark_update" 

    # Start Uvicorn in a separate thread
    uvicorn_thread = Thread(target=run_uvicorn, daemon=True) #automatically be killed when all non-daemon threads (including the main thread) have exited
    uvicorn_thread.start()

    # Create a pool of 4 worker processes
    pool = None
    try:
        pool = Pool(4)
        pool.starmap(benchmark_test_worker_process, [(BENCHMARK_TEST_CHANNEL,)] * 4)
    except KeyboardInterrupt:
        print("KeyboardInterrupt. Terminating workers.")
        if pool is not None:
            pool.terminate()  # Immediately stop the worker processes
    finally:
        if pool is not None:
            pool.close()  # Clean up the pool resources
            pool.join()  # Wait for the worker processes to exit
        print("Cleaned up resources.")


if __name__ == "__main__":
    main()