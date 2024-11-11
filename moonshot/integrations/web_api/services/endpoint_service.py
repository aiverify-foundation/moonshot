from .... import api as moonshot_api
from ..schemas.endpoint_create_dto import EndpointUpdateDTO
from ..schemas.endpoint_response_model import EndpointDataModel
from .base_service import BaseService
from .utils.exceptions_handler import exception_handler


class EndpointService(BaseService):
    @exception_handler
    def add_endpoint(self, endpoint_data: EndpointDataModel) -> None:
        moonshot_api.api_create_endpoint(
            name=endpoint_data.name,
            connector_type=endpoint_data.connector_type,
            uri=endpoint_data.uri,
            token=endpoint_data.token,
            model=endpoint_data.model,
            max_calls_per_second=endpoint_data.max_calls_per_second,
            max_concurrency=endpoint_data.max_concurrency,
            params=endpoint_data.params,
        )

    @exception_handler
    def get_all_endpoints(self) -> list[EndpointDataModel | None]:
        filtered_endpoints = []
        endpoints = moonshot_api.api_get_all_endpoint()
        for endpoint in endpoints:
            filtered_endpoints.append(EndpointDataModel.model_validate(endpoint))

        filtered_endpoints.sort(
            key=lambda endpoint: endpoint.created_date, reverse=True
        )

        return [
            EndpointDataModel.model_validate(endpoint)
            for endpoint in filtered_endpoints
        ]

    @exception_handler
    def get_endpoint(self, endpoint_id: str) -> EndpointDataModel | None:
        endpoint = moonshot_api.api_read_endpoint(endpoint_id)
        return EndpointDataModel.model_validate(endpoint)

    @exception_handler
    def get_all_endpoints_names(self) -> list[str]:
        endpoints_names = moonshot_api.api_get_all_endpoint_name()
        return endpoints_names

    @exception_handler
    def update_endpoint(
        self, endpoint_id: str, endpoint_data: EndpointUpdateDTO
    ) -> None:
        update_data = {
            k: v
            for k, v in endpoint_data.to_dict().items()
            if v is not None and k != "id"
        }
        moonshot_api.api_update_endpoint(ep_id=endpoint_id, **update_data)

    @exception_handler
    def delete_endpoint(self, endpoint_id: str) -> None:
        moonshot_api.api_delete_endpoint(endpoint_id)

    @exception_handler
    def get_all_connectors(self) -> list[str]:
        connectors = moonshot_api.api_get_all_connector_type()
        return connectors
