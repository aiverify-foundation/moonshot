from pydantic import BaseModel, RootModel

class PromptInfo(BaseModel):
    chat_record_id: int
    conn_id: str
    context_strategy: str
    prompt_template: str
    prompt: str
    prepared_prompt: str
    predicted_result: str
    duration: str
    prompt_time: str

PromptResponseModel = RootModel[dict[str, list[PromptInfo]]]


