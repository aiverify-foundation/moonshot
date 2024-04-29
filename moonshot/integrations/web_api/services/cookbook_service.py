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
            cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(cookbook.id)
            if not tags or cookbooks_recipe_has_tags(tags, cookbook.id):
                filtered_cookbooks.append(CookbookResponeDTO.model_validate(cookbook))
        return filtered_cookbooks


    @exception_handler
    def get_all_cookbooks_names(self) -> list[str]:
        cookbooks = moonshot_api.api_get_all_cookbook_name()
        return cookbooks
    

    @exception_handler
    def get_cookbook_by_id(self, cookbook_id: str) -> CookbookResponeDTO | None: 
        cookbook = moonshot_api.api_read_cookbook(cookbook_id)
        cookbook = CookbookResponeDTO(**cookbook)
        cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(cookbook.id)
        return CookbookResponeDTO.model_validate(cookbook)


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
def get_total_prompt_in_cookbook(cookbook_id: str) -> int:
    total_prompt_count = 0
    cookbook = moonshot_api.api_read_cookbook(cookbook_id)
    cookbook = CookbookResponeDTO(**cookbook)
    for recipe in cookbook.recipes:
        total_prompt_count += get_total_prompt_in_recipe(recipe)

    return total_prompt_count

@staticmethod
def cookbooks_recipe_has_tags(tags: str, cookbook_id: str) -> bool:
    cookbook = moonshot_api.api_read_cookbook(cookbook_id)
    cookbook = CookbookResponeDTO(**cookbook)
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = RecipeResponseDTO(**recipe)
        if tags in recipe.tags:
            return True
    return False