from typing import Any, NotRequired, List
from typing_extensions import TypedDict
from enum import Enum

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

class CookbookTestRunProgress(TypedDict):
    exec_id: str
    exec_name: str
    exec_type: str
    curr_duration: int
    curr_status: str
    curr_cookbook_index: int
    curr_cookbook_name: str
    curr_cookbook_total: int
    curr_recipe_index: int
    curr_recipe_name: str
    curr_recipe_total: int
    curr_progress: int
    curr_error_messages: List[str]

class UvicornLoggingConfig(TypedDict):
    version: int
    formatters: dict[str, dict[str, Any]]
    handlers: dict[str, dict[str, Any]]
    root: dict[str, dict[str, Any] | list[str]]
    disable_existing_loggers: bool


class UvicornRunArgs(TypedDict, total=False):
    host: NotRequired[str]
    port: NotRequired[int]
    ssl_keyfile: NotRequired[str]
    ssl_certfile: NotRequired[str]
    log_config: NotRequired[UvicornLoggingConfig]


class BenchmarkCollectionType(Enum):
    COOKBOOK = "cookbook"
    RECIPE = "recipe"

