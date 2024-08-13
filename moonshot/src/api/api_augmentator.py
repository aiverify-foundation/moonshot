from moonshot.src.augmentor.augmentor import Augmentor


def api_augment_recipe(recipe_id: str, attack_module: str) -> str:
    return Augmentor.augment_recipe(recipe_id, attack_module)


def api_augment_dataset(dataset_id: str, attack_module: str) -> str:
    return Augmentor.augment_dataset(dataset_id, attack_module)
