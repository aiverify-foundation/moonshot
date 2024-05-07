from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.recipes.recipe_arguments import RecipeArguments

from .... import api as moonshot_api
from ..schemas.cookbook_create_dto import CookbookCreateDTO
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
        self, tags: str, categories: str, count: bool
    ) -> list[CookbookResponseModel]:
        """
        Retrieve all cookbooks, optionally filtered by tags and categories, and with prompt counts.

        Args:
            tags (str): Filter cookbooks by tags.
            categories (str): Filter cookbooks by categories.
            count (bool): Include the total prompt count in each cookbook.

        Returns:
            list[CookbookResponseModel]: A list of cookbook response models.
        """
        retn_cookbooks = []
        cookbooks = moonshot_api.api_get_all_cookbook()
        for cookbook_dict in cookbooks:
            cookbook = CookbookArguments(**cookbook_dict)
            retn_cookbook = CookbookResponseModel(cookbook=cookbook)
            if count:
                retn_cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(
                    cookbook
                )
            if not tags and not categories:
                retn_cookbooks.append(retn_cookbook)
            if tags and cookbooks_recipe_has_tags(tags, cookbook):
                retn_cookbooks.append(retn_cookbook)
            if categories and cookbooks_recipe_has_categories(categories, cookbook):
                if cookbook not in retn_cookbooks:
                    retn_cookbooks.append(retn_cookbook)

        return [
            CookbookResponseModel.model_validate(cookbook)
            for cookbook in retn_cookbooks
        ]

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
    def get_cookbook_by_ids(self, cookbook_id: str) -> list[CookbookResponseModel]:
        """
        Retrieve cookbooks by their IDs.

        Args:
            cookbook_id (str): A comma-separated string of cookbook IDs.

        Returns:
            list[CookbookResponseModel]: A list of cookbook response models.
        """
        retn_cookbooks = []
        cb_id_list = cookbook_id.split(",")
        for id in cb_id_list:
            cookbook_dict = moonshot_api.api_read_cookbook(id)
            cookbook = CookbookArguments(**cookbook_dict)
            retn_cookbook = CookbookResponseModel(cookbook=cookbook)
            retn_cookbook.total_prompt_in_cookbook = get_total_prompt_in_cookbook(
                cookbook
            )
            retn_cookbooks.append(retn_cookbook)
        return [
            CookbookResponseModel.model_validate(cookbook)
            for cookbook in retn_cookbooks
        ]

    @exception_handler
    def update_cookbook(
        self, cookbook_data: CookbookCreateDTO, cookbook_id: str
    ) -> None:
        """
        Update an existing cookbook with new data.

        Args:
            cookbook_data (CookbookCreateDTO): Data transfer object containing new cookbook details.
            cookbook_id (str): The ID of the cookbook to update.
        """
        moonshot_api.api_update_cookbook(
            cb_id=cookbook_id,
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes,
        )

    @exception_handler
    def delete_cookbook(self, cookbook_id: str) -> None:
        """
        Delete a cookbook by its ID.

        Args:
            cookbook_id (str): The ID of the cookbook to delete.
        """
        moonshot_api.api_delete_cookbook(cookbook_id)


@staticmethod
def get_total_prompt_in_cookbook(cookbook: CookbookArguments) -> int:
    """
    Calculate the total number of prompts in a cookbook.

    This function sums up the total prompts for each recipe in the cookbook.

    Args:
        cookbook (CookbookArguments): The cookbook object containing the recipe IDs.

    Returns:
        int: The total count of prompts within the cookbook.
    """
    recipes = moonshot_api.api_read_recipes(cookbook.recipes)
    return sum(
        get_total_prompt_in_recipe(RecipeArguments(**recipe)) for recipe in recipes
    )


@staticmethod
def cookbooks_recipe_has_tags(tags: str, cookbook: CookbookArguments) -> bool:
    """
    Check if any recipe in a cookbook has the specified tags.

    Args:
        tags (str): The tags to check for in the cookbook's recipes.
        cookbook (CookbookArguments): The cookbook object containing the recipe IDs.

    Returns:
        bool: True if any recipe in the cookbook has the specified tags, False otherwise.
    """
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = RecipeArguments(**recipe)
        if tags in recipe.tags:
            return True
    return False


@staticmethod
def cookbooks_recipe_has_categories(
    categories: str, cookbook: CookbookArguments
) -> bool:
    """
    Check if any recipe in a cookbook has the specified categories.

    Args:
        categories (str): The categories to check for in the cookbook's recipes.
        cookbook (CookbookArguments): The cookbook object containing the recipe IDs.

    Returns:
        bool: True if any recipe in the cookbook has the specified categories, False otherwise.
    """
    recipe_ids = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipe_ids)
    for recipe in recipes:
        recipe = RecipeArguments(**recipe)
        if categories in recipe.categories:
            return True
    return False
