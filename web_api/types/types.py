from typing import NotRequired
from typing_extensions import TypedDict

class PromptDetails(TypedDict):
    chat_record_id: int
    conn_id: str
    context_strategy: str
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

ExecutiResultItem = dict[str, float]
ExecutionResults = dict[str, list[ExecutiResultItem]]
class ExecutionInfo(TypedDict):
    exec_id: str
    exec_name: str
    exec_type: str
    bm_max_progress_per_cookbook: int
    bm_max_progress_per_recipe: int
    curr_duration: int
    curr_status: str
    curr_cookbook_index: int
    curr_cookbook_name: str
    curr_cookbook_total: int
    curr_recipe_index: int
    curr_recipe_name: str
    curr_recipe_total: int
    curr_progress: int
    curr_results: dict[str, list[ExecutionResults]]

class UvicornRunArgs(TypedDict, total=False):
    host: NotRequired[str]
    port: NotRequired[int]
    ssl_keyfile: NotRequired[str]
    ssl_certfile: NotRequired[str]


