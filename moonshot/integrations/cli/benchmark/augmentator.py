from moonshot.api import (
    api_augment_dataset,
    api_augment_recipe,
)
from rich.console import Console
import cmd2

console = Console()

def augment_dataset(args) -> None:
    """
    Augments a dataset using the specified attack module.

    Args:
        args: An object containing the following attributes:
            dataset_id (str): The ID of the dataset to be augmented.
            attack_module_id (str): The ID of the attack module to use for augmentation.

    Returns:
        None
    """
    try:
        new_dataset_id = api_augment_dataset(args.dataset_id, args.attack_module_id)
        print(f"[augment_dataset]: Dataset {args.dataset_id} has been augmented. New dataset id is {new_dataset_id}")
    except Exception as e:
        print(f"[augment_dataset]: {str(e)}")

def augment_recipe(args) -> None:
    """
    Augments a recipe using the specified attack module.

    Args:
        args: An object containing the following attributes:
            recipe_id (str): The ID of the recipe to be augmented.
            attack_module_id (str): The ID of the attack module to use for augmentation.

    Returns:
        None
    """
    try:
        new_recipe_id = api_augment_recipe(args.recipe_id, args.attack_module_id)
        print(f"[augment_recipe]: Recipe {args.recipe_id} has been augmented. New recipe id is {new_recipe_id}")
    except Exception as e:
        print(f"[augment_recipe]: {str(e)}")

# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Augment Dataset Arguments
augment_dataset_args = cmd2.Cmd2ArgumentParser(
    description="Augment a dataset. The new dataset id will be appended with the attack module chosen.",
    epilog="Example:\n augment_dataset 'my_dataset' 'my_attack_module' "
)
augment_dataset_args.add_argument("dataset_id", type= str, help="Name of the dataset to augment.")
augment_dataset_args.add_argument("attack_module_id", type= str, help="Name of the attack module use for augmentation.")

# Augment Recipe Arguments
augment_recipe_args = cmd2.Cmd2ArgumentParser(
    description="Augment a recipe. The new recipe id will be appended with the attack module chosen.",
    epilog="Example: \n augment_recipe 'my_recipe' 'my_attack_module' "
)
augment_recipe_args.add_argument("recipe_id", type= str, help="Name of the recipe to augment.")
augment_recipe_args.add_argument("attack_module_id", type= str, help="Name of the attack module use for augmentation.")
