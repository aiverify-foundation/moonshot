from pydantic import BaseModel


class ConnectorEndpointArguments(BaseModel):
    # id (str): The ID of the endpoint which is also the filename
    id: str = ""

    # name (str): The name for the endpoint.
    name: str

    # connector_type (str): The type of the LLM connector (e.g., 'GPT-3', 'Bert', etc.).
    connector_type: str

    # uri (str): The URI (Uniform Resource Identifier) for the LLM connector's API.
    uri: str

    # token (str): The access token required to authenticate and access the LLM connector's API.
    token: str

    # max_calls_per_second (int): The number of api calls per second
    max_calls_per_second: int

    # max_concurrency (int): The number of concurrent api calls
    max_concurrency: int

    # params (dict): A dictionary that contains connection specified parameters
    params: dict

    # created_date (str): The date and time the endpoint was created in isoformat without 'T'.
    created_date: str = ""
