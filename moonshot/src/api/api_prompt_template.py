from pydantic import validate_call

from moonshot.src.prompt_templates.prompt_template import PromptTemplate


# ------------------------------------------------------------------------------
# Prompt Template APIs
# ------------------------------------------------------------------------------
def api_get_all_prompt_template_detail() -> list[dict]:
    """
    Retrieves all available prompt template details and returns them as a list of dictionaries.

    This function calls the `get_all_prompt_template_details` method from the `PromptTemplate` class
    to fetch the details of all prompt templates. It then returns these details as a list of dictionaries.

    Returns:
        list[dict]: A list of dictionaries, each representing the details of a prompt template.
    """
    return PromptTemplate.get_all_prompt_template_details()


def api_get_all_prompt_template_name() -> list[str]:
    """
    Retrieves all available prompt template names and returns them as a list.

    This function calls the `get_all_prompt_template_names` method from the `PromptTemplate` class
    to fetch the names of all prompt templates. It then returns these names as a list of strings.

    Returns:
        list[str]: A list of prompt template names.
    """
    return PromptTemplate.get_all_prompt_template_names()


@validate_call
def api_delete_prompt_template(pt_id: str) -> bool:
    """
    Deletes a prompt template by its identifier.

    This function calls the `delete` method from the `PromptTemplate` class to delete a prompt template
    identified by its unique ID. It returns True if the deletion was successful, otherwise it raises an exception.

    Args:
        pt_id (str): The unique identifier of the prompt template to be deleted.

    Returns:
        bool: True if the prompt template was successfully deleted.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return PromptTemplate.delete(pt_id)
