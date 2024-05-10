from moonshot.src.prompt_templates.prompt_template import PromptTemplate


# ------------------------------------------------------------------------------
# Prompt Template APIs
# ------------------------------------------------------------------------------
def api_get_all_prompt_template_detail() -> list[dict]:
    """
    Retrieves all available prompt template details and returns them as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing the details of a prompt template.
    """
    return PromptTemplate.get_all_prompt_template_details()


def api_get_all_prompt_template_name() -> list[str]:
    """
    Retrieves all available prompt template names and returns them as a list.

    Returns:
        list[str]: A list of prompt template names.
    """
    return PromptTemplate.get_all_prompt_template_names()


def api_delete_prompt_template(pt_id: str) -> None:
    """
    Deletes a prompt template based on the provided template id.

    Args:
        pt_id (str): The id of the prompt template to be deleted.

    Returns:
        None
    """
    PromptTemplate.delete(pt_id)
