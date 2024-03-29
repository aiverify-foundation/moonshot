from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)


# ------------------------------------------------------------------------------
# Connector Endpoint APIs
# ------------------------------------------------------------------------------
def api_create_endpoint(
    name: str,
    connector_type: str,
    uri: str,
    token: str,
    max_calls_per_second: int,
    max_concurrency: int,
    params: dict,
) -> None:
    """
    Creates a new endpoint to the connector manager.

    This function creates a new connector endpoint with the specified parameters. It constructs a
    ConnectorEndpointArguments object with the provided details and then calls the ConnectorManager's create_endpoint
    method to add the new endpoint.

    Args:
        name (str): The name of the new endpoint.
        connector_type (str): The type of the connector (e.g., 'GPT-3', 'Bert', etc.).
        uri (str): The URI for the connector's API.
        token (str): The access token for the API.
        max_calls_per_second (int): The maximum number of API calls allowed per second.
        max_concurrency (int): The maximum number of concurrent API calls.
        params (dict): Additional parameters for the connector.

    Returns:
        None
    """
    # Create a new connector endpoint arguments instance.
    # We do not need to provide id and created_date.
    # This is because during creation:
    #   1. the id is slugify from the name and stored as id.
    #   2. the created_date is based on the os file created date and time.
    connector_endpoint_args = ConnectorEndpointArguments(
        id="",
        name=name,
        connector_type=connector_type,
        uri=uri,
        token=token,
        max_calls_per_second=max_calls_per_second,
        max_concurrency=max_concurrency,
        params=params,
        created_date="",
    )
    ConnectorEndpoint.create(connector_endpoint_args)


def api_read_endpoint(ep_id: str) -> dict:
    """
    Reads an endpoint from the connector manager.

    This function reads an endpoint from the connector manager using the provided endpoint ID.

    Args:
        ep_id (str): The ID of the endpoint to read.

    Returns:
        dict: A dictionary containing the endpoint information.
    """
    return ConnectorEndpoint.read(ep_id).to_dict()


def api_update_endpoint(ep_id: str, **kwargs) -> None:
    """
    Updates an existing endpoint in the connector manager.

    This function updates an existing endpoint in the connector manager using the provided endpoint details.
    It first creates a ConnectorEndpointArguments instance with the provided details, then calls the
    ConnectorManager's update_endpoint method to update the endpoint.

    Args:
        kwargs: A dictionary of arguments for the endpoint. Possible keys are:
            name (str): The name of the endpoint.
            connector_type (str): The type of the connector.
            uri (str): The URI for the connector.
            token (str): The token for the connector.
            max_calls_per_second (int): The maximum number of API calls allowed per second.
            max_concurrency (int): The maximum number of concurrent API calls.
            params (dict): Additional parameters for the connector.

    Returns:
        None
    """
    # Check if the endpoint exists
    try:
        existing_endpoint = ConnectorEndpoint.read(ep_id)
    except Exception:
        raise RuntimeError(f"Endpoint with ID '{ep_id}' does not exist")

    # Update the fields of the existing endpoint with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_endpoint, key):
            setattr(existing_endpoint, key, value)

    # Update the endpoint
    ConnectorEndpoint.update(existing_endpoint)


def api_delete_endpoint(ep_id: str) -> None:
    """
    Deletes an existing endpoint in the connector manager.

    This function deletes an existing endpoint in the connector manager using the provided endpoint ID.
    It calls the ConnectorManager's delete_endpoint method to delete the endpoint.

    Args:
        ep_id (str): The ID of the endpoint to be deleted.

    Returns:
        None
    """
    ConnectorEndpoint.delete(ep_id)


def api_get_all_endpoint() -> list[dict]:
    """
    Retrieves a list of all available endpoints.

    This function calls the ConnectorManager's get_available_endpoints method to retrieve a list of all available
    endpoints and their details. It then converts each ConnectorEndpointArguments object into a dictionary for easier
    consumption by the caller.

    Returns:
        list[dict]: A list of dictionaries, each representing an endpoint's details.
    """
    _, endpoints = ConnectorEndpoint.get_available_items()
    return [endpoint.to_dict() for endpoint in endpoints]


def api_get_all_endpoint_name() -> list[str]:
    """
    Retrieves a list of all endpoint names.

    This function calls the ConnectorManager's get_available_endpoints method to retrieve a list of all available
    endpoint names. It extracts the names from the tuple returned by get_available_endpoints, which contains a list
    of endpoint names and a list of ConnectorEndpointArguments objects.

    Returns:
        list[str]: A list of endpoint names.
    """
    endpoints_names, _ = ConnectorEndpoint.get_available_items()
    return endpoints_names
