import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from moonshot.integrations.web_api.app import create_app
from moonshot.integrations.web_api.container import Container
from moonshot.integrations.web_api.services.metric_service import MetricService
from moonshot.integrations.web_api.services.cookbook_service import CookbookService
from moonshot.integrations.web_api.services.recipe_service import RecipeService
from moonshot.integrations.web_api.services.attack_module_service import AttackModuleService
from moonshot.integrations.web_api.services.prompt_template_service import PromptTemplateService
from moonshot.integrations.web_api.services.runner_service import RunnerService
from moonshot.integrations.web_api.services.benchmark_result_service import BenchmarkResultService
from moonshot.integrations.web_api.services.dataset_service import DatasetService
from moonshot.integrations.web_api.services.endpoint_service import EndpointService
from moonshot.integrations.web_api.services.benchmarking_service import BenchmarkingService
from moonshot.integrations.web_api.services.session_service import SessionService
from moonshot.integrations.web_api.services.context_strategy_service import ContextStrategyService
from moonshot.integrations.web_api.services.benchmark_test_state import BenchmarkTestState
from moonshot.integrations.web_api.services.bookmark_service import BookmarkService

@pytest.fixture(scope="module")
def mock_bm_test_state():
    return Mock(spec=BenchmarkTestState)

@pytest.fixture(scope="module")
def mock_cs_service():
    return Mock(spec=ContextStrategyService)

@pytest.fixture(scope="module")
def mock_am_service():
    return Mock(spec=AttackModuleService)

@pytest.fixture(scope="module")
def mock_bm_service():
    return Mock(spec=BenchmarkingService)

@pytest.fixture(scope="module")
def mock_dataset_service():
    return Mock(spec=DatasetService)

@pytest.fixture(scope="module")
def mock_endpoint_service():
    return Mock(spec=EndpointService)

@pytest.fixture(scope="module")
def mock_bm_result_service():
    return Mock(spec=BenchmarkResultService)

@pytest.fixture(scope="module")
def mock_runner_service():
    return Mock(spec=RunnerService)

@pytest.fixture(scope="module")
def mock_pt_service():
    return Mock(spec=PromptTemplateService)

@pytest.fixture(scope="module")
def mock_cookbook_service():
    return Mock(spec=CookbookService)

@pytest.fixture(scope="module")
def mock_recipe_service():
    return Mock(spec=RecipeService)

@pytest.fixture(scope="module")
def mock_metric_service():
    return Mock(spec=MetricService)

@pytest.fixture(scope="module")
def mock_session_service():
    return Mock(spec=SessionService)

@pytest.fixture(scope="module")
def mock_bookmark_service():
    return Mock(spec=BookmarkService)

@pytest.fixture(scope="module")
def test_client(
    mock_pt_service, 
    mock_runner_service,
    mock_bm_result_service,
    mock_recipe_service,
    mock_am_service,
    mock_cookbook_service,
    mock_metric_service,
    mock_endpoint_service,
    mock_dataset_service,
    mock_bm_service,
    mock_bm_test_state,
    mock_session_service,
    mock_cs_service,
    mock_bookmark_service,
    ):
    test_container = Container()
    test_container.config.from_default() 

    test_container.session_service.override(mock_session_service)
    test_container.context_strategy_service.override(mock_cs_service)
    test_container.endpoint_service.override(mock_endpoint_service)
    test_container.dataset_service.override(mock_dataset_service)
    test_container.benchmarking_service.override(mock_bm_service)
    test_container.benchmark_test_state.override(mock_bm_test_state)
    test_container.benchmark_result_service.override(mock_bm_result_service)
    test_container.runner_service.override(mock_runner_service)
    test_container.recipe_service.override(mock_recipe_service)
    test_container.prompt_template_service.override(mock_pt_service)
    test_container.am_service.override(mock_am_service)
    test_container.cookbook_service.override(mock_cookbook_service)
    test_container.metric_service.override(mock_metric_service)
    test_container.bookmark_service.override(mock_bookmark_service)
    
    # Wire the container
    test_container.wire(modules=["moonshot.integrations.web_api.routes"])

    # Create a new FastAPI app instance for testing
    app = create_app(test_container.config)

    # Use TestClient with the app instance
    return TestClient(app)
