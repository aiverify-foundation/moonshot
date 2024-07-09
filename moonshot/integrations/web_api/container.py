import importlib.resources

from dependency_injector import containers, providers

from .services.attack_module_service import AttackModuleService
from .services.auto_red_team_test_manager import AutoRedTeamTestManager
from .services.auto_red_team_test_state import AutoRedTeamTestState
from .services.benchmark_result_service import BenchmarkResultService
from .services.benchmark_test_manager import BenchmarkTestManager
from .services.benchmark_test_state import BenchmarkTestState
from .services.benchmarking_service import BenchmarkingService
from .services.bookmark_service import BookmarkService
from .services.context_strategy_service import ContextStrategyService
from .services.cookbook_service import CookbookService
from .services.dataset_service import DatasetService
from .services.endpoint_service import EndpointService
from .services.metric_service import MetricService
from .services.prompt_template_service import PromptTemplateService
from .services.recipe_service import RecipeService
from .services.runner_service import RunnerService
from .services.session_service import SessionService
from .status_updater.moonshot_ui_webhook import MoonshotUIWebhook


class Container(containers.DeclarativeContainer):
    config = providers.Configuration("config")
    config.from_dict(
        {
            "app_environment": "DEV",
            "asyncio": {
                "monitor_task": False,
            },
            "ssl": {
                "enabled": False,
                "file_path": str(
                    importlib.resources.files("moonshot").joinpath(
                        "integrations/web_api/certs"
                    )
                ),
                "cert_filename": "cert.pem",
                "key_filename": "key.pem",
            },
            "cors": {
                "enabled": False,
                "allowed_origins": "http://localhost:3000",
            },
            "log": {
                "logging": True,
                "level": "DEBUG",
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                "log_file_path": str(
                    importlib.resources.files("moonshot").joinpath(
                        "integrations/web_api/log"
                    )
                ),
                "log_file_max_size": 5242880,
                "log_file_backup_count": 3,
            },
            "temp_folder": str(
                    importlib.resources.files("moonshot").joinpath(
                        "integrations/web_api/temp"
                    )
                ),
        }
    )

    benchmark_test_state: providers.Singleton[BenchmarkTestState] = providers.Singleton(
        BenchmarkTestState
    )
    auto_red_team_test_state: providers.Singleton[
        AutoRedTeamTestState
    ] = providers.Singleton(AutoRedTeamTestState)
    webhook: providers.Singleton[MoonshotUIWebhook] = providers.Singleton(
        MoonshotUIWebhook,
        benchmark_test_state=benchmark_test_state,
        auto_red_team_test_state=auto_red_team_test_state,
    )
    runner_service: providers.Singleton[RunnerService] = providers.Singleton(
        RunnerService
    )
    auto_red_team_test_manager: providers.Singleton[
        AutoRedTeamTestManager
    ] = providers.Singleton(
        AutoRedTeamTestManager,
        auto_red_team_test_state=auto_red_team_test_state,
        progress_status_updater=webhook,
        runner_service=runner_service,
    )
    benchmark_test_manager: providers.Singleton[
        BenchmarkTestManager
    ] = providers.Singleton(
        BenchmarkTestManager,
        benchmark_test_state=benchmark_test_state,
        progress_status_updater=webhook,
        runner_service=runner_service,
    )
    session_service: providers.Singleton[SessionService] = providers.Singleton(
        SessionService,
        auto_red_team_test_manager=auto_red_team_test_manager,
        progress_status_updater=webhook,
        runner_service=runner_service,
    )
    prompt_template_service: providers.Singleton[
        PromptTemplateService
    ] = providers.Singleton(PromptTemplateService)
    context_strategy_service: providers.Singleton[
        ContextStrategyService
    ] = providers.Singleton(ContextStrategyService)
    benchmarking_service: providers.Singleton[
        BenchmarkingService
    ] = providers.Singleton(
        BenchmarkingService, benchmark_test_manager=benchmark_test_manager
    )
    endpoint_service: providers.Singleton[EndpointService] = providers.Singleton(
        EndpointService
    )
    recipe_service: providers.Singleton[RecipeService] = providers.Singleton(
        RecipeService
    )
    cookbook_service: providers.Singleton[CookbookService] = providers.Singleton(
        CookbookService
    )
    benchmark_result_service: providers.Singleton[
        BenchmarkResultService
    ] = providers.Singleton(BenchmarkResultService)
    metric_service: providers.Singleton[MetricService] = providers.Singleton(
        MetricService
    )

    dataset_service: providers.Singleton[DatasetService] = providers.Singleton(
        DatasetService,
    )
    am_service: providers.Singleton[AttackModuleService] = providers.Singleton(
        AttackModuleService,
    )
    bookmark_service: providers.Singleton[BookmarkService] = providers.Singleton(
        BookmarkService,
    )
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".routes.redteam",
            ".routes.prompt_template",
            ".routes.context_strategy",
            ".routes.benchmark",
            ".routes.endpoint",
            ".routes.recipe",
            ".routes.cookbook",
            ".routes.benchmark_result",
            ".routes.metric",
            ".routes.runner",
            ".routes.dataset",
            ".routes.attack_modules",
            ".routes.bookmark",
            ".services.benchmarking_service",
        ]
    )
