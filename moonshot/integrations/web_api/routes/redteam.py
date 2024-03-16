import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide


from ..schemas.prompt_response_model import PromptResponseModel
from ..container import Container
from ..services.utils.exceptions_handler import ServiceException
from ..schemas.prompt_template_response_model import PromptTemplatesResponseModel
from ..schemas.session_response_model import SessionMetadataModel, SessionResponseModel
from ..schemas.session_create_dto import SessionCreateDTO
from ..schemas.session_prompt_dto import SessionPromptDTO
from ..services.session_service import SessionService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
@inject
async def healthcheck():
    return {"status": "web api is up and running"}


@router.get("/v1/sessions")
@inject
async def get_all_sessions(
    session_service: SessionService = Depends(Provide[Container.session_service])
) -> list[Optional[SessionMetadataModel]]:
    try:
        return session_service.get_sessions()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.get("/v1/sessions/{session_id}")
@inject
async def get_session_by_session_id(
    session_id: str,
    include_history: bool = False,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> SessionResponseModel:
    try:
        session_data = session_service.get_session(session_id)
        if include_history:
            history = session_service.get_session_chat_history(session_id)
            if session_data is not None:
                session_data.chat_history = history
        if session_data is not None:
            return SessionResponseModel(session=session_data)
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.post("/v1/sessions")
@inject
async def create(
    session_dto: SessionCreateDTO,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> SessionResponseModel:
    try: 
        new_session = session_service.create_session(session_dto)
        updated_with_chat_ids = session_service.get_session(new_session.session_id)
        return SessionResponseModel(session=updated_with_chat_ids)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.post("/v1/sessions/{session_id}/prompt")
@inject
async def prompt(
    session_id: str,
    user_prompt: SessionPromptDTO,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> PromptResponseModel:
    try:
        result = await session_service.send_prompt(session_id, user_prompt.prompt)
        return result
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.get("/v1/prompt_templates")
@inject
def get_all_prompt_templates(
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> PromptTemplatesResponseModel:
    """
    Get all the prompt templates from the database
    """
    try:
        return session_service.get_prompt_templates()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put("/v1/sessions/{session_id}/prompt_templates/{prompt_template_name}")
@inject
async def set_prompt_template(
    session_id: str,
    prompt_template_name: str,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, bool]:
    """
    Select a prompt template for the current session
    """
    try:
        # rely on exception for now. TODO - ms lib to return or raise feedback
        session_service.select_prompt_template(session_id,prompt_template_name)
        return {"success": True }
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/v1/sessions/{session_id}/prompt_templates/{prompt_template_name}")
@inject
async def unset_prompt_template(
    session_id: str,
    prompt_template_name: str = '',
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, bool]:
    """
    Remove prompt template from the current session
    """
    try:
        # rely on exception for now. TODO - ms lib to return or raise feedback
        session_service.select_prompt_template(session_id,"")
        return {"success": True }
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
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> list[str]:
    try:
        return session_service.get_ctx_strategies()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put("/v1/sessions/{session_id}/context_strategies/{ctx_strategy_name}")
@inject
async def set_context_strategy(
    session_id: str,
    ctx_strategy_name: str,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, bool]:

    try:
        # rely on exception for now. TODO - ms lib to return or raise feedback
        session_service.select_ctx_strategy(session_id, ctx_strategy_name)
        return {"success": True }
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/v1/sessions/{session_id}/context_strategies/{ctx_strategy_name}")
@inject
async def unset_context_strategy(
    session_id: str,
    ctx_strategy_name: str = '',
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, bool]:

    try:
        # rely on exception for now. TODO - ms lib to return or raise feedback
        session_service.select_ctx_strategy(session_id, "")
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)