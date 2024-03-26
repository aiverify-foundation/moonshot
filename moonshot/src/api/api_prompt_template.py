from moonshot.src.prompt_template.prompt_template_manager import PromptTemplateManager


# ------------------------------------------------------------------------------
# Prompt Template APIs
# ------------------------------------------------------------------------------
def api_get_all_prompt_template_detail() -> list[dict]:
    """
    Retrieves all available prompt template details and returns them as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing the details of a prompt template.
    """
    return PromptTemplateManager.get_all_prompt_template_details()


def api_get_all_prompt_template_name() -> list[str]:
    """
    Retrieves all available prompt template names and returns them as a list.

    Returns:
        list[str]: A list of prompt template names.
    """
    return PromptTemplateManager.get_all_prompt_template_names()
