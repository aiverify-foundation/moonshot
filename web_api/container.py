from dependency_injector import containers, providers
from .services.benchmarking_service import BenchmarkingService
from .services.session_service import SessionService
from .services.benchmark_test_manager import BenchmarkTestManager
from .queue.implementation.in_memory_queue import InMemoryQueue
from .queue.interface.queue_connection import InterfaceQueueConnection

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    benchmarking_test_queue: providers.Singleton[InterfaceQueueConnection] = providers.Singleton(InMemoryQueue, queue_name="benchmarking_test_queue")
    benchmark_test_manager: providers.Singleton[BenchmarkTestManager] = providers.Singleton(BenchmarkTestManager)
    session_service: providers.Factory[SessionService] = providers.Factory(SessionService)
    benchmarking_service: providers.Factory[BenchmarkingService] = providers.Factory(
        BenchmarkingService,
        benchmark_test_manager=benchmark_test_manager
    )

    wiring_config = containers.WiringConfiguration(modules=[
        ".routes.redteam",
        ".routes.benchmark",
        ".routes.dev_testing",
        ".services.benchmarking_service"
    ])
