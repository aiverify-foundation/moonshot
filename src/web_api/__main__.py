import uvicorn
import os
from dotenv import load_dotenv
from threading import Thread
from dependency_injector.wiring import Provide, inject
from .queue.interface.queue_connection import InterfaceQueueConnection
from .queue.queue_job_worker import QueueJobWorker
from .app import create_app


def start_app():
    load_dotenv()
    ENABLE_SSL = os.getenv("ENABLE_SSL", "false").lower() in ['true', '1', 't', 'y', 'yes', 'enabled']
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
    app = create_app()
    singleton_benchmark_test_queue: InterfaceQueueConnection = app.container.benchmarking_test_queue()
    singleton_benchmark_test_queue.subscribe(QueueJobWorker.run_benchmark_test)
    certs_path = SSL_CERT_PATH
    if ENABLE_SSL:
        uvicorn.run(app, host="0.0.0.0", port=5000, ssl_keyfile=os.path.join(certs_path, "key.pem"), ssl_certfile=os.path.join(certs_path, "cert.pem"))
    else:
        uvicorn.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_app()