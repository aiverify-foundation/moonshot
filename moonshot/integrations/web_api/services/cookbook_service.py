from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.cookbook_create_dto import CookbookCreateDTO
from ..schemas.cookbook_response_dto import CookbookResponeDTO
from ..schemas.recipe_response_dto import RecipeResponseDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from ..services.recipe_service import get_total_prompt_in_recipe

class CookbookService(BaseService):

    @exception_handler
    def create_cookbook(self, cookbook_data: CookbookCreateDTO) -> None:
        moonshot_api.api_create_cookbook(
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes
        )
    

    @exception_handler
    def get_all_cookbooks(self, tags: str) -> list[CookbookResponeDTO | None]:
        cookbooks = moonshot_api.api_get_all_cookbook()
        filtered_cookbooks = []
        for cookbook in cookbooks:
            cookbook = CookbookResponeDTO(**cookbook)
            cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(cookbook)
            if not tags or cookbooks_recipe_has_tags(tags, cookbook):
                filtered_cookbooks.append(CookbookResponeDTO.model_validate(cookbook))
        return filtered_cookbooks


    @exception_handler
    def get_all_cookbooks_names(self) -> list[str]:
        cookbooks = moonshot_api.api_get_all_cookbook_name()
        return cookbooks
    

    @exception_handler
    def get_cookbook_by_ids(self, cookbook_id: str) -> list[CookbookResponeDTO] | None: 
        ret_cookbooks =[]
        cb_id_list = cookbook_id.split(",")
        for id in cb_id_list:
            cookbook = moonshot_api.api_read_cookbook(id)
            cookbook = CookbookResponeDTO(**cookbook)
            cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(cookbook)
            ret_cookbooks.append(cookbook)

        return [CookbookResponeDTO.model_validate(cb) for cb in ret_cookbooks]


    @exception_handler
    def update_cookbook(self, cookbook_data: CookbookCreateDTO, cookbook_id: str) -> None:
        moonshot_api.api_update_cookbook(
            cb_id=cookbook_id,
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes
        )


    @exception_handler
    def delete_cookbook(self, cookbook_id: str) -> None:
        moonshot_api.api_delete_cookbook(cookbook_id)

@staticmethod
def get_total_prompt_in_cookbook(cookbook: CookbookResponeDTO) -> int:
    total_prompt_count = 0
    for recipe_id in cookbook.recipes:
        recipe = moonshot_api.api_read_recipe(recipe_id)
        recipe = RecipeResponseDTO(**recipe)
        total_prompt_count += get_total_prompt_in_recipe(recipe)

    return total_prompt_count

@staticmethod
def cookbooks_recipe_has_tags(tags: str, cookbook: CookbookResponeDTO) -> bool:
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = RecipeResponseDTO(**recipe)
        if tags in recipe.tags:
            return True
    return False