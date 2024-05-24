from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments as Cookbook
from moonshot.src.recipes.recipe_arguments import RecipeArguments as Recipe

from .... import api as moonshot_api
from ..schemas.cookbook_create_dto import CookbookCreateDTO, CookbookUpdateDTO
from ..schemas.cookbook_response_model import CookbookResponseModel
from ..services.base_service import BaseService
from ..services.recipe_service import get_total_prompt_in_recipe
from ..services.utils.exceptions_handler import exception_handler


class CookbookService(BaseService):
    @exception_handler
    def create_cookbook(self, cookbook_data: CookbookCreateDTO) -> None:
        """
        Create a new cookbook with the given data.

        Args:
            cookbook_data (CookbookCreateDTO): Data transfer object containing cookbook details.
        """
        moonshot_api.api_create_cookbook(
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes,
        )

    @exception_handler
    def get_all_cookbooks(
        self,
        tags: str,
        categories: str,
        count: bool,
        ids: str | None = None,
        categories_excluded: str | None = None,
    ) -> list[CookbookResponseModel]:
        """
        Retrieve all cookbooks, optionally filtered by tags and categories, and with prompt counts.

        Args:
            ids (str): Filter cookbooks by IDs.
            tags (str): Filter cookbooks by tags.
            categories (str): Filter cookbooks by categories.
            count (bool): Include the total prompt count in each cookbook.

        Returns:
            list[CookbookResponseModel]: A list of cookbook response models.
        """
        cookbooks_list: list[CookbookResponseModel] = []

        if ids:
            cookbook_ids = ids.split(",")
            cookbooks = [
                moonshot_api.api_read_cookbook(cookbook_id)
                for cookbook_id in cookbook_ids
            ]
        else:
            cookbooks = moonshot_api.api_get_all_cookbook()

        for cookbook_dict in cookbooks:
            cookbook = CookbookResponseModel(**cookbook_dict)

            if not tags and not categories:
                if cookbook not in cookbooks_list:
                    cookbooks_list.append(cookbook)
                    if count:
                        cookbook.total_prompt_in_cookbook = (
                            get_total_prompt_in_cookbook(cookbook)
                        )

            if tags and cookbooks_recipe_has_tags(tags, cookbook):
                if cookbook not in cookbooks_list:
                    cookbooks_list.append(cookbook)
                    if count:
                        cookbook.total_prompt_in_cookbook = (
                            get_total_prompt_in_cookbook(cookbook)
                        )

            if categories and cookbooks_recipe_has_categories(categories, cookbook):
                if cookbook not in cookbooks_list:
                    cookbooks_list.append(cookbook)
                    if count:
                        cookbook.total_prompt_in_cookbook = (
                            get_total_prompt_in_cookbook(cookbook)
                        )

            if categories_excluded and cookbooks_recipe_has_categories(
                categories_excluded, cookbook
            ):
                cookbooks_list.remove(cookbook)

        return cookbooks_list

    @exception_handler
    def get_all_cookbooks_names(self) -> list[str]:
        """
        Retrieve the names of all cookbooks.

        Returns:
            list[str]: A list of cookbook names.
        """
        cookbooks = moonshot_api.api_get_all_cookbook_name()
        return cookbooks

    @exception_handler
    def update_cookbook(
        self, cookbook_data: CookbookUpdateDTO, cookbook_id: str
    ) -> None:
        """
        Update an existing cookbook with new data.

        Args:
            cookbook_data (CookbookCreateDTO): Data transfer object containing new cookbook details.
            cookbook_id (str): The ID of the cookbook to update.
        """
        update_data = {
            k: v
            for k, v in cookbook_data.to_dict().items()
            if v is not None and k != "id"
        }
        moonshot_api.api_update_cookbook(cb_id=cookbook_id, **update_data)

    @exception_handler
    def delete_cookbook(self, cookbook_id: str) -> None:
        """
        Delete a cookbook by its ID.

        Args:
            cookbook_id (str): The ID of the cookbook to delete.
        """
        moonshot_api.api_delete_cookbook(cookbook_id)


@staticmethod
def get_total_prompt_in_cookbook(cookbook: Cookbook) -> int:
    """
    Calculate the total number of prompts in a cookbook.

    This function sums up the total prompts for each recipe in the cookbook.

    Args:
        cookbook (Cookbook): The cookbook object containing the recipe IDs.

    Returns:
        int: The total count of prompts within the cookbook.
    """
    recipes = moonshot_api.api_read_recipes(cookbook.recipes)
    return sum(get_total_prompt_in_recipe(Recipe(**recipe)) for recipe in recipes)


@staticmethod
def cookbooks_recipe_has_tags(tags: str, cookbook: Cookbook) -> bool:
    """
    Check if any recipe in a cookbook has the specified tags.

    Args:
        tags (str): The tags to check for in the cookbook's recipes.
        cookbook (Cookbook): The cookbook object containing the recipe IDs.

    Returns:
        bool: True if any recipe in the cookbook has the specified tags, False otherwise.
    """
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = Recipe(**recipe)
        if tags in recipe.tags:
            return True
    return False


@staticmethod
def cookbooks_recipe_has_categories(categories: str, cookbook: Cookbook) -> bool:
    """
    Check if any recipe in a cookbook has the specified categories.

    Args:
        categories (str): The categories to check for in the cookbook's recipes.
        cookbook (Cookbook): The cookbook object containing the recipe IDs.
        exclude_categories (str): The categories to exclude

    Returns:
        bool: True if any recipe in the cookbook has the specified categories, False otherwise.
    """
    recipe_ids = cookbook.recipes
    categories_list = [category.lower() for category in categories.split(",")]
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = Recipe(**recipe)
        if any(
            category in [rcat.lower() for rcat in recipe.categories]
            for category in categories_list
        ):
            return True
    return False
