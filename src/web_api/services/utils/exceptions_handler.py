from typing import Any, Callable
from pydantic import ValidationError

class SessionException(Exception):
    def __init__(self, msg, method_name):
        message = f"SessionError {method_name} - {msg}"
        super().__init__(message)

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
