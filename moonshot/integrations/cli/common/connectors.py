from ast import literal_eval

import cmd2
from rich.console import Console
from rich.table import Table

from moonshot.api import (
    api_create_endpoint,
    api_delete_endpoint,
    api_get_all_connector_type,
    api_get_all_endpoint,
    api_read_endpoint,
    api_update_endpoint,
)

console = Console()


# ------------------------------------------------------------------------------
# CLI Functions
# ------------------------------------------------------------------------------
def add_endpoint(args) -> None:
    """
    Add a new endpoint.

    This function adds a new endpoint by calling the api_create_endpoint function from the
    moonshot.api module using the endpoint details provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            name (str): The name of the new endpoint.
            connector_type (str): The type of the connector (e.g., 'GPT-3', 'Bert', etc.).
            uri (str): The URI for the connector's API.
            token (str): The access token for the API.
            max_calls_per_second (int): The maximum number of API calls allowed per second.
            max_concurrency (int): The maximum number of concurrent API calls.
            params (str): A string representation of a dictionary containing additional parameters for the connector.

    Returns:
        None
    """
    params_dict = literal_eval(args.params)

    api_create_endpoint(
        args.name,
        args.connector_type,
        args.uri,
        args.token,
        args.max_calls_per_second,
        args.max_concurrency,
        params_dict,
    )


def list_endpoints() -> None:
    """
    List all endpoints.

    This function retrieves all endpoints by calling the api_get_all_endpoint function from the
    moonshot.api module. It then displays the endpoints using the display_endpoints function.

    Returns:
        None
    """
    endpoint_list = api_get_all_endpoint()
    display_endpoints(endpoint_list)


def list_connector_types() -> None:
    """
    List all connector types.

    This function retrieves all connector types by calling the api_get_all_connector_type function from the
    moonshot.api module. It then displays the connector types using the display_connector_types function.

    Returns:
        None
    """
    connector_type_list = api_get_all_connector_type()
    display_connector_types(connector_type_list)


def view_endpoint(args) -> None:
    """
    View a specific endpoint.

    This function retrieves a specific endpoint by calling the api_read_endpoint function from the
    moonshot.api module using the endpoint name provided in the args. It then displays the endpoint
    information using the display_endpoints function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            endpoint (str): The name of the endpoint to view.

    Returns:
        None
    """
    endpoint_info = api_read_endpoint(args.endpoint)
    display_endpoints([endpoint_info])


def update_endpoint(args) -> None:
    """
    Update a specific endpoint.

    This function updates a specific endpoint by calling the api_update_endpoint function from the
    moonshot.api module using the endpoint name and update values provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attributes:
            endpoint (str): The name of the endpoint to update.
            update_kwargs (str): A string representation of a dictionary. Each key-value pair in the dictionary
            represents a field to update in the endpoint and the new value for that field.

    Returns:
        None
    """
    endpoint = args.endpoint
    update_values = dict(literal_eval(args.update_kwargs))
    api_update_endpoint(endpoint, **update_values)


def delete_endpoint(args) -> None:
    """
    Delete a specific endpoint.

    This function deletes a specific endpoint by calling the api_delete_endpoint function from the
    moonshot.api module using the endpoint name provided in the args.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            endpoint (str): The name of the endpoint to delete.

    Returns:
        None
    """
    api_delete_endpoint(args.endpoint)


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_connector_types(connector_types):
    """
    Display a list of connector types.

    This function takes a list of connector types and displays them in a table format. If the list is empty, it prints a
    message indicating that no connector types were found.

    Args:
        connector_types (list): A list of connector types.

    Returns:
        None
    """
    if connector_types:
        table = Table("No.", "Connector Type")
        for connector_id, connector_type in enumerate(connector_types, 1):
            table.add_section()
            table.add_row(str(connector_id), connector_type)
        console.print(table)
    else:
        console.print("[red]There are no connector types found.[/red]")


def display_endpoints(endpoints_list):
    """
    Display a list of endpoints.

    This function takes a list of endpoints and displays them in a table format. If the list is empty, it prints a
    message indicating that no endpoints were found.

    Args:
        endpoints_list (list): A list of endpoints. Each endpoint is a dictionary with keys 'id', 'name',
        'connector_type', 'uri', 'token', 'max_calls_per_second', 'max_concurrency', 'params', and 'created_date'.

    Returns:
        None
    """
    if endpoints_list:
        table = Table(
            "No.",
            "Id",
            "Name",
            "Connector Type",
            "Uri",
            "Token",
            "Max calls per second",
            "Max concurrency",
            "Params",
            "Created Date",
        )
        for endpoint_id, endpoint in enumerate(endpoints_list, 1):
            (
                id,
                name,
                connector_type,
                uri,
                token,
                max_calls_per_second,
                max_concurrency,
                params,
                created_date,
            ) = endpoint.values()
            table.add_section()
            table.add_row(
                str(endpoint_id),
                id,
                name,
                connector_type,
                uri,
                token,
                str(max_calls_per_second),
                str(max_concurrency),
                str(params),
                created_date,
            )
        console.print(table)
    else:
        console.print("[red]There are no endpoints found.[/red]")


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add endpoint arguments
add_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Add a new endpoint.",
    epilog="Example:\n add_endpoint openai-gpt35 my-openai-endpoint "
    "MY_URI ADD_YOUR_TOKEN_HERE 10 2 \"{'temperature': 0}\"",
)
add_endpoint_args.add_argument(
    "connector_type",
    type=str,
    help="Type of connection for the endpoint",
)
add_endpoint_args.add_argument("name", type=str, help="Name of the new endpoint")
add_endpoint_args.add_argument("uri", type=str, help="URI of the new endpoint")
add_endpoint_args.add_argument("token", type=str, help="Token of the new endpoint")
add_endpoint_args.add_argument(
    "max_calls_per_second",
    type=int,
    help="Max calls per second of the new endpoint",
)
add_endpoint_args.add_argument(
    "max_concurrency", type=int, help="Max concurrency of the new endpoint"
)
add_endpoint_args.add_argument("params", type=str, help="Params of the new endpoint")

# Update endpoint arguments
update_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Update an endpoint.",
    epilog="Example:\n update_endpoint test-openai-endpoint "
    "\"[('name', 'my-special-openai-endpoint'), ('uri', 'my-uri-loc'), ('token', 'my-token-here')]\" ",
)
update_endpoint_args.add_argument("endpoint", type=str, help="Name of the endpoint")
update_endpoint_args.add_argument(
    "update_kwargs", type=str, help="Update endpoint key/value"
)

# View endpoint arguments
view_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="View an endpoint.",
    epilog="Example:\n view_endpoint test-openai-endpoint",
)
view_endpoint_args.add_argument("endpoint", type=str, help="Name of the endpoint")

# Delete endpoint arguments
delete_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Delete an endpoint.",
    epilog="Example:\n delete_endpoint test-openai-endpoint",
)
delete_endpoint_args.add_argument("endpoint", type=str, help="Name of the endpoint")
