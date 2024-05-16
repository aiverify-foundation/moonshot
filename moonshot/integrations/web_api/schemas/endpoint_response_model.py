from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments as ConnectorEndpointPydanticModel,
)


class EndpointDataModel(ConnectorEndpointPydanticModel):
    pass

    def mask_token(self):
        self.token = "*" * 20
