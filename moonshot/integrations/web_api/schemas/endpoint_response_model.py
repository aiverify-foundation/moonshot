from typing import Optional

from pydantic import BaseModel, ConfigDict
from typing_extensions import TypedDict


class AdditionalParams(TypedDict, total=False):
    max_length: int
    min_length: int

class EndpointParams(TypedDict, total=False):
    model: Optional[str]
    timeout: Optional[int]
    allow_retries: Optional[bool]
    num_of_retries: Optional[int]
    temperature: Optional[float]
    pre_prompt: Optional[str]
    post_prompt: Optional[str]
    parameters: Optional[AdditionalParams]

class EndpointDataModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    connector_type: str
    name: str
    uri: str
    token: str
    max_calls_per_second: int
    max_concurrency: int
    created_date: str
    params: EndpointParams
