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
            categories=recipe_data.categories,
            datasets=recipe_data.datasets,
            prompt_templates=recipe_data.prompt_templates,
            metrics=recipe_data.metrics,
            attack_modules=recipe_data.attack_modules
        )
    

    @exception_handler
    def get_all_recipes(self, tags: str, sort_by: str, count: bool) -> list[RecipeResponseDTO]:
        recipes = moonshot_api.api_get_all_recipe()
        filtered_recipes = []

        for recipe_dict in recipes:
            recipe = RecipeResponseDTO(**recipe_dict)
            if count:
                recipe.total_prompt_in_recipe = get_total_prompt_in_recipe(recipe)
            filtered_recipes.append(recipe)

        if tags:
            filtered_recipes = [recipe for recipe in filtered_recipes if tags in recipe.tags]

        if sort_by:
            if sort_by == "id":
                filtered_recipes.sort(key=lambda x: x.id)

        return [RecipeResponseDTO.model_validate(recipe) for recipe in filtered_recipes]


    @exception_handler
    def get_all_recipes_name(self) -> list[str]:
        recipes = moonshot_api.api_get_all_recipe_name()
        return recipes


    @exception_handler
    def get_recipe_by_ids(self, recipe_id: str) -> list[RecipeResponseDTO] | None:
        ret_recipes = []
        recipe_id_list = recipe_id.split(",")
        for id in recipe_id_list:
            recipe = moonshot_api.api_read_recipe(id)
            recipe = RecipeResponseDTO(**recipe)
            recipe.total_prompt_in_recipe = get_total_prompt_in_recipe(recipe)
            ret_recipes.append(recipe)
        return [RecipeResponseDTO.model_validate(recipe) for recipe in ret_recipes]


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
            attack_modules=recipe_data.attack_modules
        )


    @exception_handler
    def delete_recipe(self, recipe_id: str) -> None:
        moonshot_api.api_delete_recipe(recipe_id)

@staticmethod
def get_total_prompt_in_recipe(recipe: RecipeResponseDTO) -> int:
    total_prompt_count = 0
    if "num_of_datasets_prompts" in recipe.stats:
        datasets_prompts = recipe.stats["num_of_datasets_prompts"]
        for dataset, count in datasets_prompts.items():
            total_prompt_count += count
    if recipe.prompt_templates:
        total_prompt_count = total_prompt_count * recipe.stats["num_of_prompt_templates"]

    return total_prompt_count