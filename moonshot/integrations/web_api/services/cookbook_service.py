from .... import api as moonshot_api
from ..schemas.cookbook_create_dto import CookbookCreateDTO
from ..schemas.cookbook_response_dto import CookbookResponseDTO
from ..schemas.recipe_response_dto import RecipeResponseDTO
from ..services.base_service import BaseService
from ..services.recipe_service import get_total_prompt_in_recipe
from ..services.utils.exceptions_handler import exception_handler


class CookbookService(BaseService):
    @exception_handler
    def create_cookbook(self, cookbook_data: CookbookCreateDTO) -> None:
        moonshot_api.api_create_cookbook(
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes,
        )

    @exception_handler
    def get_all_cookbooks(
        self, tags: str, categories: str, count: bool
    ) -> list[CookbookResponseDTO | None]:
        cookbooks = moonshot_api.api_get_all_cookbook()
        filtered_cookbooks = []
        for cookbook in cookbooks:
            cookbook = CookbookResponseDTO(**cookbook)
            if count:
                cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(
                    cookbook
                )
            if not tags and not categories:
                filtered_cookbooks.append(CookbookResponseDTO.model_validate(cookbook))
                continue
            if tags and cookbooks_recipe_has_tags(tags, cookbook):
                filtered_cookbooks.append(CookbookResponseDTO.model_validate(cookbook))
            if categories and cookbooks_recipe_has_categories(categories, cookbook):
                if cookbook not in filtered_cookbooks:
                    filtered_cookbooks.append(
                        CookbookResponseDTO.model_validate(cookbook)
                    )
        return filtered_cookbooks

    @exception_handler
    def get_all_cookbooks_names(self) -> list[str]:
        cookbooks = moonshot_api.api_get_all_cookbook_name()
        return cookbooks

    @exception_handler
    def get_cookbook_by_ids(self, cookbook_id: str) -> list[CookbookResponseDTO] | None:
        ret_cookbooks = []
        cb_id_list = cookbook_id.split(",")
        for id in cb_id_list:
            cookbook = moonshot_api.api_read_cookbook(id)
            cookbook = CookbookResponseDTO(**cookbook)
            cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(cookbook)
            ret_cookbooks.append(cookbook)

        return [CookbookResponseDTO.model_validate(cb) for cb in ret_cookbooks]

    @exception_handler
    def update_cookbook(
        self, cookbook_data: CookbookCreateDTO, cookbook_id: str
    ) -> None:
        moonshot_api.api_update_cookbook(
            cb_id=cookbook_id,
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes,
        )

    @exception_handler
    def delete_cookbook(self, cookbook_id: str) -> None:
        moonshot_api.api_delete_cookbook(cookbook_id)


@staticmethod
def get_total_prompt_in_cookbook(cookbook: CookbookResponseDTO) -> int:
    recipes = moonshot_api.api_read_recipes(cookbook.recipes)
    return sum(
        get_total_prompt_in_recipe(RecipeResponseDTO(**recipe)) for recipe in recipes
    )


@staticmethod
def cookbooks_recipe_has_tags(tags: str, cookbook: CookbookResponseDTO) -> bool:
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = RecipeResponseDTO(**recipe)
        if tags in recipe.tags:
            return True
    return False


@staticmethod
def cookbooks_recipe_has_categories(
    categories: str, cookbook: CookbookResponseDTO
) -> bool:
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = RecipeResponseDTO(**recipe)
        if categories in recipe.categories:
            return True
    return False
