from pydantic import BaseModel

from moonshot.src.storage.db_interface import DBInterface


class AttackModuleArguments(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # name of the attack module
    name: str

    # list of connector endpoints
    connector_eps: list = []

    # list of prompt template ids to be used (if any)
    prompt_templates: list = []

    # user's prompt
    prompt: str = ""

    # system prompt
    system_prompt: str = ""

    # list of metric ids to be used (if any)
    metric_ids: list = []

    # list of context strategy ids to be used (if any)
    context_strategy_ids: list = []

    # DBAccessor for the attack module to access DB data
    db_instance: DBInterface

    # a dict that contains other params that is required by the attack module (if any)
    params: dict = {}
