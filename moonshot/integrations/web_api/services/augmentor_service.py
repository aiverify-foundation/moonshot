from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class AugmentorService(BaseService):
    @exception_handler
    def augment_recipe(self, recipe_id: str, attack_module_id: str) -> str:
        """
        Augments a recipe using the specified attack module.

        Args:
            recipe_id (str): The ID of the recipe to be augmented.
            attack_module_id (str): The ID of the attack module to use for augmentation.

        Returns:
            str: The ID of the newly created augmented recipe.
        """
        new_recipe_id = moonshot_api.api_augment_recipe(
            recipe_id=recipe_id, attack_module_id=attack_module_id
        )

        return new_recipe_id

    @exception_handler
    def augment_dataset(self, dataset_id: str, attack_module_id: str) -> str:
        """
        Augments a dataset using the specified attack module.

        Args:
            dataset_id (str): The ID of the dataset to be augmented.
            attack_module_id (str): The ID of the attack module to use for augmentation.

        Returns:
            str: The ID of the newly created augmented dataset.
        """
        new_dataset_id = moonshot_api.api_augment_dataset(
            dataset_id=dataset_id, attack_module_id=attack_module_id
        )
        return new_dataset_id

