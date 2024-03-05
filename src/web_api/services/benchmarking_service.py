import moonshot.api as moonshot_api
from ..schemas.endpoint_response_model import EndpointDataModel
from ..services.utils.exceptions_handler import exception_handler

@exception_handler
def get_all_endpoints() -> list[EndpointDataModel | None]:
    return [EndpointDataModel.model_validate(endpoint) for endpoint in moonshot_api.get_endpoints()]


@exception_handler
def add_endpoint(endpoint_data: EndpointDataModel) -> None:
    """
    Adds a new endpoint using the provided EndpointDataModel.
    
    Args:
        endpoint_data (EndpointDataModel): The data model containing the endpoint information.
    """
    moonshot_api.add_new_endpoint(
        connector_type=endpoint_data.type,
        name=endpoint_data.name,
        uri=endpoint_data.uri,
        token=endpoint_data.token,
        max_calls_per_second=endpoint_data.max_calls_per_second,
        max_concurrency=endpoint_data.max_concurrency,
        params=endpoint_data.params
    )


