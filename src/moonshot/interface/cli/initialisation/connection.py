from rich.console import Console
from rich.table import Table

from moonshot.api import api_get_connection_types, api_get_endpoints

console = Console()


def list_connect_types() -> None:
    """
    Get a list of available Language Model (LLM) connection types.
    """
    connection_types = api_get_connection_types()
    if connection_types:
        table = Table("No.", "Connection Type")
        for connection_id, connection_type in enumerate(connection_types, 1):
            table.add_section()
            table.add_row(str(connection_id), connection_type)
        console.print(table)
    else:
        console.print("[red]There are no connection types found.[/red]")


def list_endpoints() -> None:
    """
    Get a list of available Language Model (LLM) endpoints.
    """
    endpoints_list = api_get_endpoints()
    if endpoints_list:
        table = Table(
            "No.",
            "Connection Type",
            "Name",
            "Uri",
            "Token",
            "Max calls per second",
            "Max concurrency",
            "Params",
            "Created Date",
        )
        for endpoint_id, endpoint in enumerate(endpoints_list, 1):
            (
                connection_type,
                name,
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
                connection_type,
                name,
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
