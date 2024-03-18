from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..types.types import BenchmarkResult
from ..services.benchmark_test_manager import BenchmarkTestManager
from ..services.utils.results_formatter import transform_web_format
from ..schemas.cookbook_create_dto import CookbookCreateDTO
from ..schemas.cookbook_executor_create_dto import CookbookExecutorCreateDTO
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..schemas.recipe_executor_create_dto import RecipeExecutorCreateDTO
from ..services.base_service import BaseService
from ..schemas.endpoint_response_model import EndpointDataModel
from ..services.utils.exceptions_handler import exception_handler

class BenchmarkingService(BaseService):
    @inject
    def __init__(self, benchmark_test_manager: BenchmarkTestManager) -> None:
        self.benchmark_test_manager = benchmark_test_manager

    @exception_handler
    def get_all_endpoints(self) -> list[EndpointDataModel | None]:
        endpoints = moonshot_api.api_get_all_endpoint()
        return [EndpointDataModel.model_validate(endpoint) for endpoint in endpoints]


    @exception_handler
    def add_endpoint(self, endpoint_data: EndpointDataModel) -> None:
        moonshot_api.api_create_endpoint(
            connector_type=endpoint_data.connector_type,
            name=endpoint_data.name,
            uri=endpoint_data.uri,
            token=endpoint_data.token,
            max_calls_per_second=endpoint_data.max_calls_per_second,
            max_concurrency=endpoint_data.max_concurrency,
            params=endpoint_data.params
        )

    @exception_handler
    def delete_endpoint(self, endpoint_id: str) -> None:
        moonshot_api.api_delete_endpoint(endpoint_id)

    @exception_handler
    def get_all_connectors(self) -> list[str]:
        connectors = moonshot_api.api_get_all_connector_type()
        return connectors

    @exception_handler
    def get_all_recipes(self) -> list[dict]:
        recipes = moonshot_api.api_get_all_recipe()
        return recipes

    @exception_handler
    def create_recipe(self, recipe_data: RecipeCreateDTO) -> None:
        moonshot_api.api_create_recipe(
            name=recipe_data.name,
            description=recipe_data.description,
            tags=recipe_data.tags,
            datasets=recipe_data.datasets,
            prompt_templates=recipe_data.prompt_templates,
            metrics=recipe_data.metrics
        )

    @exception_handler
    def delete_recipe(self, recipe_id: str) -> None:
        moonshot_api.api_delete_recipe(recipe_id)

    @exception_handler
    def create_cookbook(self, cookbook_data: CookbookCreateDTO) -> None:
        moonshot_api.api_create_cookbook(
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes
        )
    
    @exception_handler
    def update_cookbook(self, cookbook_data: CookbookCreateDTO, cookbook_id: str) -> None:
        moonshot_api.api_update_cookbook(
            id=cookbook_id,
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes
        )

    @exception_handler
    def get_all_cookbooks(self) -> dict:
        cookbooks = moonshot_api.api_get_all_cookbook()
        return cookbooks

    @exception_handler
    def get_cookbook_by_id(self, cookbook_id: str) -> dict: 
        cookbook = moonshot_api.api_read_cookbook(cookbook_id)
        return cookbook
    
    @exception_handler
    def get_cookbooks_by_ids(self, cookbook_ids: list[str]) -> list[dict]: 
        cookbooks = moonshot_api.api_read_cookbooks(cookbook_ids)
        return cookbooks
    
    @exception_handler
    async def execute_cookbook(self, cookbook_executor_data: CookbookExecutorCreateDTO) -> str:
        id = self.benchmark_test_manager.schedule_test_task(cookbook_executor_data);
        return id

    @exception_handler
    async def execute_recipe(self, recipe_executor_data: RecipeExecutorCreateDTO):
        async_task = self.benchmark_test_manager.schedule_test_task(recipe_executor_data);
        return async_task.get_name()
    
    @exception_handler
    def get_all_results(self, executor_id: str | None = None) -> list[BenchmarkResult] | BenchmarkResult | None:
        results: list[BenchmarkResult] = moonshot_api.api_get_all_result()
        if not executor_id:
            # returning in raw format because tranforming a big list is probably expensive
            return results
        
        for result in results:
            if result["metadata"]["id"] == executor_id:
                return transform_web_format(result)
        return None

    @exception_handler
    async def cancel_executor(self, executor_id: str) -> None:
        self.benchmark_test_manager.cancel_task(executor_id);
