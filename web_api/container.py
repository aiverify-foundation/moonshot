from dependency_injector import containers, providers
from .services.benchmarking_service import BenchmarkingService
from .services.session_service import SessionService
from .services.benchmark_test_manager import BenchmarkTestManager

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    benchmark_test_manager: providers.Singleton[BenchmarkTestManager] = providers.Singleton(BenchmarkTestManager)
    session_service: providers.Factory[SessionService] = providers.Factory(SessionService)
    benchmarking_service: providers.Factory[BenchmarkingService] = providers.Factory(
        BenchmarkingService,
        benchmark_test_manager=benchmark_test_manager
    )

    wiring_config = containers.WiringConfiguration(modules=[
        ".routes.redteam",
        ".routes.benchmark",
        ".services.benchmarking_service"
    ])
