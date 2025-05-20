from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..schemas.prompt_template_response_model import PromptTemplatesResponseModel
from ..services.prompt_template_service import PromptTemplateService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Prompt Template"])


@router.get("/api/v1/prompt-templates")
@inject
def get_all_prompt_templates(
    prompt_template_service: PromptTemplateService = Depends(
        Provide[Container.prompt_template_service]
    ),
) -> PromptTemplatesResponseModel:
    """
    Retrieve all prompt templates from the database.

    Args:
        prompt_template_service (PromptTemplateService): The service responsible for retrieving prompt templates.

    Returns:
        PromptTemplatesResponseModel: A model representing all prompt templates.

    Raises:
        HTTPException: An error with status code 404 if no prompt templates are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return prompt_template_service.get_prompt_templates()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve prompt templates: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve prompt templates: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve prompt templates: {e.msg}"
            )


@router.get("/api/v1/prompt-templates/name")
@inject
def get_all_prompt_templates_names(
    prompt_template_service: PromptTemplateService = Depends(
        Provide[Container.prompt_template_service]
    ),
) -> list[str]:
    """
    Retrieve the names of all prompt templates from the database.

    Args:
        prompt_template_service (PromptTemplateService): The service responsible for retrieving prompt template names.

    Returns:
        list[str]: A list of prompt template names.

    Raises:
        HTTPException: An error with status code 404 if no prompt template names are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return prompt_template_service.get_prompt_templates_name()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404,
                detail=f"Failed to retrieve prompt template names: {e.msg}",
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400,
                detail=f"Failed to retrieve prompt template names: {e.msg}",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve prompt template names: {e.msg}",
            )


@router.delete("/api/v1/prompt-templates/{prompt_template_name}")
@inject
def delete_prompt_template(
    prompt_template_name: str,
    prompt_template_service: PromptTemplateService = Depends(
        Provide[Container.prompt_template_service]
    ),
) -> dict[str, bool]:
    """
    Delete a prompt template from the database by its name.

    Args:
        prompt_template_name (str): The name of the prompt template to delete.
        prompt_template_service (PromptTemplateService): The service responsible for deleting the prompt template.

    Returns:
        dict[str, bool]: A dictionary with a key 'success' indicating the result of the deletion operation.

    Raises:
        HTTPException: An error with status code 404 if the prompt template is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        prompt_template_service.delete_prompt_template(prompt_template_name)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete prompt template: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete prompt template: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete prompt template: {e.msg}"
            )
