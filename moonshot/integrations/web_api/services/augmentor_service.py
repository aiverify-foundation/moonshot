from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class AugmentorService(BaseService):
    @exception_handler
    def augment_recipe(self, recipe_id: str, attack_module_id: str) -> str:
        new_recipe_id = moonshot_api.api_augment_recipe(
            recipe_id=recipe_id, attack_module=attack_module_id
        )

        return new_recipe_id

    @exception_handler
    def augment_dataset(self, dataset_id: str, attack_module_id: str) -> str:
        new_dataset_id = moonshot_api.api_augment_dataset(
            dataset_id=dataset_id, attack_module=attack_module_id
        )
        return new_dataset_id
