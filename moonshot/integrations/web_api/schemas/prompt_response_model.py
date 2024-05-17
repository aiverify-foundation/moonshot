from pydantic import BaseModel, RootModel


class Chat(BaseModel):
    prompt: str
    response: str
    prompt_time: str
    response_time: str


class PromptInfo(BaseModel):
    current_runner_id: str
    current_am_id: str
    current_cs_id: str
    current_pt_id: str
    current_chats: dict[str, list[Chat]]
    current_batch_size: int
    current_status: str


PromptResponseModel = RootModel[list[PromptInfo]]
