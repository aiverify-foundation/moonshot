from enum import Enum
from typing import Any, List, NotRequired

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


class TestRunProgress(TypedDict):
    current_runner_id: str
    current_runner_name: str
    current_runner_type: str
    current_duration: int
    current_status: str
    current_cookbook_index: int
    current_cookbook_name: str
    current_cookbook_total: int
    current_recipe_index: int
    current_recipe_name: str
    current_recipe_total: int
    current_progress: int
    current_error_messages: List[str]


class RedTeamTestProgress(TypedDict):
    current_runner_id: str
    current_am_id: str
    current_pt_id: str
    current_cs_id: str
    current_chats: list[dict]
    current_batch_size: str
    current_status: str


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


class ResultMetadata(TypedDict):
    id: str
    name: str
    start_time: str
    end_time: str
    duration: int
    recipes: List[str]
    cookbooks: List[str]
    endpoints: List[str]
    prompt_selection_percentage: int
    status: str


class RequiredMetadata(TypedDict):
    metadata: ResultMetadata


class BenchmarkResult(TypedDict, RequiredMetadata, total=False):
    # This indicates that any other keys should map to dictionaries, but this is not enforced by static type checkers.
    # It serves more as documentation for developers.
    additional_properties: dict[str, Any]
