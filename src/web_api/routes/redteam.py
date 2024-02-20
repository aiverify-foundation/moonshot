# api/routes.py
from typing import Callable, Optional, Any
from fastapi import APIRouter, HTTPException, Request
from moonshot.src.common.prompt_template import get_prompt_templates
from web_api.schemas.session_response_model import SessionMetadataModel, SessionResponseModel
from web_api.schemas.session_create_dto import SessionCreateDTO 
from web_api.schemas.session_prompt_dto import SessionPromptDTO
from web_api.services.session_service import PromptDetails, get_sessions, get_session, set_current_session, send_prompt, get_session_chat_history
from web_api.services import session_service


router = APIRouter()

@router.get("/")
async def status():
    return {"status": "web api is up and running"}


@router.get("/v1/sessions")
async def get_all() -> list[Optional[SessionMetadataModel]]:
    return get_sessions()


@router.get("/v1/sessions/{session_id}")
async def get_one(session_id: str, include_history: bool = False, length: int = 5) -> SessionResponseModel:
    session_data = get_session(session_id)
    if include_history:
        history = get_session_chat_history(session_id, length)
        if session_data is not None:
            session_data.chat_history = history  
    if session_data is not None:
        return SessionResponseModel(session=session_data)
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@router.post("/v1/sessions")
async def create(session_dto: SessionCreateDTO) -> SessionResponseModel:
    return SessionResponseModel(session=session_service.create_session(session_dto))
        
@router.put("/v1/sessions/{session_id}")
async def set_active_session(session_id: str) -> SessionResponseModel:
    session_data = set_current_session(session_id)
    if session_data is not None:
        return SessionResponseModel(session=session_data)
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/v1/sessions/{session_id}/prompt")
async def prompt(session_id: str, user_prompt: SessionPromptDTO) -> dict[str, list[PromptDetails]]:
    result = await send_prompt(session_id, user_prompt.prompt, user_prompt.history_length)
    return result


@router.get("/v1/prompt_templates")
def get_all_prompt_templates() -> list[Optional[Any]]:
    """
    Get all the prompt templates from the database
    """
    return get_prompt_templates()

@router.put("/v1/prompt_templates/{prompt_template_name}")
async def select_prompt_template(prompt_template_name: str) -> dict[str, bool]:
    """
    Select a prompt template for the current session
    """
    result = session_service.select_prompt_template(prompt_template_name)
    return {"success": result }


@router.delete("/v1/prompt_templates/{prompt_template_name}")
async def delete_prompt_template(prompt_template_name: str) -> dict[str, bool]:
    """
    Delete a prompt template for the current session
    """
    result = session_service.select_prompt_template()
    return {"success": result }