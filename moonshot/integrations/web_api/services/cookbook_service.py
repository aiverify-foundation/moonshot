from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments as Cookbook
from moonshot.src.recipes.recipe_arguments import RecipeArguments as Recipe

from .... import api as moonshot_api
from ..schemas.cookbook_create_dto import CookbookCreateDTO, CookbookUpdateDTO
from ..schemas.cookbook_response_model import CookbookResponseModel
from ..services.base_service import BaseService
from ..services.recipe_service import (
    get_metric_dependency_in_recipe,
    get_total_prompt_in_recipe,
)
from ..services.utils.exceptions_handler import exception_handler


class CookbookService(BaseService):
    @exception_handler
    def create_cookbook(self, cookbook_data: CookbookCreateDTO) -> None:
        """
        Create a new cookbook with the given data.

        Args:
            cookbook_data (CookbookCreateDTO): Data transfer object containing cookbook details.
        """
        try:
            existing_cookbook = moonshot_api.api_read_cookbook(cookbook_data.name)
            if existing_cookbook:
                raise ValueError("Cookbook with this name already exists.")
        except Exception:
            # If cookbook does not exist, continue to create
            pass
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
                        (
                            cookbook.total_prompt_in_cookbook,
                            cookbook.total_dataset_in_cookbook,
                        ) = get_total_prompt_and_dataset_in_cookbook(cookbook)

            if tags and cookbook_has_tags(tags, cookbook):
                if cookbook not in cookbooks_list:
                    cookbooks_list.append(cookbook)
                    if count:
                        (
                            cookbook.total_prompt_in_cookbook,
                            cookbook.total_dataset_in_cookbook,
                        ) = get_total_prompt_and_dataset_in_cookbook(cookbook)

            if categories and cookbook_has_categories(categories, cookbook):
                if cookbook not in cookbooks_list:
                    cookbooks_list.append(cookbook)
                    if count:
                        (
                            cookbook.total_prompt_in_cookbook,
                            cookbook.total_dataset_in_cookbook,
                        ) = get_total_prompt_and_dataset_in_cookbook(cookbook)

            if categories_excluded:
                excluded_categories_set = set(
                    category.lower() for category in categories_excluded.split(",")
                )
                cookbook_categories_set = set(
                    category.lower() for category in cookbook.categories
                )
                # Exclude only if all categories in the cookbook are in the excluded list
                if cookbook_categories_set.issubset(excluded_categories_set):
                    cookbooks_list.remove(cookbook)

        for cookbook in cookbooks_list:
            cookbook.required_config = cookbook_metrics_dependency(cookbook)

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
def get_total_prompt_and_dataset_in_cookbook(cookbook: Cookbook) -> tuple[int, int]:
    """
    Calculate the total number of prompts in a cookbook.

    This function sums up the total prompts for each recipe in the cookbook.

    Args:
        cookbook (Cookbook): The cookbook object containing the recipe IDs.

    Returns:
        int: The total count of prompts within the cookbook.
    """
    recipes = moonshot_api.api_read_recipes(cookbook.recipes)
    total_prompts, total_datasets = zip(
        *(get_total_prompt_in_recipe(Recipe(**recipe)) for recipe in recipes)
    )
    return sum(total_prompts), sum(total_datasets)


@staticmethod
def cookbook_has_tags(tags: str, cookbook: Cookbook) -> bool:
    """
    Check if a cookbook has the specified tags.

    Args:
        tags (str): The tags to check for in the cookbook.
        cookbook (Cookbook): The cookbook object.

    Returns:
        bool: True if the cookbook has the specified tags, False otherwise.
    """
    tags_list = [tag.lower() for tag in tags.split(",")]
    return any(tag in [ctag.lower() for ctag in cookbook.tags] for tag in tags_list)


@staticmethod
def cookbook_has_categories(categories: str, cookbook: Cookbook) -> bool:
    """
    Check if a cookbook has the specified categories.

    Args:
        categories (str): The categories to check for in the cookbook.
        cookbook (Cookbook): The cookbook object.

    Returns:
        bool: True if the cookbook has the specified categories, False otherwise.
    """
    categories_list = [category.lower() for category in categories.split(",")]
    return any(
        category in [ccat.lower() for ccat in cookbook.categories]
        for category in categories_list
    )


@staticmethod
def cookbook_metrics_dependency(cookbook: Cookbook) -> dict | None:
    """
    Retrieve a list of endpoint and configuration dependencies for all recipes in a given cookbook.

    Args:
        cookbook (Cookbook): The cookbook object containing the recipe IDs.

    Returns:
        dict[str, list[str]] | None: A dictionary with aggregated endpoint and configuration dependencies
        if any are found, otherwise None.
    """
    recipes_in_cookbook = cookbook.recipes
    recipes = moonshot_api.api_read_recipes(recipes_in_cookbook)
    aggregated_endpoints = set()
    aggregated_configurations = {}

    for recipe in recipes:
        recipe = Recipe(**recipe)
        dependency = get_metric_dependency_in_recipe(recipe)
        if dependency:
            # Aggregate endpoints
            aggregated_endpoints.update(dependency.get("endpoints", []))

            # Aggregate configurations
            for key, value in dependency.get("configurations", {}).items():
                if key in aggregated_configurations:
                    aggregated_configurations[key].extend(
                        v for v in value if v not in aggregated_configurations[key]
                    )
                else:
                    aggregated_configurations[key] = value

    aggregated_dependencies = {
        "endpoints": list(aggregated_endpoints),
        "configurations": aggregated_configurations,
    }

    return (
        aggregated_dependencies
        if aggregated_dependencies["endpoints"]
        or aggregated_dependencies["configurations"]
        else None
    )
