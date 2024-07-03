from ast import literal_eval

import cmd2
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from moonshot.api import (
    api_create_endpoint,
    api_delete_endpoint,
    api_get_all_connector_type,
    api_get_all_endpoint,
    api_read_endpoint,
    api_update_endpoint,
)
from moonshot.src.utils.find_feature import find_keyword

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
    try:
        params_dict = literal_eval(args.params)

        new_endpoint_id = api_create_endpoint(
            args.name,
            args.connector_type,
            args.uri,
            args.token,
            args.max_calls_per_second,
            args.max_concurrency,
            params_dict,
        )
        print(f"[add_endpoint]: Endpoint ({new_endpoint_id}) created.")
    except Exception as e:
        print(f"[add_endpoint]: {str(e)}")


def list_endpoints(args) -> list | None:
    """
    List all endpoints.

    This function retrieves all endpoints by calling the api_get_all_endpoint function from the
    moonshot.api module. It then displays the endpoints using the display_endpoints function.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find endpoint(s) with a keyword.

    Returns:
        list | None: A list of ConnectorEndpoint or None if there is no result.
    """
    try:
        endpoints_list = api_get_all_endpoint()
        keyword = args.find.lower() if args.find else ""
        if keyword:
            filtered_endpoints_list = find_keyword(keyword, endpoints_list)
            if filtered_endpoints_list:
                display_endpoints(filtered_endpoints_list)
                return filtered_endpoints_list
            else:
                print("No endpoints containing keyword found.")
                return None
        else:
            display_endpoints(endpoints_list)
            return endpoints_list
    except Exception as e:
        print(f"[list_endpoints]: {str(e)}")


def list_connector_types(args) -> list | None:
    """
    List all connector types.

    This function retrieves all connector types by calling the api_get_all_connector_type function from the
    moonshot.api module. It then displays the connector types using the display_connector_types function.

    Args:
        args: A namespace object from argparse. It should have an optional attribute:
        find (str): Optional field to find connector type(s) with a keyword.

    Returns:
        list | None: A list of Connector or None if there is no result.
    """
    try:
        connector_type_list = api_get_all_connector_type()
        keyword = args.find.lower() if args.find else ""
        if keyword:
            filtered_connector_type_list = find_keyword(keyword, connector_type_list)
            if filtered_connector_type_list:
                display_connector_types(filtered_connector_type_list)
                return filtered_connector_type_list
            else:
                print("No connectors containing keyword found.")
                return None
        else:
            display_connector_types(connector_type_list)
            return connector_type_list
    except Exception as e:
        print(f"[list_connector_types]: {str(e)}")


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
    try:
        endpoint_info = api_read_endpoint(args.endpoint)
        display_endpoints([endpoint_info])
    except Exception as e:
        print(f"[view_endpoint]: {str(e)}")


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
    try:
        endpoint = args.endpoint
        update_values = dict(literal_eval(args.update_kwargs))
        api_update_endpoint(endpoint, **update_values)
        print("[update_endpoint]: Endpoint updated.")
    except Exception as e:
        print(f"[update_endpoint]: {str(e)}")


def delete_endpoint(args) -> None:
    """
    Delete a specific endpoint.

    This function deletes a specific endpoint by calling the api_delete_endpoint function from the
    moonshot.api module using the endpoint name provided in the args. Before deletion, it asks for
    user confirmation. If the user confirms, the endpoint is deleted; otherwise, the deletion is cancelled.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            endpoint (str): The name of the endpoint to delete.

    Returns:
        None
    """
    # Confirm with the user before deleting an endpoint
    confirmation = console.input(
        "[bold red]Are you sure you want to delete the endpoint (y/N)? [/]"
    )
    if confirmation.lower() != "y":
        console.print("[bold yellow]Endpoint deletion cancelled.[/]")
        return
    try:
        api_delete_endpoint(args.endpoint)
        print("[delete_endpoint]: Endpoint deleted.")
    except Exception as e:
        print(f"[delete_endpoint]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def display_connector_types(connector_types: list) -> None:
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
        table = Table(
            title="List of Connector Types",
            show_lines=True,
            expand=True,
            header_style="bold",
        )
        table.add_column("No.", width=2)
        table.add_column("Connector Type", justify="left", width=78)
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
            title="List of Connector Endpoints",
            show_lines=True,
            expand=True,
            header_style="bold",
        )
        table.add_column("No.", justify="left", width=2)
        table.add_column("Id", justify="left", width=10)
        table.add_column("Name", justify="left", width=10)
        table.add_column("Connector Type", justify="left", width=10)
        table.add_column("Uri", justify="left", width=10)
        table.add_column("Token", justify="left", width=10)
        table.add_column("Max Calls Per Second", justify="left", width=5)
        table.add_column("Max concurrency", justify="left", width=5)
        table.add_column("Params", justify="left", width=30)
        table.add_column("Created Date", justify="left", width=8)

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
                escape(str(params)),
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
    description="Add a new endpoint. The 'name' argument will be slugified to create a unique identifier.",
    epilog="Example:\n add_endpoint openai-connector 'OpenAI GPT3.5 Turbo 1106' "
    "MY_URI ADD_YOUR_TOKEN_HERE 1 1 \"{'temperature': 0.5, 'model': 'gpt-3.5-turbo-1106'}\"",
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
    epilog=(
        "Available keys:\n"
        "  name: name of the endpoint\n"
        "  uri: URI of the endpoint\n"
        "  token: Token of the endpoint\n"
        "  max_calls_per_second: Rate limit for max calls per second\n"
        "  max_concurrency: Rate limit for max concurrency\n"
        "  params: Extra arguments for the endpoint\n\n"
        "Example:\n"
        "  update_endpoint openai-gpt4 \"[('name', 'my-special-openai-endpoint'), "
        "('uri', 'my-uri-loc'), ('token', 'my-token-here')]\""
    ),
)
update_endpoint_args.add_argument(
    "endpoint",
    type=str,
    help="ID of the endpoint. This field is not editable via CLI after creation.",
)
update_endpoint_args.add_argument(
    "update_kwargs", type=str, help="Update endpoint key/value"
)

# View endpoint arguments
view_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="View an endpoint.",
    epilog="Example:\n view_endpoint openai-gpt4",
)
view_endpoint_args.add_argument("endpoint", type=str, help="ID of the endpoint")

# Delete endpoint arguments
delete_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Delete an endpoint.",
    epilog="Example:\n delete_endpoint openai-gpt4",
)
delete_endpoint_args.add_argument("endpoint", type=str, help="ID of the endpoint")

# List endpoint arguments
list_endpoints_args = cmd2.Cmd2ArgumentParser(
    description="List all endpoints.",
    epilog='Example:\n list_endpoints -f "gpt"',
)

list_endpoints_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find endpoint(s) with keyword",
    nargs="?",
)


# List connector types arguments
list_connector_types_args = cmd2.Cmd2ArgumentParser(
    description="List all connector types.",
    epilog='Example:\n list_connector_types -f "openai"',
)

list_connector_types_args.add_argument(
    "-f",
    "--find",
    type=str,
    help="Optional field to find connector type(s) with keyword",
    nargs="?",
)
