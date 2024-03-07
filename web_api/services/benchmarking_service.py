import moonshot.api as moonshot_api
from web_api.schemas.recipe_create_dto import RecipeCreateDTO
from web_api.services.base_service import BaseService
from ..schemas.endpoint_response_model import EndpointDataModel
from ..services.utils.exceptions_handler import exception_handler

class BenchmarkingService(BaseService):

    @exception_handler
    def get_all_endpoints(self) -> list[EndpointDataModel | None]:
        endpoints = moonshot_api.api_get_all_endpoints()
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
        connectors = moonshot_api.api_get_all_connectors()
        return connectors

    @exception_handler
    def get_all_recipes(self) -> list[dict]:
        recipes = moonshot_api.api_get_all_recipes()
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


