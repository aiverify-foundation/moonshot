import uvicorn
from threading import Thread
from dependency_injector.wiring import Provide, inject

from .queue.interface.queue_connection import InterfaceQueueConnection
from .queue.queue_job_worker import QueueJobWorker
from .app import create_app

def start_app():
    app = create_app()
    singleton_benchmark_test_queue: InterfaceQueueConnection = app.container.benchmarking_test_queue()
    singleton_benchmark_test_queue.subscribe(QueueJobWorker.run_benchmark_test)
    uvicorn.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_app()