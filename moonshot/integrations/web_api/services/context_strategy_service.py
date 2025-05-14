from .... import api as moonshot_api
from ..services.utils.exceptions_handler import exception_handler
from .base_service import BaseService


class ContextStrategyService(BaseService):
    @exception_handler
    def get_ctx_strategy(self) -> list[dict]:
        strategies = moonshot_api.api_get_all_context_strategy_metadata()
        return strategies

    @exception_handler
    def get_ctx_strategy_name(self) -> list[str]:
        strategies = moonshot_api.api_get_all_context_strategies()
        return strategies

    @exception_handler
    def delete_ctx_strategy(self, ctx_strategy_name: str) -> None:
        moonshot_api.api_delete_context_strategy(ctx_strategy_name)
