from pydantic import BaseModel, RootModel

from ..schemas.session_response_model import ChatRecord


class PromptInfo(BaseModel):
    current_runner_id: str
    current_chats: dict[str, list[ChatRecord]]
    current_batch_size: int
    current_status: str


PromptResponseModel = RootModel[PromptInfo]
