# api/routes.py
from typing import Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..container import Container
from ..schemas.session_response_model import SessionMetadataModel, SessionResponseModel
from ..schemas.session_create_dto import SessionCreateDTO
from ..schemas.session_prompt_dto import SessionPromptDTO
from ..services.session_service import SessionService, PromptDetails


router = APIRouter()


@router.get("/")
async def status():
    return {"status": "web api is up and running"}


@router.get("/v1/sessions")
@inject
async def get_all(
    session_service: SessionService = Depends(Provide[Container.session_service])
) -> list[Optional[SessionMetadataModel]]:
    return session_service.get_sessions()


@router.get("/v1/sessions/{session_id}")
@inject
async def get_one(
    session_id: str,
    include_history: bool = False,
    length: int = 5,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> SessionResponseModel:
    session_data = session_service.get_session(session_id)
    if include_history:
        history = session_service.get_session_chat_history(session_id, length)
        if session_data is not None:
            session_data.chat_history = history
    if session_data is not None:
        return SessionResponseModel(session=session_data)
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/v1/sessions")
@inject
async def create(
    session_dto: SessionCreateDTO,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> SessionResponseModel:
    return SessionResponseModel(session=session_service.create_session(session_dto))


@router.put("/v1/sessions/{session_id}")
@inject
async def set_active_session(
    session_id: str,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> SessionResponseModel:
    session_data = session_service.set_current_session(session_id)
    if session_data is not None:
        return SessionResponseModel(session=session_data)
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/v1/sessions/{session_id}/prompt")
@inject
async def prompt(
    session_id: str,
    user_prompt: SessionPromptDTO,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, list[PromptDetails]]:
    result = await session_service.send_prompt(session_id, user_prompt.prompt, user_prompt.history_length)
    return result


@router.get("/v1/prompt_templates")
@inject
def get_all_prompt_templates(
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> list[Optional[Any]]:
    """
    Get all the prompt templates from the database
    """
    return session_service.get_prompt_templates()


@router.put("/v1/prompt_templates/{prompt_template_name}")
@inject
async def set_prompt_template(
    prompt_template_name: str,
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, bool]:
    """
    Select a prompt template for the current session
    """
    result = session_service.select_prompt_template(prompt_template_name)
    return {"success": result}


@router.delete("/v1/prompt_templates/{prompt_template_name}")
@inject
async def unset_prompt_template(
    prompt_template_name: str = '',
    session_service: SessionService = Depends(Provide[Container.session_service])
    ) -> dict[str, bool]:
    """
    Remove prompt template from the current session
    """
    result = session_service.select_prompt_template()
    return {"success": result}
