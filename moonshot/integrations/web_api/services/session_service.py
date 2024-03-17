from typing import Any
from ..types.types import PromptDetails, SessionChats
from .base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from ..schemas.session_create_dto import SessionCreateDTO
from ..schemas.session_response_model import SessionMetadataModel
from .... import api as moonshot_api


class SessionService(BaseService):

    @exception_handler
    def create_session(self, session_create_dto: SessionCreateDTO) -> SessionMetadataModel:
        new_session = moonshot_api.api_create_session(
            session_create_dto.name,
            session_create_dto.description,
            session_create_dto.endpoints,
            session_create_dto.context_strategy,
            session_create_dto.prompt_template
        )

        return SessionMetadataModel(
            session_id=new_session.metadata.session_id,
            name=new_session.metadata.  name,
            description=new_session.metadata.description,
            created_epoch=new_session.metadata.created_epoch,
            created_datetime=new_session.metadata.created_datetime,
            endpoints=new_session.metadata.endpoints,
            prompt_template=new_session.metadata.prompt_template,
            context_strategy=new_session.metadata.context_strategy,
            chat_ids=new_session.metadata.chat_ids,
            chat_history=None
        )

    @exception_handler
    def get_session(self, session_id: str) -> SessionMetadataModel | None:
        sessions = self.get_sessions()
        for session in sessions:
            if session and session["session_id"] == session_id:
                return SessionMetadataModel.model_validate(session)
        return None
        

    @exception_handler
    def get_sessions(self) -> list[SessionMetadataModel | None]:
        return moonshot_api.api_get_all_session_details();


    @exception_handler
    def get_session_chat_history(self, session_id: str) -> dict[str, list[PromptDetails]]:
        session_chats: SessionChats = moonshot_api.api_get_session_chats_by_session_id(session_id)
        all_chats_dict: dict[str, list[PromptDetails]] = {}
        for chat in session_chats:
            all_chats_dict[chat['chat_id']] = chat['chat_history']
        return all_chats_dict

    @exception_handler
    async def send_prompt(self, session_id: str, user_prompt: str) -> dict[str, list[PromptDetails]]:
        user_prompt = user_prompt.strip()
        await moonshot_api.api_send_prompt(session_id, user_prompt)
        all_chats_dict = self.get_session_chat_history(session_id)
        return all_chats_dict

    @exception_handler
    def select_prompt_template(self, session_id: str, prompt_template_name: str = ''):
        moonshot_api.api_update_prompt_template(session_id,prompt_template_name)
    
    @exception_handler
    def get_prompt_templates(self) -> list[dict[str, Any]]:
        templates = moonshot_api.api_get_all_prompt_template_details()
        return templates
    
    @exception_handler
    def get_ctx_strategies(self) -> list[str]:
        strategies = moonshot_api.api_get_all_context_strategy_names()
        return strategies
    
    @exception_handler
    def select_ctx_strategy(self, session_id: str, ctx_strategy_name: str) -> None:
        moonshot_api.api_update_context_strategy(session_id, ctx_strategy_name)
    
