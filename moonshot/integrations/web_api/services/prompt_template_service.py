from typing import Any
from .base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from .... import api as moonshot_api


class PromptTemplateService(BaseService):

    @exception_handler
    def get_prompt_templates(self) -> list[dict[str, Any]]:
        templates = moonshot_api.api_get_all_prompt_template_detail()
        return templates
    
    @exception_handler
    def get_ctx_strategies(self) -> list[str]:
        strategies = moonshot_api.api_get_all_context_strategy_name()
        return strategies