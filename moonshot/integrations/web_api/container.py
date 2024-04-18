from dependency_injector import containers, providers

from moonshot.integrations.web_api.services.benchmark_test_state import BenchmarkTestState

from .status_updater.webhook import Webhook
from .services.benchmarking_service import BenchmarkingService
from .services.prompt_template_service import PromptTemplateService
from .services.endpoint_service import EndpointService
from .services.recipe_service import RecipeService
from .services.cookbook_service import CookbookService
from .services.session_service import SessionService
from .services.benchmark_result_service import BenchmarkResultService
from .services.benchmark_test_manager import BenchmarkTestManager
from .services.metric_service import MetricService
from .services.runner_service import RunnerService
from .services.dataset_service import DatasetService
from .services.attack_strategy_service import AttackStrategyService 

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
    prompt_template_service: providers.Singleton[PromptTemplateService] = providers.Singleton(
        PromptTemplateService,
    )
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
    metric_service: providers.Singleton[MetricService] = providers.Singleton(
        MetricService,
    )
    runner_service: providers.Singleton[RunnerService] = providers.Singleton(
        RunnerService,
    )
    dataset_service: providers.Singleton[DatasetService] = providers.Singleton(
        DatasetService,
    )
    as_service: providers.Singleton[AttackStrategyService] = providers.Singleton(
        AttackStrategyService,
    )
    wiring_config = containers.WiringConfiguration(modules=[
        ".routes.redteam",
        ".routes.prompt_template",
        ".routes.benchmark",
        ".routes.endpoint",
        ".routes.recipe",
        ".routes.cookbook",
        ".routes.benchmark_result",
        ".routes.metric",
        ".routes.runner",
        ".routes.dataset",
        ".routes.attack_strategy",
        ".services.benchmarking_service"
    ])
