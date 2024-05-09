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
