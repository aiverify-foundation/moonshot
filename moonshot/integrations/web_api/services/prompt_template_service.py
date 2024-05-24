from typing import Any

from .... import api as moonshot_api
from ..services.utils.exceptions_handler import exception_handler
from .base_service import BaseService


class PromptTemplateService(BaseService):
    @exception_handler
    def get_prompt_templates(self) -> list[dict[str, Any]]:
        """
        Retrieve all prompt templates with their details.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing the details of each prompt template.
        """
        templates = moonshot_api.api_get_all_prompt_template_detail()
        return templates

    @exception_handler
    def get_prompt_templates_name(self) -> list[str]:
        """
        Retrieve the names of all prompt templates.

        Returns:
            list[str]: A list of names of all prompt templates.
        """
        templates = moonshot_api.api_get_all_prompt_template_name()
        return templates

    @exception_handler
    def delete_prompt_template(self, pt_id: str):
        """
        Delete a prompt template by its identifier.

        Args:
            pt_id (str): The unique identifier of the prompt template to be deleted.
        """
        moonshot_api.api_delete_prompt_template(pt_id)
