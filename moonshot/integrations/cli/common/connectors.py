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
from moonshot.integrations.cli.cli_errors import (
    ERROR_COMMON_ADD_ENDPOINT_CONNECTOR_TYPE_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_MAX_CALLS_PER_SECOND_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_MAX_CONCURRENCY_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_MODEL_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_NAME_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_PARAMS_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_TOKEN_VALIDATION,
    ERROR_COMMON_ADD_ENDPOINT_URI_VALIDATION,
    ERROR_COMMON_DELETE_ENDPOINT_ENDPOINT_VALIDATION,
    ERROR_COMMON_LIST_CONNECTOR_TYPES_FIND_VALIDATION,
    ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION,
    ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION_1,
    ERROR_COMMON_LIST_ENDPOINTS_FIND_VALIDATION,
    ERROR_COMMON_LIST_ENDPOINTS_PAGINATION_VALIDATION,
    ERROR_COMMON_LIST_ENDPOINTS_PAGINATION_VALIDATION_1,
    ERROR_COMMON_UPDATE_ENDPOINT_ENDPOINT_VALIDATION,
    ERROR_COMMON_UPDATE_ENDPOINT_VALUES_VALIDATION,
    ERROR_COMMON_UPDATE_ENDPOINT_VALUES_VALIDATION_1,
    ERROR_COMMON_VIEW_ENDPOINT_ENDPOINT_VALIDATION,
)
from moonshot.integrations.cli.utils.process_data import filter_data

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
            model (str): The model used by the endpoint.
            params (str): A string representation of a dictionary containing additional parameters for the connector.

    Returns:
        None
    """
    try:
        if not isinstance(args.name, str) or not args.name or args.name is None:
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_NAME_VALIDATION)

        if (
            not isinstance(args.connector_type, str)
            or not args.connector_type
            or args.connector_type is None
        ):
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_CONNECTOR_TYPE_VALIDATION)

        if not isinstance(args.uri, str) or not args.uri or args.uri is None:
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_URI_VALIDATION)

        if not isinstance(args.token, str) or not args.token or args.token is None:
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_TOKEN_VALIDATION)

        if (
            not isinstance(args.max_calls_per_second, int)
            or not args.max_calls_per_second
            or args.max_calls_per_second is None
            or args.max_calls_per_second < 0
        ):
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_MAX_CALLS_PER_SECOND_VALIDATION)

        if (
            not isinstance(args.max_concurrency, int)
            or not args.max_concurrency
            or args.max_concurrency is None
            or args.max_calls_per_second < 0
        ):
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_MAX_CONCURRENCY_VALIDATION)

        if not isinstance(args.model, str) or args.model is None:
            raise TypeError(ERROR_COMMON_ADD_ENDPOINT_MODEL_VALIDATION)

        try:
            params_dict = literal_eval(args.params)
        except Exception:
            raise SyntaxError(ERROR_COMMON_ADD_ENDPOINT_PARAMS_VALIDATION)
        if not isinstance(params_dict, dict):
            raise ValueError(ERROR_COMMON_ADD_ENDPOINT_PARAMS_VALIDATION)

        new_endpoint_id = api_create_endpoint(
            args.name,
            args.connector_type,
            args.uri,
            args.token,
            args.max_calls_per_second,
            args.max_concurrency,
            args.model,
            params_dict,
        )
        print(f"[add_endpoint]: Endpoint ({new_endpoint_id}) created.")
    except Exception as e:
        print(f"[add_endpoint]: {str(e)}")


def list_endpoints(args) -> list | None:
    """
    List all endpoints.

    This function retrieves all endpoints by calling the api_get_all_endpoint function from the
    moonshot.api module. It then displays the endpoints using the _display_endpoints function.

    Args:
        args: A namespace object from argparse. It should have the following optional attributes:
            find (str): Optional field to find endpoint(s) with a keyword.
            pagination (str): Optional field to paginate endpoints.

    Returns:
        list | None: A list of ConnectorEndpoint or None if there is no result.
    """
    try:
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_COMMON_LIST_ENDPOINTS_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_COMMON_LIST_ENDPOINTS_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_COMMON_LIST_ENDPOINTS_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(ERROR_COMMON_LIST_ENDPOINTS_PAGINATION_VALIDATION_1)
        else:
            pagination = ()

        endpoints_list = api_get_all_endpoint()
        keyword = args.find.lower() if args.find else ""

        if endpoints_list:
            filtered_endpoints_list = filter_data(endpoints_list, keyword, pagination)
            if filtered_endpoints_list:
                _display_endpoints(filtered_endpoints_list)
                return filtered_endpoints_list

        console.print("[red]There are no endpoints found.[/red]")
        return None
    except Exception as e:
        print(f"[list_endpoints]: {str(e)}")


def list_connector_types(args) -> list | None:
    """
    List all connector types.

    This function retrieves all connector types by calling the api_get_all_connector_type function from the
    moonshot.api module. It then displays the connector types using the _display_connector_types function.

    Args:
        args: A namespace object from argparse. It should have the following optional attributes:
            find (str): Optional field to find connector type(s) with a keyword.
            pagination (str): Optional field to paginate connector types.

    Returns:
        list | None: A list of Connector or None if there is no result.
    """
    try:
        if args.find is not None:
            if not isinstance(args.find, str) or not args.find:
                raise TypeError(ERROR_COMMON_LIST_CONNECTOR_TYPES_FIND_VALIDATION)

        if args.pagination is not None:
            if not isinstance(args.pagination, str) or not args.pagination:
                raise TypeError(ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION)
            try:
                pagination = literal_eval(args.pagination)
                if not (
                    isinstance(pagination, tuple)
                    and len(pagination) == 2
                    and all(isinstance(i, int) for i in pagination)
                ):
                    raise ValueError(
                        ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION_1
                    )
            except (ValueError, SyntaxError):
                raise ValueError(
                    ERROR_COMMON_LIST_CONNECTOR_TYPES_PAGINATION_VALIDATION_1
                )
        else:
            pagination = ()

        connector_type_list = api_get_all_connector_type()
        keyword = args.find.lower() if args.find else ""

        if connector_type_list:
            filtered_connector_type_list = filter_data(
                connector_type_list, keyword, pagination
            )
            if filtered_connector_type_list:
                _display_connector_types(filtered_connector_type_list)
                return filtered_connector_type_list

        console.print("[red]There are no connector types found.[/red]")
        return None
    except Exception as e:
        print(f"[list_connector_types]: {str(e)}")


def view_endpoint(args) -> None:
    """
    View a specific endpoint.

    This function retrieves a specific endpoint by calling the api_read_endpoint function from the
    moonshot.api module using the endpoint name provided in the args. It then displays the endpoint
    information using the _display_endpoints function.

    Args:
        args: A namespace object from argparse. It should have the following attribute:
            endpoint (str): The name of the endpoint to view.

    Returns:
        None
    """
    try:
        if (
            not isinstance(args.endpoint, str)
            or not args.endpoint
            or args.endpoint is None
        ):
            raise TypeError(ERROR_COMMON_VIEW_ENDPOINT_ENDPOINT_VALIDATION)

        endpoint_info = api_read_endpoint(args.endpoint)
        _display_endpoints([endpoint_info])
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
        if (
            args.endpoint is None
            or not isinstance(args.endpoint, str)
            or not args.endpoint
        ):
            raise ValueError(ERROR_COMMON_UPDATE_ENDPOINT_ENDPOINT_VALIDATION)
        endpoint = args.endpoint

        if (
            args.update_kwargs is None
            or not isinstance(args.update_kwargs, str)
            or not args.update_kwargs
        ):
            raise ValueError(ERROR_COMMON_UPDATE_ENDPOINT_VALUES_VALIDATION)

        if literal_eval(args.update_kwargs) and all(
            isinstance(i, tuple) for i in literal_eval(args.update_kwargs)
        ):
            update_kwargs = dict(literal_eval(args.update_kwargs))
        else:
            raise ValueError(ERROR_COMMON_UPDATE_ENDPOINT_VALUES_VALIDATION_1)
        api_update_endpoint(endpoint, **update_kwargs)
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
        if (
            args.endpoint is None
            or not isinstance(args.endpoint, str)
            or not args.endpoint
        ):
            raise ValueError(ERROR_COMMON_DELETE_ENDPOINT_ENDPOINT_VALIDATION)
        api_delete_endpoint(args.endpoint)
        print("[delete_endpoint]: Endpoint deleted.")
    except Exception as e:
        print(f"[delete_endpoint]: {str(e)}")


# ------------------------------------------------------------------------------
# Helper functions: Display on cli
# ------------------------------------------------------------------------------
def _display_connector_types(connector_types: list) -> None:
    """
    Display a list of connector types.

    This function takes a list of connector types and displays them in a table format. If the list is empty, it prints a
    message indicating that no connector types were found.

    Args:
        connector_types (list): A list of connector types.

    Returns:
        None
    """
    table = Table(
        title="List of Connector Types",
        show_lines=True,
        expand=True,
        header_style="bold",
    )
    table.add_column("No.", width=2)
    table.add_column("Connector Type", justify="left", width=78)

    for idx, connector_type in enumerate(connector_types, 1):
        table.add_section()
        table.add_row(str(idx), connector_type)
    console.print(table)


def _display_endpoints(endpoints_list):
    """
    Display a list of endpoints.

    This function takes a list of endpoints and displays them in a table format. If the list is empty, it prints a
    message indicating that no endpoints were found.

    Args:
        endpoints_list (list): A list of endpoints. Each endpoint is a dictionary with keys 'id', 'name',
        'connector_type', 'uri', 'token', 'max_calls_per_second', 'max_concurrency', 'model', 'params',
        and 'created_date'.

    Returns:
        None
    """
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
    table.add_column("Max Concurrency", justify="left", width=5)
    table.add_column("Model", justify="left", width=5)
    table.add_column("Params", justify="left", width=30)
    table.add_column("Created Date", justify="left", width=8)

    for idx, endpoint in enumerate(endpoints_list, 1):
        (
            id,
            name,
            connector_type,
            uri,
            token,
            max_calls_per_second,
            max_concurrency,
            model,
            params,
            created_date,
            *other_args,
        ) = endpoint.values()
        table.add_section()
        idx = endpoint.get("idx", idx)
        table.add_row(
            str(idx),
            id,
            name,
            connector_type,
            uri,
            token,
            str(max_calls_per_second),
            str(max_concurrency),
            str(model),
            escape(str(params)),
            created_date,
        )
    console.print(table)


# ------------------------------------------------------------------------------
# Cmd2 Arguments Parsers
# ------------------------------------------------------------------------------
# Add endpoint arguments
add_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Add a new endpoint. The 'name' argument will be slugified to create a unique identifier.",
    epilog="Example:\n add_endpoint openai-connector 'OpenAI GPT3.5 Turbo 1106' "
    "MY_URI ADD_YOUR_TOKEN_HERE 1 1 'gpt-3.5-turbo-1106' \"{'temperature': 0.5}\"",
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
add_endpoint_args.add_argument("model", type=str, help="Model of the new endpoint")
add_endpoint_args.add_argument("params", type=str, help="Params of the new endpoint")

# Update endpoint arguments
update_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Update an endpoint.",
    epilog=(
        "Available keys:\n"
        "  name: Name of the endpoint\n"
        "  uri: URI of the endpoint\n"
        "  token: Token of the endpoint\n"
        "  max_calls_per_second: Rate limit for max calls per second\n"
        "  max_concurrency: Rate limit for max concurrency\n"
        "  model: Model of the endpoint\n"
        "  params: Extra arguments for the endpoint\n\n"
        "Example:\n"
        "  update_endpoint openai-gpt4 \"[('name', 'my-special-openai-endpoint'), "
        "('uri', 'my-uri-loc'), ('token', 'my-token-here'), ('params', {'hello': 'world'})]\""
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

list_endpoints_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate endpoint(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
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

list_connector_types_args.add_argument(
    "-p",
    "--pagination",
    type=str,
    help="Optional tuple to paginate connector type(s). E.g. (2,10) returns 2nd page with 10 items in each page.",
    nargs="?",
)
