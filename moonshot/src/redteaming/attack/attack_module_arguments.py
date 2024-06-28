import asyncio

from pydantic import BaseModel

from moonshot.src.redteaming.session.red_teaming_progress import RedTeamingProgress
from moonshot.src.storage.db_interface import DBInterface


class AttackModuleArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # list of connector endpoints
    connector_ids: list = []

    # list of prompt template ids to be used (if any)
    prompt_templates: list = []

    # user's prompt
    prompt: str

    # system prompt
    system_prompt: str = ""

    # list of metric ids to be used (if any)
    metric_ids: list = []

    # list of context strategy ids and other params to be used (if any)
    context_strategy_info: list = []

    # DBAccessor for the attack module to access DB data
    db_instance: DBInterface

    # chat batch size for returning chat information by callback
    chat_batch_size: int = 0

    # callback function to return chat information
    red_teaming_progress: RedTeamingProgress | None = None

    # an asyncio event to cancel red teaming if a cancel signal is sent
    cancel_event: asyncio.Event

    # a dict that contains other params that is required by the attack module (if any)
    optional_params: dict = {}
