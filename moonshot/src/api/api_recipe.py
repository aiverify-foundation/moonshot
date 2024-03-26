from moonshot.src.benchmarking.recipes.recipe import Recipe
from moonshot.src.benchmarking.recipes.recipe_arguments import RecipeArguments


# ------------------------------------------------------------------------------
# Recipe APIs
# ------------------------------------------------------------------------------
def api_create_recipe(
    name: str,
    description: str,
    tags: list[str],
    datasets: list[str],
    prompt_templates: list[str],
    metrics: list[str],
) -> None:
    """
    Creates a new recipe.

    This function takes a name, description, tags, datasets, prompt templates, and metrics as input, and creates a
    new recipe. It constructs a RecipeArguments object with the provided details and then calls the Recipe's
    create_recipe method to add the new recipe.

    Args:
        name (str): The name of the new recipe.
        description (str): The description of the recipe.
        tags (list[str]): The tags associated with the recipe.
        datasets (list[str]): The datasets used in the recipe.
        prompt_templates (list[str]): The prompt templates used in the recipe.
        metrics (list[str]): The metrics used in the recipe.

    Returns:
        None
    """
    # Create a new recipe
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    rec_args = RecipeArguments(
        id="",
        name=name,
        description=description,
        tags=tags,
        datasets=datasets,
        prompt_templates=prompt_templates,
        metrics=metrics,
    )
    Recipe.create(rec_args)


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


def api_read_recipes(rec_ids: list[str]) -> list[dict]:
    """
    Reads multiple recipes and returns their information.

    This function takes a list of recipe IDs as input, reads the corresponding recipes,
    and returns a list of dictionaries containing each recipe's information.

    Args:
        rec_ids (list[str]): The IDs of the recipes.

    Returns:
        list[dict]: A list of dictionaries, each containing a recipe's information.
    """
    # This function uses list comprehension to iterate over the list of recipe IDs,
    # calling the read_recipe method for each ID and converting the result to a dictionary.
    # The resulting list of dictionaries is then returned.
    return [Recipe.read(rec_id).to_dict() for rec_id in rec_ids]


def api_update_recipe(rec_id: str, **kwargs) -> None:
    """
    Updates an existing recipe in the recipe manager.

    This function updates an existing recipe in the recipe manager using the provided recipe details.
    It first checks if the recipe exists, then updates the fields of the existing recipe with the provided kwargs,
    and finally calls the Recipe's update_recipe method to update the recipe.

    Args:
        rec_id (str): The ID of the recipe to update.
        kwargs: A dictionary of arguments for the recipe. Possible keys are:
            name (str): The name of the recipe.
            description (str): The description of the recipe.
            tags (list[str]): The tags associated with the recipe.
            datasets (list[str]): The datasets used in the recipe.
            prompt_templates (list[str]): The prompt templates used in the recipe.
            metrics (list[str]): The metrics used in the recipe.

    Raises:
        RuntimeError: If the recipe with the provided ID does not exist.

    Returns:
        None
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

    # Update the endpoint
    Recipe.update(existing_recipe)


def api_delete_recipe(rec_id: str) -> None:
    """
    Deletes a recipe.

    This method takes a recipe ID as input, deletes the corresponding JSON file from the directory specified by
    `EnvironmentVars.RECIPES`. If the operation fails for any reason, an exception is raised and the
    error is printed.

    Args:
        rec_id (str): The ID of the recipe to delete.

    Raises:
        Exception: If there is an error during file deletion or any other operation within the method.
    """
    Recipe.delete(rec_id)


def api_get_all_recipe() -> list[dict]:
    """
    Retrieves all available recipes.

    This function calls the get_available_recipes method to retrieve all available recipes. It then converts each
    recipe into a dictionary using the to_dict method and returns a list of these dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing a recipe.
    """
    _, recipes = Recipe.get_available_items()
    return [recipe.to_dict() for recipe in recipes]


def api_get_all_recipe_name() -> list[str]:
    """
    Retrieves all available recipe names.

    This function calls the get_available_recipes method to retrieve all available recipes. It then extracts the names
    of each recipe and returns a list of these names.

    Returns:
        list[str]: A list of strings, each representing a recipe name.
    """
    recipes_names, _ = Recipe.get_available_items()
    return recipes_names
