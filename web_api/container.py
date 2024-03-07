from dependency_injector import containers, providers

from web_api.services.benchmarking_service import BenchmarkingService
from .services.session_service import SessionService
from .queue.implementation.in_memory_queue import InMemoryQueue
from .queue.interface.queue_connection import InterfaceQueueConnection

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        ".routes.redteam",
        ".routes.benchmark",
        # ".routes.dev_testing",
        ".app"
    ])
    benchmarking_test_queue: providers.Singleton[InterfaceQueueConnection] = providers.Singleton(InMemoryQueue, queue_name="benchmarking_test_queue")
    session_service: providers.Factory[SessionService] = providers.Factory(SessionService)
    benchmarking_service: providers.Factory[BenchmarkingService] = providers.Factory(BenchmarkingService)
