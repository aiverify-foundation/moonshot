from .... import api as moonshot_api
from .base_service import BaseService
from .utils.exceptions_handler import exception_handler


class AttackModuleService(BaseService):
    @exception_handler
    def get_all_attack_module(self) -> list[str]:
        """
        Retrieves a list of all available attack modules.

        This method wraps the `api_get_all_attack_modules` function from the moonshot API and returns
        a list of attack module names.

        Returns:
            list[str]: A list of strings, each denoting the name of an attack module.
        """
        attack_modules = moonshot_api.api_get_all_attack_modules()
        return attack_modules

    @exception_handler
    def get_all_attack_module_metadata(self) -> list[dict]:
        """
        Retrieves metadata for all available attack modules.

        This method calls the `api_get_all_attack_module_metadata` function from the moonshot API. It collects
        metadata for each attack module, which includes details such as the module's name, description, and
        any other relevant information provided by the module's `get_metadata` method.

        Returns:
            list[dict]: A list of dictionaries, each containing metadata of an attack module.
        """
        am_metadata = moonshot_api.api_get_all_attack_module_metadata()
        return am_metadata

    @exception_handler
    def update_attack_module_config(
        self, attack_module_id: str, update_args: dict
    ) -> bool:
        """
        Updates the configuration of a specific attack module.

        Args:
            attack_module_id (str): The ID of the attack module to be updated.
            update_args (dict): The updated configuration parameters.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        bool_updated = moonshot_api.api_update_attack_module_config(
            attack_module_id, **update_args
        )
        return bool_updated

    @exception_handler
    def delete_attack_module_config(self, attack_module_id: str) -> bool:
        """
        Deletes the configuration of a specific attack module.

        Args:
            attack_module_id (str): The ID of the attack module to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        bool_deleted = moonshot_api.api_delete_attack_module_config(attack_module_id)
        return bool_deleted
