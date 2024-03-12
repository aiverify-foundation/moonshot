from pydantic import BaseModel, ConfigDict
from typing import Optional, Union

class EndpointCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    connector_type: str
    name: str
    uri: str
    token: str
    max_calls_per_second: int
    max_concurrency: int
    params: Optional[dict[str, Union[str, int]]] = None
