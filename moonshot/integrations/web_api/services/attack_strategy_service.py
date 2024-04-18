from dependency_injector.wiring import inject
from .... import api as moonshot_api
from .base_service import BaseService
from .utils.exceptions_handler import exception_handler


class AttackStrategyService(BaseService):

    @exception_handler
    def get_all_attack_strategies(self) -> list[str]:
        attack_strategies = ["attack_strat_1", "attack_strat_2", "attack_strat_3"]
        return attack_strategies

    @exception_handler
    def get_attack_strategy_by_id(self, as_id: str) -> str: 
        attack_strategy = "attack_strat_3"
        return attack_strategy
