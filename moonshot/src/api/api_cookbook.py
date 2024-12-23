from pydantic import conlist, validate_call

from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments
from moonshot.src.recipes.recipe import Recipe


# ------------------------------------------------------------------------------
# Cookbook APIs
# ------------------------------------------------------------------------------
@validate_call
def api_create_cookbook(name: str, description: str, recipes: list[str]) -> str:
    """
    Creates a new cookbook.

    This function takes the name, description, and recipes for a new cookbook as input. It then creates a new
    CookbookArguments object with these details and an empty id. The id is left empty because it will be generated
    from the name during the creation process. The function then calls the Cookbook's create method to
    create the new cookbook.

    Args:
        name (str): The name of the new cookbook.
        description (str): A brief description of the new cookbook.
        tags (list[str]): A list of tags associated with the cookbook.
        categories (list[str]): A list of categories the cookbook belongs to.
        recipes (list[str]): A list of recipes to be included in the new cookbook.

    Returns:
        str: The ID of the newly created cookbook.
    """
    # Create a new cookbook
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    # We do not need to provide tags and categories as they will be generated based on the recipes selected.
    cb_args = CookbookArguments(
        id="",
        name=name,
        description=description,
        tags=[],
        categories=[],
        recipes=recipes,
    )
    return Cookbook.create(cb_args)


@validate_call
def api_read_cookbook(cb_id: str) -> dict:
    """
    Retrieves a cookbook based on the provided cookbook ID.

    This function reads a cookbook using the `read` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.

    Args:
        cb_id (str): A cookbook ID.

    Returns:
        dict: A dictionary representing a cookbook.
    """
    return Cookbook.read(cb_id).to_dict()


@validate_call
def api_read_cookbooks(cb_ids: conlist(str, min_length=1)) -> list[dict]:
    """
    Retrieves a list of cookbooks based on the provided list of cookbook IDs.

    This function iterates over the list of provided cookbook IDs, reads each cookbook using the `read` method
    of the `Cookbook` class, and converts the returned `Cookbook` objects to dictionaries using their `to_dict` method.
    It then returns a list of these dictionary representations.

    Args:
        cb_ids (conlist(str, min_length=1)): A list of cookbook IDs.

    Returns:
        list[dict]: A list of dictionaries representing the cookbooks.
    """
    return [Cookbook.read(cb_id).to_dict() for cb_id in cb_ids]


@validate_call
def api_update_cookbook(cb_id: str, **kwargs) -> bool:
    """
    Updates the fields of an existing cookbook with the provided keyword arguments.

    This function first checks if the cookbook with the given ID exists. If it does, it updates the fields
    of the cookbook with the provided keyword arguments. If a field does not exist on the cookbook, it is ignored.
    After updating the fields, it persists the changes to the cookbook.

    Args:
        cb_id (str): The ID of the cookbook to update.
        **kwargs: Arbitrary keyword arguments representing the fields to update and their new values.

    Returns:
        bool: True if the cookbook was successfully updated.

    Raises:
        RuntimeError: If the cookbook with the given ID does not exist.
    """
    # Check if the cookbook exists
    try:
        existing_cookbook = Cookbook.read(cb_id)
    except Exception:
        raise RuntimeError(f"Cookbook with ID '{cb_id}' does not exist")

    # Update the fields of the existing cookbook with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_cookbook, key):
            setattr(existing_cookbook, key, value)

    # Update the cookbook's categories and tags if any of the recipe(s) are changed
    if "recipes" in kwargs:
        consolidated_tags = set()
        consolidated_categories = set()
        for key, value in kwargs.items():
            if key == "recipes":
                for recipe_id in value:
                    recipe = Recipe.read(recipe_id)
                    consolidated_tags.update(recipe.tags)
                    consolidated_categories.update(recipe.categories)
        # Consolidate and set the tags and categories
        existing_cookbook.tags = list(consolidated_tags)
        existing_cookbook.categories = list(consolidated_categories)

    # Perform pydantic check on the updated existing cookbook
    CookbookArguments.model_validate(existing_cookbook.to_dict())

    # Update the cookbook
    return Cookbook.update(existing_cookbook)


@validate_call
def api_delete_cookbook(cb_id: str) -> bool:
    """
    Deletes a cookbook based on the provided cookbook ID.

    This function calls the `delete` method of the `Cookbook` class with the given cookbook ID. If the cookbook
    is successfully deleted, the method returns True, otherwise it returns False.

    Args:
        cb_id (str): The ID of the cookbook to delete.

    Returns:
        bool: True if the cookbook was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return Cookbook.delete(cb_id)


def api_get_all_cookbook() -> list[dict]:
    """
    Retrieves all available cookbooks.

    This function calls the `get_available_items` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns a list
    of dictionaries, each representing a cookbook.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookbook.
    """
    _, cookbooks = Cookbook.get_available_items()
    return [cookbook.to_dict() for cookbook in cookbooks]


def api_get_all_cookbook_name() -> list[str]:
    """
    Retrieves the names of all available cookbooks.

    This function calls the `get_available_items` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns the
    list of cookbook IDs, which are the names of the cookbooks.

    Returns:
        list[str]: A list of cookbook names.
    """
    cookbooks_names, _ = Cookbook.get_available_items()
    return cookbooks_names
