from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.cookbooks.cookbook_arguments import CookbookArguments


# ------------------------------------------------------------------------------
# Cookbook APIs
# ------------------------------------------------------------------------------
def api_create_cookbook(name: str, description: str, recipes: list[str]) -> None:
    """
    Creates a new cookbook.

    This function takes the name, description, and recipes for a new cookbook as input. It then creates a new
    CookbookArguments object with these details and an empty id. The id is left empty because it will be generated
    from the name during the creation process. The function then calls the Cookbook's create_cookbook method to
    create the new cookbook.

    Args:
        name (str): The name of the new cookbook.
        description (str): A brief description of the new cookbook.
        recipes (list[str]): A list of recipes to be included in the new cookbook.
    """
    # Create a new cookbook
    # We do not need to provide the id.
    # This is because during creation:
    # 1. the id is slugify from the name and stored as id.
    cb_args = CookbookArguments(
        id="",
        name=name,
        description=description,
        recipes=recipes,
    )
    Cookbook.create(cb_args)


def api_read_cookbook(cb_id: str) -> dict:
    """
    Retrieves a cookbook based on the provided cookbook ID.

    This function reads a cookbook using the `read_cookbook` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.

    Args:
        cb_id (str): A cookbook ID.

    Returns:
        dict: A dictionary representing a cookbook.
    """
    return Cookbook.read(cb_id).to_dict()


def api_read_cookbooks(cb_ids: list[str]) -> list[dict]:
    """
    Retrieves a list of cookbooks based on the provided list of cookbook IDs.

    This function iterates over the list of cookbook IDs, reads each cookbook using the `read_cookbook` method
    of the `Cookbook` class, and converts the returned `Cookbook` object to a dictionary using its `to_dict` method.
    It returns a list of these dictionaries.

    Args:
        cb_ids (list[str]): A list of cookbook IDs.

    Returns:
        list[dict]: A list of dictionaries, each representing a cookbook.
    """
    return [Cookbook.read(cb_id).to_dict() for cb_id in cb_ids]


def api_update_cookbook(cb_id: str, **kwargs) -> None:
    """
    Updates an existing cookbook in the cookbook manager.

    This function updates an existing cookbook in the cookbook manager using the provided cookbook details.
    It first checks if the cookbook exists, then updates the fields of the existing cookbook with the provided kwargs,
    and finally calls the Cookbook's update_cookbook method to update the cookbook.

    Args:
        cb_id (str): The ID of the cookbook to update.
        kwargs: A dictionary of arguments for the cookbook. Possible keys are:
            name (str): The name of the cookbook.
            description (str): The description of the cookbook.
            recipes (list[str]): The list of recipes in the cookbook.

    Raises:
        RuntimeError: If the cookbook with the provided ID does not exist.

    Returns:
        None
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

    # Update the cookbook
    Cookbook.update(existing_cookbook)


def api_delete_cookbook(cb_id: str) -> None:
    """
    Deletes a cookbook.

    This function calls the `delete_cookbook` method of the `Cookbook` class, which deletes the cookbook
    corresponding to the provided ID.

    Args:
        cb_id (str): The ID of the cookbook to delete.
    """
    Cookbook.delete(cb_id)


def api_get_all_cookbook() -> list[dict]:
    """
    Retrieves all available cookbooks.

    This function calls the `get_available_cookbooks` method of the `Cookbook` class, which returns a tuple
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

    This function calls the `get_available_cookbooks` method of the `Cookbook` class, which returns a tuple
    containing a list of cookbook IDs and a list of `CookbookArguments` objects. The function then returns the
    list of cookbook IDs, which are the names of the cookbooks.

    Returns:
        list[str]: A list of cookbook names.
    """
    cookbooks_names, _ = Cookbook.get_available_items()
    return cookbooks_names
