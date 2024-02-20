from typing import Optional
from moonshot.src.redteaming.session import Session

from web_api.schemas.endpoint_response_model import EndpointDataModel
from moonshot.src.common.connection import get_endpoints
from web_api.services.custom_exceptions import SessionException
from moonshot.src.common.prompt_template import get_prompt_templates
from pydantic import ValidationError
from typing import Any, Callable, Optional

def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise SessionException(f"{e}", __name__)
        except ValidationError as e:
            raise SessionException(f"A validation error occurred: {e}", __name__)
        except Exception as e:
            raise SessionException(f"An unexpected error occurred: {e}", __name__)
    return wrapper

@exception_handler
def get_all_endpoints() -> list[Optional[EndpointDataModel]]:
    print("Get all endpoints with the following details ============================== :")
    return [EndpointDataModel.model_validate(endpoint) for endpoint in get_endpoints()]


