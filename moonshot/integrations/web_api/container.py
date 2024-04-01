from dependency_injector import containers, providers

from moonshot.integrations.web_api.services.benchmark_test_state import BenchmarkTestState

from .status_updater.webhook import Webhook
from .services.benchmarking_service import BenchmarkingService
from .services.endpoint_service import EndpointService
from .services.recipe_service import RecipeService
from .services.cookbook_service import CookbookService
from .services.session_service import SessionService
from .services.benchmark_result_service import BenchmarkResultService
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
    endpoint_service: providers.Singleton[EndpointService] = providers.Singleton(
        EndpointService,
    )
    recipe_service: providers.Singleton[RecipeService] = providers.Singleton(
        RecipeService,
    )
    cookbook_service: providers.Singleton[CookbookService] = providers.Singleton(
        CookbookService,
    )
    benchmark_result_service: providers.Singleton[BenchmarkResultService] = providers.Singleton(
        BenchmarkResultService,
    )
    wiring_config = containers.WiringConfiguration(modules=[
        ".routes.redteam",
        ".routes.benchmark",
        ".routes.endpoint_routes",
        ".routes.recipe_routes",
        ".routes.cookbook_routes",
        ".routes.benchmark_result_routes",
        ".services.benchmarking_service"
    ])
    