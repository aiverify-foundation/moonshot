from typing_extensions import TypedDict
from pydantic import BaseModel, ConfigDict
from typing import Optional

class Parameters(TypedDict, total=False):
    max_length: int
    min_length: int
class Params(TypedDict, total=False):
    timeout: int
    allow_retries: bool
    num_of_retries: int
    temperature: float
    pre_prompt: str
    post_prompt: str
    parameters: Parameters
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
    params: Optional[Params] = None
