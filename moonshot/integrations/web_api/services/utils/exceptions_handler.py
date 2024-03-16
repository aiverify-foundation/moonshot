from typing import Any, Callable
from pydantic import ValidationError

class ServiceException(Exception):
    error_code: str
    msg: str

    def __init__(self, msg: str, method_name: str, error_code: str = 'UnknownSessionError'):
        self.error_code = error_code
        message = f"[ServiceException] {error_code} in {method_name} - {msg}"
        self.msg = message 
        super().__init__(message)

def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise ServiceException(f"A file not found error occurred: {e}", func.__name__, "FileNotFound")
        except ValidationError as e:
            raise ServiceException(f"A validation error occurred: {e}", func.__name__, "ValidationError")
        except ValueError as e:
            raise ServiceException(f"An value error occurred: {e}", func.__name__, "ValueError")
        except Exception as e:
            raise ServiceException(f"An unexpected error occurred: {e}", func.__name__, "UnexpectedError")
    return wrapper
