from typing import Any, Optional

from pydantic import BaseModel


class AttackModuleArguments(BaseModel):
    name: str  # name of the attack module

    connector_instances: list  # list of Connector instance to connect to the endpoints specified in the Recipe

    stop_strategy_instances: (
        list  # list of Stop Strategy instances used to stop the automated red teaming
    )

    datasets: Optional[list] = []  # list of names of datasets to be used (if any)

    prompt_templates: Optional[list] = (
        []
    )  # list of prompt template names to be used (if any)

    metric_instances: Optional[list] = (
        []
    )  # list of metric instances to be used (if any)

    context_strategy: Optional[
        Any
    ]  # a Context Strategy instance to be used. it is a loaded instance (if any)

    params: Optional[dict] = (
        {}
    )  # a dict that contains other params that is required by the attack module (if any)
