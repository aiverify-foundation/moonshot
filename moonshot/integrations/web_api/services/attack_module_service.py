from .... import api as moonshot_api
from .base_service import BaseService
from .utils.exceptions_handler import exception_handler


class AttackModuleService(BaseService):
    @exception_handler
    def get_all_attack_module(self) -> list[str]:
        attack_modules = moonshot_api.api_get_all_attack_modules()
        return attack_modules
