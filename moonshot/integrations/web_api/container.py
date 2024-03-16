from dependency_injector import containers, providers

from moonshot.integrations.web_api.services.benchmark_test_state import BenchmarkTestState

from .status_updater.webhook import Webhook
from .services.benchmarking_service import BenchmarkingService
from .services.session_service import SessionService
from .services.benchmark_test_manager import BenchmarkTestManager
import importlib.resources

class Container(containers.DeclarativeContainer):

    config = providers.Configuration('config')
    config.from_dict({
        'app_environment': 'DEV',
        'asyncio': {
            'monitor_task': False,
        },
        'ssl': {
            'enabled': False,
            'file_path': str(importlib.resources.files("moonshot").joinpath("integrations/web_api/certs")),
            'cert_filename': 'cert.pem',
            'key_filename': 'key.pem',
        },
        'cors': {
            'enabled': False,
            'allowed_origins': 'http://localhost:3000',
        },
        'log': {
            'logging': True,
            'level': 'DEBUG',
            'format': "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            'log_file_path': str(importlib.resources.files("moonshot").joinpath("integrations/web_api/log")),
            'log_file_max_size': 5242880,
            'log_file_backup_count': 3
        }
    })

    benchmark_test_state: providers.Singleton[BenchmarkTestState] = providers.Singleton(BenchmarkTestState)
    webhook: providers.Singleton[Webhook] = providers.Singleton(
        Webhook,
        benchmark_test_state=benchmark_test_state)
    benchmark_test_manager: providers.Singleton[BenchmarkTestManager] = providers.Singleton(
        BenchmarkTestManager,
        benchmark_test_state=benchmark_test_state,
        webhook=webhook)
    session_service: providers.Factory[SessionService] = providers.Factory(SessionService)
    benchmarking_service: providers.Singleton[BenchmarkingService] = providers.Singleton(
        BenchmarkingService,
        benchmark_test_manager=benchmark_test_manager,
    )

    wiring_config = containers.WiringConfiguration(modules=[
        ".routes.redteam",
        ".routes.benchmark",
        ".services.benchmarking_service"
    ])
