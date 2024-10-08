from pydantic import validate_call

from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)


# ------------------------------------------------------------------------------
# Connector Endpoint APIs
# ------------------------------------------------------------------------------
@validate_call
def api_create_endpoint(
    name: str,
    connector_type: str,
    uri: str,
    token: str,
    max_calls_per_second: int,
    max_concurrency: int,
    model: str,
    params: dict,
) -> str:
    """
    Creates a new connector endpoint.

    This function creates a new connector endpoint with the specified parameters. It initializes
    a ConnectorEndpointArguments instance and then uses the ConnectorEndpoint class to create
    the endpoint.

    Args:
        name (str): The name of the endpoint.
        connector_type (str): The type of the connector.
        uri (str): The URI for the connector.
        token (str): The token for authentication with the connector.
        max_calls_per_second (int): The maximum number of calls allowed per second.
        max_concurrency (int): The maximum number of concurrent calls allowed.
        model (str): The model used by the connector.
        params (dict): Additional parameters for the connector.

    Returns:
        str: The ID of the newly created connector endpoint.
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
        model=model,
        params=params,
        created_date="",
    )
    return ConnectorEndpoint.create(connector_endpoint_args)


@validate_call
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


@validate_call
def api_update_endpoint(ep_id: str, **kwargs) -> bool:
    """
    Updates an existing endpoint with new values.

    This function updates an existing endpoint in the connector manager using the provided endpoint ID and
    keyword arguments.

    Each keyword argument corresponds to an attribute of the endpoint that should be updated.

    Args:
        ep_id (str): The ID of the endpoint to update.
        **kwargs: Arbitrary keyword arguments representing the attributes to update.

    Returns:
        bool: True if the update was successful.

    Raises:
        RuntimeError: If the endpoint with the given ID does not exist or the update failed.
    """
    # Check if the endpoint exists
    try:
        existing_endpoint = ConnectorEndpoint.read(ep_id)
    except Exception:
        raise RuntimeError(
            f"[api_update_endpoint]: Endpoint with ID '{ep_id}' does not exist"
        )

    # Update the fields of the existing endpoint with the provided kwargs
    for key, value in kwargs.items():
        if hasattr(existing_endpoint, key):
            setattr(existing_endpoint, key, value)

    # Perform pydantic check on the updated existing endpoint
    ConnectorEndpointArguments.model_validate(existing_endpoint.to_dict())

    # Update the endpoint
    return ConnectorEndpoint.update(existing_endpoint)


@validate_call
def api_delete_endpoint(ep_id: str) -> bool:
    """
    Deletes an endpoint from the connector manager.

    This function deletes an endpoint from the connector manager using the provided endpoint ID.

    Args:
        ep_id (str): The ID of the endpoint to delete.

    Returns:
        bool: True if the deletion was successful.

    Raises:
        RuntimeError: If the endpoint with the given ID does not exist or the deletion failed.
    """
    return ConnectorEndpoint.delete(ep_id)


def api_get_all_endpoint() -> list[dict]:
    """
    Retrieves a list of all available endpoints.

    This function calls the ConnectorEndpoint's get_available_items method to retrieve a list of all available
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

    This function calls the ConnectorEndpoint's get_available_items method to retrieve a list of all available
    endpoint names. It extracts the names from the tuple returned by get_available_items, which contains a list
    of endpoint names and a list of ConnectorEndpointArguments objects.

    Returns:
        list[str]: A list of endpoint names.
    """
    endpoints_names, _ = ConnectorEndpoint.get_available_items()
    return endpoints_names
