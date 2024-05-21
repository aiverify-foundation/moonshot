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
# from moonshot.integrations.web_api.services.context_strategies import context_strategies

@pytest.fixture(scope="module")
def mock_am_service():
    return Mock(spec=AttackModuleService)

# @pytest.fixture(scope="module")
# def mock_cs_service():
#     return Mock(spec=AttackModuleService)

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
def test_client(mock_pt_service, mock_recipe_service, mock_am_service, mock_cookbook_service, mock_metric_service):
    test_container = Container()
    test_container.config.from_default() 

    test_container.recipe_service.override(mock_recipe_service)
    test_container.prompt_template_service.override(mock_pt_service)
    test_container.am_service.override(mock_am_service)
    test_container.cookbook_service.override(mock_cookbook_service)
    test_container.metric_service.override(mock_metric_service)

    # Wire the container
    test_container.wire(modules=["moonshot.integrations.web_api.routes"])

    # Create a new FastAPI app instance for testing
    app = create_app(test_container.config)

    # Use TestClient with the app instance
    return TestClient(app)
