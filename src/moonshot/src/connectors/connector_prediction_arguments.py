from typing import Callable, Union

from pydantic import BaseModel

from moonshot.src.connectors.connector import Connector


class ConnectorPredictionArguments(BaseModel):
    # connection (Connection): An instance of the Connection class.
    connector: Connector

    # prompts_template_info (dict): A dictionary containing information about the prompts' template.
    prompts_template_info: dict

    # prompts_callback_function (Callable): A prompts callback function to handle prompts.
    prompts_callback_function: Union[Callable, None]
