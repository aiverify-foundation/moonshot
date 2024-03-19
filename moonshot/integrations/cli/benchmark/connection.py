from ast import literal_eval

import cmd2
from rich.console import Console

from moonshot.api import api_create_endpoint

console = Console()


def add_endpoint(args) -> None:
    """
    Add an endpoint for a Language Model (LLM) connector.
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


# Add endpoint arguments
add_endpoint_args = cmd2.Cmd2ArgumentParser(
    description="Add a new endpoint.",
    epilog="Example:\n add_endpoint hf-gpt2 my-hf-gpt2 "
    "https://www.api.com/myapi 1234 10 1 \"{'temperature': 0}\"",
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
