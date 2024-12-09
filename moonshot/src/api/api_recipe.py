from pydantic import conlist, validate_call

from moonshot.src.recipes.recipe import Recipe
from moonshot.src.recipes.recipe_arguments import RecipeArguments


# ------------------------------------------------------------------------------
# Recipe APIs
# ------------------------------------------------------------------------------
@validate_call
def api_create_recipe(
    name: str,
    description: str,
    tags: list[str],
    categories: list[str],
    datasets: list[str],
    prompt_templates: list[str],
    metrics: list[str],
    grading_scale: dict[str, list[int]],
) -> str:
    """
    Creates a new recipe with the given parameters.

    This function takes various parameters that define a recipe, creates a RecipeArguments
    object with these parameters, and then calls the Recipe.create method to create a new
    recipe in the system.

    Args:
        name (str): The name of the recipe.
        description (str): A description of the recipe.
        tags (list[str]): A list of tags associated with the recipe.
        categories (list[str]): A list of categories the recipe belongs to.
        datasets (list[str]): A list of datasets used in the recipe.
        prompt_templates (list[str]): A list of prompt templates for the recipe.
        metrics (list[str]): A list of metrics to evaluate the recipe.
        grading_scale (dict[str, list[int]]): A grading scale dictionary where the key is the grade and the
        value is a list of integers representing the scale.

    Returns:
        str: The ID of the newly created recipe.
    """
    rec_args = RecipeArguments(
        id="",
        name=name,
        description=description,
        tags=tags,
        categories=categories,
        datasets=datasets,
        prompt_templates=prompt_templates,
        metrics=metrics,
        grading_scale=grading_scale,
    )
    return Recipe.create(rec_args)


@validate_call
def api_read_recipe(rec_id: str) -> dict:
    """
    Reads a recipe and returns its information.

    This function takes a recipe ID as input, reads the corresponding recipe,
    and returns a dictionary containing the recipe's information.

    Args:
        rec_id (str): The ID of the recipe.

    Returns:
        dict: A dictionary containing the recipe's information.
    """
    return Recipe.read(rec_id).to_dict()


@validate_call
def api_read_recipes(rec_ids: conlist(str, min_length=1)) -> list[dict]:
    """
    Reads multiple recipes and returns their information.

    This function takes a list of recipe IDs as input, reads the corresponding recipes,
    and returns a list of dictionaries containing each recipe's information.

    Args:
        rec_ids (conlist(str, min_length=1)): The IDs of the recipes.

    Returns:
        list[dict]: A list of dictionaries, each containing a recipe's information.
    """
    # This function uses list comprehension to iterate over the list of recipe IDs,
    # calling the read_recipe method for each ID and converting the result to a dictionary.
    # The resulting list of dictionaries is then returned.
    return [Recipe.read(rec_id).to_dict() for rec_id in rec_ids]


@validate_call
def api_update_recipe(rec_id: str, **kwargs) -> bool:
    """
    Updates a recipe with the given keyword arguments.

    This function takes a recipe ID and arbitrary keyword arguments, checks if the recipe exists,
    and updates the fields of the recipe with the provided values. If the recipe does not exist,
    a RuntimeError is raised. If the update is successful, it returns True.

    Args:
        rec_id (str): The ID of the recipe to update.
        **kwargs: Arbitrary keyword arguments representing the fields to update.

    Returns:
        bool: True if the recipe was successfully updated.

    Raises:
        RuntimeError: If the recipe with the given ID does not exist.
    """
    # Check if the recipe exists
    try:
        existing_recipe = Recipe.read(rec_id)
    except Exception:
        raise RuntimeError(f"Recipe with ID '{rec_id}' does not exist")

    # Update the fields of the existing recipe with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_recipe, key):
            setattr(existing_recipe, key, value)

    # Perform pydantic check on the updated existing recipe
    RecipeArguments.model_validate(existing_recipe.to_dict())

    # Update the recipe
    return Recipe.update(existing_recipe)


@validate_call
def api_delete_recipe(rec_id: str) -> bool:
    """
    Deletes a recipe identified by its unique recipe ID.

    This function takes a recipe ID, verifies the existence of the recipe, and if found, calls the delete method from
    the Recipe class to remove the recipe from storage.

    If the deletion is successful, it returns True.
    If the recipe does not exist or an exception occurs during deletion, a RuntimeError is raised with an
    appropriate error message.

    Args:
        rec_id (str): The unique identifier for the recipe to be deleted.

    Returns:
        bool: True if the recipe was successfully deleted.

    Raises:
        RuntimeError: If the deletion process encounters an error.
    """
    return Recipe.delete(rec_id)


def api_get_all_recipe() -> list[dict]:
    """
    Retrieves all available recipes.

    This function calls the get_available_items method to retrieve all available recipes. It then converts each
    recipe into a dictionary using the to_dict method and returns a list of these dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing a recipe.
    """
    _, recipes = Recipe.get_available_items()
    return [recipe.to_dict() for recipe in recipes]


def api_get_all_recipe_name() -> list[str]:
    """
    Retrieves all available recipe names.

    This function calls the get_available_items method to retrieve all available recipes. It then extracts the names
    of each recipe and returns a list of these names.

    Returns:
        list[str]: A list of strings, each representing a recipe name.
    """
    recipes_names, _ = Recipe.get_available_items()
    return recipes_names
