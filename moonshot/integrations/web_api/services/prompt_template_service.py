from typing import Any

from .... import api as moonshot_api
from ..services.utils.exceptions_handler import exception_handler
from .base_service import BaseService


class PromptTemplateService(BaseService):
    @exception_handler
    def get_prompt_templates(self) -> list[dict[str, Any]]:
        templates = moonshot_api.api_get_all_prompt_template_detail()
        return templates

    @exception_handler
    def get_prompt_templates_name(self) -> list[str]:
        templates = moonshot_api.api_get_all_prompt_template_name()
        return templates

    @exception_handler
    def get_ctx_strategies(self) -> list[str]:
        strategies = moonshot_api.api_get_all_context_strategy_name()
        return strategies

    @exception_handler
    def delete_ctx_strategy(self, ctx_strategy_name: str) -> None:
        moonshot_api.api_delete_context_strategy(ctx_strategy_name)
