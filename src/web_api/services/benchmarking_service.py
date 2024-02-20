from web_api.schemas.endpoint_response_model import EndpointDataModel
from moonshot.src.common.connection import get_endpoints
from web_api.services.utils.exceptions_handler import exception_handler

@exception_handler
def get_all_endpoints() -> list[EndpointDataModel | None]:
    return [EndpointDataModel.model_validate(endpoint) for endpoint in get_endpoints()]


