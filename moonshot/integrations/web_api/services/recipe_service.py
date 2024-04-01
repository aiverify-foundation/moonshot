from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
class RecipeService(BaseService):
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
