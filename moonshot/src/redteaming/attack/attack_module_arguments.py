from typing import Any

from pydantic import BaseModel


class AttackModuleArguments(BaseModel):
    # name of the attack module
    name: str

    # num of prompts used
    num_of_prompts: int

    # list of Connector instance to connect to the endpoints specified in the Recipe
    connector_instances: list

    # list of names of datasets to be used (if any)
    datasets: list = []

    # list of prompt template names to be used (if any)
    prompt_templates: list = []

    # user's prompt
    prompt: str = ""

    # list of metric instances to be used (if any)
    metric_instances: list = []

    # list of context strategy instance to be used (if any)
    context_strategies: list = []

    # DBAccessor for the attack module to access DB data
    db_instance: Any

    # a dict that contains other params that is required by the attack module (if any)
    params: dict = {}
