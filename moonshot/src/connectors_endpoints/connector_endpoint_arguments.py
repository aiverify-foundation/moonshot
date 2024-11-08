from pydantic import BaseModel, Field


class ConnectorEndpointArguments(BaseModel):
    # id (str): The ID of the endpoint which is also the filename
    # During creation, id is not required. The id is automatically generated and returned
    id: str

    name: str = Field(min_length=1)  # name (str): The name for the endpoint.

    connector_type: str  # connector_type (str): The type of the LLM connector (e.g., 'GPT-3', 'Bert', etc.).

    uri: str  # uri (str): The URI (Uniform Resource Identifier) for the LLM connector's API.

    token: str  # token (str): The access token required to authenticate and access the LLM connector's API.

    max_calls_per_second: int = Field(
        gt=0
    )  # max_calls_per_second (int): The number of api calls per second

    max_concurrency: int = Field(
        gt=0
    )  # max_concurrency (int): The number of concurrent api calls

    model: str  # model (str): The model identifier for the LLM connector.

    params: dict  # params (dict): A dictionary that contains connection specified parameters

    # created_date (str): The date and time the endpoint was created in isoformat without 'T'.
    # During creation, created_date is not required. The created_date is automatically generated and returned
    created_date: str = ""

    def to_dict(self) -> dict:
        """
        Converts the ConnectorEndpointArguments instance into a dictionary.

        This method takes all the attributes of the ConnectorEndpointArguments instance and constructs a dictionary
        with attribute names as keys and their corresponding values. This includes the id, name, connector_type, uri,
        token, max_calls_per_second, max_concurrency, model, params, and created_date. This dictionary can be used for
        serialization purposes, such as storing the endpoint information in a JSON file or sending it over a network.

        Returns:
            dict: A dictionary representation of the ConnectorEndpointArguments instance.
        """

        return {
            "id": self.id,
            "name": self.name,
            "connector_type": self.connector_type,
            "uri": self.uri,
            "token": self.token,
            "max_calls_per_second": self.max_calls_per_second,
            "max_concurrency": self.max_concurrency,
            "model": self.model,
            "params": self.params,
            "created_date": self.created_date,
        }
