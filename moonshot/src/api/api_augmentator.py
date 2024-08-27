from moonshot.src.augmentor.augmentor import Augmentor


def api_augment_recipe(recipe_id: str, attack_module: str) -> str:
    """
    Augments a recipe using the specified attack module.

    Args:
        recipe_id (str): The ID of the recipe to be augmented.
        attack_module (str): The attack module to use for augmentation.

    Returns:
        str: The augmented recipe.
    """
    return Augmentor.augment_recipe(recipe_id, attack_module)


def api_augment_dataset(dataset_id: str, attack_module: str) -> str:
    """
    Augments a dataset using the specified attack module.

    Args:
        dataset_id (str): The ID of the dataset to be augmented.
        attack_module (str): The attack module to use for augmentation.

    Returns:
        str: The augmented dataset.
    """
    return Augmentor.augment_dataset(dataset_id, attack_module)
