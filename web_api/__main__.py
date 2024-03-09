import uvicorn
import os
import logging
from dotenv import load_dotenv
from threading import Thread

from .types.types import UvicornRunArgs

from .container import Container
from .logging_conf import configure_logging
from .queue.interface.queue_connection import InterfaceQueueConnection
from .queue.queue_job_worker import QueueJobWorker
from .app import create_app


def start_app():
    load_dotenv()
    container: Container = Container()
    container.config.from_yaml("web_api/config.yml", required=True)
    configure_logging(container.config)
    logging.info(f"Environment: {container.config.app_environment()}")
    ENABLE_SSL = container.config.ssl.enabled()
    SSL_CERT_PATH = container.config.ssl.file_path()
    app = create_app(container.config)
    # singleton_benchmark_test_queue: InterfaceQueueConnection = app.container.benchmarking_test_queue()
    # singleton_benchmark_test_queue.subscribe(QueueJobWorker.run_benchmark_test)
    
    run_kwargs: UvicornRunArgs = {}
    run_kwargs['port'] = 5000
    run_kwargs['host'] = "0.0.0.0"
    if ENABLE_SSL:
        if not SSL_CERT_PATH:
            logging.debug("SSL_CERT_PATH not set, not enabling SSL")
        elif os.path.exists(os.path.join(SSL_CERT_PATH, "key.pem")) and os.path.exists(os.path.join(SSL_CERT_PATH, "cert.pem")):
            run_kwargs["ssl_keyfile"] = str(os.path.join(SSL_CERT_PATH, str(container.config.ssl.key_filename())))
            run_kwargs["ssl_certfile"] = str(os.path.join(SSL_CERT_PATH, str(container.config.ssl.cert_filename())))
        else:
            logging.debug("SSL_CERT_PATH does not contain necessary files, not enabling SSL")
    uvicorn.run(app, **run_kwargs)

if __name__ == "__main__":
    start_app()