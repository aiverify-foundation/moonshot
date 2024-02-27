from typing_extensions import TypedDict
from moonshot.src.redteaming.session import Session, get_all_sessions
from .base_service import BaseService
from web_api.services.utils.exceptions_handler import SessionException, exception_handler
from web_api.schemas.session_create_dto import SessionCreateDTO
from web_api.schemas.session_response_model import SessionMetadataModel


class PromptDetails(TypedDict):
    chat_id: int
    connection_id: str
    context_strategy: int
    prompt_template: str
    prompt: str
    prepared_prompt: str
    predicted_result: str
    duration: str

class SessionService(BaseService):

    @exception_handler
    def create_session(session_create_dto: SessionCreateDTO, set_as_current_session: bool = False) -> SessionMetadataModel:
        new_session_instance = Session(session_create_dto.name, session_create_dto.description, session_create_dto.endpoints)
        if not new_session_instance.metadata.session_id.strip():
            raise SessionException("Session creation failed", __name__)
        if set_as_current_session:
            Session.current_session = new_session_instance
        return SessionMetadataModel(
            session_id=new_session_instance.metadata.session_id,
            name=new_session_instance.metadata.name,
            description=new_session_instance.metadata.description,
            created_epoch=new_session_instance.metadata.created_epoch,
            created_datetime=new_session_instance.metadata.created_datetime,
            endpoints=new_session_instance.metadata.endpoints,
            metadata_file=new_session_instance.metadata.metadata_file,
            prompt_template=new_session_instance.metadata.prompt_template,
            context_strategy=new_session_instance.metadata.context_strategy,
            chats=[],
            filename="",
            chat_history=None
        )

    @exception_handler
    def get_session(session_id: str) -> SessionMetadataModel | None:
        session_data = next((session for session in get_sessions() if session.session_id == session_id), None)
        return session_data

    @exception_handler
    def get_sessions() -> list[SessionMetadataModel | None]:
        return [SessionMetadataModel.model_validate(session) for session in get_all_sessions()]

    @exception_handler
    def set_current_session(session_id: str) -> SessionMetadataModel | None:
        session_data = get_session(session_id)
        session_instance: Session = Session.load_session(session_id)
        Session.current_session = session_instance
        return session_data



    def get_session_chat_history(session_id: str, history_length: int | None) -> dict[str, list[PromptDetails]]:
        try:
            session_instance = Session.load_session(session_id)
            session_previous_prompts: list[PromptDetails] = session_instance.get_session_previous_prompts(history_length)
            session_chats = session_instance.get_session_chats()
            all_chats_dict: dict[str, list[PromptDetails]] = {}
            for i, chat in enumerate(session_chats):
                all_chats_dict[chat.get_id()] = session_previous_prompts[i][::-1]
        except Exception as e:
            raise SessionException(f"An unexpected error occurred: {e}", __name__)
        
        return all_chats_dict

    async def send_prompt(session_id: str, user_prompt: str, history_length: int | None) -> dict[str, list[PromptDetails]]:
        user_prompt = user_prompt.strip()
        try:
            session_instance = Session.load_session(session_id)
            await session_instance.send_prompt_async(user_prompt)
            all_chats_dict = get_session_chat_history(session_id, history_length)
        except Exception as e:
            raise SessionException(f"An unexpected error occurred: {e}", __name__)
        
        return all_chats_dict

    def select_prompt_template(prompt_template_name: str = '') -> bool:
        # Check if current session exists
        if Session.current_session:
            if prompt_template_name == '':
                Session.current_session.set_prompt_template()
            else:
                Session.current_session.set_prompt_template(prompt_template_name)
            return True

        return False

