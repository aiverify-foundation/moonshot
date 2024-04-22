from moonshot.src.recipes.recipe import Recipe
from moonshot.src.recipes.recipe_arguments import RecipeArguments


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
    attack_modules: list[str],
) -> None:
    """
    Creates a new recipe and stores it in a JSON file.

    This function accepts multiple parameters to define a recipe, including its name, description, tags, datasets,
    prompt templates, metrics, and attack modules. It constructs a new RecipeArguments object using these parameters
    and invokes the Recipe.create method to persist the new recipe in a JSON file.

    The recipe's ID is automatically generated based on the recipe's name using a slugification process,
    thus it is not a required input.

    Args:
        name (str): The name of the recipe.
        description (str): The description of the recipe.
        tags (list[str]): A list of tags associated with the recipe.
        datasets (list[str]): A list of datasets the recipe utilizes.
        prompt_templates (list[str]): A list of prompt templates for the recipe.
        metrics (list[str]): A list of metrics to evaluate the recipe.
        attack_modules (list[str]): A list of attack modules the recipe employs.

    Returns:
        None
    """
    rec_args = RecipeArguments(
        id="",
        name=name,
        description=description,
        tags=tags,
        datasets=datasets,
        prompt_templates=prompt_templates,
        metrics=metrics,
        attack_modules=attack_modules,
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
    Updates a recipe with the provided fields.

    This function takes a recipe ID and a variable number of keyword arguments as input.
    It first checks if the recipe with the given ID exists. If it does, it updates the fields
    of the existing recipe with the provided keyword arguments. If the recipe does not exist,
    it raises a RuntimeError.

    Args:
        rec_id (str): The ID of the recipe to update.
        **kwargs: Variable number of keyword arguments representing the fields to update.

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
