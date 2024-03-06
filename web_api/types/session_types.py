from typing_extensions import TypedDict

class PromptDetails(TypedDict):
    chat_record_id: int
    conn_id: str
    context_strategy: int
    prompt_template: str
    prompt: str
    prepared_prompt: str
    predicted_result: str
    duration: str
    prompt_time: str


class EndpointChatHistory(TypedDict):
    chat_id: str
    endpoint: str
    chat_history: list[PromptDetails]

SessionChats = list[EndpointChatHistory]

SessionChatsGroupedBySessionId = dict[str, list[PromptDetails]]

