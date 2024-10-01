from pydantic import conlist, validate_call

from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint


# ------------------------------------------------------------------------------
# Connector APIs
# ------------------------------------------------------------------------------
@validate_call
def api_create_connector_from_endpoint(ep_id: str) -> Connector:
    """
    Creates a connector based on the provided endpoint ID.

    This function retrieves the endpoint arguments using the provided endpoint ID and then creates a connector
    based on those arguments. It utilizes the ConnectorEndpoint's read method to fetch the endpoint
    arguments and then calls the Connector's create method to initialize and return the connector.

    Args:
        ep_id (str): The ID of the endpoint for which to create a connector.

    Returns:
        Connector: An initialized Connector object.
    """
    return Connector.create(ConnectorEndpoint.read(ep_id))


@validate_call
def api_create_connectors_from_endpoints(
    ep_ids: conlist(str, min_length=1)
) -> list[Connector]:
    """
    Creates connectors for multiple endpoints based on their IDs.

    This function takes a list of endpoint IDs, retrieves the corresponding endpoint arguments for each ID,
    and then creates a connector for each set of arguments. It utilizes the ConnectorEndpoint's read method
    to fetch the endpoint arguments and then calls the Connector's create method to initialize the connectors.

    Args:
        ep_ids (conlist(str, min_length=1)): A list of endpoint IDs for which to create connectors.

    Returns:
        list[Connector]: A list of initialized Connector objects.
    """
    return [Connector.create(ConnectorEndpoint.read(ep_id)) for ep_id in ep_ids]


def api_get_all_connector_type() -> list[str]:
    """
    Retrieves a list of all available connector types.

    This function calls the Connector's get_available_items method to retrieve a list of all available
    connector types. It returns the list of connector types.

    Returns:
        list[str]: A list of connector types.
    """
    return Connector.get_available_items()
