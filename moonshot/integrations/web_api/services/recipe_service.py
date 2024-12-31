from moonshot.src.recipes.recipe_arguments import RecipeArguments as Recipe

from .... import api as moonshot_api
from ..schemas.recipe_create_dto import RecipeCreateDTO, RecipeUpdateDTO
from ..schemas.recipe_response_model import RecipeResponseModel
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class RecipeService(BaseService):
    @exception_handler
    def create_recipe(self, recipe_data: RecipeCreateDTO) -> None:
        """
        Create a new recipe with the given data.

        Args:
            recipe_data (RecipeCreateDTO): Data transfer object containing recipe details.
        """
        moonshot_api.api_create_recipe(
            name=recipe_data.name,
            description=recipe_data.description,
            tags=recipe_data.tags,
            categories=recipe_data.categories,
            datasets=recipe_data.datasets,
            prompt_templates=recipe_data.prompt_templates,
            metrics=recipe_data.metrics,
            grading_scale=recipe_data.grading_scale,
        )

    @exception_handler
    def get_all_recipes(
        self,
        tags: str,
        categories: str,
        sort_by: str,
        count: bool,
        ids: str | None = None,
    ) -> list[RecipeResponseModel]:
        """
        Retrieve all recipes, with optional filters for tags, categories, sorting, and including prompt counts.

        Args:
            ids (str, optional): Filter recipes by IDs. If None, no ID-based filtering is applied.
            tags (str, optional): Filter recipes by tags. If None, no tag-based filtering is applied.
            categories (str, optional): Filter recipes by categories. If None, no category-based filtering is applied.
            sort_by (str, optional): Sort recipes by a specified field. If None, no sorting is applied.
            count (bool, optional): Include the total prompt count in each recipe if True.

        Returns:
            list[RecipeResponseModel]: A list of recipe, filtered and sorted, with optional prompt counts.
        """
        filtered_recipes: list[RecipeResponseModel] = []

        if ids:
            recipe_ids = ids.split(",")
            recipes = [moonshot_api.api_read_recipe(id) for id in recipe_ids]
        else:
            recipes = moonshot_api.api_get_all_recipe()

        for recipe_dict in recipes:
            recipe = RecipeResponseModel(**recipe_dict)
            if count:
                recipe.total_prompt_in_recipe, _ = get_total_prompt_in_recipe(recipe)
            filtered_recipes.append(recipe)

        # TODO - do all filtering in 1 pass
        if tags:
            filtered_recipes = [
                recipe for recipe in filtered_recipes if tags in recipe.tags
            ]

        if categories:
            categories_list = categories.split(",") if categories else []
            if categories_list:
                filtered_recipes = [
                    recipe
                    for recipe in filtered_recipes
                    if any(
                        category.lower() in (cat.lower() for cat in recipe.categories)
                        for category in categories_list
                    )
                ]
        if sort_by:
            if sort_by == "id":
                filtered_recipes.sort(key=lambda x: x.id)

        for recipe in filtered_recipes:
            recipe.required_config = get_metric_dependency_in_recipe(recipe)

        return filtered_recipes

    @exception_handler
    def get_all_recipes_name(self) -> list[str]:
        """
        Retrieve the names of all recipes.

        Returns:
            list[str]: A list of recipe names.
        """
        recipes = moonshot_api.api_get_all_recipe_name()
        return recipes

    @exception_handler
    def update_recipe(self, recipe_data: RecipeUpdateDTO, recipe_id: str) -> None:
        """
        Update an existing recipe with new data.

        Args:
            recipe_data (RecipeCreateDTO): Data transfer object containing new recipe details.
            recipe_id (str): The ID of the recipe to update.
        """
        update_data = {
            k: v
            for k, v in recipe_data.to_dict().items()
            if v is not None and k not in ["id", "stats"]
        }

        moonshot_api.api_update_recipe(rec_id=recipe_id, **update_data)

    @exception_handler
    def delete_recipe(self, recipe_id: str) -> None:
        """
        Delete a recipe by its ID.

        Args:
            recipe_id (str): The ID of the recipe to delete.
        """
        moonshot_api.api_delete_recipe(recipe_id)


@staticmethod
def get_total_prompt_in_recipe(recipe: Recipe) -> tuple[int, int]:
    """
    Calculate the total number of prompts in a recipe.

    This function sums up the number of dataset prompts and then multiplies
    the result by the number of prompt templates if they exist.

    Args:
        recipe (Recipe): The recipe object containing the stats and
                                  prompt templates information.

    Returns:
        int: The total count of prompts within the recipe.
        int: The total count of datasets within the recipe.
    """
    # Initialize total prompt count
    total_prompt_count = 0

    # Add counts from dataset prompts if available
    datasets_prompts = recipe.stats.get("num_of_datasets_prompts", {})
    total_prompt_count += sum(datasets_prompts.values())

    # If there are prompt templates, scale the total count by the number of templates
    if recipe.prompt_templates:
        total_prompt_count *= len(recipe.prompt_templates)

    return total_prompt_count, int(recipe.stats.get("num_of_datasets", 0))


@staticmethod
def get_metric_dependency_in_recipe(recipe: Recipe) -> dict | None:
    """
    Retrieve endpoint and configuration dependencies for a given recipe.

    This function gathers all available metrics along with their endpoints and configurations,
    then identifies and compiles the dependencies based on the metrics present in the provided recipe.

    Args:
        recipe (Recipe): The recipe object containing metrics information.

    Returns:
        dict[str, dict[str, list[str]]] | None: A dictionary with 'endpoints' and 'configurations' as keys,
        where 'endpoints' is a list of endpoint dependencies and 'configurations' is a dictionary of configuration
        dependencies. Returns None if no dependencies are found.
    """
    metrics = recipe.metrics
    all_metrics = moonshot_api.api_get_all_metric()
    aggregated_endpoints = set()
    aggregated_configurations = {}

    for metric in metrics:
        metric_data = next((m for m in all_metrics if m["id"] == metric), None)
        if metric_data:
            # Aggregate endpoints
            aggregated_endpoints.update(metric_data.get("endpoints", []))

            # Aggregate configurations
            for key, value in metric_data.get("configurations", {}).items():
                if key in aggregated_configurations:
                    aggregated_configurations[key].extend(
                        v for v in value if v not in aggregated_configurations[key]
                    )
                else:
                    aggregated_configurations[key] = value

    aggregated_data = {
        "endpoints": list(aggregated_endpoints),
        "configurations": aggregated_configurations,
    }
    return (
        aggregated_data
        if aggregated_data["endpoints"] or aggregated_data["configurations"]
        else None
    )
