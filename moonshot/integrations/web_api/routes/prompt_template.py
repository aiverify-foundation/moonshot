import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from ..container import Container
from ..services.utils.exceptions_handler import ServiceException
from ..schemas.prompt_template_response_model import PromptTemplatesResponseModel
from ..services.prompt_template_service import PromptTemplateService

router = APIRouter()

@router.get("/v1/prompt_templates")
@inject
def get_all_prompt_templates(
    prompt_template_service: PromptTemplateService = Depends(Provide[Container.prompt_template_service])
    ) -> PromptTemplatesResponseModel:
    """
    Get all the prompt templates from the database
    """
    try:
        return prompt_template_service.get_prompt_templates()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.get("/v1/prompt_templates/name")
@inject
def get_all_prompt_templates_names(
    prompt_template_service: PromptTemplateService = Depends(Provide[Container.prompt_template_service])
    ) -> list[str]:
    """
    Get all the prompt templates from the database
    """
    try:
        return prompt_template_service.get_prompt_templates_name()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)



@router.get("/v1/context_strategies")
@inject
def get_all_context_strategies(
    prompt_template_service: PromptTemplateService = Depends(Provide[Container.prompt_template_service])
    ) -> list[str]:
    """
    Get all the context strategies from the database
    """
    try:
        return prompt_template_service.get_ctx_strategies()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)
        

@router.delete("/v1/context_strategies/{ctx_strategy_name}")
@inject
def delete_context_strategy(
    ctx_strategy_name: str,
    prompt_template_service: PromptTemplateService = Depends(Provide[Container.prompt_template_service])
    ) -> dict[str, bool]:
    """
    Delete context strategies from the database
    """
    try:
        prompt_template_service.delete_ctx_strategy(ctx_strategy_name)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)
