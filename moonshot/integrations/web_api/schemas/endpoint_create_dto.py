from typing import Optional, Union
from typing_extensions import TypedDict

from pydantic import BaseModel, ConfigDict
from ..schemas.endpoint_response_model import EndpointParams

class EndpointCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    connector_type: str
    name: str
    uri: str
    token: str
    max_calls_per_second: int
    max_concurrency: int
    params: EndpointParams

class EndpointUpdateDTO(TypedDict, total = False):
    connector_type: str
    name: str
    uri: str
    token: str
    max_calls_per_second: int
    max_concurrency: int
    params: EndpointParams