from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..schemas.recipe_response_dto import RecipeResponseDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class RecipeService(BaseService):

    @exception_handler
    def create_recipe(self, recipe_data: RecipeCreateDTO) -> None:
        moonshot_api.api_create_recipe(
            name=recipe_data.name,
            description=recipe_data.description,
            tags=recipe_data.tags,
            datasets=recipe_data.datasets,
            prompt_templates=recipe_data.prompt_templates,
            metrics=recipe_data.metrics,
            type=recipe_data.type,
            attack_strategies=recipe_data.attack_strategies
        )
    

    @exception_handler
    def get_all_recipes(self) -> list[RecipeResponseDTO | None]:
        recipes = moonshot_api.api_get_all_recipe()
        return [RecipeResponseDTO.model_validate(recipe) for recipe in recipes]
    

    @exception_handler
    def get_all_recipes_name(self) -> list[str]:
        recipes = moonshot_api.api_get_all_recipe_name()
        return recipes


    @exception_handler
    def get_recipe_by_id(self, recipe_id: str) -> RecipeResponseDTO | None: 
        recipe = moonshot_api.api_read_recipe(recipe_id)
        return RecipeResponseDTO.model_validate(recipe)


    @exception_handler
    def update_recipe(self, recipe_data: RecipeCreateDTO, recipe_id: str) -> None:
        moonshot_api.api_update_recipe(
            rec_id=recipe_id,
            name=recipe_data.name,
            description=recipe_data.description,
            tags=recipe_data.tags,
            datasets=recipe_data.datasets,
            prompt_templates=recipe_data.prompt_templates,
            metrics=recipe_data.metrics,
            type=recipe_data.type,
            attack_strategies=recipe_data.attack_strategies
        )


    @exception_handler
    def delete_recipe(self, recipe_id: str) -> None:
        moonshot_api.api_delete_recipe(recipe_id)
